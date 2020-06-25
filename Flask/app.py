import pyrebase
from flask import Flask, request
from flask_restful import Resource, Api
from parse_pdf import convert_pdf

app = Flask(__name__)
api = Api(app)

class ocrAPI(Resource):
	def get(self, uuid_no):
		config = {
		    'apiKey': "AIzaSyB6QldxJGAfyNeo-Ql7aXXcEKl1rz1LwS4",
		    'authDomain': "ocr-hack-v0.firebaseapp.com",
		    'databaseURL': "https://ocr-hack-v0.firebaseio.com",
		    'projectId': "ocr-hack-v0",
		    'storageBucket': "ocr-hack-v0.appspot.com",
		    'messagingSenderId': "860184810119",
		    'appId': "1:860184810119:web:8e188783b7a4644d02de22",
		    'measurementId': "G-8M2FNH93GQ"
				}

		firebase = pyrebase.initialize_app(config)

		storage = firebase.storage()

		pdf_file = str(uuid_no) + '.pdf'
		storage.child("ScannedPDFs/"+pdf_file).download(pdf_file)


		response = convert_pdf(pdf_file)

		return (response)


api.add_resource(ocrAPI,'/reqtform/<uuid_no>')

if __name__ == '__main__':
   app.run()