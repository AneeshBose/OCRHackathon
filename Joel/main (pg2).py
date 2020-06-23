from shapely.geometry import Polygon
from PIL import Image
import json
import matplotlib.pyplot as plt
import matplotlib



target_fields = ['Cologuard Order Number','Date Received by ES Labs',"Health Organization Name","Provider Name","Provider NPI", "Patient Name","Patient Date of Birth","Patient Sex","Patient Phone Number","Patient Shipping Address","Please Confirm Secure Fax #","Subscriber ID","Group Number","Policy Owner/Holder Name","Policy Owner/Holder Date of Birth"]
special_target_fields = ["Insurance Type",'Insurance Carrier Name',"ICD-10 Codes"]


other_texts = ['EXACT', 'COLOGUARD\u00ae ORDER', 'EXACT SCIENCES LABORATORIES, LLC', 'SCIENCES', '145 E Badger Rd, Ste 100. Madison, WI 53713', 'REQUISITION FORM', 'LABORATORIES', 'p: 844-870-8870 | ExactLabs.com', 'Stool-based ONA test with hemoglobin Immunoassay component', 'NPI: 1629407069 TIN: 463095174', 'Provider & Order Information,', 'PROVIDER INFORMATION', 'ORDER INFORMATION', 'This section is not intended to influence the medical judgment of an ordering', 'provider In determining whether this test is right for any particular patient. The', 'following codes are listed as a convenience. Ordering practitioners should report', 'the diagnosis code(s) that best describes the reason for performing the test.', 'ICD-10 Code:', 'Z12.11 and Z12.12 (Encounter for screening for malignant', 'neoplasm of colon [Z12.11] and rectum [212.12])', 'Certification', 'I am a licensed healthcare provider authorized to order Cologuard. This', 'test is medically necessary and the patient is eligible to use Cologuard.', 'will maintain the privacy of test results and related information as', 'required by HIPAA. I authorize Exact Sciences Laboratories to obtain', 'reimbursement for Cologuard and to directly contact and collect', 'additional samples from the patient as appropriate.', "'To receive results for this order, please provide secure FAX number only", 'Patient Demographics, Attacholc', 'PATIENT ETHNICITY AND RACE The completion of this section is optional.', "Please mark one or more to indicate your patient's race:", 'Patient Insurance/Billing Information.','PATIENT AUTHORIZATIONS, ASSIGNMENT OF BENEFITS (AOB) & FINANCIAL RESPONSIBILITIES', 'i authorize Exact Sciences Laboratories (Exact) to bill my insurance/health pion and furnish them with my Cologuard order information, test results, or other information requested', 'for reimbursement. I assign all rights and benefits under my insurance plans to Exoct ond authorize Exact to appeal and contest any reimbursement denial, including in any', 'administrative or civil proceedings necessary to pursue reimbursement, I authorize all reimbursements to be poid directly to the laboratory in consideration for services performed', 'I understand that i am responsible for any amount not paid, including amounts for non-covered services or services determined by my plon to be provided by an out-of-network', 'provider. I further understand that if I am a Medicard enrollee in a state where Exact is enrolled as a Medicaid provider, Exact will accept as payment in full the amounts paid by the', 'Medicaid progrom, plus ony deductible, cainsurance or copayment which may be required by the Medicaid program to be paid by me.', 'For Lab Use Only', 'FRM-3004-05-c', 'Fax completed form to 844-870-8875', 'February 2019', 'Sample Collected: _/ /_', 'Sample Received _/ /']
target_offsets = {'ICD-10 Codes': [0, -18, 286, -18, 286, 118, 0, 118], 'Insurance Type': [0, -15, 160, -16, 160, 25, 0, 26], 'Insurance Carrier Name': [0, -13, 452, -14, 452, 26, 0, 27]}

target_bounding_boxes = {}



filename = 'Sample_2b'
filename_jpg = filename + '.jpg'
filename_json = filename + '.json'
file_json = open(filename_json,'r')
analysis = file_json.read()
analysis = json.loads(analysis)

# For Visualization only
vertices = []
vertices_handwritten = []

# Count each occurence of 'City, State, Zip'
csz_counter = 0

def calculate_bounding_box(inputBox,offset):
	bounding_box = []
	bounding_box.append(offset[0])
	bounding_box.append(inputBox[1] + offset[1])
	bounding_box.append(1240)
	bounding_box.append(inputBox[3] + offset[3])
	bounding_box.append(1240)
	bounding_box.append(inputBox[5] + offset[5])
	bounding_box.append(offset[6])
	bounding_box.append(inputBox[7] + offset[7])
	return(bounding_box)

# Initialize target boxes
for index,line in enumerate(analysis["analyzeResult"]["readResults"][0]["lines"]):
	flag = 0
	for field in target_fields:
		if field.lower() in line['text'].lower() and field not in target_bounding_boxes:
			bounding_box_points = calculate_bounding_box(line['boundingBox'],[0,-5,0,-5,0,5,0,5])
			target_bounding_boxes[field] = [(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)]
			vertices.append([(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)])
			flag = 1
			break
	if flag == 0:
		for field in special_target_fields:
			if field.lower() in line['text'].lower() and field not in target_bounding_boxes:
				target_offsets[field][0] = 450
				target_offsets[field][6] = 450
				bounding_box_points = calculate_bounding_box(line['boundingBox'],target_offsets[field])
				target_bounding_boxes[field] = [(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)]
				vertices.append([(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)])


for i in target_fields:
	if i not in target_bounding_boxes:
		print(i)

field_mappings = {}


for index, line in enumerate(analysis["analyzeResult"]["readResults"][0]["lines"]):
	bounding_coord = [(line['boundingBox'][i], line['boundingBox'][i + 1]) for i in range(0, len(line['boundingBox']), 2)]
	# polygon_htext is response for each line in response
	polygon_htext = Polygon(bounding_coord)
	x1_coord = bounding_coord[0][0]
	for target_field in target_bounding_boxes:
		polygon_ptext = Polygon(target_bounding_boxes[target_field])

		if polygon_ptext.contains(polygon_htext) == True:
			if target_field not in field_mappings:
				field_mappings[target_field] = [[line['text'], x1_coord]]
			else:
				field_mappings[target_field] += [[line['text'], x1_coord]]
				field_mappings[target_field].sort(key=lambda x: x[1])

			break
		else:
			pass


for key_field in field_mappings:
	row = ''
	for vals in field_mappings[key_field]:
		row += vals[0] + ' '

	if 'City, State, Zip' in key_field:
		key_field_index = row.lower().find('City, State, Zip'.lower())
		key_field_len = len(key_field)
		str_key_field = row[key_field_index:key_field_index + key_field_len]
		key_field_prep = row.replace(str_key_field, '')
		
	else:
		key_field_index = row.lower().find(key_field.lower())
		key_field_len = len(key_field)
		str_key_field = row[key_field_index:key_field_index + key_field_len]
		key_field_prep = row.replace(str_key_field, '')

	underscore_prep = key_field_prep.replace('_', '')
	colon_prep = underscore_prep.replace(':', '')
	dot_prep = colon_prep.lstrip('.')
	dot_prep = dot_prep.rstrip('.')
	final_prep = (dot_prep.lstrip()).rstrip()
	field_mappings[key_field] = final_prep


print(field_mappings)
print(len(field_mappings))


image = Image.open(filename_jpg)
ax = plt.imshow(image)
for polygon in vertices:
	patch = matplotlib.patches.Polygon(polygon, closed=True, fill=False, linewidth=2, color='y')
	ax.axes.add_patch(patch)
	# plt.text(vertices[0][0], vertices[0][1], text, fontsize=20, va="top")

for polygon2 in vertices_handwritten:
	patch = matplotlib.patches.Polygon(polygon2, closed=True, fill=False, linewidth=2, color='b')
	ax.axes.add_patch(patch)
	# plt.text(vertices_handwritten[0][0], vertices_handwritten[0][1], text, fontsize=20, va="top")
plt.show()
