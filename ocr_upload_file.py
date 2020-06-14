import json
import os
import sys
import requests
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO
import pickle
from PIL import Image


# image_path = 'Aneesh_1'
# image_pdf = image_path + '.pdf'
# file_in_bytes = open(image_pdf, "rb").read()

image_path = '1'
image_jpg = image_path + '.jpg'



image = Image.open(image_jpg)
image = image.resize((1240,1754))
image2 = image.save('Sample_1b.jpg')

file_in_bytes = open('Sample_1b.jpg', "rb").read()


missing_env = False
# Add your Computer Vision subscription key and endpoint to your environment variables.
endpoint = 'https://computervisionmedicalsciences.cognitiveservices.azure.com'
subscription_key = 'd0e3653430044e4c88cb7806a08041ce'

text_recognition_url = endpoint + "/vision/v3.0/read/analyze"

# Set image_url to the URL of an image that you want to recognize.

headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type' : 'application/octet-stream'}
data = file_in_bytes
response = requests.post(
    text_recognition_url, headers=headers, json=None, data = data)
response.raise_for_status()

# Extracting text requires two API calls: One call to submit the
# image for processing, the other to retrieve the text found in the image.

# Holds the URI used to retrieve the recognized text.
operation_url = response.headers["Operation-Location"]

# The recognized text isn't immediately available, so poll to wait for completion.
analysis = {}
poll = True
while (poll):
    response_final = requests.get(
        response.headers["Operation-Location"], headers=headers)
    analysis = response_final.json()

    print(json.dumps(analysis, indent=4))

    write_data = json.dumps(analysis, indent = 4)

    time.sleep(1)
    if ("analyzeResult" in analysis):
        poll = False
    if ("status" in analysis and analysis['status'] == 'failed'):
        poll = False
out_file = image_path+'.json'
_ = open(out_file, "w").write(write_data)

polygons = []
if ("analyzeResult" in analysis):
    # Extract the recognized text, with bounding boxes.
    polygons = [(line["boundingBox"], line["text"])
                for line in analysis["analyzeResult"]["readResults"][0]["lines"]]

# Display the image and overlay it with the extracted text.
# image = Image.open(BytesIO(requests.get(image_url).content))
image = Image.open('Sample_1b.jpg')
ax = plt.imshow(image)
for polygon in polygons:
    vertices = [(polygon[0][i], polygon[0][i+1])
                for i in range(0, len(polygon[0]), 2)]
    text = polygon[1]
    patch = Polygon(vertices, closed=True, fill=False, linewidth=2, color='y')
    ax.axes.add_patch(patch)
    # plt.text(vertices[0][0], vertices[0][1], text, fontsize=20, va="top")
plt.show()




