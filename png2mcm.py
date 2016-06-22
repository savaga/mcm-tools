import png
from pprint import pprint, pformat
import pdb
import sys, getopt
import contextlib

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

def print_help(name):
    print '%s -i <inputfile.png> -o <outputfile.mcm> [-a|--ascii] [-x|--xsize] <x size> [-y|--ysize] <y size> [-s|--start] <start> [-p--padding]' % name

ascii_print = None
padding = None
inputfile = None
outputfile = None
xchars = 0
ychars = 0
startat = 0

try:
    opts, args = getopt.getopt(sys.argv[1:],"pahi:o:x:y:s:",["ifile=","ofile=","ascii","xsize=","ysize=","start","padding"])
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
    elif opt in ("-a", "--ascii"):
        ascii_print = True
    elif opt in ("-x", "--xsize"):
        xchars = int(arg)
    elif opt in ("-y", "--ysize"):
        ychars = int(arg)
    elif opt in ("-s", "--start"):
        startat = int(arg)
    elif opt in ("-p", "--padding"):
        padding = True

if inputfile is None:
    print_help(sys.argv[0])
    sys.exit(1)

p = png.Reader(filename=inputfile)
t = p.read_flat()
xsize = t[0]
ysize = t[1]
data = t[2]

if xchars > xsize/12:
    xchars = xsize/12
else:
    xchars = xchars or xsize/12

if ychars > ysize/18:
    ychars = ysize/18
else:
    ychars = ychars or ysize/18

current_char = 0
with smart_open(outputfile) as fh:
    if ascii_print:
        for i in xrange(0, len(data), xsize*4):
            for j in xrange(0, xsize*4, 4):
                if data[i + j + 1] == 0:
                    fh.write('#')
                else:
                    fh.write(' ')
            fh.write('\n')
    else:
        print >>fh, "MAX7456"
        while startat > current_char:
            for b in xrange(64):
                print >>fh, "01010101"
            current_char += 1

        for line in xrange(ychars):
            for char in xrange(xchars):
                for y in xrange(18):
                    for byte in xrange(3):
                        out = 0
                        for bit in xrange(4):
                            d = data[bit*4 + byte*16 + y*xsize*4 + char*12*4 + line*xsize*4*18]
                            if d == 255:
                                out += 2 << ((3-bit)*2)
                            if d > 0 and d < 255:
                                out += 1 << ((3-bit)*2)
                        print >>fh, format(out, '08b')
                for pad in xrange(10):
                    print >>fh, "11111111"
                current_char += 1

        while current_char < 256:
            for b in xrange(64):
                print >>fh, "01010101"
            current_char += 1
