import glob
import logging


def get_files(base_path: str, file_type: str, log: bool = False) -> list:
    """Returns the paths, relative to base_path, of all log-files inside base_path"""

    files = glob.glob(f"{base_path}/**/*.{file_type}", recursive=True)

    if log is True:
        logging.info(
            f"... found {len(files)} {file_type}-files in {base_path}"
        )

    return files


def split_last(string: str, separator: str) -> tuple:

    split_list = string.split(separator)

    return separator.join(split_list[:-1]), split_list[-1]
