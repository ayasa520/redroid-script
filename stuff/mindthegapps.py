import os
import shutil
from stuff.general import General
from tools.helper import get_download_dir, host, print_color, run, bcolors


class MindTheGapps(General):
    dl_links = {
        "14.0.0": {
            "x86_64": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240226/MindTheGapps-14.0.0-x86_64-20240226.zip",
                "a827a84ccb0cf5914756e8561257ed13",
            ],
            "x86": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240226/MindTheGapps-14.0.0-x86-20240226.zip",
                "45736b21475464e4a45196b9aa9d3b7f",
            ],
            "arm64": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240226/MindTheGapps-14.0.0-arm64-20240226.zip",
                "a0905cc7bf3f4f4f2e3f59a4e1fc789b",
            ],
            "arm": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240226/MindTheGapps-14.0.0-arm-20240226.zip",
                "fa167a3b7a10c4d3e688a59cd794f75b",
            ],
        },
        "13.0.0": {
            "x86_64": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240226/MindTheGapps-13.0.0-x86_64-20240226.zip",
                "eee87a540b6e778f3a114fff29e133aa",
            ],
            "x86": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240226/MindTheGapps-13.0.0-x86-20240226.zip",
                "d928c5eabb4394a97f2d7a5c663e7c2e",
            ],
            "arm64": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240226/MindTheGapps-13.0.0-arm64-20240226.zip",
                "ebdf35e17bc1c22337762fcf15cd6e97",
            ],
            "arm": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240619/MindTheGapps-13.0.0-arm-20240619.zip",
                "ec7aa5efc9e449b101bc2ee7448a49bf",
            ],
        },
        "13.0.0_64only": {
            "x86_64": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240226/MindTheGapps-13.0.0-x86_64-20240226.zip",
                "eee87a540b6e778f3a114fff29e133aa",
            ],
            "arm64": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240226/MindTheGapps-13.0.0-arm64-20240226.zip",
                "ebdf35e17bc1c22337762fcf15cd6e97",
            ],
        },
        "12.0.0_64only": {
            "x86_64": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240619/MindTheGapps-12.1.0-x86_64-20240619.zip",
                "05d6e99b6e6567e66d43774559b15fbd"
            ],
            "arm64": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240619/MindTheGapps-12.1.0-arm64-20240619.zip",
                "94dd174ff16c2f0006b66b25025efd04",
            ],
        },
        "12.0.0": {
            "x86_64": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240619/MindTheGapps-12.1.0-x86_64-20240619.zip",
                "05d6e99b6e6567e66d43774559b15fbd"
            ],
            "x86": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240619/MindTheGapps-12.1.0-x86-20240619.zip",
                "ff2421a75afbdda8a003e4fd25e95050"
            ],
            "arm64": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240619/MindTheGapps-12.1.0-arm64-20240619.zip",
                "94dd174ff16c2f0006b66b25025efd04",
            ],
            "arm": [
                "https://github.com/s1204IT/MindTheGappsBuilder/releases/download/20240619/MindTheGapps-12.1.0-arm-20240619.zip",
                "5af756b3b5776c2f6ee024a9f7f42a2f",
            ],
        },
    }

    arch = host()
    download_loc = get_download_dir()
    dl_file_name = os.path.join(download_loc, "mindthegapps.zip")
    dl_link = ...
    act_md5 = ...
    copy_dir = "./mindthegapps"
    extract_to = "/tmp/mindthegapps/extract"

    def __init__(self, version):
        self.version = version
        self.dl_link = self.dl_links[self.version][self.arch[0]][0]
        self.act_md5 = self.dl_links[self.version][self.arch[0]][1]

    def download(self):
        print_color("Downloading MindTheGapps now .....", bcolors.GREEN)
        super().download()

    def copy(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        if not os.path.exists(self.extract_to):
            os.makedirs(self.extract_to)

        shutil.copytree(
            os.path.join(self.extract_to, "system", ),
            os.path.join(self.copy_dir, "system"), dirs_exist_ok=True, )
