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

    solutions = levels[0]
    for i in range(1, L):
        new_solutions = [0] * (i + 1)
        for j in range(0, i):
            left = solutions[j] + levels[i][j]
            if new_solutions[j] < left:
                new_solutions[j] = left
            right = solutions[j] + levels[i][j + 1]
            if new_solutions[j + 1] < right:
                new_solutions[j + 1] = right
        solutions = new_solutions

    result = max(solutions)

    write_file(output_file, result)

if __name__ == '__main__':
    main()

