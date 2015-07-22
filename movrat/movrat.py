import random

def compare(a, b):
    return a < b

def swap(array, i, j):
    (array[i], array[j]) = (array[j], array[i])

def shuffle(array):
    n = len(array)
    for i in range(0, n - 2):
        random_item_index = random.randint(i, n - 1)
        swap(array, i, random_item_index)

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

# merge sort
def sort(array):
    result = merge_sort_recursive(array, 0, len(array) - 1)
    for i in range(0, len(result)):
        array[i] = result[i]

def merge_sort_recursive(array, left, right):
    if left < right:
        middle = (left + right) / 2
        left_part = merge_sort_recursive(array, left, middle)
        right_part = merge_sort_recursive(array, middle + 1, right)
        result = merge(left_part, right_part)
        return result

    return [array[left]]

def merge(left_array, right_array):
    result = [None] * (len(left_array) + len(right_array))
    left_pos = right_pos = result_pos = 0

    while result_pos < len(result):
        if left_pos >= len(left_array) or (right_pos < len(right_array) and compare(right_array[right_pos], left_array[left_pos])):
            result[result_pos] = right_array[right_pos]
            right_pos += 1
        else:
            result[result_pos] = left_array[left_pos]
            left_pos += 1

        result_pos += 1

    return result


def main():
    input_file = "movrat.in"
    output_file = "movrat.out"

    # read data
    lines = read_file(input_file)
    n = lines[1]
    data = []
    data.append(lines[2])
    low = lines[3]
    high = lines[4]

    # do job
    sort(data)
    result = sum(data[low : n - high]) / (n - low - high)

    # write data
    write_file(output_file, result)

if __name__ == "__main__":
    main()
