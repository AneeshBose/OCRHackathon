from shapely.geometry import Polygon
from PIL import Image
import json 
import matplotlib.pyplot as plt
import matplotlib

target_fields = ['Healthcare Organization Name', 'Provider Name', 'NPI #', 'Other(s)', 'Location Address', 'City, State, Zip1', 'Phone Number', 'Secure Fax Number', 'Patient ID/MRN', 'Phone Number (required)', 'First Name', 'Language Preference (optional)', 'DOB (mm/dd/yyyy)', 'Shipping Address', 'Billing Address', 'City, State, Zip2', 'City, State, Zip3', 'Policyholder Name', 'Primary Insurance Carrier', 'Claims Submission Address', 'Subscriber ID/Policy Number', 'Prior-Authorization Code (if available)', 'Patient Signature']

other_texts = ['EXACT', 'COLOGUARD\u00ae ORDER', 'EXACT SCIENCES LABORATORIES, LLC', 'SCIENCES', '145 E Badger Rd, Ste 100. Madison, WI 53713', 'REQUISITION FORM', 'LABORATORIES', 'p: 844-870-8870 | ExactLabs.com', 'Stool-based ONA test with hemoglobin Immunoassay component', 'NPI: 1629407069 TIN: 463095174', 'Provider & Order Information,', 'PROVIDER INFORMATION', 'ORDER INFORMATION', 'This section is not intended to influence the medical judgment of an ordering', 'provider In determining whether this test is right for any particular patient. The', 'following codes are listed as a convenience. Ordering practitioners should report', 'the diagnosis code(s) that best describes the reason for performing the test.', 'ICD-10 Code:', 'Z12.11 and Z12.12 (Encounter for screening for malignant', 'neoplasm of colon [Z12.11] and rectum [212.12])', '@ Other(s)', 'Certification', 'I am a licensed healthcare provider authorized to order Cologuard. This', 'test is medically necessary and the patient is eligible to use Cologuard.', 'will maintain the privacy of test results and related information as', 'required by HIPAA. I authorize Exact Sciences Laboratories to obtain', 'reimbursement for Cologuard and to directly contact and collect', 'additional samples from the patient as appropriate.', "'To receive results for this order, please provide secure FAX number only", 'Ordering Provider Signature', 'Date of Order', 'Patient Demographics, Attacholc', 'O Home', 'O Mobile', 'O Work', 'Language Preference (optional):.', 'DOB (mm/dd/yyyy):.', 'Sex: O Male', 'O Female', 'Shipping Address:,', 'Same as Shipping', 'City, State, Zip:(Left2)', 'City, State, Zip:(Right1)', 'PATIENT ETHNICITY AND RACE The completion of this section is optional.', 'Is your patient of Hispanic or Latino origin or descent? O Yes', 'O No', "Please mark one or more to indicate your patient's race:", 'O White O Black or African-American O Asian O Native Hawaiian or other Pacific Islander O American Indian or Alaska Native', 'Patient Insurance/Billing Information.', 'Does patient wish Exact Sciences to bill their insurance? O Yes (complete below)', 'O No (patient will self-pay)', 'Relationship to patient: O Self O Spouse OOther', 'Type: O Private O Medicare O Medicare Advantage O Medicaid O Tricare', 'Plan: _', 'Prior-Authorization Code (if available): _', 'PATIENT AUTHORIZATIONS, ASSIGNMENT OF BENEFITS (AOB) & FINANCIAL RESPONSIBILITIES', 'i authorize Exact Sciences Laboratories (Exact) to bill my insurance/health pion and furnish them with my Cologuard order information, test results, or other information requested', 'for reimbursement. I assign all rights and benefits under my insurance plans to Exoct ond authorize Exact to appeal and contest any reimbursement denial, including in any', 'administrative or civil proceedings necessary to pursue reimbursement, I authorize all reimbursements to be poid directly to the laboratory in consideration for services performed', 'I understand that i am responsible for any amount not paid, including amounts for non-covered services or services determined by my plon to be provided by an out-of-network', 'provider. I further understand that if I am a Medicard enrollee in a state where Exact is enrolled as a Medicaid provider, Exact will accept as payment in full the amounts paid by the', 'Medicaid progrom, plus ony deductible, cainsurance or copayment which may be required by the Medicaid program to be paid by me.', 'Patient Signature:', 'For Lab Use Only', 'FRM-3004-05-c', 'Fax completed form to 844-870-8875', 'February 2019', 'Sample Collected: _/ /_', 'Sample Received _/ /']

target_offsets = {'Healthcare Organization Name': [-51, -38, 600, -36, 600, 16, -51, 15], 'Provider Name': [-52, -29, 599, -30, 599, 12, -52, 12], 'NPI #': [-51, -25, 600, -23, 600, 44, -51, 43], 'Other(s)': [-26, -11, 605, -12, 605, 18, -26, 20], 'Location Address': [-53, -34, 598, -34, 598, 19, -53, 19], 'City, State, Zip1': [-53, -24, 598, -25, 598, 19, -53, 20], 'Phone Number': [-52, -19, 599, -19, 599, 12, -52, 12], 'Secure Fax Number': [-53, -19, 598, -17, 598, 6, -53, 4], 'Patient ID/MRN': [-51, -16, 600, -16, 600, 13, -51, 13], 'Phone Number (required)': [-24, -18, 607, -19, 607, -3, -24, -2], 'First Name': [-55, -24, 596, -25, 596, 17, -55, 18], 'Language Preference (optional)': [-26, -19, 605, -18, 605, 14, -26, 13], 'DOB (mm/dd/yyyy)': [-56, -17, 595, -18, 595, 0, -56, 0], 'Shipping Address': [-54, -24, 597, -24, 597, 51, -54, 51], 'Billing Address': [-28, -19, 603, -20, 603, 55, -28, 56], 'City, State, Zip2': [-54, -20, 597, -21, 597, 8, -54, 8], 'City, State, Zip3': [-26, -18, 605, -17, 605, 36, -26, 35], 'Policyholder Name': [-55, -20, 1186, -20, 1186, 16, -55, 17], 'Primary Insurance Carrier': [-54, -19, 1187, -19, 1187, 17, -54, 16], 'Claims Submission Address': [-56, -17, 1185, -17, 1185, 15, -56, 14], 'Subscriber ID/Policy Number': [-55, -17, 1186, -17, 1186, 15, -55, 14], 'Prior-Authorization Code (if available)': [-57, -15, 1184, -15, 1184, 6, -57, 6], 'Patient Signature': [-60, -15, 1181, -15, 1181, 17, -60, 17]}
target_bounding_boxes = {}
handwritten_texts = {}
field_mappings = {}


filename = 'Aneesh_2_p0b'
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
	bounding_box.append(inputBox[0] + offset[0])
	bounding_box.append(inputBox[1] + offset[1])
	bounding_box.append(inputBox[0] + 1 + offset[2])
	bounding_box.append(inputBox[3] + offset[3])
	bounding_box.append(inputBox[0] + 1 + offset[4])
	bounding_box.append(inputBox[5] + offset[5])	
	bounding_box.append(inputBox[6] + offset[6])
	bounding_box.append(inputBox[7] + offset[7])
	return(bounding_box)


# Initialize target boxes
for index,line in enumerate(analysis["analyzeResult"]["readResults"][0]["lines"]):
	if ('City, State, Zip').lower() in line['text'].lower():
		csz_counter += 1
		csz_key = 'City, State, Zip' + str(csz_counter)

		bounding_box_points = calculate_bounding_box(line['boundingBox'],target_offsets[csz_key])
		target_bounding_boxes[csz_key] = [(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)]

		vertices.append([(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)])


	elif line['text'] in other_texts:
		pass

	else:
		flag = 0
		for field in target_fields:
			if 'Policyholder' not in field:
				if field.lower() in line['text'].lower() and field not in target_bounding_boxes:
					# print(field)
					bounding_box_points = calculate_bounding_box(line['boundingBox'],target_offsets[field])
					target_bounding_boxes[field] = [(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)]
					vertices.append([(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)])
					flag = 1
					break
			else:
				if (line['text'].lower()).startswith(field.lower()):
					# print(field)
					bounding_box_points = calculate_bounding_box(line['boundingBox'],target_offsets[field])
					target_bounding_boxes[field] = [(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)]
					vertices.append([(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)])
					flag = 1
					break
		if flag == 0:
			bounding_box_points = line['boundingBox']
			handwritten_box = [(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)]
			vertices_handwritten.append(handwritten_box)


for index, line in enumerate(analysis["analyzeResult"]["readResults"][0]["lines"]):
	bounding_coord = [(line['boundingBox'][i], line['boundingBox'][i + 1]) for i in
					  range(0, len(line['boundingBox']), 2)]
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
				# print(field_mappings)
				field_mappings[target_field].sort(key=lambda x: x[1])
			# print("Target Field", target_field)
			# print("Handwritten text", line['text'])
			break

for i in target_fields:
	if i not in field_mappings:
		print(i)


for key_field in field_mappings:
	row = ''
	for vals in field_mappings[key_field]:
		row += vals[0]+' '
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
	final_prep = (colon_prep.lstrip()).rstrip()
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