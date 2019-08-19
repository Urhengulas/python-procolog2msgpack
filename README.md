# python-pocolog2msgpack
> Python wrapper around the docker container of [rock-core/tools-pocolog2msgpack](https://github.com/rock-core/tools-pocolog2msgpack)

**Table of content**
- [about](#about)
- [dependencies](#dependencies)
- [getting started](#getting-started)

## about
This project provides a python interface for the pocolog2msgpack tool, to convert Rock's pocolog format to MessagePack.

## dependencies
| dependencies | version |
| :----------- | :------ |
| python       | 3.5+    |
| docker       | 19.03+  |

## getting started

1. Install package from pip
	```shell
   	$ pip install pocolog2msgpack
   	```
1. Write own converter
	```python
	from pocolog2msgpack import Converter

	base_path = "data/"
	conv = Converter(base_path=base_path)
	```
    1. convert batch of files
    	* convert all `log`-files in `data/log/`
    	* resulting msg-files in same sub-dir, but under `data/msg`
		```python
		log_path = f"{base_path}/log/"
		
		conv.convert_batch(
			base_path=log_path,
			file_type="log",
			cache=True,
		)
		```
    1. convert single file
    	* convert file `data/log/poco.log`
    	* resulting msg-file in `data/msg/poco.msg`
		```python
		from pocolog2msgpack import X2YFile

		file = X2YFile(
			file_name="data/poco.log",
			file_type="log",
		)

		conv.convert(
			log_2_msg_file = file,
		)
		```
