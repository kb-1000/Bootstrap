import config
import subprocess
from termcolor import colored
import pathlib
import os
import traceback

pathlib.Path("./build").mkdir(exist_ok=True)
pathlib.Path("./sources").mkdir(exist_ok=True)

output = f"./build/{config.OUTPUT_FILE}"

if os.path.exists(output):
    os.remove(output)

print(f"\n{colored('==>', 'blue')} Creating image file:\n")
subprocess.call(["dd", "if=/dev/zero", "bs=1M", "count=0",
                 "seek=10", f"of={output}", "status=progress", "oflag=sync"])
print(f"{colored('==>', 'blue')} Creating MBR.")
subprocess.call(["parted", "-s", output, "mklabel", "msdos"])
print(f"{colored('==>', 'blue')} Creating partition.")
subprocess.call(["parted", "-s", output, "mkpart", "primary", "1", "100%"])
print(f"{colored('==>', 'blue')} Formatting in format echfs.")
subprocess.call(["echfs-utils", "-m", "-p0", output, "quick-format", "32768"])
print(f"{colored('==>', 'blue')} Adding qloader2 config file.")
subprocess.call(["echfs-utils", "-m", "-p0", output,
                 "import", "./qloader2.cfg", "qloader2.cfg"])

for source in config.SOURCES:
    git = source["git"]
    name = source["name"]

    if not os.path.exists(f"./sources/{name}"):
        print(f"\n{colored('==>', 'blue')} Cloning source '{name}'\n")
        exit_code = subprocess.call(["git", "clone", git, f"./sources/{name}"])

        if exit_code != 0:
            print(f"\n{colored('E:', 'red')} Git exited with non-zero exit code.\n")
            exit(exit_code)
    else:
        print(
            f"\n{colored('==>', 'blue')} Pulling latest changes for source '{name}':\n")
        os.chdir(f"./sources/{name}")
        exit_code = subprocess.call(["git", "pull"])

        if exit_code != 0:
            print(
                f"\n{colored('W:', 'yellow')} Git exited with non-zero exit code.\n")

        os.chdir("../../")

    os.chdir("./build")

    cmd = source.get("cmd")

    if cmd:
        print(
            f"\n{colored('==>', 'blue')} Calling build command for source '{name}':\n")
        exit_code = subprocess.call(cmd.split())

        if exit_code != 0:
            print(
                f"\n{colored('E:', 'red')} The build command for source '{name}' failed.\n")
            exit(exit_code)
    else:
        print(f"\n{colored('W:', 'yellow')} No command for source '{name}'.\n")

    files = source.get("files")

    if files:
        print(f"\n{colored('==>', 'blue')} Copying files for source '{name}':\n")

        for file in files:
            src = file["src"]
            dest = file["dest"]

            print(f"{src} {colored('==>', 'blue')} {dest}")
            exit_code = subprocess.call(["echfs-utils", "-m", "-p0",
                                         f"../{output}", "import", src, dest])

            if exit_code != 0:
                print(
                    f"\n{colored('E:', 'red')} Copying files from build source '{name}' failed.\n")
                exit(exit_code)

    os.chdir("..")

print(f"\n{colored('==>', 'green')} Done!\n")
