def read_file(input_file):
    L = 0
    levels = []
    with open(input_file, 'r') as f:
        L = int(f.readline())
        for line in f.readlines():
            levels.append(map(int, line.split()))

    return L, levels

def write_file(output_file, result):
    with open(output_file, 'w') as f:
        f.write(str(result))

def main():
    input_file = 'career.in'
    output_file = 'career.out'

    L, levels = read_file(input_file)
    levels.reverse()

    solutions = levels[0]
    for i in range(1, L):
        for j in range(0, L):
            left = levels[i][j - 1] if 0 < j < L - i + 1 else 0
            right = levels[i][j] if j < L - i else 0
            solutions[j] = solutions[j] + max(left, right)

    result = max(solutions)

    write_file(output_file, result)

if __name__ == '__main__':
    main()

