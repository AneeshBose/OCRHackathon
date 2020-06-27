import pyrebase
from flask import Flask, request
from flask_restful import Resource, Api
from parse_pdf import first_page
from utils import convert_pdf, resize_image
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
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
		upload_file = str(uuid_no)
		storage.child(upload_file).download(upload_file)

		image_paths = []
		if upload_file.endswith('.pdf'):
			image_paths = convert_pdf(upload_file)
		else:
			image_paths.append(upload_file)

		resize_image(image_paths)
		response = first_page(image_paths[0])

		return (response)


api.add_resource(ocrAPI,'/reqtform/<uuid_no>')

if __name__ == '__main__':
   app.run()