from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
import time
from shapely.geometry import Polygon
from utils import req_target_fields, req_other_texts, req_target_offsets, calculate_req_bounding_box
from utils import info_target_fields, info_special_target_fields, info_other_texts, info_target_offsets, calculate_info_bounding_box
from utils import execute_api, char2num, req_firebase_keys, validate_checkbox, info_firebase_keys
from utils import resize_image


def requisiton_page(images):
	for index,img in enumerate(images):
		req_flag = 0
		byte_img = open(img, "rb").read()
		# byte_img = convert_pil_to_bytes(img)
		resp = execute_api(byte_img)
		target_bounding_boxes = {}
		# Count each occurence of 'City, State, Zip'
		csz_counter = 0
		# Initialize target boxes
		for index, line in enumerate(resp["analyzeResult"]["readResults"][0]["lines"]):
			if ('requisition' in line['text'].lower()) or ('demographic' in line['text'].lower()):
				req_flag = 1
			if 'City, State, Zip'.lower() in line['text'].lower() and line['boundingBox'][0] < 120:
				csz_counter += 1
				csz_key = 'City, State, Zip' + str(csz_counter)

				bounding_box_points = calculate_req_bounding_box(line['boundingBox'], req_target_offsets[csz_key])
				target_bounding_boxes[csz_key] = [(bounding_box_points[i], bounding_box_points[i + 1]) for i in
												  range(0, len(bounding_box_points), 2)]
			elif line['text'] in req_other_texts:
				pass

			else:
				for field in req_target_fields:
					if 'Policyholder' not in field:
						if field.lower() in line['text'].lower() and field not in target_bounding_boxes:
							bounding_box_points = calculate_req_bounding_box(line['boundingBox'], req_target_offsets[field])
							target_bounding_boxes[field] = [(bounding_box_points[i], bounding_box_points[i + 1]) for i in
															range(0, len(bounding_box_points), 2)]
							break
					else:
						if (line['text'].lower()).startswith(field.lower()):
							# print(field)
							bounding_box_points = calculate_req_bounding_box(line['boundingBox'], req_target_offsets[field])
							target_bounding_boxes[field] = [(bounding_box_points[i], bounding_box_points[i + 1]) for i in
															range(0, len(bounding_box_points), 2)]
							break

		if req_flag == 0:
			continue
		field_mappings = {}
		shipping_add = []
		billing_add = []
		ship_line_1 = []
		ship_line_2 = []
		bill_line_1 = []
		bill_line_2 = []

		for index, line in enumerate(resp["analyzeResult"]["readResults"][0]["lines"]):
			bounding_coord = [(line['boundingBox'][i], line['boundingBox'][i + 1]) for i in
							  range(0, len(line['boundingBox']), 2)]
			# polygon_htext is response for each line in response
			polygon_htext = Polygon(bounding_coord)
			x1_coord = bounding_coord[0][0]
			for target_field in target_bounding_boxes:
				polygon_ptext = Polygon(target_bounding_boxes[target_field])

				if polygon_ptext.contains(polygon_htext) == True:

					if 'Shipping Address' in target_field:
						shipping_add.append((line['text'], [(line['boundingBox'][i], line['boundingBox'][i + 1]) for i in
															range(0, len(line['boundingBox']), 2)]))
					elif 'Billing Address' in target_field:
						billing_add.append((line['text'], [(line['boundingBox'][i], line['boundingBox'][i + 1]) for i in
														   range(0, len(line['boundingBox']), 2)]))
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
				baseline = max(pair[1][2][1], pair[1][3][1])
		for pair in shipping_add:
			if int((min(pair[1][0][1], pair[1][1][1]) + max(pair[1][2][1], pair[1][3][1])) / 2) <= baseline:
				ship_line_1.append(pair)
			else:
				ship_line_2.append(pair)

		ship_add = ''
		ship_line_1.sort(key=lambda x: x[1][0][0])
		for pair in ship_line_1:
			ship_add += pair[0] + ' '
		ship_line_2.sort(key=lambda x: x[1][0][0])
		for pair in ship_line_2:
			ship_add += pair[0] + ' '
		field_mappings['Shipping Address'] = [[ship_add, 0]]

		for pair in billing_add:
			if 'Billing Address' in pair[0]:
				baseline = max(pair[1][2][1], pair[1][3][1])
		for pair in billing_add:
			if int((min(pair[1][0][1], pair[1][1][1]) + max(pair[1][2][1], pair[1][3][1])) / 2) <= baseline:
				bill_line_1.append(pair)
			else:
				bill_line_2.append(pair)
		bill_add = ''
		bill_line_1.sort(key=lambda x: x[1][0][0])
		for pair in bill_line_1:
			bill_add += pair[0] + ' '
		bill_line_2.sort(key=lambda x: x[1][0][0])
		for pair in bill_line_2:
			bill_add += pair[0] + ' '
		bill_add = bill_add.replace('Same as Shipping ', '')
		bill_add = bill_add.replace(']','').replace('[','')


		field_mappings['Billing Address'] = [[bill_add, 0]]


		# 2 cases to handle for same as shipping case when Billing Address is empty!!!!
		# print(field_mappings['Shipping Address'],field_mappings['Billing Address'])

		for key_field in field_mappings:
			row = ''
			for vals in field_mappings[key_field]:
				row += vals[0] + ' '
			if 'City, State, Zip' in key_field:
				key_field_index = row.lower().find('City, State, Zip'.lower())
				key_field_len = len(key_field)
				str_key_field = row[key_field_index:key_field_index + key_field_len]
				key_field_prep = row.replace(str_key_field, '',1)
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
			second_field = left_text[key_field_index1 + len('Group Number'):key_field_index2]
			third_field = left_text[key_field_index2 + len('Plan'):]
			field_mappings['Subscriber ID/Policy Number'], field_mappings['Group Number'], field_mappings[
				'Plan'] = first_field, second_field, third_field
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
			close_bracket_split = field_mappings['DOB (m'].split(')')[1]
			key_field_index = close_bracket_split.lower().find('Sex'.lower())
			first_field = close_bracket_split[:key_field_index]
			second_field = close_bracket_split[key_field_index+len('Sex'):].lstrip()
			is_male = validate_checkbox(second_field, 'male')
			is_female = validate_checkbox(second_field, 'female')
			if is_male:
				field_mappings['Sex'] = "male"
			elif is_female:
				field_mappings['Sex'] = "female"
			else:
				field_mappings['Sex'] = "male"

			field_mappings['DOB (mm/dd/yyyy)'] = first_field
			field_mappings['DOB (mm/dd/yyyy)'] = field_mappings['DOB (mm/dd/yyyy)'].lstrip().rstrip()
			del field_mappings['DOB (m']

		cases = ["DOB", "Number", "NPI", "Date","MRN"]
		for key in field_mappings.keys():
			for case in cases:
				if case in key:
					field_mappings[key] = char2num(field_mappings[key],key)
					break

		is_home = False
		is_mob = False
		is_work = False

		is_male = False
		is_female = False

		is_descent_yes = False
		is_descent_no = False

		is_white = False
		is_black = False
		is_asian = False
		is_haw = False
		is_ind = False

		is_billpay_yes = False
		is_billpay_no = False

		is_rel_self = False
		is_rel_spouse = False
		is_rel_other = False

		is_type_private = False
		is_type_medicare = False
		is_type_medicareadvt = False
		is_type_medicaid = False
		is_type_tricare = False

		for index, line in enumerate(resp["analyzeResult"]["readResults"][0]["lines"]):
			if not is_home:
				is_home = validate_checkbox(line['text'], 'home')
			if not is_mob:
				is_mob = validate_checkbox(line['text'], 'mobile')
			if not is_work:
				is_work = validate_checkbox(line['text'], 'work')

			'''
			#sex male female
			if not is_male:
				is_male = validate_checkbox(line['text'], 'male')
			if not is_female:
				is_female = validate_checkbox(line['text'], 'female')
			'''
			#descent yes no
			if not is_descent_yes:
				is_descent_yes = validate_checkbox(line['text'], 'Yes')
			if not is_descent_no:
				is_descent_no = validate_checkbox(line['text'], 'No')

			#race white black asian hawaiian indian
			if not is_white:
				is_white = validate_checkbox(line['text'], 'White')
			if not is_black:
				is_black = validate_checkbox(line['text'], 'Black or African-American')
			if not is_asian:
				is_asian = validate_checkbox(line['text'], 'Asian')
			if not is_haw:
				is_haw = validate_checkbox(line['text'], 'Native Hawaiian or other Pacific Islander')
			if not is_ind:
				is_ind = validate_checkbox(line['text'], 'American Indian or Alaska Native')

			#billpay yes no
			if not is_billpay_yes:
				is_billpay_yes = validate_checkbox(line['text'], 'Yes (complete below)')
			if not is_billpay_no:
				is_billpay_no = validate_checkbox(line['text'], 'No (patient will self-pay)')

			#rel self spouse other
			if not is_rel_self:
				is_rel_self = validate_checkbox(line['text'], 'Self')
			if not is_rel_spouse:
				is_rel_spouse = validate_checkbox(line['text'], 'Spouse')
			if not is_rel_other:
				is_rel_other = validate_checkbox(line['text'], 'Other')

			#type private medicare medicareadvt medicaid tricare
			if not is_type_private:
				is_type_private = validate_checkbox(line['text'], 'Private')
			if not is_type_medicare:
				is_type_medicare = validate_checkbox(line['text'], 'Medicare')
			if not is_type_medicareadvt:
				is_type_medicareadvt = validate_checkbox(line['text'], 'Medicare Advantage')
			if not is_type_medicaid:
				is_type_medicaid = validate_checkbox(line['text'], 'Medicaid')
			if not is_type_tricare:
				is_type_tricare = validate_checkbox(line['text'], 'Tricare')

		if is_home:
			field_mappings['Contact type'] = 'home'
		elif is_mob:
			field_mappings['Contact type'] = 'mobile'
		elif is_work:
			field_mappings['Contact type'] = 'work'
		else:
			field_mappings['Contact type'] = 'home'

		'''
		if is_male:
			field_mappings['Sex'] = "male"
		elif is_female:
			field_mappings['Sex'] = 'female'
		else:
			field_mappings['Sex'] = "male"
		'''

		if is_descent_yes:
			field_mappings['Origin'] = "yes"
		elif is_descent_no:
			field_mappings['Origin'] = "no"
		else:
			field_mappings['Origin'] = "yes"

		if is_white:
			field_mappings['Race'] = 'white'
		elif is_black:
			field_mappings['Race'] = 'black'
		elif is_asian:
			field_mappings['Race'] = 'asian'
		elif is_haw:
			field_mappings['Race'] = 'hawaiian'
		elif is_ind:
			field_mappings['Race'] = 'indian'
		else:
			field_mappings['Race'] = 'white'

		if is_billpay_yes:
			field_mappings['Pay Insurance'] = 'yes'
		elif is_billpay_no:
			field_mappings['Pay Insurance'] = 'no'
		else:
			field_mappings['Pay Insurance'] = 'yes'

		if is_rel_self:
			field_mappings['Relationship to patient'] = 'self'
		elif is_rel_spouse:
			field_mappings['Relationship to patient'] = 'spouse'
		elif is_rel_other:
			field_mappings['Relationship to patient'] = 'other'
		else:
			field_mappings['Relationship to patient'] = 'self'

		if is_type_private:
			field_mappings['Type'] = 'private'
		elif is_type_medicare:
			field_mappings['Type'] = 'medicare'
		elif is_type_medicareadvt:
			field_mappings['Type'] = 'medicareadvt'
		elif is_type_medicaid:
			field_mappings['Type'] = 'medicaid'
		elif is_type_tricare:
			field_mappings['Type'] = 'tricare'
		else:
			field_mappings['Type'] = 'private'

		for key in req_firebase_keys:
			if key not in field_mappings:
				field_mappings[req_firebase_keys[key]] = ''
			else:
				field_mappings[req_firebase_keys[key]] = field_mappings[key]
				del field_mappings[key]



			
		ba_remove_spaces = field_mappings['ba'].replace(' ','')
		if ba_remove_spaces == '':
			field_mappings['ba'] = field_mappings['sa']

		field_mappings['sfn'] = field_mappings['sfn'].replace('*','')

		if field_mappings['oth'] == '':
			field_mappings['icd'] = 'z12'

		else:
			field_mappings['icd'] = 'other'

		return field_mappings


def info_page(images):
	for index,img in enumerate(images):
		info_flag = 0
		byte_img = open(img, "rb").read()
		# byte_img = convert_pil_to_bytes(img)
		resp = execute_api(byte_img)
		target_bounding_boxes = {}

		for index, line in enumerate(resp["analyzeResult"]["readResults"][0]["lines"]):
			flag = 0
			if 'thank' in line['text'].lower():
				info_flag = 1
			for field in info_target_fields:
				if field.lower() in line['text'].lower() and field not in target_bounding_boxes:
					bounding_box_points = calculate_info_bounding_box(line['boundingBox'], [0, -5, 0, -5, 0, 5, 0, 5])
					target_bounding_boxes[field] = [(bounding_box_points[i], bounding_box_points[i + 1]) for i in
													range(0, len(bounding_box_points), 2)]
					flag = 1
					break
			if flag == 0:
				for field in info_special_target_fields:
					if field.lower() in line['text'].lower() and field not in target_bounding_boxes:
						info_target_offsets[field][0] = 450
						info_target_offsets[field][6] = 450
						bounding_box_points = calculate_info_bounding_box(line['boundingBox'], info_target_offsets[field])
						target_bounding_boxes[field] = [(bounding_box_points[i], bounding_box_points[i + 1]) for i in
														range(0, len(bounding_box_points), 2)]

		if info_flag == 0:
			continue

		#print(target_bounding_boxes)
		field_mappings = {}

		for index, line in enumerate(resp["analyzeResult"]["readResults"][0]["lines"]):
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

		cases = ["DOB", "Number", "NPI", "Date", "#"]
		for key in field_mappings.keys():
			for case in cases:
				if case in key:
					field_mappings[key] = char2num(field_mappings[key],key)
					break

		for key in info_firebase_keys:
			if key not in field_mappings:
				field_mappings[info_firebase_keys[key]] = ''
			else:
				field_mappings[info_firebase_keys[key]] = field_mappings[key]
				del field_mappings[key]

		if field_mappings['con'] == '':
			field_mappings['con'] = '0000'

		return field_mappings
