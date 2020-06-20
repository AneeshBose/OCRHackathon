from shapely.geometry import Polygon
from PIL import Image
import json 
import matplotlib.pyplot as plt
import matplotlib

target_fields = ['Healthcare Organization Name', 'Provider Name', 'NPI #', 'Other(s)', 'Location Address', 'City, State, Zip1', 'Phone Number', 'Secure Fax Number', 'Patient ID/MRN', 'Phone Number (required)', 'First Name', 'Language Preference (optional)', 'DOB (mm/dd/yyyy)', 'Shipping Address', 'Billing Address', 'City, State, Zip2', 'City, State, Zip3', 'Policyholder Name', 'Primary Insurance Carrier', 'Claims Submission Address', 'Subscriber ID/Policy Number', 'Prior-Authorization Code (if available)', 'Date']
other_texts = ['EXACT', 'COLOGUARD\u00ae ORDER', 'EXACT SCIENCES LABORATORIES, LLC', 'SCIENCES', '145 E Badger Rd, Ste 100. Madison, WI 53713', 'REQUISITION FORM', 'LABORATORIES', 'p: 844-870-8870 | ExactLabs.com', 'Stool-based ONA test with hemoglobin Immunoassay component', 'NPI: 1629407069 TIN: 463095174', 'Provider & Order Information,', 'PROVIDER INFORMATION', 'ORDER INFORMATION', 'This section is not intended to influence the medical judgment of an ordering', 'provider In determining whether this test is right for any particular patient. The', 'following codes are listed as a convenience. Ordering practitioners should report', 'the diagnosis code(s) that best describes the reason for performing the test.', 'ICD-10 Code:', 'Z12.11 and Z12.12 (Encounter for screening for malignant', 'neoplasm of colon [Z12.11] and rectum [212.12])', '@ Other(s)', 'Certification', 'I am a licensed healthcare provider authorized to order Cologuard. This', 'test is medically necessary and the patient is eligible to use Cologuard.', 'will maintain the privacy of test results and related information as', 'required by HIPAA. I authorize Exact Sciences Laboratories to obtain', 'reimbursement for Cologuard and to directly contact and collect', 'additional samples from the patient as appropriate.', "'To receive results for this order, please provide secure FAX number only", 'Ordering Provider Signature', 'Date of Order', 'Patient Demographics, Attacholc', 'O Home', 'O Mobile', 'O Work', 'Language Preference (optional):.', 'DOB (mm/dd/yyyy):.', 'Sex: O Male', 'O Female', 'Shipping Address:,', 'Same as Shipping', 'City, State, Zip:(Left2)', 'City, State, Zip:(Right1)', 'PATIENT ETHNICITY AND RACE The completion of this section is optional.', 'Is your patient of Hispanic or Latino origin or descent? O Yes', 'O No', "Please mark one or more to indicate your patient's race:", 'O White O Black or African-American O Asian O Native Hawaiian or other Pacific Islander O American Indian or Alaska Native', 'Patient Insurance/Billing Information.', 'Does patient wish Exact Sciences to bill their insurance? O Yes (complete below)', 'O No (patient will self-pay)', 'Relationship to patient: O Self O Spouse OOther', 'Type: O Private O Medicare O Medicare Advantage O Medicaid O Tricare', 'Plan: _', 'Prior-Authorization Code (if available): _', 'PATIENT AUTHORIZATIONS, ASSIGNMENT OF BENEFITS (AOB) & FINANCIAL RESPONSIBILITIES', 'i authorize Exact Sciences Laboratories (Exact) to bill my insurance/health pion and furnish them with my Cologuard order information, test results, or other information requested', 'for reimbursement. I assign all rights and benefits under my insurance plans to Exoct ond authorize Exact to appeal and contest any reimbursement denial, including in any', 'administrative or civil proceedings necessary to pursue reimbursement, I authorize all reimbursements to be poid directly to the laboratory in consideration for services performed', 'I understand that i am responsible for any amount not paid, including amounts for non-covered services or services determined by my plon to be provided by an out-of-network', 'provider. I further understand that if I am a Medicard enrollee in a state where Exact is enrolled as a Medicaid provider, Exact will accept as payment in full the amounts paid by the', 'Medicaid progrom, plus ony deductible, cainsurance or copayment which may be required by the Medicaid program to be paid by me.', 'Patient Signature:', 'For Lab Use Only', 'FRM-3004-05-c', 'Fax completed form to 844-870-8875', 'February 2019', 'Sample Collected: _/ /_', 'Sample Received _/ /']

target_offsets = {'Healthcare Organization Name': [-2, -21, 565, -19, 565, 16, -2, 15], 'Provider Name': [-2, -29, 564, -30, 564, 12, -2, 12], 'NPI #': [-2, -25, 565, -23, 565, 16, -2, 15], 'Other(s)': [-2, -11, 553, -12, 553, 18, -2, 20], 'Location Address': [-3, -34, 563, -34, 563, 19, -3, 19], 'City, State, Zip1': [-2, -24, 563, -25, 563, 19, -2, 20], 'Phone Number': [-2, -19, 564, -19, 564, 12, -2, 12], 'Secure Fax Number': [-2, -19, 563, -17, 563, 6, -2, 4], 'Patient ID/MRN': [-2, -16, 565, -16, 565, 13, -2, 13], 'Phone Number (required)': [-2, -18, 560, -19, 560, -3, -2, -2], 'First Name': [-4, -24, 563, -25, 563, 17, -4, 18], 'Language Preference (optional)': [-2, -19, 555, -18, 555, 14, -2, 13], 'DOB (mm/dd/yyyy)': [-2, -17, 319, -18, 319, 0, -2, 0], 'Shipping Address': [-2, -24, 564, -24, 564, 51, -2, 51], 'Billing Address': [-2, -19, 554, -20, 554, 55, -2, 56], 'City, State, Zip2': [-2, -20, 566, -21, 566, 2, -2, 2], 'City, State, Zip3': [-2, -18, 555, -17, 555, 36, -2, 35], 'Policyholder Name': [-2, -20, 1184, -20, 1184, 16, -2, 17], 'Primary Insurance Carrier': [-2, -19, 1185, -19, 1185, 17, -2, 16], 'Claims Submission Address': [-2, -17, 1183, -17, 1183, 15, -2, 14], 'Subscriber ID/Policy Number': [-2, -17, 1184, -17, 1184, 15, -2, 14], 'Prior-Authorization Code (if available)': [-2, -15, 1182, -15, 1182, 6, -2, 6], 'Date': [-2, -12, 385, -14, 385, 6, -2, 7]}
target_bounding_boxes = {}
handwritten_texts = {}
field_mappings = {}


filename = 'Aneesh_1-2b'
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
	if line['text'].startswith('City, State, Zip'):
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
			if field in line['text']:
				# print(field)
				bounding_box_points = calculate_bounding_box(line['boundingBox'],target_offsets[field])
				target_bounding_boxes[field] = [(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)]
				vertices.append([(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)])

				flag = 1
				break

		if flag == 0:
			# print("Handwritten text:", line['text'])
			handwritten_bounding_box = line['boundingBox']
			handwritten_texts[line['text']] = [(handwritten_bounding_box[i], handwritten_bounding_box[i+1]) for i in range(0, len(handwritten_bounding_box), 2)]
			
			vertices_handwritten.append([(handwritten_bounding_box[i], handwritten_bounding_box[i+1]) for i in range(0, len(handwritten_bounding_box), 2)])
			# print(handwritten_texts)



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

# #Option A
# for handwritten_text in handwritten_texts:
# 	print(handwritten_text)
# 	polygon_htext = Polygon(handwritten_texts[handwritten_text])
# 	for target_field in target_bounding_boxes:
# 		polygon_ptext = Polygon(target_bounding_boxes[target_field])

# 		if polygon_ptext.contains(polygon_htext) == True:
# 			field_mappings[target_field] = handwritten_text
# 			print("Target Field",target_field)
# 			print("Handwritten text",handwritten_text)
# 			break
# 		else:
# 			print("FAIL")
# print(field_mappings)
# print(len(field_mappings))

# print(target_bounding_boxes)
# #Option B
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
		else:
			pass
			# print("FAIL")
for key_field in field_mappings:
	row = ''
	for vals in field_mappings[key_field]:
		row += vals[0]+' '
	if 'City, State, Zip' in key_field:
		key_field_prep = row.replace('City, State, Zip', '')
	else:
		key_field_prep = row.replace(key_field, '')
	underscore_prep = key_field_prep.replace('_', '')
	colon_prep = underscore_prep.replace(':', '')
	final_prep = (colon_prep.lstrip()).rstrip()
	field_mappings[key_field] = final_prep
print(field_mappings)