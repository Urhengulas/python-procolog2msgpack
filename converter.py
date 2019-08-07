import logging
import os

import docker

from converter.utilities import get_files, get_msg_file_name

logging.basicConfig(level=logging.INFO)


class Converter():
    client: docker.DockerClient = docker.from_env()
    image_name: str = "af01/pocolog2msgpack"

    def __init__(self) -> None:
        logging.info("Init Converter")

    def convert(self, file_name: str, vol_name: str = "data/") -> None:
        logging.info(f"Start converting {file_name}")

        vol_dir = os.path.abspath(vol_name)
        msg_file_name = get_msg_file_name(file_name)

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


class BatchConverter():
    conv: Converter = Converter()

    def __init__(self, base_path: str, file_type: str) -> None:
        self.log_files = get_files(
            base_path=base_path,
            file_type=file_type,
            log=True,
        )

        logging.info("Init BatchConverter")

    def convert(self, vol_name: str = "data/", cache: bool = False) -> None:

        for file_name in self.log_files:
            if cache is True and self.msg_exists(file_name) is True:
                logging.info(f"msg-file {msg_file_name} already exists")
                continue
            else:
                self.conv.convert(
                    file_name=file_name,
                    vol_name=vol_name,
                )

    def msg_exists(self, file_name: str) -> bool:
        msg_files = get_files("data/msg/", file_type="msg")
        msg_file_name = get_msg_file_name(file_name)

        if msg_file_name in msg_files:
            return True
        else:
            return False


def main() -> None:

    conv = BatchConverter(base_path="data/log/", file_type="log")
    conv.convert()


if __name__ == "__main__":
    main()
