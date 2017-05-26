import sys
from PIL import Image
import serial
import time


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
    print("width=%d,height=%d\n" % (width, height))
    for x in range(height):
        for y in range(width):
            r, g, b = pix[y, x]
            pix[y, x] = g,r,b
            im.putpixel((y,x),(r&0xc0,g&0xc0,b&0xc0))
            pix_arr.append(((r & 7) << 5) + ((g & 7) << 2) + (b & 3))
    im.show()
    return pix_arr


def get_desired_input(prompt, key):
    while True:
        print(prompt)
        str = sys.stdin.readline()
        if str == key:
            break
        else:
            print("input error, please input again\n")


# configure seril port
ser = serial.Serial()
try:
    ser.baudrate = 115200
    ser.port = "COM4"
    ser.open()
except serial.SerialException as err:
    sys.exit(err)

# stage 1: sending image pixels
# get_desired_input("sending image pixels, press [enter] to confirm", '\n')
pix_arr = read_image('../pic/monkey.jpg')
# ser.write(pix_arr)
start_time = time.time()

# stage 2: reading codes
codebook = []
codebook_mask = []
# read codebook
# for i in range(256):
#     codebook.append(ser.read())
#     codebook_mask.append(ser.read())

# read codes
# codes = ser.read(320*200)
end_time = time.time()
print("Huffman encode tiem = %fs" % (end_time - start_time))
# stage 3: sending codebook and codes




ser.close()
