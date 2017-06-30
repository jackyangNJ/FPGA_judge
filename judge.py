import sys
from PIL import Image
import serial
import time
import getopt

# global parameters
baud = 115200
port_name = "COM4"
picture = "colors.bmp"

def read_image(path):
    '''
    parse a image to get the highest 2 bits of r,g,b
    :param path: picture path
    :return: array of pix, scanned by line
    '''
    pix_arr = []
    im = Image.open(path)
    pix = im.load()

    width = im.size[0]
    height = im.size[1]
    print("image width=%d,height=%d\n" % (width, height))
    for x in range(height):
        for y in range(width):
            r, g, b = pix[y, x]
            im.putpixel((y, x), (r & 0xc0, g & 0xc0, b & 0xc0))
            pix_arr.append(((r & 0xc0) >> 2) + ((g & 0xc0) >> 4) + ((b & 0xc0) >> 6))
    im.show()
    return pix_arr


def get_desired_input(prompt, key):
    '''
    pause program until get specified key
    '''
    while True:
        print(prompt)
        str = sys.stdin.readline()
        if str == key:
            break
        else:
            print("input error, please input again\n")


def judge(port_name, baud, picture):
    # configure seril port
    ser = serial.Serial()
    try:
        ser.baudrate = baud
        ser.port = port_name
        ser.open()
    except serial.SerialException as err:
        sys.exit(err)

    # stage 1: sending image pixels
    get_desired_input("sending image pixels, press [enter] to confirm", '\n')
    pix_arr = read_image('pic/' + picture)
    print("sending image")
    ser.write(pix_arr)
    print("sending image over!")

    # record starting time
    start_time = time.time()

    # stage 2: reading codes
    codes = []
    code = ""
    # read codebook
    while True:
        code_old = code
        code = ser.read()
        if code_old == b'#' and code == b'$':
            break
        codes.append(int(code[0]))

    # print encoding time
    end_time = time.time()
    print("Huffman encoding time = %fs" % (end_time - start_time))

    # stage 3: sending codebook and codes
    get_desired_input("sending codebook and codes, press [enter] to confirm", '\n')
    print("sending codebook and codes")
    ser.write(codes)
    ser.write(b"#!")
    print("sending codebook and codes over!")

    # finish tasks
    ser.close()


def usage():
    print(' -h help \n' \
          ' -n serial port name'
          ' -b serial baud rate\n' \
          ' -p picture name, ex xx.jpg\n' \
          '')


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:b:p:")
    except getopt.GetoptError as err:
        usage()
        sys.exit(err)

    global baud,port_name,picture
    for o, a in opts:
        if o in ("-h", "--help"):
            sys.exit(usage())
        elif o in "-b":
            baud = 115200
        elif o in "-p":
            picture = a
        elif o in "-n":
            port_name = a
    # running judge system
    judge(port_name, baud, picture)


if __name__ == "__main__":
    main()
