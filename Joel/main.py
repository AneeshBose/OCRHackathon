from shapely.geometry import Polygon
from PIL import Image
import json 
import matplotlib.pyplot as plt
# from matplotlib.patches import Polygon


target_fields = ['Healthcare Organization Name:','Provider Name:','NPI #:','Other(s)','Location Address:','City, State, Zip','Phone Number:','Secure Fax Number":','Patient ID/MRN:','Phone Number (required):','First Name:','Last Name:','Language Preference (optional):','DOB (mm/dd/yyyy):','Shipping Address:','Billing Address:','City, State, Zip:','City, State, Zip:','Policyholder Name:','Policyholder DOB:','Primary Insurance Carrier:','Claims Submission Address:','Subscriber ID/Policy Number:','Group Number:','Plan:','Prior-Authorization Code (if available):','Date:']
other_texts = ['EXACT', 'COLOGUARD\u00ae ORDER', 'EXACT SCIENCES LABORATORIES, LLC', 'SCIENCES', '145 E Badger Rd, Ste 100. Madison, WI 53713', 'REQUISITION FORM', 'LABORATORIES', 'p: 844-870-8870 | ExactLabs.com', 'Stool-based ONA test with hemoglobin Immunoassay component', 'NPI: 1629407069 TIN: 463095174', 'Provider & Order Information,', 'PROVIDER INFORMATION', 'ORDER INFORMATION', 'This section is not intended to influence the medical judgment of an ordering', 'provider In determining whether this test is right for any particular patient. The', 'following codes are listed as a convenience. Ordering practitioners should report', 'the diagnosis code(s) that best describes the reason for performing the test.', 'ICD-10 Code:', 'Z12.11 and Z12.12 (Encounter for screening for malignant', 'neoplasm of colon [Z12.11] and rectum [212.12])', '@ Other(s)', 'Certification', 'I am a licensed healthcare provider authorized to order Cologuard. This', 'test is medically necessary and the patient is eligible to use Cologuard.', 'will maintain the privacy of test results and related information as', 'required by HIPAA. I authorize Exact Sciences Laboratories to obtain', 'reimbursement for Cologuard and to directly contact and collect', 'additional samples from the patient as appropriate.', "'To receive results for this order, please provide secure FAX number only", 'Ordering Provider Signature', 'Date of Order', 'Patient Demographics, Attacholc', 'O Home', 'O Mobile', 'O Work', 'Language Preference (optional):.', 'DOB (mm/dd/yyyy):.', 'Sex: O Male', 'O Female', 'Shipping Address:,', 'Same as Shipping', 'City, State, Zip:(Left2)', 'City, State, Zip:(Right1)', 'PATIENT ETHNICITY AND RACE The completion of this section is optional.', 'Is your patient of Hispanic or Latino origin or descent? O Yes', 'O No', "Please mark one or more to indicate your patient's race:", 'O White O Black or African-American O Asian O Native Hawaiian or other Pacific Islander O American Indian or Alaska Native', 'Patient Insurance/Billing Information.', 'Does patient wish Exact Sciences to bill their insurance? O Yes (complete below)', 'O No (patient will self-pay)', 'Relationship to patient: O Self O Spouse OOther', 'Type: O Private O Medicare O Medicare Advantage O Medicaid O Tricare', 'Plan: _', 'Prior-Authorization Code (if available): _', 'PATIENT AUTHORIZATIONS, ASSIGNMENT OF BENEFITS (AOB) & FINANCIAL RESPONSIBILITIES', 'i authorize Exact Sciences Laboratories (Exact) to bill my insurance/health pion and furnish them with my Cologuard order information, test results, or other information requested', 'for reimbursement. I assign all rights and benefits under my insurance plans to Exoct ond authorize Exact to appeal and contest any reimbursement denial, including in any', 'administrative or civil proceedings necessary to pursue reimbursement, I authorize all reimbursements to be poid directly to the laboratory in consideration for services performed', 'I understand that i am responsible for any amount not paid, including amounts for non-covered services or services determined by my plon to be provided by an out-of-network', 'provider. I further understand that if I am a Medicard enrollee in a state where Exact is enrolled as a Medicaid provider, Exact will accept as payment in full the amounts paid by the', 'Medicaid progrom, plus ony deductible, cainsurance or copayment which may be required by the Medicaid program to be paid by me.', 'Patient Signature:', 'For Lab Use Only', 'FRM-3004-05-c', 'Fax completed form to 844-870-8875', 'February 2019', 'Sample Collected: _/ /_', 'Sample Received _/ /']

target_offsets = {'Plan:':[0,0,0,0,0,0,0,0],'Prior-Authorization Code (if available):':[0,0,0,0,0,0,0,0],'Shipping Address:':[0,0,0,0,0,0,0,0],'Language Preference (optional):': [0,0,0,0,0,0,0,0],'Healthcare Organization Name:': [290, -21, 274, -19, 274, 16, 290, 15], 'Provider Name:': [147, -29, 420, -30, 420, 12, 147, 12], 'NPI #:': [63, -25, 506, -23, 506, 16, 63, 15], 'Location Address:': [161, -34, 400, -34, 400, 19, 161, 19], 'City, State, Zip1': [134, -24, 426, -25, 426, 19, 134, 20], 'Phone Number:': [147, -19, 417, -19, 417, 12, 147, 12], 'Secure Fax Number":': [194, -19, 368, -17, 368, 6, 194, 4], 'Patient ID/MRN:': [149, -16, 414, -16, 414, 13, 149, 13], 'Phone Number (required):': [244, -18, 313, -19, 313, -3, 244, -2], 'First Name:': [102, -21, 130, -22, 130, 17, 102, 18], 'Last Name:': [103, -20, 219, -20, 219, 18, 103, 18], 'DOB (mm/dd/yyyy):': [168, -24, 393, -24, 393, 51, 168, 51], 'Billing Address:': [141, -19, 408, -20, 408, 55, 141, 56], 'City, State, Zip2': [136, -20, 429, -21, 429, 2, 136, 2], 'City, State, Zip3': [136, -18, 416, -17, 416, 36, 136, 35], 'Policyholder Name:': [178, -20, 179, -20, 179, 15, 178, 16], 'Policyholder DOB:': [163, -18, 113, -16, 113, 19, 163, 18], 'Primary Insurance Carrier:': [241, -19, 227, -19, 227, 17, 241, 16], 'Claims Submission Address:': [254, -17, 876, -17, 875, 15, 254, 14], 'Subscriber ID/Policy Number:': [268, -19, 165, -19, 164, 13, 268, 12], 'Group Number:': [144, -20, 199, -20, 199, 13, 144, 13], 'Date:': [51, -12, 333, -14, 334, 6, 51, 7]}
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



# Count each occurence of 'City, State, Zip'
csz_counter = 0

# Initialize target boxes
for index,line in enumerate(analysis["analyzeResult"]["readResults"][0]["lines"]):
	if line['text'].startswith('City, State, Zip'):
		csz_counter += 1
		csz_key = 'City, State, Zip' + str(csz_counter)

		bounding_box_points = [x1 + x2 for (x1,x2) in zip(line['boundingBox'],target_offsets[csz_key])]
		target_bounding_boxes[csz_key] = [(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)]

		vertices.append([(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)])


	elif line['text'] in other_texts:
		pass

	# # Option A
	# elif line['text'] in target_fields:
	# 	print("Inside Target Fields")
	# 	bounding_box_points = [x1 + x2 for (x1,x2) in zip(line['boundingBox'],target_offsets[line['text']])]
	# 	target_bounding_boxes[line['text']] = [(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)]
	# 	vertices.append([(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)])


	# else:
	# 	print("Handwritten text:", line['text'])
	# 	handwritten_bounding_box = line['boundingBox']
	# 	handwritten_texts[line['text']] = [(handwritten_bounding_box[i], handwritten_bounding_box[i+1]) for i in range(0, len(handwritten_bounding_box), 2)]

	# Option B 
	else:
		flag = 0
		for field in target_fields:
			if line['text'].startswith(field):
				print(field)
				bounding_box_points = [x1 + x2 for (x1,x2) in zip(line['boundingBox'],target_offsets[field])]
				target_bounding_boxes[field] = [(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)]
				vertices.append([(bounding_box_points[i], bounding_box_points[i+1]) for i in range(0, len(bounding_box_points), 2)])

				flag = 1
				break

		if flag == 0:
			# print("Handwritten text:", line['text'])
			handwritten_bounding_box = line['boundingBox']
			handwritten_texts[line['text']] = [(handwritten_bounding_box[i], handwritten_bounding_box[i+1]) for i in range(0, len(handwritten_bounding_box), 2)]
			print(handwritten_texts)

# image = Image.open(filename_jpg)
# ax = plt.imshow(image)
# for polygon in vertices:
#     patch = Polygon(polygon, closed=True, fill=False, linewidth=2, color='y')
#     ax.axes.add_patch(patch)
#     # plt.text(vertices[0][0], vertices[0][1], text, fontsize=20, va="top")
# plt.show()


print(handwritten_texts)

for handwritten_text in handwritten_texts:
	print(handwritten_text)
	polygon_htext = Polygon(handwritten_texts[handwritten_text])
	for target_field in target_bounding_boxes:
		polygon_ptext = Polygon(target_bounding_boxes[target_field])

		if polygon_ptext.contains(polygon_htext) == True:
			field_mappings[target_field] = handwritten_text
			print("Target Field",target_field)
			print("Handwritten text",handwritten_text)
			break
		else:
			print("FAIL")
print(field_mappings)