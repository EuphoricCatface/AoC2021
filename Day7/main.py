import sys
# # crabs can align to the average of their positions
# no they don't
# The calculation will result in only one local minimum. We can move in that direction until it goes back up.
DEBUG = 1


def fuel_consumption(data, point):
    fuel_sum = 0
    for i in data:
        # fuel_sum += abs(point - i) # part 1
        distance = abs(point - i)
        fuel_sum += distance * (distance + 1) / 2
    return fuel_sum


def main():
    input_str = sys.stdin.read()
    input_str = input_str.strip()
    input_int_list = \
        list(map(
            int, input_str.split(",")
        ))

    average = round(sum(input_int_list) / len(input_int_list))
    maximum = max(input_int_list)
    if DEBUG == 1:
        print(average)

    # let's start from average, and then do binary search
    point = average
    left_end = 0
    right_end = maximum
    while True:
        point_usage = fuel_consumption(input_int_list, point)
        left_usage = fuel_consumption(input_int_list, point - 1)
        right_usage = fuel_consumption(input_int_list, point + 1)

        if left_usage < point_usage and point_usage > right_usage:
            print("Error: Assumption was wrong, unless logic was wrong")
            return
        if left_usage > point_usage > right_usage:
            left_end = point
            point = int((left_end + right_end) / 2)
            continue
        if left_usage < point_usage < right_usage:
            right_end = point
            point = int((left_end + right_end) / 2)
            continue
        if left_usage > point_usage and point_usage < right_usage:
            print(f"We fount optimum at {point} and the usage is {point_usage}")
            return

        print(f"huh, we got a tie here around {point}")


if __name__ == "__main__":
    main()
