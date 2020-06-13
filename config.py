BUILD_TYPE = "Debug"
OUTPUT_FILE = "Firework.img"
SOURCES = [
    {
        "name": "Kernel",
        "git": "https://github.com/Firework-OS/Kernel.git",
        "cmd": f"make TARGET={BUILD_TYPE} OUTPUTDIR=../../build/Kernel -C ../sources/Kernel",
        "files": [
            {"src": "./Kernel/Kernel.elf", "dest": "/Firework/System/Kernel.elf"}
        ]
    },
    {
        "name": "qloader2",
        "git": "https://github.com/qloader2/qloader2.git",
        "cmd": "../sources/qloader2/qloader2-install ../sources/qloader2/qloader2.bin ./Firework.img"
    },
]
