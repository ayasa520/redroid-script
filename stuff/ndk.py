import os
import shutil
from stuff.general import General
from tools.helper import bcolors, get_download_dir, print_color, run

class Ndk(General):
    download_loc = get_download_dir()
    copy_dir = "./ndk"
    dl_link = "https://github.com/supremegamers/vendor_google_proprietary_ndk_translation-prebuilt/archive/9324a8914b649b885dad6f2bfd14a67e5d1520bf.zip"
    dl_file_name = os.path.join(download_loc, "libndktranslation.zip")
    extract_to = "/tmp/libndkunpack"
    act_md5 = "c9572672d1045594448068079b34c350"
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
        shutil.copytree(os.path.join(self.extract_to, "vendor_google_proprietary_ndk_translation-prebuilt-9324a8914b649b885dad6f2bfd14a67e5d1520bf", "prebuilts"), os.path.join(self.copy_dir, "system"), dirs_exist_ok=True)

        init_path = os.path.join(self.copy_dir, "system", "etc", "init", "ndk_translation.rc")
        os.chmod(init_path, 0o644)
        # if not os.path.isfile(init_path):
        #     os.makedirs(os.path.dirname(init_path), exist_ok=True)
        # with open(init_path, "w") as initfile:
        #     initfile.write(self.init_rc_component)
