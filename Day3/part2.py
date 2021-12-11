import sys
import operator


# criteria: True is O2, False is CO2
def filter_data(nth: int, data: list[str], criteria: bool) -> list:
    count_list: tuple[list[str], list[str]] = (list(), list())

    for line in data:
        count_list[int(line[nth])].append(line)

    if len(count_list[0]) == len(count_list[1]):
        return count_list[int(criteria)]

    if (len(count_list[1]) > len(count_list[0])) == criteria:
        return count_list[1]
    else:
        return count_list[0]


def main():
    input_str = sys.stdin.read()

    input_width = input_str.find("\n")
    input_list = input_str.split("\n")
    while "" in input_list:
        input_list.remove("")

    o2_list = input_list.copy()
    for i in range(input_width):
        o2_list = filter_data(i, o2_list, True)
        if len(o2_list) == 1:
            break
    print(f"{o2_list=}")

    co2_list = input_list.copy()
    for i in range(input_width):
        co2_list = filter_data(i, co2_list, False)
        if len(co2_list) == 1:
            break
    print(f"{co2_list=}")

    print(f"answer = {int(o2_list[0], 2) * int(co2_list[0], 2)}")
    # print(gamma_rate * epsilon_rate)


if __name__ == "__main__":
    main()
