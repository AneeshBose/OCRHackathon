from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image

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
