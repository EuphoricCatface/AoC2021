import sys
import ast
import operator


LINE_TYPE = tuple[tuple[int, int], tuple[int, int]]
BOARD_DIMENSION_TYPE = tuple[tuple[int, int], tuple[int, int]]

DEBUG = True


def filter_lines_hv45(line_txt: str) -> tuple[list[LINE_TYPE], list[LINE_TYPE], list[LINE_TYPE]]:
    line_txt_list = line_txt.split("\n")

    invalid_lines = 0
    horizontal_count = 0
    vertical_count = 0
    slanted45_count = 0
    slanted_odd_count = 0  # will be ignored

    filtered_list_h = []
    filtered_list_v = []
    filtered_list_45 = []
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

        if coord1[1] == coord2[1]:
            horizontal_count = horizontal_count + 1
            filtered_list_h.append(coord_tuple)
            continue

        if coord1[0] == coord2[0]:
            vertical_count = vertical_count + 1
            filtered_list_v.append(coord_tuple)
            continue

        subtract_coord = tuple(map(operator.sub, coord1, coord2))
        if abs(subtract_coord[0]) == abs(subtract_coord[1]):
            slanted45_count += 1
            filtered_list_45.append(coord_tuple)
            continue

        slanted_odd_count = slanted_odd_count + 1

    print(f"{invalid_lines=}, {vertical_count=}, {horizontal_count=}, {slanted45_count=}, {slanted_odd_count=}")

    return filtered_list_h, filtered_list_v, filtered_list_45


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


if __name__ == '__main__':
    data_ = sys.stdin.read()

    filtered_lines_h: list[LINE_TYPE]
    filtered_lines_v: list[LINE_TYPE]
    filtered_lines_45:list[LINE_TYPE]
    board_dimensions: BOARD_DIMENSION_TYPE

    filtered_lines_h, filtered_lines_v, filtered_lines_45 = filter_lines_hv45(data_)
    raise NotImplementedError
    board_dimensions = board_dimension(filtered_lines_h + filtered_lines_v)

    total = place_lines_and_check_hv(board_dimensions, filtered_lines_h, filtered_lines_v)

    print(f"{total=}")
