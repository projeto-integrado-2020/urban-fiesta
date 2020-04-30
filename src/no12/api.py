from flask_restx import Api, Resource


api = Api()


@api.route("/eventos")
class Events(Resource):
    def get(self):
        return {"message": "Nenhum evento por enquanto."}
