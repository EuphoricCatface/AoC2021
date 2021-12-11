import sys


def main():
    aim = 0
    forward = 0
    depth = 0

    puzzle_input = sys.stdin.read()

    for line in puzzle_input.split("\n"):
        try:
            cmd, amount = line.split()
        except ValueError:
            print(f"Warning: line is not fit for parsing ({line})")
            continue
        amount = int(amount)

        if cmd == "forward":
            forward += amount
            depth += aim * amount
        # elif cmd == "backward":
        #     forward -= amount

        elif cmd == "up":
            aim -= amount
        elif cmd == "down":
            aim += amount

    print(forward * depth)


if __name__ == "__main__":
    main()
