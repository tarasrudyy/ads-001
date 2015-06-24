import math

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
    input_file = "bugtrk.in"
    output_file = "bugtrk.out"

    # read data
    lines = read_file(input_file)

    N = lines[1][0]
    W = lines[1][1]
    H = lines[1][2]

    # find minimum side of the square
    side = max(W, H, int(math.ceil(math.sqrt(N * W * H))))

    # test side
    small_side = min(W, H)
    big_side = max(W, H)

    while True:
        elements_in_row = (side - side % small_side) / small_side
        number_of_rows = (side - side % big_side) / big_side
        if elements_in_row * number_of_rows >= N:
            break
        else:
            side = min(small_side * (elements_in_row + 1), big_side * (number_of_rows + 1))

    result = side

    # write data
    write_file(output_file, result)

if __name__ == "__main__":
    main()