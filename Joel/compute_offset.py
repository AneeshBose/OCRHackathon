import json
target_fields = ['Healthcare Organization Name:','Provider Name:','NPI #:','Other(s):','Location Address:','City, State, Zip1:','Phone Number:','Secure Fax Number:','Patient ID/MRN:','Phone Number (required):','First Name:','Last Name:','Language Preference (optional):','DOB (mm/dd/yyyy):','Shipping Address:','Billing Address:','City, State, Zip2:','City, State, Zip3:','Policyholder Name:','Policyholder DOB:','Primary Insurance Carrier:','Claims Submission Address:','Subscriber ID/Policy Number:','Group Number:','Plan:','Prior-Authorization Code (if available):','Date:']
target_offsets = {}



def get_offset(inputBox,outputBox):
	offset = [x2- x1 for (x1,x2) in zip(inputBox,outputBox)]
	return(offset)



input_filename = 'Sample_1b'
input_filename_json = input_filename + '.json'
input_file_json = open(input_filename_json,'r')
analysis = input_file_json.read()
input_analysis = json.loads(analysis)

ref_filename = 'Reference_bb'
ref_filename_json = ref_filename + '.json'
ref_file_json = open(ref_filename_json,'r')
analysis = ref_file_json.read()
ref_analysis = json.loads(analysis)

csz_counter = 0

for index,line in enumerate(input_analysis["analyzeResult"]["readResults"][0]["lines"]):
	if line['text'].startswith('City, State, Zip'):
		csz_counter += 1
		csz_key = 'City, State, Zip' + str(csz_counter) +':'
		target_offsets[csz_key] = get_offset(line['boundingBox'],ref_analysis["analyzeResult"]["readResults"][0]["lines"][index]['boundingBox'])

	elif line['text'] in target_fields:
		target_offsets[line['text']] = get_offset(line['boundingBox'],ref_analysis["analyzeResult"]["readResults"][0]["lines"][index]['boundingBox'])

	elif line['text'].startswith('DOB ('):
		target_offsets['DOB (mm/dd/yyyy):'] = get_offset(line['boundingBox'],ref_analysis["analyzeResult"]["readResults"][0]["lines"][index]['boundingBox'])

	elif line['text'].startswith('Shipping Add'):
		target_offsets['Shipping Address:'] = get_offset(line['boundingBox'],ref_analysis["analyzeResult"]["readResults"][0]["lines"][index]['boundingBox'])

	elif line['text'].startswith('Plan'):
		target_offsets['Plan:'] = get_offset(line['boundingBox'],ref_analysis["analyzeResult"]["readResults"][0]["lines"][index]['boundingBox'])
	
	elif line['text'].startswith('@'):
		target_offsets['Other(s):'] = get_offset(line['boundingBox'],ref_analysis["analyzeResult"]["readResults"][0]["lines"][index]['boundingBox'])

	elif line['text'].startswith('Language'):
		target_offsets['Language Preference (optional):'] = get_offset(line['boundingBox'],ref_analysis["analyzeResult"]["readResults"][0]["lines"][index]['boundingBox'])

	elif line['text'].startswith('Prior-Authorization '):
		target_offsets['Prior-Authorization Code (if available):'] = get_offset(line['boundingBox'],ref_analysis["analyzeResult"]["readResults"][0]["lines"][index]['boundingBox'])



print(target_offsets)
print(len(target_fields))
print(len(target_offsets))


newl = []
for i in target_fields:
	if i.endswith(':'):
		newl.append(i[0:-1])

newd = {}
for i in target_offsets:
	if i.endswith(':'):
		newd[i[0:-1]] = target_offsets[i]
	else:
		newd[i] = target_offsets[i]

print(newl)
print(newd)

print(len(newl))
print(len(newd))