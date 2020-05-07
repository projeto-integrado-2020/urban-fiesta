from flask_restx import reqparse

authenticate = reqparse.RequestParser()
authenticate.add_argument("email", type=str, required=True)
authenticate.add_argument("password", type=str, required=True)

user = reqparse.RequestParser()
user.add_argument("email", type=str, required=True)
user.add_argument("password", type=str, required=True)
user.add_argument("first_name", type=str)
user.add_argument("last_name", type=str)

get_user_email = reqparse.RequestParser()
get_user_email.add_argument("email", type=str, required=True)

event = reqparse.RequestParser()
event.add_argument("event_name", type=str, required=True)
event.add_argument("time", required=True)
event.add_argument("date", required=True)
event.add_argument("local", type=str, required=True)
event.add_argument("ticket_price", type=float, required=True)
event.add_argument("event_photo")
event.add_argument("description", type=str)
event.add_argument("age_limit", type=int)