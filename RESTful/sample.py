from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Every Resource has to be a class

class Student(Resource):
    def get(self, name):
        return {'student': name}


api.add_resource(Student, '/student/<string:name>') #http://127.0.0.1:5000/student/Michael

app.run(port=5000)
