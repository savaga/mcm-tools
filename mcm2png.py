from pprint import pprint, pformat
import pdb
import sys, getopt
import contextlib
import png

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'wb')
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

def print_help(name):
    print '%s -i <inputfile> -o <outputfile>' % name

def read_font(filename):
    data = []
    with open(filename, "r") as ih:
        lines = [line.rstrip('\n') for line in ih]
        if lines[0] == "MAX7456":
            char_array = []
            char_lines = 0
            for line in lines[1:]:
                if line == "":
                    break
                char_array.append(line)
                char_lines += 1
                if (char_lines == 64):
                    data.append(list(char_array))
                    char_array = []
                    char_lines = 0
    print "Read %s chars from %s" % (len(data), filename)
    return list(data)

def parse_font(data, ofile, draw_net = False):
    img_x = 192
    img_y = 288
    if draw_net:
        img_x += 15
        img_y += 15
    img = png.Writer(img_x, img_y)#, greyscale=True)
    img_list = []
    i = 0
    for char_row in xrange(0, 256, 16):
        for ch_row in xrange(0, 54, 3):
            img_line = []
            for char_col in xrange(16):
                char_line = []
                for pix in xrange(2,-1,-1):
                    byte = data[char_col + char_row][ch_row + pix]
                    byte = byte[::-1]
                    for bit in xrange(0, 8, 2):
                        if byte[bit:bit+2] == '01':
                            char_line.extend([255,255,255])
                        elif byte[bit:bit+2] == '00':
                            char_line.extend([0,0,0])
                        elif byte[bit:bit+2] == '10':
                            char_line.extend([128, 128, 128])
                        else:
                            print byte[bit:bit+2]
                        i += 1

                img_line.extend(char_line[::-1])
                if draw_net and char_col < 15:
                    img_line.extend([255,0,0])
            img_list.append(tuple(img_line))
        if draw_net and char_row < 240:
            img_list.append([255,0,0]*img_x)
    img.write(ofile, img_list)

inputfile = None
outputfile = None
draw_net = False

try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:o:n",["ifile=","ofile=", "net"])
except getopt.GetoptError:
    print_help(sys.argv[0])
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print_help(sys.argv[0])
        sys.exit()
    elif opt in ("-i", "--ifile"):
        inputfile = arg
    elif opt in ("-o", "--ofile"):
        outputfile = arg
    elif opt in ("-n", "--net"):
        draw_net = True

if inputfile is None:
    print_help(sys.argv[0])
    sys.exit(1)

current_char = 0
idata = read_font(inputfile)
with smart_open(outputfile) as of:
    parse_font(idata, of, draw_net=draw_net)
