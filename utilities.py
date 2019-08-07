import glob
import logging


def get_files(base_path: str, file_type: str, log: bool = False) -> list:
    """Returns the paths, relative to base_path, of all log-files inside base_path"""

    raw_files = glob.glob(f"{base_path}/**/*.{file_type}", recursive=True)
    files = ["/".join(f.split("/")[2:]) for f in raw_files]

    if log is True:
        logging.info(f"... found {len(files)} {file_type}-files")

    return files


def get_msg_file_name(file_name: str) -> bool:
    return f"{file_name.split('/')[-1].split('.')[0]}.msg"
