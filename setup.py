import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pocolog2msgpack",
    version="0.1.1",
    description="""Python wrapper around procolog2msgpack,
    to convert rock-log- to msgpack-files""",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Johann Hemmann",
    author_email="johann.hemmann@dfki.de",
    project_urls={
            "Source Code": "https://github.com/Urhengulas/python-procolog2msgpack",
    },
    license="LGPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(
        exclude=("convert_log_files")
    ),
    include_package_data=True,
    install_requires=[
        "msgpack",
        "docker",
    ],
    python_reqires=">=3.5"
)
