from shapely.geometry import Polygon
from PIL import Image
import json
import matplotlib.pyplot as plt
import matplotlib
from utils import char2num

target_fields = ['Healthcare Organization Name', 'Provider Name', 'NPI #', 'Other(s)', 'Location Address', 'City, State, Zip1', 'Phone Number', 'Secure Fax Number', 'Patient ID/MRN', 'Phone Number (required)', 'First Name', 'Language Preference (optional)', 'DOB (m', 'Shipping Address', 'Billing Address', 'City, State, Zip2', 'Policyholder Name', 'Primary Insurance Carrier', 'Claims Submission Address', 'Subscriber ID/Policy Number', 'Prior-Authorization Code (if available)', 'Patient Signature']
other_texts = ['EXACT', 'COLOGUARD\u00ae ORDER', 'EXACT SCIENCES LABORATORIES, LLC', 'SCIENCES', '145 E Badger Rd, Ste 100. Madison, WI 53713', 'REQUISITION FORM', 'LABORATORIES', 'p: 844-870-8870 | ExactLabs.com', 'Stool-based ONA test with hemoglobin Immunoassay component', 'NPI: 1629407069 TIN: 463095174', 'Provider & Order Information,', 'PROVIDER INFORMATION', 'ORDER INFORMATION', 'This section is not intended to influence the medical judgment of an ordering', 'provider In determining whether this test is right for any particular patient. The', 'following codes are listed as a convenience. Ordering practitioners should report', 'the diagnosis code(s) that best describes the reason for performing the test.', 'ICD-10 Code:', 'Z12.11 and Z12.12 (Encounter for screening for malignant', 'neoplasm of colon [Z12.11] and rectum [212.12])', 'Certification', 'I am a licensed healthcare provider authorized to order Cologuard. This', 'test is medically necessary and the patient is eligible to use Cologuard.', 'will maintain the privacy of test results and related information as', 'required by HIPAA. I authorize Exact Sciences Laboratories to obtain', 'reimbursement for Cologuard and to directly contact and collect', 'additional samples from the patient as appropriate.', "'To receive results for this order, please provide secure FAX number only", 'Patient Demographics, Attacholc', 'PATIENT ETHNICITY AND RACE The completion of this section is optional.', "Please mark one or more to indicate your patient's race:", 'Patient Insurance/Billing Information.','PATIENT AUTHORIZATIONS, ASSIGNMENT OF BENEFITS (AOB) & FINANCIAL RESPONSIBILITIES', 'i authorize Exact Sciences Laboratories (Exact) to bill my insurance/health pion and furnish them with my Cologuard order information, test results, or other information requested', 'for reimbursement. I assign all rights and benefits under my insurance plans to Exoct ond authorize Exact to appeal and contest any reimbursement denial, including in any', 'administrative or civil proceedings necessary to pursue reimbursement, I authorize all reimbursements to be poid directly to the laboratory in consideration for services performed', 'I understand that i am responsible for any amount not paid, including amounts for non-covered services or services determined by my plon to be provided by an out-of-network', 'provider. I further understand that if I am a Medicard enrollee in a state where Exact is enrolled as a Medicaid provider, Exact will accept as payment in full the amounts paid by the', 'Medicaid progrom, plus ony deductible, cainsurance or copayment which may be required by the Medicaid program to be paid by me.', 'For Lab Use Only', 'FRM-3004-05-c', 'Fax completed form to 844-870-8875', 'February 2019', 'Sample Collected: _/ /_', 'Sample Received _/ /']

target_offsets = {'Healthcare Organization Name': [-51, -38, 605, -36, 605, 16, -51, 15], 'Provider Name': [-52, -29, 604, -30, 604, 12, -52, 12], 'NPI #': [-51, -25, 605, -23, 605, 44, -51, 43], 'Other(s)': [-26, -11, 605, -12, 605, 18, -26, 20], 'Location Address': [-53, -34, 603, -34, 603, 19, -53, 19], 'City, State, Zip1': [-53, -24, 603, -25, 603, 19, -53, 20], 'Phone Number': [-52, -19, 604, -19, 604, 12, -52, 12], 'Secure Fax Number': [-53, -19, 603, -17, 603, 6, -53, 4], 'Patient ID/MRN': [-51, -16, 605, -16, 605, 13, -51, 13], 'Phone Number (required)': [-24, -18, 607, -19, 607, -3, -24, -2], 'First Name': [-55, -24, 601, -25, 601, 17, -55, 18], 'Language Preference (optional)': [-26, -19, 605, -18, 605, 14, -26, 13], 'DOB (m': [-56, -17, 600, -18, 600, 0, -56, 0], 'Shipping Address': [-54, -24, 602, -24, 602, 51, -54, 51], 'Billing Address': [-28, -19, 603, -20, 603, 55, -28, 56], 'City, State, Zip2': [-54, -20, 1187, -21, 1187, 8, -54, 8], 'Policyholder Name': [-55, -20, 1186, -20, 1186, 16, -55, 17], 'Primary Insurance Carrier': [-54, -19, 1187, -19, 1187, 17, -54, 16], 'Claims Submission Address': [-56, -17, 1185, -17, 1185, 15, -56, 14], 'Subscriber ID/Policy Number': [-55, -17, 1186, -17, 1186, 15, -55, 14], 'Prior-Authorization Code (if available)': [-57, -15, 1184, -15, 1184, 6, -57, 6], 'Patient Signature': [-60, -30, 1181, -30, 1181, 17, -60, 17]}
target_bounding_boxes = {}
handwritten_texts = {}


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
csz_counter = 0
for index,line in enumerate(analysis["analyzeResult"]["readResults"][0]["lines"]):
	if ('City, State, Zip').lower() in line['text'].lower():
		if line['boundingBox'][0] < 120:
			print(line['boundingBox'])
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

print(target_bounding_boxes)

field_mappings = {}
shipping_add = []
billing_add = []
ship_line_1 = []
ship_line_2 = []
bill_line_1 = []
bill_line_2 = []

for index, line in enumerate(analysis["analyzeResult"]["readResults"][0]["lines"]):
	bounding_coord = [(line['boundingBox'][i], line['boundingBox'][i + 1]) for i in range(0, len(line['boundingBox']), 2)]
	# polygon_htext is response for each line in response
	polygon_htext = Polygon(bounding_coord)
	x1_coord = bounding_coord[0][0]
	for target_field in target_bounding_boxes:
		polygon_ptext = Polygon(target_bounding_boxes[target_field])

		if polygon_ptext.contains(polygon_htext) == True:
			print(line['text'])
			print(target_field)

			if 'Shipping Address' in target_field:
				shipping_add.append((line['text'],[(line['boundingBox'][i],line['boundingBox'][i+1]) for i in range(0,len(line['boundingBox']),2)]))
			elif 'Billing Address' in target_field:
				billing_add.append((line['text'],[(line['boundingBox'][i],line['boundingBox'][i+1]) for i in range(0,len(line['boundingBox']),2)]))
			else:
				if target_field not in field_mappings:
					field_mappings[target_field] = [[line['text'], x1_coord]]
				else:
					field_mappings[target_field] += [[line['text'], x1_coord]]
					field_mappings[target_field].sort(key=lambda x: x[1])
				break
		else:
			pass



for pair in shipping_add:
	if 'Shipping Address' in pair[0]:
		baseline = max(pair[1][2][1],pair[1][3][1])
for pair in shipping_add:
	if int((min(pair[1][0][1],pair[1][1][1]) + max(pair[1][2][1],pair[1][3][1]))/2) <= baseline:
		ship_line_1.append(pair)
	else:
		ship_line_2.append(pair)


ship_add = ''
ship_line_1.sort(key = lambda x:x[1][0][0])
for pair in ship_line_1:
	ship_add += pair[0]+' '
ship_line_2.sort(key = lambda x:x[1][0][0])
for pair in ship_line_2:
	ship_add += pair[0]+' '
field_mappings['Shipping Address'] = [[ship_add,0]]

for pair in billing_add:
	if 'Billing Address' in pair[0]:
		baseline = max(pair[1][2][1],pair[1][3][1])
for pair in billing_add:
	if int((min(pair[1][0][1],pair[1][1][1]) + max(pair[1][2][1],pair[1][3][1]))/2) <= baseline:
		bill_line_1.append(pair)
	else:
		bill_line_2.append(pair)
bill_add = ''
bill_line_1.sort(key = lambda x:x[1][0][0])
for pair in bill_line_1:
	bill_add += pair[0]+' '
bill_line_2.sort(key = lambda x:x[1][0][0])
for pair in bill_line_2:
	bill_add += pair[0]+' '
bill_add = bill_add.replace('Same as Shipping ','')
field_mappings['Billing Address'] = [[bill_add,0]]

#2 cases to handle for same as shipping case when Billing Address is empty!!!!
#print(field_mappings['Shipping Address'],field_mappings['Billing Address'])

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
	dot_prep = colon_prep.lstrip('.')
	dot_prep = dot_prep.rstrip('.')
	final_prep = (dot_prep.lstrip()).rstrip()
	field_mappings[key_field] = final_prep

if 'Policyholder Name' in field_mappings:
	left_text = field_mappings['Policyholder Name']
	key_field_index = left_text.lower().find('Policyholder DOB'.lower())
	first_field = left_text[:key_field_index]
	second_field = left_text[key_field_index + len('Policyholder DOB'):]
	field_mappings['Policyholder Name'], field_mappings['Policyholder DOB'] = first_field, second_field
	field_mappings['Policyholder Name'] = field_mappings['Policyholder Name'].lstrip().rstrip()

	key_field_index = field_mappings['Policyholder DOB'].lower().find('Relationship'.lower())
	field_mappings['Policyholder DOB'] = field_mappings['Policyholder DOB'][:key_field_index]
	field_mappings['Policyholder DOB'] = field_mappings['Policyholder DOB'].lstrip().rstrip()

if 'First Name' in field_mappings:
	left_text = field_mappings['First Name']
	key_field_index = left_text.lower().find('Last Name'.lower())
	first_field = left_text[:key_field_index]
	second_field = left_text[key_field_index + len('Last Name'):]
	field_mappings['First Name'], field_mappings['Last Name'] = first_field, second_field
	field_mappings['First Name'] = field_mappings['First Name'].lstrip().rstrip()
	field_mappings['Last Name'] = field_mappings['Last Name'].lstrip().rstrip()

if 'City, State, Zip2' in field_mappings:
	left_text = field_mappings['City, State, Zip2']
	key_field_index = left_text.lower().find('city, State, Zip'.lower())
	first_field = left_text[:key_field_index]
	second_field = left_text[key_field_index + len('city, State, Zip'):]
	field_mappings['City, State, Zip2'], field_mappings['City, State, Zip3'] = first_field, second_field
	field_mappings['City, State, Zip2'] = field_mappings['City, State, Zip2'].lstrip().rstrip()
	field_mappings['City, State, Zip3'] = field_mappings['City, State, Zip3'].lstrip().rstrip()

if 'Primary Insurance Carrier' in field_mappings:
	left_text = field_mappings['Primary Insurance Carrier']
	key_field_index = left_text.lower().find('Type'.lower())
	first_field = left_text[:key_field_index]
	field_mappings['Primary Insurance Carrier'] = first_field
	field_mappings['Primary Insurance Carrier'] = field_mappings['Primary Insurance Carrier'].lstrip().rstrip()

if 'Subscriber ID/Policy Number' in field_mappings:
	left_text = field_mappings['Subscriber ID/Policy Number']
	key_field_index1 = left_text.lower().find('Group Number'.lower())
	key_field_index2 = left_text.lower().find('Plan'.lower())
	first_field = left_text[:key_field_index1]
	second_field = left_text[key_field_index1 + len('Group Number') :key_field_index2]
	third_field = left_text[key_field_index2 + len('Plan'):]
	field_mappings['Subscriber ID/Policy Number'], field_mappings['Group Number'], field_mappings['Plan'] = first_field, second_field, third_field
	field_mappings['Subscriber ID/Policy Number'] = field_mappings['Subscriber ID/Policy Number'].lstrip().rstrip()
	field_mappings['Group Number'] = field_mappings['Group Number'].lstrip().rstrip()
	field_mappings['Plan'] = field_mappings['Plan'].lstrip().rstrip()

if 'Patient Signature' in field_mappings:
	left_text = field_mappings['Patient Signature']
	key_field_index = left_text.lower().find('Date'.lower())
	first_field = left_text[:key_field_index]
	second_field = left_text[key_field_index + len('Date'):]
	field_mappings['Date'] = second_field
	field_mappings['Date'] = field_mappings['Date'].lstrip().rstrip()
	del field_mappings['Patient Signature']

if 'DOB (m' in field_mappings:
	left_text = field_mappings['DOB (m']
	key_field_index = left_text.lower().find('Sex'.lower())
	first_field = left_text[:key_field_index]
	field_mappings['DOB (mm/dd/yyyy)'] = first_field
	field_mappings['DOB (mm/dd/yyyy)'] = field_mappings['DOB (mm/dd/yyyy)'].lstrip().rstrip()
	del field_mappings['DOB (m']
    
cases = ["DOB","Number","NPI","Date"]
for key in field_mappings.keys():
    for case in cases:
        if case in key:
            field_mappings[key] = char2num(field_mappings[key])
            break

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
