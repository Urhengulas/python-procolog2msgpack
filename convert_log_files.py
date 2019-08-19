import argparse
import logging

# from converter.converter import Converter
from procolog2msgpack.converter import Converter

logging.basicConfig(level=logging.INFO)


def convert(base_path: str):

    log_path = f"{base_path}/log/"

    conv = Converter(base_path=base_path)
    conv.convert_batch(
        base_path=log_path,
        file_type="log",
        cache=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=".")

    args = vars(parser.parse_args())
    base_path = args.get("path")

    convert(base_path)


if __name__ == "__main__":
    main()
