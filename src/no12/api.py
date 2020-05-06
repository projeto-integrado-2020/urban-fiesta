from flask_restx import Api, Resource, reqparse
from flask_login import login_user, logout_user, current_user, login_required
from mongoengine import errors

from .models import User
from .extensions import login


api = Api()


confirm_password = reqparse.RequestParser()
confirm_password.add_argument("password", type=str, required=True)

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
def load_user(user_id: str):
    """Check if user is logged-in on every page load."""
    try:
        user = User.objects.get(id=user_id)
    except errors.DoesNotExist:
        return None
    else:
        return user


def get_user_by_email(email: str):
    """Wrapper around mongoengine to do error handling."""
    try:
        user = User.objects.get(email=email)
    except errors.DoesNotExist:
        return None
    else:
        return user


@api.route("/index")
class Events(Resource):
    def get(self):
        if current_user.is_authenticated:
            user = current_user.email
        else:
            user = "Guest"
        return {
            "message": "Nenhum evento por enquanto.",
            "usuários cadastrados": User.objects.count(),
            "usuário logado": user,
        }


@api.route("/user")
class UserResource(Resource):
    @api.expect(get_user_parser)
    def get(self):
        args = get_user_parser.parse_args()
        user = get_user_by_email(args["email"])
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
        login_user(user)
        return {"message": "Usuário cadastrado com sucesso!"}

    @login_required
    @api.expect(user_parser)
    def put(self):
        """Change user first and last name."""
        args = user_parser.parse_args()
        user = current_user
        user.first_name = args["first_name"]
        user.last_name = args["last_name"]
        user.save()
        return {"message": "Dados alterados com sucesso."}

    @api.expect(confirm_password)
    @login_required
    def delete(self):
        args = confirm_password.parse_args()
        user = current_user
        if user.check_password(args["password"]):
            logout_user()
            user.delete()
            return {"message": "Usuário deletado com sucesso."}
        return {"message": "Senha incorreta."}


@api.route("/login")
class LoginResource(Resource):
    @api.expect(authenticate)
    def post(self):
        args = authenticate.parse_args()
        user = get_user_by_email(args["email"])
        if user:
            if user.check_password(args["password"]):
                login_user(user)
                return {"message": "Usuário logado com sucesso."}
            else:
                return {"message": "Senha incorreta."}
        return {"message": "Usuário não cadastrado."}


@api.route("/logout")
class LogoutResource(Resource):
    def get(self):
        logout_user()
        return {"message": "Logout efetuado com sucesso."}
