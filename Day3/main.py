import sys
import operator


def main():
    input_str = sys.stdin.read()
    gamma_rate = 0
    epsilon_rate = 0

    input_length = 0

    input_width = input_str.find("\n")
    count_array = [0 for _ in range(input_width)]

    for line in input_str.split("\n"):
        if line == "":
            continue

        line_array = list(map(int, list(line)))
        count_array = list(map(operator.add, count_array, line_array))
        input_length += 1

    if input_length / 2 == 1:
        print("Warning: input_length is even")
    count_array.reverse()

    for i, count in enumerate(count_array):
        if count > (input_length / 2):
            gamma_rate += 2 ** i
        else:
            epsilon_rate += 2 ** i

    print(gamma_rate * epsilon_rate)


if __name__ == "__main__":
    main()