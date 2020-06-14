def get_offset(inputBox, outputBox):
    offset = [x1 - x2 for (x1, x2) in zip(outputBox, inputBox)]
    return offset
    
def get_out_bounding(inputBox, offset):
    outputBox = [x1 + x2 for (x1, x2) in zip(inputBox, offset)]
    return outputBox
