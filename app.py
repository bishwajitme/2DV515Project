from flask import Flask
# request, render_template, jsonify
from flask_restful import Resource, Api
from Search import Search


app = Flask(__name__)
api = Api(app)


class Index(Resource):
    def get(self):
        return {"data": "hello world"}, 200, {'Access-Control-Allow-Origin': '*'}



api.add_resource(Index, '/')
api.add_resource(Search, '/search/<string:search_term>')

if __name__ == '__main__':
    app.run(debug=True)
