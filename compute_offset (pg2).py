import json
target_fields = ['Cologuard Order Number','Date Received by ES Labs',"Health Organization Name","Provider Name","Provider NPI", "Patient Name","Patient Date of Birth","Patient Sex","Patient Phone Number","Patient Shipping Address","Please Confirm Secure Fax #","Subscriber ID","Group Number","Policy Owner/Holder Name","Policy Owner/Holder Date of Birth"]
special_target_fields = ["Insurance Type:",'Insurance Carrier Name: (Example: Blue Cross, Aetna)',"ICD-10 Codes Z12.11 and Z12.12:"]
target_offsets = {}



# def get_offset(inputBox,outputBox):
# 	offset = [x2- x1 for (x1,x2) in zip(inputBox,outputBox)]
# 	return(offset)


def get_offset(inputBox,outputBox):
	bounding_box = []
	bounding_box.append(outputBox[0] - inputBox[0])
	bounding_box.append(outputBox[1] - inputBox[1])
	bounding_box.append(outputBox[2] + 1 - inputBox[0])
	bounding_box.append(outputBox[3] - inputBox[3])
	bounding_box.append(outputBox[4] + 1 - inputBox[0])
	bounding_box.append(outputBox[5] - inputBox[5])	
	bounding_box.append(outputBox[6] - inputBox[6])
	bounding_box.append(outputBox[7] - inputBox[7])
	return(bounding_box)




input_filename = 'Sample_2b'
input_filename_json = input_filename + '.json'
input_file_json = open(input_filename_json,'r')
analysis = input_file_json.read()
input_analysis = json.loads(analysis)

ref_filename = 'Reference_bb(pg2)'
ref_filename_json = ref_filename + '.json'
ref_file_json = open(ref_filename_json,'r')
analysis = ref_file_json.read()
ref_analysis = json.loads(analysis)


for index,line in enumerate(input_analysis["analyzeResult"]["readResults"][0]["lines"]):
	if line['text'] in special_target_fields:
		target_offsets[line['text']] = get_offset(line['boundingBox'],ref_analysis["analyzeResult"]["readResults"][0]["lines"][index]['boundingBox'])


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