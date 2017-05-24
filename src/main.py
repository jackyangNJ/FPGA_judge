from PIL import Image
import serial

def read_image(path):
    '''
    
    :param path: picture path
    :return: array of pix, scanned by line
    '''
    pix_arr = []
    im = Image.open(path)
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    print("width=%d,height=%d\n"%(width,height))
    for x in range(height):
        for y in range(width):
            r, g, b = pix[y, x]
            pix_arr.append(((r&7)<<5)+((g&7)<<2)+((b&3)))
    return pix_arr


ser = serial.Serial('/dev/ttyAMA0',115200)


pix_arr = read_image('../pic/black.jpg')

