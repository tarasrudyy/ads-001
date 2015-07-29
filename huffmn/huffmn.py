import sys
import struct
import os.path
import timeit
from heapq import *
from collections import defaultdict

MB = 1048576

def bytes_from_file(filename, chunksize=8192):
    with open(filename, 'r', 1 * MB) as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for byte in chunk:
                    yield byte
            else:
                break

def calc_bytes_rate(filename, rates):
    for byte in bytes_from_file(filename):
        rates[byte] += 1

def code_it(codes, s, node):
    if node.item:
        if not s:
            codes[node.item] = '0'
        else:
            codes[node.item] = s
    else:
        code_it(codes, s + '0', node.left)
        code_it(codes, s + '1', node.right)

def build_codes(rates):
    item_queue = [Node(byte, rate) for byte, rate in rates.iteritems()]
    heapify(item_queue)
    while len(item_queue) > 1:
        l = heappop(item_queue)
        r = heappop(item_queue)
        n = Node(None, r.weight + l.weight)
        n.setChildren(l, r)
        heappush(item_queue, n)

    codes = defaultdict(str)
    code_it(codes, '', item_queue[0])
    return codes, item_queue

def compress(input_file, output_file):
    # init progress bar
    data_counter = 0
    data_size = os.path.getsize(input_file)
    print_progress(data_counter, data_size)

    rates = defaultdict(int)
    calc_bytes_rate(input_file, rates)
    codes, tree = build_codes(rates)

    # create empty file
    file_out = open(output_file, 'wb')

    # write rates
    header = (struct.pack('I', rates[chr(b)]) for b in range(0, 256))
    file_out.write(''.join(header))

    buff = bytearray()
    code_string = ''
    for byte in bytes_from_file(input_file):
        code_string += codes[byte]
        while len(code_string) >= 8:
            buff.append(int(code_string[0:8], 2))
            code_string = code_string[8:]

        if len(buff) > 1 * MB:
            file_out.write(buff)
            del buff[:]

        data_counter += 1
        print_progress(data_counter, data_size)

    unused_bits = (8 - len(code_string)) % 8

    # we have uncompleted byte
    if unused_bits:
        buff.append(int(code_string.ljust(8, '0'), 2))

    # write last byte to identify unused bits
    buff.append(unused_bits)

    if len(buff) > 0:
        file_out.write(buff)

    file_out.close()

    print_progress(data_size, data_size)


def decompress(input_file, output_file):
    # init progress bar
    print_progress(0, 100)

    # read header
    file_in = open(input_file, 'rb')
    # 256 symbols, 4 bytes each
    header = file_in.read(1024)
    unpacked_header = struct.unpack('256I', header)
    # restore rates
    rates = defaultdict(int)
    for b, rate in enumerate(unpacked_header):
        if rate > 0:
            rates[chr(b)] = rate
    # build huffman tree
    codes, tree = build_codes(rates)

    # calculate and store binary codes for the 256 symbols
    bin_codes = dict((k, ''.join(['1' if ((1 << i) & k) else '0' for i in range(7, -1, -1)])) for k in range(256))

    # read encoded data
    bit_string = ''.join([bin_codes[ord(byte)] for line in file_in for byte in line])
    file_in.close()

    # remove end code and extra bits
    bit_string = bit_string[:-8 - int(bit_string[-8:], 2)]

    # update data size for progress
    data_counter = 0
    data_size = len(bit_string)
    print_progress(data_counter, data_size)

    # create empty file
    file_out = open(output_file, 'w')

    root = tree[0]
    start = root
    for b in bit_string:
        data_counter += 1
        print_progress(data_counter, data_size)
        root = root.left if b == '0' else root.right

        if root.left is None and root.right is None:
            # found a leaf node, you found a symbol then
            file_out.write(root.item)
            root = start

    file_out.close()

    print_progress(100, 100)

def print_progress(val, end_val, bar_length=50):
    percent = float(val) / end_val
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\rProgress: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()

def print_help():
    print "Huffman compression script"
    print ""
    print "usage: python huffmn.py [ compress | decompress ] <input_file> <output_file>"
    exit()

def main():
    if len(sys.argv) == 4:
        command = sys.argv[1]
        if command not in ['compress', 'decompress']:
            print_help()

        input_file = sys.argv[2]
        if not os.path.isfile(input_file):
            print_help()

        output_file = sys.argv[3]
        if not os.path.isfile(input_file):
            print_help()

        if command == 'compress':
            timer = timeit.Timer(lambda: compress(input_file, output_file))
        elif command == 'decompress':
            decompress(input_file, output_file)
            timer = timeit.Timer(lambda: uncompress(input_file, output_file))
    else:
        print_help()

    seconds_elapsed = timer.timeit(1)
    print ""
    print ""
    print "Time elapsed: %d sec" % seconds_elapsed
    if command == 'compress':
        compression_ratio = (100.0 * os.path.getsize(output_file)) / os.path.getsize(input_file)
        print "Compression ratio: %0.2f" % compression_ratio + "%"


class Node(object):
    left = None
    right = None
    item = None
    weight = 0

    def __init__(self, i, w):
        self.item = i
        self.weight = w

    def setChildren(self, ln, rn):
        self.left = ln
        self.right = rn

    def __repr__(self):
        return "%s - %s - %s _ %s" % (self.item, self.weight, self.left, self.right)

    def __cmp__(self, a):
        res = cmp(self.weight, a.weight)
        if res == 0 and hasattr(a, 'item'):
            # symbols have same weight, compare by lexical order then
            res = cmp(self.item, a.item)

        return res

if __name__ == "__main__":
    main()
