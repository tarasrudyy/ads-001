def read_file(input_file):
    lines = []
    with open(input_file) as f:
        for line in f:
            l = line.split()
            lines.append(l[0])
    return lines

def write_file(output_file, value):
    with open(output_file, 'w') as f:
        f.write(str(value))


def main():
    input_file = "wchain.in"
    output_file = "wchain.out"

    # read data
    lines = read_file(input_file)

    result = 0

    # write data
    write_file(output_file, result)

if __name__ == "__main__":
    main()
