import sys
import collections
DEBUG = 1
MINUS_ZERO = -255


class Board:
    board_count = 0

    def __init__(self):
        self.board: list[list[int]] = []
        self.serial = Board.board_count
        Board.board_count += 1
        self.init_row_count = 0
        self.score = -1

    def fill_line(self, line: [list[int]]):
        self.init_row_count += 1
        if self.init_row_count >= 6:
            print(f"Warning: Board has more than 5 lines, {self.serial=}")

        self.board.append(line)

    def call(self, number) -> tuple[int, int]:
        coord: tuple[int, int] = -1, -1

        # QUIRK: board is already won only if score is not negative (-1)
        if self.score >= 0:
            return coord

        for i, line in enumerate(self.board):
            if number in line:
                coord = i, line.index(number)

        # QUIRK: set a number as negative if called
        if coord != (-1, -1):
            self.board[coord[0]][coord[1]] = -number
            # fsck there's no such thing as -0 uhh
            if number == 0:
                self.board[coord[0]][coord[1]] = MINUS_ZERO

        if DEBUG == 1:
            if 1:  # self.serial == 42:
                # print(self.board)
                for i in self.board:
                    if number in i:
                        print(f"How on earth did {number} fall through?!")
                    elif 0:  # -number in i:
                        print(f"{number} is checked here, it seems.")

        # return coord
        # Oops, array index and (x, y) coord goes reverse!
        # test_win is coded for (x, y) coord
        return coord[1], coord[0]

    def test_win(self, coord: tuple) -> bool:
        # if won, set score

        # row test
        row_fail = False
        for i in self.board[coord[1]]:
            if i >= 0:
                row_fail = True
                break
        if not row_fail:
            return True

        # column test
        column_fail = False
        for row in self.board:
            if row[coord[0]] >= 0:
                column_fail = True
                break
        if not column_fail:
            return True

        # row_fail AND column_fail
        return False

    def calc_score(self, last_number):
        if DEBUG == 1:
            print(f"{self.serial=}, {last_number=}\n{self.board}")
        not_called_sum = 0
        for row in self.board:
            for elem in row:
                if elem >= 0:
                    not_called_sum += elem

        self.score = not_called_sum * last_number


def main():
    input_str = sys.stdin.read()
    input_deque = collections.deque(input_str.split("\n"))

    calls = list(map(int, input_deque.popleft().split(",")))

    boards: list[Board] = []

    while True:
        tail = input_deque.pop()
        if tail == "":
            continue
        else:
            input_deque.append(tail)
            break

    while input_deque:
        line = input_deque.popleft()
        if line == "":
            boards.append(Board())
            if 0:  # DEBUG == 1:
                print("board added", flush=True)
            continue

        if 0:  # DEBUG == 1:
            print("adding line", flush=True)
            print(line.split(" "))

        numbers = line.split(" ")
        while "" in numbers:
            numbers.remove("")

        boards[-1].fill_line(
            list(map(int, numbers))
        )

    if 0:  # DEBUG == 1:
        for board in boards:
            print(board.board)

    for call in calls:
        if DEBUG == 1:
            print(call)
        for board in boards:
            coord = board.call(call)
            if coord == (-1, -1):
                continue
            is_win = board.test_win(coord)
            if not is_win:
                continue
            board.calc_score(call)

    max_score = -1

    for i, board in enumerate(boards):
        if DEBUG == 1:
            print(f"Board {i} score {board.score}")
        if board.score > max_score:
            max_score = board.score
    print(max_score)


if __name__ == "__main__":
    main()
