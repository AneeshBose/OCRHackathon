# PixelWaveOCR - Creating Digital Revolution

This codebase contains submission of Exact Sciences OCR Hackathon

### Objective: 
To build a highly accurate OCR solution that takes a manually filled form as input through any electronic device and converts it to a digital form with minimal human dependency.

### Build Target: 
The tool should be able to automate the labor of manual data entry process and make it more inclusive by handling multiple languages and forms, even for the differently abled, so that everyone is able to get access to world-class healthcare facilities.

### HomePage: [PixelWave OCR](https://ocr-hack-v0.web.app)
Visit: https://ocr-hack-v0.web.app

To login, use the below default credentials:  
Username: admin  
Password: admin

### Processing: Requisition Form: 
  -  To upload and run OCR on a patient’s requisition form, choose the **Form 1** option after logging in. 
  -  In order to process a file, upload the file using **Choose files** option and then hit **Upload file** (Supported file formats are **.pdf, .jpg, .jpeg, .png, .tiff**). 
  -  Once the upload is successful, you’ll be automatically redirected to the processed form’s page (please wait about 5 seconds for this to happen). 
  -  If there are any corrections to be made, one can edit during this phase. After successfully making the required changes (incase of any discrepancy) hit on the **Submit** button and then confirm the same. 
  -  If you wish to export the response from our custom OCR API as a JSON, hit on **Export JSON** button. After successfully submitting the form, you will be redirected to the requisition form’s upload / search page.
  -  To search for a patient, use the **Patient ID or MRN** as the search value. While you are on the preview page, one can retrieve all the data on the form from the database.

### Processing: Information Needed Form: 
  -  The **Form 2** button has the provision to process and preview the 'Information Needed' page. The supported file formats remain the same. 
  -  On choosing the file and uploading it, you’ll be redirected to the page where you can make changes and then submit. 
  -  One can preview the submitted form using the 'Order number'. If no order number is mentioned then the default value will be randomly generated and stored. 

### Technology Stack:
 - **Backend** - Python
 - **Frontend** - HTML, CSS, Bootstrap, Javascript, JQuery
 - **Framework** - Flask
 - **Database** - Firebase
 - **OCR** - PixelWave Custom Model + Microsoft Computer Vision Read API
 - **API Hosting** - Heroku

### Executing it locally:
#### Pre-requisite:
1. Python 3.x and pip needs to be installed.  
2. Install Poppler (Ref: https://pypi.org/project/pdf2image/) 

#### Setup:
```sh
$ pip install -r requirement.txt
```
#### Data:
Maintain all the files to be tested in the same directory as app.py

#### Execution:
```sh
$ python app.py
```
#### To get json output use the following API endpoints:
Open the below links in a browser after replacing <file_name> with the filename of the file to be tested.
  - **Requisition form** - localhost:8000/reqtform/<file_name>/0
  - **Information Needed Form** - localhost:8000/reqtform/<file_name>/1  
Eg: To run OCR recognition in Information Needed form for filename as Sample.pdf, open browser with localhost:8000/reqtform/Sample.pdf/1

### Future Scope: 
- Using AI to map addresses. Although we expect a higher accuracy, to improve the same, we also plan to use AI to make sure that incase of any mismatch/ wrongly recognized city name, state name etc. our application will auto correct the names and fasten the processing minimizing the human dependency to a much greater extent. 
- Braille OCR and multi-lingual: OBR (Optical Braille Recognition) will be an added advantage to our platform that will recognizes Braille characters and converts to English language to accommodate a wider range of patients. Although we support only English, we will be able to support other international languages, as our API can be configured by simply accepting an additional parameter as the language. 
- Ability to process multiple files parallelly [batch processing]. Currently our application takes approximately 8-10 seconds to process each file, with more computational power, we will be able to process multiple files at the same time. 
- Support Multiple Formats: Currently our application supports 5 formats [PDF, JPEG, JPG, PNG, TIFF] and we look forward to scale up the supported formats. 5. Support Offline Processing: Currently the application depends on internet for analyzing and processing the form. We plan to make the processing offline so that the application can also work with minimum internet dependency.
