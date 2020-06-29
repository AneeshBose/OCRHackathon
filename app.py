from flask import Flask, request
from flask_restful import Resource, Api
from parse_pdf import requisiton_page,info_page
from utils import convert_pdf, resize_image
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class ocrAPI(Resource):
	def get(self, uuid_no,page_id):
		upload_file = str(uuid_no)
		image_paths = []
		if upload_file.endswith('.pdf'):
			image_paths = convert_pdf(upload_file)
		else:
			image_paths.append(upload_file)

		resize_image(image_paths)
		if page_id == '0':
			response = requisiton_page(image_paths)
		if page_id == '1':
			response = info_page(image_paths)

		return (response)


api.add_resource(ocrAPI,'/reqtform/<uuid_no>/<page_id>')

if __name__ == '__main__':
   app.run()
