from PIL import Image
import json 
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

filename = 'Sample_1b'
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
target_fields = ['Healthcare Organization Name:','Provider Name:','NPI #:','Other(s)','Location Address:','City, State, Zip','Phone Number:','Secure Fax Number":','Patient ID/MRN:','Phone Number (required):','First Name:','Last Name:','Language Preference (optional):','DOB (mm/dd/yyyy):','Shipping Address:','Billing Address:','City, State, Zip:','City, State, Zip:','Policyholder Name:','Policyholder DOB:','Primary Insurance Carrier:','Claims Submission Address:','Subscriber ID/Policy Number:','Group Number:','Plan:','Prior-Authorization Code (if available):','Date:']
other_texts = []

for polygon in polygons:
    if polygon[1] not in target_fields:
        other_texts.append(polygon[1])
# 	print("LineText is: ",polygon[1])



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

# print(other_texts)

