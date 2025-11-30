import argparse

from app.cashfloh import main


def parse_args():
    parser = argparse.ArgumentParser(prog="cashfloh")
    parser.add_argument("categories", type=str)  # , nargs="+"
    parser.add_argument("rules", type=str)  # , nargs="+"
    parser.add_argument("inputpath", type=str)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.categories, args.rules, args.inputpath)
