import gzip
import os
import shutil
import re
from stuff.general import General
from tools.helper import bcolors, download_file, host, print_color, run, get_download_dir

class Magisk(General):
    download_loc = get_download_dir()
    dl_link = "https://github.com/ayasa520/Magisk/releases/download/debug-7be6d81-30200/Magisk-7be6d81-30200-debug.apk"
    dl_file_name = os.path.join(download_loc, "magisk.apk")
    act_md5 = "834b0f063ea713bea48b92c7d5648ce9"
    extract_to = "/tmp/magisk_unpack"
    copy_dir = "./magisk"
    magisk_dir = os.path.join(copy_dir, "system", "etc", "init", "magisk")
    machine = host()
    oringinal_bootanim = """
service bootanim /system/bin/bootanimation
    class core animation
    user graphics
    group graphics audio
    disabled
    oneshot
    ioprio rt 0
    task_profiles MaxPerformance
    
"""
    bootanim_component = """
on post-fs-data
    start logd
    exec u:r:su:s0 root root -- {MAGISKSYSTEMDIR}/magiskpolicy --live --magisk
    exec u:r:magisk:s0 root root -- {MAGISKSYSTEMDIR}/magiskpolicy --live --magisk
    exec u:r:update_engine:s0 root root -- {MAGISKSYSTEMDIR}/magiskpolicy --live --magisk
    exec u:r:su:s0 root root -- {MAGISKSYSTEMDIR}/{magisk_name} --auto-selinux --setup-sbin {MAGISKSYSTEMDIR} {MAGISKTMP}
    exec u:r:su:s0 root root -- {MAGISKTMP}/magisk --auto-selinux --post-fs-data
on nonencrypted
    exec u:r:su:s0 root root -- {MAGISKTMP}/magisk --auto-selinux --service
on property:vold.decrypt=trigger_restart_framework
    exec u:r:su:s0 root root -- {MAGISKTMP}/magisk --auto-selinux --service
on property:sys.boot_completed=1
    mkdir /data/adb/magisk 755
    exec u:r:su:s0 root root -- {MAGISKTMP}/magisk --auto-selinux --boot-complete
    exec -- /system/bin/sh -c "if [ ! -e /data/data/io.github.huskydg.magisk ] ; then pm install /system/etc/init/magisk/magisk.apk ; fi"
   
on property:init.svc.zygote=restarting
    exec u:r:su:s0 root root -- {MAGISKTMP}/magisk --auto-selinux --zygote-restart
   
on property:init.svc.zygote=stopped
    exec u:r:su:s0 root root -- {MAGISKTMP}/magisk --auto-selinux --zygote-restart
    """.format(MAGISKSYSTEMDIR="/system/etc/init/magisk", MAGISKTMP="/sbin", magisk_name="magisk")

    def download(self):
        print_color("Downloading latest Magisk-Delta now .....", bcolors.GREEN)
        super().download()   

    def copy(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        if not os.path.exists(self.magisk_dir):
            os.makedirs(self.magisk_dir, exist_ok=True)

        if not os.path.exists(os.path.join(self.copy_dir, "sbin")):
            os.makedirs(os.path.join(self.copy_dir, "sbin"), exist_ok=True)

        print_color("Copying magisk libs now ...", bcolors.GREEN)
        
        arch_map = {
            "x86": "x86",
            "x86_64": "x86_64",
            "arm": "armeabi-v7a",
            "arm64": "arm64-v8a"
        }
        lib_dir = os.path.join(self.extract_to, "lib", arch_map[self.machine[0]])
        for parent, dirnames, filenames in os.walk(lib_dir):
            for filename in filenames:
                o_path = os.path.join(lib_dir, filename)  
                filename = re.search('lib(.*)\.so', filename)
                n_path = os.path.join(self.magisk_dir, filename.group(1))
                shutil.copyfile(o_path, n_path)
                run(["chmod", "+x", n_path])
        shutil.copyfile(self.dl_file_name, os.path.join(self.magisk_dir,"magisk.apk") )

        # Updating Magisk from Magisk manager will modify bootanim.rc, 
        # So it is necessary to backup the original bootanim.rc.
        bootanim_path = os.path.join(self.copy_dir, "system", "etc", "init", "bootanim.rc")
        gz_filename = os.path.join(bootanim_path)+".gz"
        with gzip.open(gz_filename,'wb') as f_gz:
            f_gz.write(self.oringinal_bootanim.encode('utf-8'))
        with open(bootanim_path, "w") as initfile:
            initfile.write(self.oringinal_bootanim+self.bootanim_component)

        os.chmod(bootanim_path, 0o644)
