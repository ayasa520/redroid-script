import os
import re
import shutil
from stuff.general import General
from tools.helper import bcolors, get_download_dir, print_color, run


class Houdini(General):
    download_loc = get_download_dir()
    copy_dir = "./houdini"
    init_rc_component = """
on early-init
    mount binfmt_misc binfmt_misc /proc/sys/fs/binfmt_misc

on property:ro.enable.native.bridge.exec=1
    copy /system/etc/binfmt_misc/arm_exe /proc/sys/fs/binfmt_misc/register
    copy /system/etc/binfmt_misc/arm_dyn /proc/sys/fs/binfmt_misc/register

on property:ro.enable.native.bridge.exec64=1
    copy /system/etc/binfmt_misc/arm64_exe /proc/sys/fs/binfmt_misc/register
    copy /system/etc/binfmt_misc/arm64_dyn /proc/sys/fs/binfmt_misc/register

on property:sys.boot_completed=1
    exec -- /system/bin/sh -c "echo ':arm_exe:M::\\\\x7f\\\\x45\\\\x4c\\\\x46\\\\x01\\\\x01\\\\x01\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x02\\\\x00\\\\x28::/system/bin/houdini:P' >> /proc/sys/fs/binfmt_misc/register"
    exec -- /system/bin/sh -c "echo ':arm_dyn:M::\\\\x7f\\\\x45\\\\x4c\\\\x46\\\\x01\\\\x01\\\\x01\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x03\\\\x00\\\\x28::/system/bin/houdini:P' >> /proc/sys/fs/binfmt_misc/register"
    exec -- /system/bin/sh -c "echo ':arm64_exe:M::\\\\x7f\\\\x45\\\\x4c\\\\x46\\\\x02\\\\x01\\\\x01\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x02\\\\x00\\\\xb7::/system/bin/houdini64:P' >> /proc/sys/fs/binfmt_misc/register"
    exec -- /system/bin/sh -c "echo ':arm64_dyn:M::\\\\x7f\\\\x45\\\\x4c\\\\x46\\\\x02\\\\x01\\\\x01\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x03\\\\x00\\\\xb7::/system/bin/houdini64:P' >> /proc/sys/fs/binfmt_misc/register"
"""
    dl_links = {
        #  8.1.0 from cros R79 Android N not working
        # "8.1.0":[
        #     "https://github.com/rote66/vendor_intel_proprietary_houdini/archive/9246014ddf22d5e34f294d726dc48ca446b0e20e.zip",
        #     "b0a9ddc0d817d290a15b132091a37f36"],
        "8.1.0":[
            "https://github.com/rote66/vendor_intel_proprietary_houdini/archive/46682f423b8497db3f96222f2669d770eff764c3.zip",
            "cd4dd2891aa18e7699d33dcc3fe3ffd4"],
        "9.0.0":[
            "https://github.com/rote66/vendor_intel_proprietary_houdini/archive/46682f423b8497db3f96222f2669d770eff764c3.zip",
            "cd4dd2891aa18e7699d33dcc3fe3ffd4"],
        "11.0.0": [
            "https://github.com/supremegamers/vendor_intel_proprietary_houdini/archive/81f2a51ef539a35aead396ab7fce2adf89f46e88.zip",
            "fbff756612b4144797fbc99eadcb6653"],
        "12.0.0": [
            "https://github.com/supremegamers/vendor_intel_proprietary_houdini/archive/0e0164611d5fe5595229854759c30a9b5c1199a5.zip",
            "9709701b44b6ab7fc311c7dc95945bd0"],
        #  13.0.0 from wsa-13 not working
        # "13.0.0": [
        #     "https://github.com/supremegamers/vendor_intel_proprietary_houdini/archive/5460519aa63a23201ba0f3d45cfc382b2e9b30a0.zip",
        #     "08d8d8ed9c4b00eba3fa21ecd527eb87"],
        "13.0.0": [
            "https://github.com/rote66/vendor_intel_proprietary_houdini/archive/740353bf4391969902bc80ee2a9258db18481b45.zip",
            "d4824c0c00e8fa9611e1db5124ec61f9"],
        "14.0.0": [
            "https://github.com/rote66/vendor_intel_proprietary_houdini/archive/740353bf4391969902bc80ee2a9258db18481b45.zip",
            "d4824c0c00e8fa9611e1db5124ec61f9"]
        # "15.0.0": [
        #     "https://github.com/rote66/vendor_intel_proprietary_houdini/archive/740353bf4391969902bc80ee2a9258db18481b45.zip",
        #     "d4824c0c00e8fa9611e1db5124ec61f9"]
    }
    dl_file_name = os.path.join(download_loc, "libhoudini.zip")
    extract_to = "/tmp/houdiniunpack"

    def __init__(self, version):
        self.version = version
        if version in self.dl_links.keys():
            self.dl_link = self.dl_links[version][0]
            self.act_md5 = self.dl_links[version][1]
        else:
            raise ValueError(
                "No available libhoudini for Android {}".format(version))

    def download(self):
        print_color("Downloading libhoudini now .....", bcolors.GREEN)
        super().download()

    def copy(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        run(["chmod", "+x", self.extract_to, "-R"])

        print_color("Copying libhoudini library files ...", bcolors.GREEN)
        name = re.findall("([a-zA-Z0-9]+)\.zip", self.dl_link)[0]
        shutil.copytree(os.path.join(self.extract_to, "vendor_intel_proprietary_houdini-" + name,
                        "prebuilts"), os.path.join(self.copy_dir, "system"), dirs_exist_ok=True)

        init_path = os.path.join(self.copy_dir, "system", "etc", "init", "houdini.rc")
        if not os.path.isfile(init_path):
            os.makedirs(os.path.dirname(init_path), exist_ok=True)
        with open(init_path, "w") as initfile:
            initfile.write(self.init_rc_component)
        os.chmod(init_path, 0o644)
