import sys
# part 1 is quite easy. Let's count the outputs of unique length


def main():
    input_str = sys.stdin.read()
    input_str.strip()

    count = 0
    for line in input_str.split("\n"):
        if len(line) == 0:
            continue

        # output format is different from the examples o_O
        # if line[-1] == '|':
        #     continue
        line = line[line.find("|")+1:]
        line.strip()

        for output in line.split():
            if len(output) in [2, 3, 4, 7]:
                count += 1

    print(count)


if __name__ == "__main__":
    main()
