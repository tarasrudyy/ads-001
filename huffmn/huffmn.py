import sys
import struct
import os.path
import timeit
from heapq import *
from collections import defaultdict

MB = 1048576

def bytes_from_file(filename):
    with open(filename, 'rb', 1 * MB) as f:
        while True:
            chunk = f.read(1 * MB)
            if chunk:
                for byte in chunk:
                    yield byte
            else:
                break

def calculate_bytes_rate(filename, rates):
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

def calculate_unused_bits(rates, codes):
    result = 0
    for c in rates:
        result += rates[c] * len(codes[c])
    return 8 - result % 8, result

def compress(input_file, output_file):
    # init progress bar
    data_counter = 0
    data_size = os.path.getsize(input_file)
    print_progress(data_counter, data_size)

    rates = defaultdict(int)
    calculate_bytes_rate(input_file, rates)
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

    # we have uncompleted byte
    if len(code_string) < 8:
        buff.append(int(code_string.ljust(8, '0'), 2))

    if len(buff) > 0:
        file_out.write(buff)

    file_out.close()

    print_progress(data_size, data_size)

def decompress(input_file, output_file):
    # read header
    file_in = open(input_file, 'rb', 1 * MB)

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

    unused_bits, total_bits = calculate_unused_bits(rates, codes)

    # update data size for progress
    data_counter = 0
    data_size = total_bits
    print_progress(data_counter, data_size)

    # create empty file
    file_out = open(output_file, 'wb')

    # read encoded data
    bit_string = ''
    while True:
        chunk1 = file_in.read(512)
        chunk2 = file_in.read(512)
        buff = bytearray(chunk1 + chunk2)

        bit_string += ''.join([bin(byte)[2:].rjust(8, '0') for byte in buff])
        # end of file - remove unused bits
        if chunk2 == '':
            bit_string = bit_string[:-unused_bits]

        root = tree[0]
        for b in bit_string:
            data_counter += 1
            print_progress(data_counter, data_size)
            root = root.left if b == '0' else root.right

            if root.left is None and root.right is None:
                # found a leaf node, you found a symbol then
                file_out.write(root.item)
                code_len = len(codes[root.item])
                bit_string = bit_string[code_len:]
                root = tree[0]

        # end of file
        if chunk2 == '':
            break

    file_in.close()
    file_out.close()

    print_progress(data_size, data_size)

def print_progress(val, end_val=1 * MB, bar_length=100):
    if end_val > 1 * MB and val % (end_val / 100) == 0:
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
            timer = timeit.Timer(lambda: decompress(input_file, output_file))
    else:
        print_help()

    seconds_elapsed = timer.timeit(1)
    print ""
    print ("Time elapsed: %f sec" % seconds_elapsed)
    if command == 'compress':
        compression_ratio = (100.0 * os.path.getsize(output_file)) / os.path.getsize(input_file)
        if compression_ratio <= 100:
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
