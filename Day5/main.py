# This is a sample Python script.
import sys
import ast
import operator

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

LINE_TYPE = tuple[tuple[int, int], tuple[int, int]]
BOARD_DIMENSION_TYPE = tuple[tuple[int, int], tuple[int, int]]

DEBUG = True


def filter_lines(line_txt: str) -> list[LINE_TYPE]:
    line_txt_list = line_txt.split("\n")

    invalid_lines = 0
    dot_count = 0  # probably should be counted
    vertical_count = 0
    horizontal_count = 0
    slanted_count = 0  # will be ignored

    filtered_list = []

    print(f"total lines: {len(line_txt_list)}")

    for ln_num, line in enumerate(line_txt_list):
        elements = line.split(' ')  # tuple, ->, tuple
        if len(elements) != 3:
            print(f"Wrong Input{ln_num}: {line}")
            continue

        coord1: tuple = ast.literal_eval(elements[0])
        coord2: tuple = ast.literal_eval(elements[2])

        # I mean, I saw the data and there weren't "wrong input" inside :d
        # if issubclass(tuple, coord1.__class__) or \
        #         issubclass(tuple, coord2.__class__):
        #     print(f"Wrong Input{ln_num}: {line}")
        #     invalid_lines = invalid_lines + 1
        #     continue

        coord_tuple = (coord1, coord2)
        filtered_list.append(coord_tuple)
        # will be pop()-ed if it turns out to be slanted

        if coord1 == coord2:
            dot_count = dot_count + 1
            continue

        if coord1[0] == coord2[0]:
            vertical_count = vertical_count + 1
            continue

        if coord1[1] == coord2[1]:
            horizontal_count = horizontal_count + 1
            continue

        slanted_count = slanted_count + 1
        filtered_list.pop()

    print(f"{invalid_lines=}, {dot_count=}, {vertical_count=}, {horizontal_count=}, {slanted_count=}")

    return filtered_list


def filter_lines_hv(line_txt: str) -> tuple[list[LINE_TYPE], list[LINE_TYPE]]:
    line_txt_list = line_txt.split("\n")

    invalid_lines = 0
    # dot_count = 0  # probably should be counted
    horizontal_count = 0
    vertical_count = 0
    slanted_count = 0  # will be ignored

    filtered_list_h = []
    filtered_list_v = []
    # Dots will be counted as horizontal.
    # Does not violate the logic here.

    print(f"total lines: {len(line_txt_list)}")

    for ln_num, line in enumerate(line_txt_list):
        elements = line.split(' ')  # tuple, ->, tuple
        if len(elements) != 3:
            print(f"Wrong Input{ln_num}: {line}")
            continue

        coord1: tuple = ast.literal_eval(elements[0])
        coord2: tuple = ast.literal_eval(elements[2])

        coord_tuple = (coord1, coord2)
        # filtered_list.append(coord_tuple)

        # if coord1 == coord2:
        #     dot_count = dot_count + 1
        #     continue

        if coord1[1] == coord2[1]:
            horizontal_count = horizontal_count + 1
            filtered_list_h.append(coord_tuple)
            continue

        if coord1[0] == coord2[0]:
            vertical_count = vertical_count + 1
            filtered_list_v.append(coord_tuple)
            continue

        slanted_count = slanted_count + 1
        # filtered_list.pop()

    print(f"{invalid_lines=}, {vertical_count=}, {horizontal_count=}, {slanted_count=}")

    return filtered_list_h, filtered_list_v


def board_dimension(lines: list[LINE_TYPE]) -> BOARD_DIMENSION_TYPE:
    x_min = 9999
    x_max = 0
    y_min = 9999
    y_max = 0

    for line in lines:
        if line[0][0] < x_min:
            x_min = line[0][0]
        if line[1][0] < x_min:
            x_min = line[1][0]
        if line[0][0] > x_max:
            x_max = line[0][0]
        if line[1][0] > x_max:
            x_max = line[1][0]

        if line[0][1] < y_min:
            y_min = line[0][1]
        if line[1][1] < y_min:
            y_min = line[1][1]
        if line[0][1] > y_max:
            y_max = line[0][1]
        if line[1][1] > y_max:
            y_max = line[1][1]

    if DEBUG:
        print(f"board top left: {x_min},{y_min}\nboard bottom right: {x_max},{y_max}")
    return (x_min, y_min), (x_max, y_max)


def place_lines_and_check(dim: BOARD_DIMENSION_TYPE, lines: list[LINE_TYPE]):
    grand_total: int = 0
    board: list

    width = dim[1][0] - dim[0][0]
    height = dim[1][1] - dim[0][1]

    row = [0 for _ in range(width)]
    board = [row[:] for _ in range(height)]
    # row[:] - avoid shallow copy

    # sheesh, we need to test vertical or horizontal now
    # maybe not. let's try rearranging filtered_lines
    raise NotImplementedError


def place_lines_and_check_hv(dim: BOARD_DIMENSION_TYPE, v_lines: list[LINE_TYPE], h_lines: list[LINE_TYPE]):
    grand_total: int = 0
    board: list

    # width = dim[1][0] - dim[0][0] + 1
    # height = dim[1][1] - dim[0][1] + 1
    width = dim[1][0] - dim[0][0] + 5  # FIXME: arbitrary dirty expansion
    height = dim[1][1] - dim[0][1] + 5

    if DEBUG:
        print(f"boardsz: {width},{height}")

    row = [0 for _ in range(width)]
    board = [row[:] for _ in range(height)]
    # row[:] - avoid shallow copy

    for h_line in h_lines:
        advance: tuple[int, int]
        increasing: bool = h_line[0] < h_line[1]
        increment = int(increasing) * 2 - 1  # -1 or 1
        advance = (0, increment)

        # start = h_line[0]
        # end = h_line[1]
        # Example works like this because it covers all board.
        # We need to subtract dim[0] which is minimum value of the board
        start = tuple(map(operator.sub, h_line[0], dim[0]))
        end = tuple(map(operator.sub, h_line[1], dim[0]))

        current = start
        if DEBUG:
            print(f"{h_line[0]=}{h_line[1]=}")
            print(f"{start=},{end=},{advance=}", flush=True)
        while True:
            if DEBUG:
                print(f"{current=}", flush=True)
            board[current[0]][current[1]] += 1
            if board[current[0]][current[1]] == 2:
                grand_total += 1
            if current == end:
                break
            current = tuple(map(operator.add, current, advance))

    for v_line in v_lines:
        advance: tuple[int, int]
        increasing: bool = v_line[0] < v_line[1]
        increment = int(increasing) * 2 - 1  # -1 or 1
        advance = (increment, 0)

        # start = v_line[0]
        # end = v_line[1]
        # Example works like this because it covers all board.
        # We need to subtract dim[0] which is minimum value of the board
        start = tuple(map(operator.sub, v_line[0], dim[0]))
        end = tuple(map(operator.sub, v_line[1], dim[0]))

        current = start
        if DEBUG:
            print(f"{v_line[0]=}{v_line[1]=}")
            print(f"{start=},{end=},{advance=}", flush=True)
        while True:
            if DEBUG:
                print(f"{current=}", flush=True)
            board[current[0]][current[1]] += 1
            if board[current[0]][current[1]] == 2:
                grand_total += 1
            if current == end:
                break
            current = tuple(map(operator.add, current, advance))
    if DEBUG:
        print(board)
        print(f"{grand_total=}")
    return grand_total


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data_ = sys.stdin.read()

    # filtered_lines: list[LINE_TYPE]
    filtered_lines_h: list[LINE_TYPE]
    filtered_lines_v: list[LINE_TYPE]
    board_dimensions: BOARD_DIMENSION_TYPE

    # filtered_lines = filter_lines(data_)
    filtered_lines_h, filtered_lines_v = filter_lines_hv(data_)
    # board_dimensions = board_dimension(filtered_lines)
    board_dimensions = board_dimension(filtered_lines_h + filtered_lines_v)

    total = place_lines_and_check_hv(board_dimensions, filtered_lines_h, filtered_lines_v)

    print(f"{total=}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
