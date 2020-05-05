from flask import redirect, url_for
from flask_restx import Api, Resource, fields, reqparse
from flask_login import logout_user
from mongoengine import errors

from .models import User
from .extensions import login


api = Api()


authenticate = reqparse.RequestParser()
authenticate.add_argument("email", type=str, required=True)
authenticate.add_argument("password", type=str, required=True)

user_parser = reqparse.RequestParser()
user_parser.add_argument("email", type=str, required=True)
user_parser.add_argument("password", type=str, required=True)
user_parser.add_argument("first_name", type=str)
user_parser.add_argument("last_name", type=str)

get_user_parser = reqparse.RequestParser()
get_user_parser.add_argument("email", type=str, required=True)


@login.user_loader
def load_user(user_id):
    return User.get(user_id)


def get_user(email: str):
    try:
        user = User.objects.get(email=email)
    except errors.DoesNotExist:
        return None
    else:
        return user


@api.route("/index")
class Events(Resource):
    def get(self):
        return {
            "message": "Nenhum evento por enquanto.",
            "usuários cadastrados": User.objects.count(),
        }


@api.route("/user")
class UserResource(Resource):
    @api.expect(get_user_parser)
    def get(self):
        args = get_user_parser.parse_args()
        user = get_user(args["email"])
        if user:
            return user.to_json()
        return {"message": "Usuário não cadastrado."}

    @api.expect(user_parser)
    def post(self):
        args = user_parser.parse_args()
        try:
            user = User()
            user.email = args["email"]
            user.set_password(args["password"])
            user.first_name = args["first_name"]
            user.last_name = args["last_name"]
            user.save()
        except errors.NotUniqueError:
            return {"message": "Email já cadastrado."}
        return {"message": "Usuário cadastrado com sucesso!"}

    @api.expect(user_parser)
    def put(self):
        """Change user first and last name."""
        args = user_parser.parse_args()
        user = get_user(args["email"])
        if user:
            if user.check_password(args["password"]):
                user.first_name = args["first_name"]
                user.last_name = args["last_name"]
                user.save()
                return {"message": "Dados alterados com sucesso."}
            return {"message": "Senha incorreta."}
        return {"message": "Usuário não cadastrado."}

    @api.expect(authenticate)
    def delete(self):
        args = authenticate.parse_args()
        user = get_user(args["email"])
        if user:
            if user.check_password(args["password"]):
                user.delete()
                return {"message": "Usuário deletado com sucesso."}
            return {"message": "Senha incorreta."}
        return {"message": "Usuário não cadastrado."}
