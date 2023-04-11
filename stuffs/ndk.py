import os
import shutil
from stuffs.general import General
from tools.helper import bcolors, get_download_dir, print_color, run

class Ndk(General):
    download_loc = get_download_dir()
    copy_dir = "./ndk"
    dl_link = "https://github.com/supremegamers/vendor_google_proprietary_ndk_translation-prebuilt/archive/181d9290a69309511185c4417ba3d890b3caaaa8.zip"
    dl_file_name = os.path.join(download_loc, "libndktranslation.zip")
    extract_to = "/tmp/libndkunpack"
    act_md5 = "0beff55f312492f24d539569d84f5bfb"
#     init_rc_component = """
# # Enable native bridge for target executables
# on early-init
#     mount binfmt_misc binfmt_misc /proc/sys/fs/binfmt_misc

# on property:ro.enable.native.bridge.exec=1
#     copy /system/etc/binfmt_misc/arm_exe /proc/sys/fs/binfmt_misc/register
#     copy /system/etc/binfmt_misc/arm_dyn /proc/sys/fs/binfmt_misc/register
#     copy /system/etc/binfmt_misc/arm64_exe /proc/sys/fs/binfmt_misc/register
#     copy /system/etc/binfmt_misc/arm64_dyn /proc/sys/fs/binfmt_misc/register
# """
    
    def download(self):
        print_color("Downloading libndk now .....", bcolors.GREEN)
        super().download()

    def copy(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        run(["chmod", "+x", self.extract_to, "-R"])
    
        print_color("Copying libndk library files ...", bcolors.GREEN)
        shutil.copytree(os.path.join(self.extract_to, "vendor_google_proprietary_ndk_translation-prebuilt-181d9290a69309511185c4417ba3d890b3caaaa8", "prebuilts"), os.path.join(self.copy_dir, "system"), dirs_exist_ok=True)

        init_path = os.path.join(self.copy_dir, "system", "etc", "init", "ndk_translation.rc")
        os.chmod(init_path, 0o644)
        # if not os.path.isfile(init_path):
        #     os.makedirs(os.path.dirname(init_path), exist_ok=True)
        # with open(init_path, "w") as initfile:
        #     initfile.write(self.init_rc_component)
