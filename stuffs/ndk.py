import os
import shutil
from stuffs.general import General
from tools.helper import bcolors, get_download_dir, print_color, run

class Ndk(General):
    download_loc = get_download_dir()
    sys_image_mount = "./ndk"
    dl_link = "https://www.dropbox.com/s/eaf4dj3novwiccp/libndk_translation_Module-c6077f3398172c64f55aad7aab0e55fad9110cf3.zip?dl=1"
    dl_file_name = os.path.join(download_loc, "libndktranslation.zip")
    extract_to = "/tmp/libndkunpack"
    act_md5 = "4456fc1002dc78e544e8d9721bb24398"
    init_rc_component = """
# Enable native bridge for target executables
on early-init
    mount binfmt_misc binfmt_misc /proc/sys/fs/binfmt_misc

on property:ro.enable.native.bridge.exec=1
    copy /system/etc/binfmt_misc/arm_exe /proc/sys/fs/binfmt_misc/register
    copy /system/etc/binfmt_misc/arm_dyn /proc/sys/fs/binfmt_misc/register
    copy /system/etc/binfmt_misc/arm64_exe /proc/sys/fs/binfmt_misc/register
    copy /system/etc/binfmt_misc/arm64_dyn /proc/sys/fs/binfmt_misc/register
"""
    
    def download(self):
        print_color("Downloading libndk now .....", bcolors.GREEN)
        super().download()

    def copy(self):
        run(["chmod", "+x", self.extract_to, "-R"])
    
        print_color("Copying libndk library files ...", bcolors.GREEN)
        shutil.copytree(os.path.join(self.extract_to, "libndk_translation_Module-c6077f3398172c64f55aad7aab0e55fad9110cf3", "system"), os.path.join(self.sys_image_mount, "system"), dirs_exist_ok=True)

        init_path = os.path.join(self.sys_image_mount, "system", "etc", "init", "libndk.rc")
        if not os.path.isfile(init_path):
            os.makedirs(os.path.dirname(init_path), exist_ok=True)
        with open(init_path, "w") as initfile:
            initfile.write(self.init_rc_component)
