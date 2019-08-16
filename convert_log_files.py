import logging
import sys

from converter.converter import Converter

logging.basicConfig(level=logging.INFO)


def main():
    base_path = sys.argv[1]

    log_path = f"{base_path}/log/"

    conv = Converter(base_path=base_path)
    conv.convert_batch(
        base_path=log_path,
        file_type="log",
        cache=True,
    )


if __name__ == "__main__":
    main()
