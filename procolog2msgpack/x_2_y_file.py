from dataclasses import dataclass

from .utilities import get_files, split_last


@dataclass()
class X2YFile():
    """Class to enable handling of filename properties

    Attributes
    ---
    base_path: str
        entry path until beginning of file_type-dir
    dir_path: str
        path following `base_path` to the file_type-dir of the file
    file: str
        name of the file, without type/extension
    """

    base_path: str
    dir_path: str
    file: str

    __slots__ = ["base_path", "dir_path", "file"]

    def __init__(self, file_name: str, file_type: str):

        base_path, file_path = split_last(file_name, f"/{file_type}/")
        dir_path, name = split_last(file_path, "/")
        file, _ = split_last(name, ".")

        self.base_path = base_path
        self.dir_path = dir_path
        self.file = file

    def get_file_name(self, file_type: str) -> str:

        return f"{self.file}.{file_type}"

    def get_file_path(self, file_type: str, full: bool = False) -> str:

        file_path_list = [
            self.get_dir_path(file_type=file_type, full=full),
            self.get_file_name(file_type=file_type),
        ]

        return "/".join(file_path_list)

    def get_dir_path(self, file_type: str, full: bool = False) -> str:

        dir_path_list = [
            file_type,
            self.dir_path,
        ]

        if full is True:
            dir_path_list.insert(0, self.base_path)

        return "/".join(dir_path_list)

    def file_exists(self, file_type: str):

        type_path = f"{self.base_path}/{file_type}/"

        msg_files = get_files(type_path, file_type=file_type)
        msg_file_path = self.get_file_path(file_type=file_type, full=True)

        if msg_file_path in msg_files:
            return True
        else:
            return False
