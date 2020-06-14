from PIL import Image
import json 
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

filename = '2'
filename_json = filename + '.json'
filename_jpg = filename + '.jpg'


file_json = open(filename_json,'r')
analysis = file_json.read()
analysis = json.loads(analysis)

polygons = []
if ("analyzeResult" in analysis):
    # Extract the recognized text, with bounding boxes.
    polygons = [(line["boundingBox"], line["text"])
                for line in analysis["analyzeResult"]["readResults"][0]["lines"]]


for polygon in polygons:
	print(polygon[1])

# Display the image and overlay it with the extracted text.
# image = Image.open(BytesIO(requests.get(image_url).content))
image = Image.open(filename_jpg)
ax = plt.imshow(image)
for polygon in polygons:
    vertices = [(polygon[0][i], polygon[0][i+1])
                for i in range(0, len(polygon[0]), 2)]
    text = polygon[1]
    patch = Polygon(vertices, closed=True, fill=False, linewidth=2, color='y')
    ax.axes.add_patch(patch)
    # plt.text(vertices[0][0], vertices[0][1], text, fontsize=20, va="top")
plt.show()
plt.savefig('sample_1.pdf')

