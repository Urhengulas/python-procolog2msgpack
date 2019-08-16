import logging
import os

import docker

from .utilities import get_files
from .x_2_y_file import X2YFile

logging.basicConfig(level=logging.INFO)


class Converter():
    """Class to convert log- to msg-files"""

    client: docker.DockerClient = docker.from_env()
    image_name: str = "af01/pocolog2msgpack"

    def __init__(self, base_path: str) -> None:
        logging.info("Init Converter")

        vol_dir = os.path.abspath(base_path)

        self.container = cont = self.client.containers.run(
            image=self.image_name,
            entrypoint="sleep",
            command="infinity",
            volumes={
                vol_dir: {
                    "bind": "/rdp",
                    "mode": "rw",
                },
            },
            working_dir="/rdp",
            remove=True,
            detach=True,
        )
        logging.info(f"... done ({cont})")

    def __del__(self) -> None:
        logging.info(f"Stop and remove Converter ({self.container})")

        # only STOP is needed, since REMOVE is done by container automatically
        self.container.stop(timeout=10)
        logging.info("... done.")

    def convert(self, log_2_msg_file: X2YFile) -> None:
        logging.info(f"... Convert {log_2_msg_file}")

        os.makedirs(
            log_2_msg_file.get_dir_path(file_type="msg", full=True),
            exist_ok=True
        )

        log_file_path = log_2_msg_file.get_file_path(file_type="log")
        msg_file_path = log_2_msg_file.get_file_path(file_type="msg")

        command = f"bash /opt/rock/run.sh -l {log_file_path} -o {msg_file_path}"
        logging.debug(f"... ... CMD: {command}")

        ret = self.container.exec_run(
            cmd=command,
        )
        logging.info(f"... ... done (return code: {ret.exit_code})")
        logging.debug(f"... ... output:\n{ret.output.decode('utf-8')}")

        return None

    def convert_batch(self, base_path: str, file_type: str, cache: bool = True) -> None:
        logging.info(f"Start converting {file_type}-files in {base_path}")
        log_files = get_files(
            base_path=base_path,
            file_type=file_type,
            log=True,
        )
        logging.debug(f"... files: {log_files}")

        for file_name in log_files:
            log_2_msg_file = X2YFile(file_name=file_name, file_type=file_type)

            if cache is True:

                file_exists = log_2_msg_file.file_exists(file_type="msg")
                if file_exists is True:
                    logging.info(
                        f"... msg-file for {log_2_msg_file} already exists")
                    continue

            self.convert(log_2_msg_file)

        logging.info("... done converting")


def main() -> None:

    base_path = "data"
    log_path = f"{base_path}/log/"

    conv = Converter(base_path=base_path)
    conv.convert_batch(
        base_path=log_path,
        file_type="log",
        cache=True,
    )


if __name__ == "__main__":
    main()
