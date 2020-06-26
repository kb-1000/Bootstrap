# Bootstrap
The Python script that bundles a Firework image

## Instructions

### Installing dependencies

This tool uses [Python Poetry](https://python-poetry.org/) as its dependency manager, please install it before continuing!


Go to the root of this repo and run `poetry update` to install the dependencies for the script itself.


To build the projects you'll need to install the following:

* [LLD](https://lld.llvm.org/)
* [Clang](https://clang.llvm.org/)
* [Netwide Assembler](https://www.nasm.us)
* [Make](https://www.gnu.org/software/make/)
* [echfs](https://github.com/qword-os/echfs)

In a debian based distro, you can install _**some**_ of them like this: `sudo apt install build-essential clang lld nasm make python3 python3-pip python3-venv curl fuse libfuse-dev pkg-config`


### Configuration

Edit things in the `config.py` to personalize your Firework distribution.

### Running
In the root of the project run `poetry run python3 fwstrap.py`


Afterwards, if the build is successfull, a file called `OUTPUT_NAME (in your config)` will be created in the `build` older
