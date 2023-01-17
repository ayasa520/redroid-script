import os
import shutil
from stuffs.general import General
from tools.helper import bcolors, get_download_dir, print_color, run


class Widevine(General):
    download_loc = get_download_dir()
    vendor_image_mount = "./widevine"
    dl_link = "https://codeload.github.com/supremegamers/vendor_google_proprietary_widevine-prebuilt/zip/94c9ee172e3d78fecc81863f50a59e3646f7a2bd"
    dl_file_name = os.path.join(download_loc, "widevine.zip")
    extract_to = "/tmp/widevineunpack"
    act_md5 = "a31f325453c5d239c21ecab8cfdbd878"

    def download(self):
        print_color("Downloading widevine now .....", bcolors.GREEN)
        super().download()

    def copy(self):
        run(["chmod", "+x", self.extract_to, "-R"])
        print_color("Copying widevine library files ...", bcolors.GREEN)
        shutil.copytree(os.path.join(self.extract_to, "vendor_google_proprietary_widevine-prebuilt-94c9ee172e3d78fecc81863f50a59e3646f7a2bd",
                        "prebuilts"), os.path.join(self.vendor_image_mount, "vendor"), dirs_exist_ok=True)
