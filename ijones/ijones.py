def read_file(input_file):
    lines = []
    lines.append(input_file)
    with open(input_file) as f:
        for line in f:
            if ' ' in line:
                lines.append(map(int, line.split(' ')))
            else:
                lines.append(int(line))
    return lines

def write_file(output_file, value):
    with open(output_file, 'w') as f:
        f.write(str(value))


def main():
    input_file = 'ijones.in'
    output_file = 'ijones.out'

    # read data
    lines = read_file(input_file)

    result = 0

    # write data
    write_file(output_file, result)

if __name__ == "__main__":
    main()
