import sys


def main():
    forward = 0
    down = 0

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
        elif cmd == "backward":
            forward -= amount

        elif cmd == "up":
            down -= amount
        elif cmd == "down":
            down += amount

    print(forward * down)


if __name__ == "__main__":
    main()
