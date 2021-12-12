import sys
# part 1 is quite easy. Let's count the outputs of unique length

# part 2 strategy
# Let's call normal 7seg configuration in capital
# (Clockwise configuration; not int the question's way.
# Specific configuration doesn't matter in this puzzle)
# pass 1: count lines
# [count 5: 2, 3, 5]
# 5 - pass 1:
# Determine F or G by comparing 1 and 4
# -> Determine 5 by presence of both
# 5 - pass 2:
# Determine E by comparing 1 and absences in 5
# -> 2 if E is present, else 3
# [count 6: 0, 6, 9]
# 6 - pass 1:
# Determine 6 by comparing absences with 1
# 6 - pass 2:
# Determine F or G by comparing 1 and 4
# -> 9 if both are present, else 0

FULL_SIGNAL = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
DEBUG = 1


def deduction(line: str):
    try:
        conditions_str, numbers_signal_str = line.split('|')
    except ValueError:
        return
    conditions_str.strip()
    numbers_signal_str.strip()
    unsolved_5count: list[set] = list()
    unsolved_6count: list[set] = list()
    every_5count: list[set] = list()
    every_6count: list[set] = list()
    # signal_to_int = dict()
    int_to_signal = [{'-'} for _ in range(10)]
    result = list("----")

    # Pass 1: quick, obvious check
    numbers_signal_list = numbers_signal_str.split()
    for i, symbol in enumerate(numbers_signal_list):
        length = len(symbol)
        if length == 2:
            result[i] = 1
        elif length == 3:
            result[i] = 7
        elif length == 4:
            result[i] = 4
        elif length == 5:
            unsolved_5count.append(set(symbol))
        elif length == 6:
            unsolved_6count.append(set(symbol))
        elif length == 7:
            result[i] = 8

    if (not unsolved_5count) and (not unsolved_6count):
        value = 0
        for i in result:
            value *= 10
            value += i
        return value

    # Darn, we gotta do some calc now
    def list_sub(x, y):
        return [item for item in x if item not in y]

    for i, symbol in enumerate(conditions_str.split()):
        symbol = set(symbol)
        length = len(symbol)
        if length == 2:
            int_to_signal[1] = symbol
        elif length == 3:
            int_to_signal[7] = symbol
        elif length == 4:
            int_to_signal[4] = symbol
        elif length == 5:
            every_5count.append(symbol)
        elif length == 6:
            every_6count.append(symbol)
        elif length == 7:
            int_to_signal[8] = symbol

    # https://stackoverflow.com/questions/3428536/python-list-subtraction-operation
    b_c = list(int_to_signal[1])
    f_g = list_sub(list(int_to_signal[4]), b_c)

    while True:  # goto substitute
        if not unsolved_5count and 0:
            break

        # pass 1: find 5
        for signal in every_5count:
            if f_g[0] in signal and \
                    f_g[1] in signal:
                int_to_signal[5] = signal
                if signal in unsolved_5count:
                    unsolved_5count.remove(signal)
                break
        if not unsolved_5count and 0:
            break

        # pass 2: Find E to figure 2/3
        b_e = FULL_SIGNAL.copy().difference(int_to_signal[5])
        e = b_e.difference(b_c).pop()

        while unsolved_5count:
            signal = unsolved_5count.pop()
            if e in signal:
                int_to_signal[2] = signal
            else:
                int_to_signal[3] = signal

        if unsolved_5count:
            print("unsolved_5count logic fault")
        break

    while True:  # goto substitute
        if not unsolved_6count and 0:
            break

        # pass 1: find 6 by comparing the absence with 1
        for signal in unsolved_6count.copy():
            b_supposed = FULL_SIGNAL.copy().difference(signal).pop()
            if b_supposed in b_c:
                int_to_signal[6] = signal
                if signal in unsolved_6count:
                    unsolved_6count.remove(signal)
                break
        if not unsolved_6count and 0:
            break

        # pass 2: Determine 9/0 by using F, G
        while unsolved_6count:
            signal = unsolved_6count.pop()
            if f_g[0] in signal and \
                    f_g[1] in signal:
                int_to_signal[9] = signal
            else:
                int_to_signal[0] = signal

        if unsolved_6count:
            print("unsolved_6count logic fault")
        break

    for i, signal in enumerate(numbers_signal_list):
        result[i] = int_to_signal.index(set(signal))

    if DEBUG == 1:
        print(f"{int_to_signal}")

    value = 0
    for i in result:
        value *= 10
        value += i
    return value
    # print(f"{conditions_str=} {numbers_signal_str=} {unsolved_5count=} {unsolved_6count=}")


def main():
    input_str = sys.stdin.read()
    input_str = input_str.strip()

    summation = 0
    for line in input_str.split("\n"):
        result = deduction(line)
        if DEBUG == 1:
            print(f"{result}, {line}")
        summation += result

    print(f"{summation=}")


if __name__ == "__main__":
    main()
