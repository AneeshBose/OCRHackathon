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

def char2num(raw_str):
    processed_str = ''
    char_num_dict = {'O':0 , 'D':0 , 'Q':0, 'I':1, 'J':1, 'L':1, 'Z':2, 'H':4, 'U':4, 'S':5, 'G':5, 'C':6, 'T':7, 'B':8, 'o':0, 'a':0, 'd':0, 'p':0, 'q':0, 'i':1, 'l':1, 'f':1, 'z':2, 'h':4, 'u':4, 'v':4, 's':5, 'c':6, 'b':6, 'g':9, 'j':9}
    for char in raw_str:
        if char in char_num_dict:
            processed_str += str(char_num_dict[char])
        else:
            processed_str += char
    return processed_str
        
            