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
        f.write("%.2f" % value)


def main():
    input_file = "discnt.in"
    output_file = "discnt.out"

    # read data
    lines = read_file(input_file)

    prices = sorted(lines[1])
    prices.reverse()
    discount = (100.0 - lines[2]) / 100
    top_items_amount = len(prices) / 3
    for i in range(0, top_items_amount):
        prices[i] *= discount

    result = sum(prices)

    # write data
    write_file(output_file, result)

if __name__ == "__main__":
    main()
