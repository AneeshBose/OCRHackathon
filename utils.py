from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
import requests
import json
import time

req_target_fields = ['Healthcare Organization Name', 'Provider Name', 'NPI #', 'Other(s)', 'Location Address', 'City, State, Zip1', 'Phone Number', 'Secure Fax Number', 'Patient ID/MRN', 'Phone Number (required)', 'First Name', 'Language Preference (optional)', 'DOB (m', 'Shipping Address', 'Billing Address', 'City, State, Zip2', 'Policyholder Name', 'Primary Insurance Carrier', 'Claims Submission Address', 'Subscriber ID/Policy Number', 'Prior-Authorization Code (if available)', 'Patient Signature']
req_other_texts = ['EXACT', 'COLOGUARD\u00ae ORDER', 'EXACT SCIENCES LABORATORIES, LLC', 'SCIENCES', '145 E Badger Rd, Ste 100. Madison, WI 53713', 'REQUISITION FORM', 'LABORATORIES', 'p: 844-870-8870 | ExactLabs.com', 'Stool-based ONA test with hemoglobin Immunoassay component', 'NPI: 1629407069 TIN: 463095174', 'Provider & Order Information,', 'PROVIDER INFORMATION', 'ORDER INFORMATION', 'This section is not intended to influence the medical judgment of an ordering', 'provider In determining whether this test is right for any particular patient. The', 'following codes are listed as a convenience. Ordering practitioners should report', 'the diagnosis code(s) that best describes the reason for performing the test.', 'ICD-10 Code:', 'Z12.11 and Z12.12 (Encounter for screening for malignant', 'neoplasm of colon [Z12.11] and rectum [212.12])', 'Certification', 'I am a licensed healthcare provider authorized to order Cologuard. This', 'test is medically necessary and the patient is eligible to use Cologuard.', 'will maintain the privacy of test results and related information as', 'required by HIPAA. I authorize Exact Sciences Laboratories to obtain', 'reimbursement for Cologuard and to directly contact and collect', 'additional samples from the patient as appropriate.', "'To receive results for this order, please provide secure FAX number only", 'Patient Demographics, Attacholc', 'PATIENT ETHNICITY AND RACE The completion of this section is optional.', "Please mark one or more to indicate your patient's race:", 'Patient Insurance/Billing Information.','PATIENT AUTHORIZATIONS, ASSIGNMENT OF BENEFITS (AOB) & FINANCIAL RESPONSIBILITIES', 'i authorize Exact Sciences Laboratories (Exact) to bill my insurance/health pion and furnish them with my Cologuard order information, test results, or other information requested', 'for reimbursement. I assign all rights and benefits under my insurance plans to Exoct ond authorize Exact to appeal and contest any reimbursement denial, including in any', 'administrative or civil proceedings necessary to pursue reimbursement, I authorize all reimbursements to be poid directly to the laboratory in consideration for services performed', 'I understand that i am responsible for any amount not paid, including amounts for non-covered services or services determined by my plon to be provided by an out-of-network', 'provider. I further understand that if I am a Medicard enrollee in a state where Exact is enrolled as a Medicaid provider, Exact will accept as payment in full the amounts paid by the', 'Medicaid progrom, plus ony deductible, cainsurance or copayment which may be required by the Medicaid program to be paid by me.', 'For Lab Use Only', 'FRM-3004-05-c', 'Fax completed form to 844-870-8875', 'February 2019', 'Sample Collected: _/ /_', 'Sample Received _/ /']
req_target_offsets = {'Healthcare Organization Name': [-51, -41, 605, -39, 605, 19, -51, 18], 'Provider Name': [-52, -32, 604, -33, 604, 15, -52, 15], 'NPI #': [-51, -28, 605, -26, 605, 47, -51, 46], 'Other(s)': [-26, -14, 605, -15, 605, 21, -26, 23], 'Location Address': [-53, -37, 603, -37, 603, 22, -53, 22], 'City, State, Zip1': [-53, -27, 603, -28, 603, 22, -53, 23], 'Phone Number': [-52, -22, 604, -22, 604, 15, -52, 15], 'Secure Fax Number': [-53, -22, 603, -20, 603, 9, -53, 7], 'Patient ID/MRN': [-51, -19, 605, -19, 605, 16, -51, 16], 'Phone Number (required)': [-24, -21, 607, -22, 607, 0, -24, 1], 'First Name': [-55, -27, 601, -28, 601, 20, -55, 21], 'Language Preference (optional)': [-26, -22, 605, -21, 605, 17, -26, 16], 'DOB (m': [-56, -20, 600, -21, 600, 3, -56, 3], 'Shipping Address': [-54, -27, 602, -27, 602, 54, -54, 54], 'Billing Address': [-28, -22, 603, -23, 603, 58, -28, 59], 'City, State, Zip2': [-54, -23, 1187, -24, 1187, 11, -54, 11], 'Policyholder Name': [-55, -23, 1186, -23, 1186, 19, -55, 20], 'Primary Insurance Carrier': [-54, -22, 1187, -22, 1187, 20, -54, 19], 'Claims Submission Address': [-56, -20, 1185, -20, 1185, 18, -56, 17], 'Subscriber ID/Policy Number': [-55, -20, 1186, -20, 1186, 18, -55, 17], 'Prior-Authorization Code (if available)': [-57, -18, 1184, -18, 1184, 9, -57, 9], 'Patient Signature': [-60, -33, 1181, -33, 1181, 20, -60, 20]}
req_firebase_keys = {"Healthcare Organization Name": "hon","Provider Name": "pn", "NPI #": "npi", "Other(s)": "oth", "Location Address": "la", "City, State, Zip1": "csz1", "Phone Number": "ph", "Secure Fax Number": "sfn", "Patient ID/MRN": "mrn", "First Name": "fn", "Language Preference (optional)": "lp", "City, State, Zip2": "csz2", "Policyholder Name": "phn", "Primary Insurance Carrier": "pic", "Claims Submission Address": "csa", "Subscriber ID/Policy Number": "sid", "Prior-Authorization Code (if available)": "pac", "Shipping Address": "sa", 'Phone Number (required)':'phr','Date of Order':'doo','ICD-10 Code':'icd','Relationship to patient':'rel','Origin':'descent','Race':'race','Pay Insurance':'billpay','Type':'type','Sex':'sex',"Billing Address": "ba", "Policyholder DOB": "policydob", "Last Name": "ln", "City, State, Zip3": "csz3", "Group Number": "gpn", "Plan": "plan", "Date": "dat", "DOB (mm/dd/yyyy)": "dob",'Contact type':'phrr'}





info_target_fields = ['Cologuard Order Number','Date Received by ES Labs',"Health Organization Name","Provider Name","Provider NPI", "Patient Name","Patient Date of Birth","Patient Sex","Patient Phone Number","Subscriber ID","Group Number","Policy Owner/Holder Name","Policy Owner/Holder Date of Birth"]
info_special_target_fields = ["Please Confirm Secure Fax #","Patient Shipping Address",'Healthcare Provider Signature',"Insurance Type",'Insurance Carrier Name',"ICD-10 Codes"]
info_other_texts = []
info_target_offsets = {'Healthcare Provider Signature': [0, -16, 511, -17, 511, 31, 0, 32],'Patient Shipping Address': [0, -15, 256, -16, 256, 13, 0, 13],'Please Confirm Secure Fax #': [0, -16, 278, -16, 278, 34, 0, 34],'ICD-10 Codes': [0, -18, 286, -18, 286, 118, 0, 118], 'Insurance Type': [0, -15, 160, -16, 160, 25, 0, 26], 'Insurance Carrier Name': [0, -13, 452, -14, 452, 26, 0, 27]}
info_firebase_keys = {'Insurance Carrier Name':'icn',"Insurance Type":'it',"ICD-10 Codes":'icd','Healthcare Provider Signature':'hps','Cologuard Order Number':'con','Date Received by ES Labs':'drbel',"Health Organization Name":'hon',"Provider Name":'pn',"Provider NPI":'pnpi', "Patient Name":'ppn',"Patient Date of Birth":'ppdob',"Patient Sex":'pps',"Patient Phone Number":'pppn',"Patient Shipping Address":'ppsa',"Please Confirm Secure Fax #":'pcsf',"Subscriber ID":'sid',"Group Number":'gpn',"Policy Owner/Holder Name":'hn',"Policy Owner/Holder Date of Birth":'hndob'}



def get_offset(inputBox, outputBox):
    offset = [x1 - x2 for (x1, x2) in zip(outputBox, inputBox)]
    return offset

def get_out_bounding(inputBox, offset):
    outputBox = [x1 + x2 for (x1, x2) in zip(inputBox, offset)]
    return outputBox

def calculate_req_bounding_box(inputBox,offset):
    bounding_box = []
    bounding_box.append(inputBox[0] + offset[0])
    bounding_box.append(inputBox[1] + offset[1])
    bounding_box.append(inputBox[0] + 1 + offset[2])
    bounding_box.append(inputBox[3] + offset[3])
    bounding_box.append(inputBox[0] + 1 + offset[4])
    bounding_box.append(inputBox[5] + offset[5])
    bounding_box.append(inputBox[6] + offset[6])
    bounding_box.append(inputBox[7] + offset[7])
    return bounding_box


def calculate_info_bounding_box(inputBox,offset):
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

def char2num(raw_str,key_value):
    processed_str = ''
    char_num_dict = {'O':0 ,' ':'','D':0 , 'Q':0, 'I':1, 'J':1, 'L':1, 'Z':2, 'H':4, 'U':4, 'S':5, 'G':5, 'C':6, 'T':7, 'B':8, 'o':0, 'a':0, 'd':0, 'p':0, 'q':0, 'i':1, 'l':1, 'f':1, 'z':2, 'h':4, 'u':4, 'v':4, 's':5, 'c':6, 'b':6, 'g':9, 'j':9}
    for char in raw_str:
        if ((key_value == 'NPI #') or (key_value == 'Group Number') or (key_value == 'Patient ID/MRN')) and (char.isalnum() == False):
            pass
        else:
            if char in char_num_dict:
                processed_str += str(char_num_dict[char])
            else:
                processed_str += char
    return processed_str

def resize_image(image_paths):
    for image_path in image_paths:
        img = Image.open(image_path)
        img = img.resize((1240, 1754), Image.ANTIALIAS)
        img.save(image_path)


def convert_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=150)
    image_path = pdf_path.split('.pdf')[0]
    image_paths = []
    for index,page in enumerate(pages):
        page.save(image_path+str(index)+'.PNG', 'PNG')
        image_paths.append(image_path+str(index)+'.PNG')
    return(image_paths)

def execute_api(byte_img):
    endpoint = 'https://computervisionmedicalsciences.cognitiveservices.azure.com'
    subscription_key = 'd0e3653430044e4c88cb7806a08041ce'

    text_recognition_url = endpoint + "/vision/v3.0/read/analyze"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    data = byte_img
    response = requests.post(
        text_recognition_url, headers=headers, json=None, data=data)
    response.raise_for_status()
    poll = True
    resp_data = None
    while poll:
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()

        #print(json.dumps(analysis, indent=4))

        resp_data = json.dumps(analysis, indent=4)

        time.sleep(1)
        if "analyzeResult" in analysis:
            poll = False
        if "status" in analysis and analysis['status'] == 'failed':
            poll = False
    return analysis


def validate_checkbox(line, value):
    possible_chars = ['O', 'o', '0']
    pos = line.lower().find(value)
    #if value in line.lower():
    #    print(line.lower())
    if pos == -1:
        return False
    elif pos == 0:
        return True
    elif pos == 1:
        if line[0] in possible_chars:
            return False
        else:
            return True
    else:
        if line[pos - 1] in possible_chars or line[pos - 2] in possible_chars:
            return False
        else:
            return True
