import os
import re
import shutil
from stuffs.general import General
from tools.helper import bcolors, get_download_dir, host, print_color, run


class Widevine(General):
    def __init__(self, android_version) -> None:
        super().__init__()
        self.android_version = android_version
        self.dl_link = self.dl_links[self.machine[0]][android_version][0]
        self.act_md5 = self.dl_links[self.machine[0]][android_version][1]

    download_loc = get_download_dir()
    machine = host()
    copy_dir = "./widevine"
    dl_links = {
        # "x86": {
        #     "11.0.0": ["https://github.com/supremegamers/vendor_google_proprietary_widevine-prebuilt/archive/48d1076a570837be6cdce8252d5d143363e37cc1.zip",
        #                "f587b8859f9071da4bca6cea1b9bed6a"]
        # },
        "x86_64": {
            "11.0.0": ["https://github.com/supremegamers/vendor_google_proprietary_widevine-prebuilt/archive/48d1076a570837be6cdce8252d5d143363e37cc1.zip",
                       "f587b8859f9071da4bca6cea1b9bed6a"],
            "12.0.0": ["https://github.com/supremegamers/vendor_google_proprietary_widevine-prebuilt/archive/3bba8b6e9dd5ffad5b861310433f7e397e9366e8.zip",
                       "3e147bdeeb7691db4513d93cfa6beb23"],
            "13.0.0": ["https://github.com/supremegamers/vendor_google_proprietary_widevine-prebuilt/archive/a8524d608431573ef1c9313822d271f78728f9a6.zip",
                       "5c55df61da5c012b4e43746547ab730f"]
        },
        # "armeabi-v7a":
        # {
        #     "11.0.0": ["https://github.com/supremegamers/vendor_google_proprietary_widevine-prebuilt/archive/7b6e37ef0b63408f7d0232e67192020ba0aa402b.zip",
        #                "3c3a136dc926ae5fc07826359720dbab"]
        # },
        "arm64-v8a": {
            "11.0.0": ["https://github.com/supremegamers/vendor_google_proprietary_widevine-prebuilt/archive/a1a19361d36311bee042da8cf4ced798d2c76d98.zip",
                       "fed6898b5cfd2a908cb134df97802554"]
        }
    }
    dl_file_name = os.path.join(download_loc, "widevine.zip")
    extract_to = "/tmp/widevineunpack"

    def download(self):
        print_color("Downloading widevine now .....", bcolors.GREEN)
        super().download()

    def copy(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        run(["chmod", "+x", self.extract_to, "-R"])
        print_color("Copying widevine library files ...", bcolors.GREEN)
        name = re.findall("([a-zA-Z0-9]+)\.zip", self.dl_link)[0]
        shutil.copytree(os.path.join(self.extract_to, "vendor_google_proprietary_widevine-prebuilt-"+name,
                        "prebuilts"), os.path.join(self.copy_dir, "vendor"), dirs_exist_ok=True)

        if "x86" in self.machine[0] and self.android_version == "11.0.0":
            os.symlink("./libprotobuf-cpp-lite-3.9.1.so",
                       os.path.join(self.copy_dir, "vendor", "lib", "libprotobuf-cpp-lite.so"))
            os.symlink("./libprotobuf-cpp-lite-3.9.1.so", os.path.join(self.copy_dir,
                       "vendor", "lib64", "libprotobuf-cpp-lite.so"))

        for file in os.listdir(os.path.join(self.copy_dir, "vendor", "etc", "init")):
            if file.endswith('.rc'):
                os.chmod(os.path.join(self.copy_dir, "vendor", "etc", "init", file), 0o644)