import collections
import glob
import logging


def get_files(base_path: str, file_type: str, log: bool = False) -> list:
    """Returns the paths, relative to base_path, of all log-files inside base_path"""

    raw_files = glob.glob(f"{base_path}/**/*.{file_type}", recursive=True)
    files = ["/".join(f.split("/")[2:]) for f in raw_files]

    if log is True:
        logging.info(
            f"... found {len(files)} {file_type}-files in {base_path}"
        )

    return files


def get_new_extension(file_name: str, new_type: str) -> str:
    without_ext = ".".join(file_name.split(".")[:-1])
    with_new_ext = f"{without_ext}.{new_type}"

    return with_new_ext


def split_path_name(file_path: str) -> dict:

    path_list = file_path.split("/")
    file_dict = {
        "path": "/".join(path_list[:-1]),
        "name": "/".join(path_list[-1]),
        "full": file_path,
    }

    return file_dict


def process_file(file_path: str, new_extension: str = "") -> dict:

    file_dict = split_path_name(file_path)

    if new_extension != "":
        file_dict["old_name"] = file_dict.get("name")
        new_name = file_dict["name"] = get_new_extension(file_name)

        ret["full"] = f"{file_dict.get('path')}/{new_name}"

    return file_dict
