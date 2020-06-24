from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image

req_target_fields = ['Healthcare Organization Name', 'Provider Name', 'NPI #', 'Other(s)', 'Location Address', 'City, State, Zip1', 'Phone Number', 'Secure Fax Number', 'Patient ID/MRN', 'Phone Number (required)', 'First Name', 'Language Preference (optional)', 'DOB (m', 'Shipping Address', 'Billing Address', 'City, State, Zip2', 'Policyholder Name', 'Primary Insurance Carrier', 'Claims Submission Address', 'Subscriber ID/Policy Number', 'Prior-Authorization Code (if available)', 'Patient Signature']
req_other_texts = ['EXACT', 'COLOGUARD\u00ae ORDER', 'EXACT SCIENCES LABORATORIES, LLC', 'SCIENCES', '145 E Badger Rd, Ste 100. Madison, WI 53713', 'REQUISITION FORM', 'LABORATORIES', 'p: 844-870-8870 | ExactLabs.com', 'Stool-based ONA test with hemoglobin Immunoassay component', 'NPI: 1629407069 TIN: 463095174', 'Provider & Order Information,', 'PROVIDER INFORMATION', 'ORDER INFORMATION', 'This section is not intended to influence the medical judgment of an ordering', 'provider In determining whether this test is right for any particular patient. The', 'following codes are listed as a convenience. Ordering practitioners should report', 'the diagnosis code(s) that best describes the reason for performing the test.', 'ICD-10 Code:', 'Z12.11 and Z12.12 (Encounter for screening for malignant', 'neoplasm of colon [Z12.11] and rectum [212.12])', 'Certification', 'I am a licensed healthcare provider authorized to order Cologuard. This', 'test is medically necessary and the patient is eligible to use Cologuard.', 'will maintain the privacy of test results and related information as', 'required by HIPAA. I authorize Exact Sciences Laboratories to obtain', 'reimbursement for Cologuard and to directly contact and collect', 'additional samples from the patient as appropriate.', "'To receive results for this order, please provide secure FAX number only", 'Patient Demographics, Attacholc', 'PATIENT ETHNICITY AND RACE The completion of this section is optional.', "Please mark one or more to indicate your patient's race:", 'Patient Insurance/Billing Information.','PATIENT AUTHORIZATIONS, ASSIGNMENT OF BENEFITS (AOB) & FINANCIAL RESPONSIBILITIES', 'i authorize Exact Sciences Laboratories (Exact) to bill my insurance/health pion and furnish them with my Cologuard order information, test results, or other information requested', 'for reimbursement. I assign all rights and benefits under my insurance plans to Exoct ond authorize Exact to appeal and contest any reimbursement denial, including in any', 'administrative or civil proceedings necessary to pursue reimbursement, I authorize all reimbursements to be poid directly to the laboratory in consideration for services performed', 'I understand that i am responsible for any amount not paid, including amounts for non-covered services or services determined by my plon to be provided by an out-of-network', 'provider. I further understand that if I am a Medicard enrollee in a state where Exact is enrolled as a Medicaid provider, Exact will accept as payment in full the amounts paid by the', 'Medicaid progrom, plus ony deductible, cainsurance or copayment which may be required by the Medicaid program to be paid by me.', 'For Lab Use Only', 'FRM-3004-05-c', 'Fax completed form to 844-870-8875', 'February 2019', 'Sample Collected: _/ /_', 'Sample Received _/ /']
req_target_offsets = {'Healthcare Organization Name': [-51, -38, 605, -36, 605, 16, -51, 15], 'Provider Name': [-52, -29, 604, -30, 604, 12, -52, 12], 'NPI #': [-51, -25, 605, -23, 605, 44, -51, 43], 'Other(s)': [-26, -11, 605, -12, 605, 18, -26, 20], 'Location Address': [-53, -34, 603, -34, 603, 19, -53, 19], 'City, State, Zip1': [-53, -24, 603, -25, 603, 19, -53, 20], 'Phone Number': [-52, -19, 604, -19, 604, 12, -52, 12], 'Secure Fax Number': [-53, -19, 603, -17, 603, 6, -53, 4], 'Patient ID/MRN': [-51, -16, 605, -16, 605, 13, -51, 13], 'Phone Number (required)': [-24, -18, 607, -19, 607, -3, -24, -2], 'First Name': [-55, -24, 601, -25, 601, 17, -55, 18], 'Language Preference (optional)': [-26, -19, 605, -18, 605, 14, -26, 13], 'DOB (m': [-56, -17, 600, -18, 600, 0, -56, 0], 'Shipping Address': [-54, -24, 602, -24, 602, 51, -54, 51], 'Billing Address': [-28, -19, 603, -20, 603, 55, -28, 56], 'City, State, Zip2': [-54, -20, 1187, -21, 1187, 8, -54, 8], 'Policyholder Name': [-55, -20, 1186, -20, 1186, 16, -55, 17], 'Primary Insurance Carrier': [-54, -19, 1187, -19, 1187, 17, -54, 16], 'Claims Submission Address': [-56, -17, 1185, -17, 1185, 15, -56, 14], 'Subscriber ID/Policy Number': [-55, -17, 1186, -17, 1186, 15, -55, 14], 'Prior-Authorization Code (if available)': [-57, -15, 1184, -15, 1184, 6, -57, 6], 'Patient Signature': [-60, -30, 1181, -30, 1181, 17, -60, 17]}


def save_pdf_to_image(pdf_path):
    images = convert_from_path(pdf_path, dpi=120)
    for i in range(len(images)):
        img = images[i].resize((1240,1754), Image.ANTIALIAS)
        img.save(pdf_path[:-2]+str(i)+'.jpg')

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

def char2num(raw_str):
    processed_str = ''
    char_num_dict = {'O':0 , 'D':0 , 'Q':0, 'I':1, 'J':1, 'L':1, 'Z':2, 'H':4, 'U':4, 'S':5, 'G':5, 'C':6, 'T':7, 'B':8, 'o':0, 'a':0, 'd':0, 'p':0, 'q':0, 'i':1, 'l':1, 'f':1, 'z':2, 'h':4, 'u':4, 'v':4, 's':5, 'c':6, 'b':6, 'g':9, 'j':9}
    for char in raw_str:
        if char in char_num_dict:
            processed_str += str(char_num_dict[char])
        else:
            processed_str += char
    return processed_str
