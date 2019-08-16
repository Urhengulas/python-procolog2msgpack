# python-procolog2msgpack
> Python wrapper around the docker container of [rock-core/tools-pocolog2msgpack](https://github.com/rock-core/tools-pocolog2msgpack)

**Table of content**
- [dependencies](#dependencies)
- [getting started](#getting-started)

## dependencies
| dependencie | version      |
| :---------- | :----------- |
| python      | >=3.7        |
| pipenv      | >=2018.11.28 |
| docker      | >=19.03      |

## getting started

1. install dependencies
   ```shell
   $ make dep
   ```
1. convert log-files
   ```python
   # convert files in data/log/
   $ make run
   ```
   **OR**
   ```python
   # convert files in <parent_dir_of_log-dir>/log/
   $ pipenv run python convert_log_files.py --path <parent_dir_of_log-dir>
   ```

