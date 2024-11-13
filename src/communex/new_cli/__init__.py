import sys

def main(args: list[str]) -> int:
    return 0

def entrypoint() -> int:
    args = sys.argv[1:]

    return main(args)

if __name__ == '__main__':
    entrypoint()
