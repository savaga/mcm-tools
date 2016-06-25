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
    print '%s -i <inputfile.mcm> -o <outputfile.mcm> -f <from pos> -t <to pos> -c <count>' % name

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

inputfile = None
outputfile = None
copy_from = 0
copy_to   = 0
chars_num = 0

try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:o:f:t:c:",["ifile=","ofile=","from=","to=","count="])
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
    elif opt in ("-f", "--from"):
        copy_from = int(arg, 0)
    elif opt in ("-t", "--to"):
        copy_to = int(arg, 0)
    elif opt in ("-c", "--count"):
        chars_num = int(arg, 0)

if inputfile is None:
    print_help(sys.argv[0])
    sys.exit(1)

current_char = 0
idata = read_font(inputfile)
odata = read_font(outputfile)

for i in xrange(chars_num):
    odata[copy_to + i] = idata[copy_from + i]

with smart_open(outputfile) as fh:
    print >>fh, "MAX7456"
    for char in odata:
        for line in char:
            print >>fh, line
