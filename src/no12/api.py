from flask import redirect, url_for
from flask_restx import Api, Resource, fields, reqparse
from flask_login import logout_user
from mongoengine import errors

from .models import User
from .models import Event
from .extensions import login
from no12 import parsers 

api = Api()

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

def get_event(event_name: str):
    try:
        event = Event.objects.get(event_name=event_name)
    except errors.DoesNotExist:
        return None
    else:
        return event

@api.route("/index")
class Events(Resource):
    def get(self):
        return {
            "Eventos cadastrados": Event.objects.count(),
            "usuários cadastrados": User.objects.count(),
        }

@api.route("/user")
class UserResource(Resource):
    @api.expect(parsers.get_user_email)
    def get(self):
        args = parsers.get_user_email.parse_args()
        user = get_user(args["email"])
        if user:
            return user.to_json()
        return {"message": "Usuário não cadastrado."}

    @api.expect(parsers.user)
    def post(self):
        args = parsers.user.parse_args()
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

    @api.expect(parsers.user)
    def put(self):
        """Change user first and last name."""
        args = parsers.user.parse_args()
        user = get_user(args["email"])
        if user:
            if user.check_password(args["password"]):
                user.first_name = args["first_name"]
                user.last_name = args["last_name"]
                user.save()
                return {"message": "Dados alterados com sucesso."}
            return {"message": "Senha incorreta."}
        return {"message": "Usuário não cadastrado."}

    @api.expect(parsers.authenticate)
    def delete(self):
        args = parsers.authenticate.parse_args()
        user = get_user(args["email"])
        if user:
            if user.check_password(args["password"]):
                user.delete()
                return {"message": "Usuário deletado com sucesso."}
            return {"message": "Senha incorreta."}
        return {"message": "Usuário não cadastrado."}

@api.route("/event")
class EventResource(Resource):
    @api.expect(parsers.get_event)
    def get(self):
        args = parsers.get_event.parse_args()
        event = get_event(args["event_name"])
        if event:
            return event.to_json()
        return {"message": "Evento não cadastrado."}
    @api.expect(parsers.event)
    def post(self):
        try:
            args = parsers.event.parse_args()
            event = Event()
            event.event_name = args["event_name"]
            event.time = args["time"]
            event.date = args["date"]
            event.local = args["local"]
            event.ticket_price = args["ticket_price"]
            event.event_photo = args["event_photo"]
            event.description = args["description"]
            event.age_limit = args["age_limit"]
            event.save()
        except errors.NotUniqueError:
            return {"message": "Evento já cadastrado."}
        return {"message": "Evento cadastrado com sucesso!"}
