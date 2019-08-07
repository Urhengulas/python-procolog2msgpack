import glob
import logging
import os

import docker

logging.basicConfig(level=logging.INFO)


class Converter():
    client = client = docker.from_env()
    image_name = "af01/pocolog2msgpack"

    def __init__(self):
        logging.info("Init Converter")

    def convert(self, file_name: str, vol_name: str = "data/", cache: bool = True) -> None:
        logging.info(f"Start converting {file_name}")

        if cache is True and msg_exists(file_name) is True:
            return
        else:
            self._convert_to_msg(file_name, vol_name)

    def _convert_to_msg(self, file_name: str, vol_name: str = "data/") -> None:

        vol_dir = self._get_vol_dir(vol_name)
        msg_file_name = self.get_msg_file_name(file_name)

        command = f"-l ./log/{file_name} -o ./msg/{msg_file_name}"
        logging.debug(f"... CMD: {command}")

        self.client.containers.run(
            image=self.image_name,
            command=command,
            volumes={
                vol_dir: {
                    "bind": "/rdp",
                    "mode": "rw",
                },
            },
            working_dir="/rdp",
            remove=True,
        )
        logging.info(f"... done")

    def _get_vol_dir(self, vol: str) -> str:
        pwd = os.getcwd()
        vol_dir = f"{pwd}/{vol}"

        logging.debug(f"... volume directory: {vol_dir}")

        return vol_dir

    def get_msg_file_name(self, file_name: str) -> bool:
        return f"{file_name.split('/')[-1].split('.')[0]}.msg"

    def msg_exists(self, file_name: str) -> bool:
        msg_files = get_files("data/msg/", file_type="msg")
        msg_file_name = self.get_msg_file_name(file_name)

        logging.info(f"file_name: {msg_file_name}\nfiles: {msg_files}")

        if msg_file_name in msg_files:
            logging.info(f"... msg-file {msg_file_name} already exists")
            return True
        else:
            return False


def get_files(base_path: str, file_type: str, log: bool = False) -> list:
    """Returns the paths, relative to base_path, of all log-files inside base_path"""

    raw_files = glob.glob(f"{base_path}/**/*.{file_type}", recursive=True)
    files = ["/".join(f.split("/")[2:]) for f in raw_files]

    if log is True:
        logging.info(f"... found {len(files)} {file_type}-files")

    return files


def main() -> None:

    conv = Converter()

    log_files = get_files(base_path="data/log/", file_type="log", log=True)

    for file_name in log_files:
        conv.convert(
            file_name=file_name,
            cache=False,
        )


if __name__ == "__main__":
    main()
