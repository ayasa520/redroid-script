import os
import shutil
from stuffs.general import General
from tools.helper import get_download_dir, host, print_color, run, bcolors

class LiteGapps(General):
    # https://master.dl.sourceforge.net/project/litegapps/litegapps/x86_64/33/lite/2024-02-24/AUTO-LiteGapps-x86_64-13.0-20240224-official.zip?viasf=1
    dl_link_fmt = "https://master.dl.sourceforge.net/project/litegapps/litegapps/{0}/{1}/lite/2024-02-24/AUTO-LiteGapps-{0}-{2}-20240224-official.zip"
    api_level_map = {
        "15.0.0": "35",
        "14.0.0": "34",
        "13.0.0": "33",
        "12.0.0": "31",
        "11.0.0": "30",
        "10.0.0": "29",
        "9.0.0": "28",
        "8.1.0": "27",
        "8.0.0": "26",
        "7.1.2": "25",
        "7.1.1": "25",
        "7.1.0": "25",
        "7.0.0": "24",
    }
    arch = host()
    download_loc = get_download_dir()
    dl_file_name = os.path.join(download_loc, "litegapps.zip")
    act_md5 = ""
    copy_dir = "./litegapps"
    extract_to = "/tmp/litegapps/extract"

    def __init__(self, version):
        self.version = version
        self.dl_link = self.dl_link_fmt.format(self.arch[0], self.api_level_map[self.version], '.'.join(self.version.split('.')[:2]))

    def download(self):
        print_color("Downloading LiteGapps now .....", bcolors.GREEN)
        super().download()
    
    def copy(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        if not os.path.exists(self.extract_to):
            os.makedirs(self.extract_to)
        if not os.path.exists(os.path.join(self.extract_to, "appunpack")):
            os.makedirs(os.path.join(self.extract_to, "appunpack"))

        # extract extract_to/files/files.tar.xz file to extract_to/appunpack
        run(["tar", "-xvf", os.path.join(self.extract_to, "files", "files.tar.xz"), "-C", os.path.join(self.extract_to, "appunpack")])
        shutil.copytree(os.path.join(self.extract_to, "appunpack", self.arch[0], self.api_level_map[self.version], "system"), os.path.join(self.copy_dir, "system"), dirs_exist_ok=True)