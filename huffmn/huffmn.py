import sys
import timeit
from heapq import *
from collections import defaultdict

def bytes_from_file(filename, chunksize=8192):
    with open(filename, 'rb', 1048576) as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for byte in chunk:
                    yield byte
            else:
                break

def write_file(filename, bytes):
    with open(filename, 'wb') as f:
        f.write(bytes)

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
    return codes

def huffman(data, codes):
    return ''.join([codes[b] for b in data])

def compress(input_file, output_file):
    rates = defaultdict(int)
    calc_bytes_rate(input_file, rates)
    codes = build_codes(rates);
    print codes

def main():
    input_file = 'test.txt' if len(sys.argv) == 1 else sys.argv[1]
    output_file = input_file + '.huf' if len(sys.argv) <= 2 else sys.argv[2]

    timer = timeit.Timer(lambda: compress(input_file, output_file))
    seconds_elapsed = timer.timeit(1)

    print "Time elapsed: %d sec" % seconds_elapsed

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
        return cmp(self.weight, a.weight)

if __name__ == "__main__":
    main()
