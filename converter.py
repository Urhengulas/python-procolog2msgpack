import logging
import os

import docker

from converter.utilities import get_files, process_file

logging.basicConfig(level=logging.INFO)


class Converter():
    """Class to convert log- to msg-files"""

    client: docker.DockerClient = docker.from_env()
    image_name: str = "af01/pocolog2msgpack"

    def __init__(self, vol_name: str = "data/") -> None:
        logging.info("Init Converter")

        vol_dir = os.path.abspath(vol_name)

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

    def convert(self, file_name: str) -> None:
        logging.info(f"Start converting {file_name}")

        # TODO: think about solution to use e.g. base_path instead of hard-coded path-fragments

        p_file = process_file(file_name, new_extension="msg")

        log_file_path = f"./log/{p_file.full}"
        msg_file_path = f"./msg/{processed_file.get('')}"

        msg_file_name = extract_file_name(msg_file_path)
        msg_file_path = f"./test/{msg_file_name}"

        os.makedirs(f"./data/msg/{msg_file_path}", exist_ok=True)

        command = f"bash /opt/rock/run.sh -l {log_file_path} -o {msg_file_path}"
        logging.info(f"... CMD: {command}")

        ret = self.container.exec_run(
            cmd=command,
        )
        logging.info(f"... done (return code: {ret.exit_code})")
        logging.info(f"... output:\n{ret.output.decode('utf-8')}")

        return None

    def convert_batch(self, base_path: str, file_type: str, cache: bool = True) -> None:
        logging.info(f"Start converting {file_type}-files in {base_path}")
        log_files = get_files(
            base_path=base_path,
            file_type=file_type,
            log=True,
        )

        for file_name in log_files:
            if cache is True and self._msg_exists(file_name) is True:
                logging.info(f"... msg-file for {file_name} already exists")
                continue
            else:
                self.convert(file_name=file_name)

    def _msg_exists(self, file_name: str) -> bool:
        msg_files = get_files("data/msg/", file_type="msg")
        msg_file_path = get_new_extension(file_name, new_type="msg")

        if msg_file_path in msg_files:
            return True
        else:
            return False


def main() -> None:

    conv = Converter()
    conv.convert_batch(
        base_path="data/log/20161029_FLC_test",
        file_type="log",
        cache=False,
    )


if __name__ == "__main__":
    main()
