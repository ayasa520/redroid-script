

import os
import zipfile
import hashlib

from tools.helper import bcolors, download_file, print_color

class General:
    def download(self):
        loc_md5 = ""
        if os.path.isfile(self.dl_file_name):
            with open(self.dl_file_name,"rb") as f:
                bytes = f.read()
                loc_md5 = hashlib.md5(bytes).hexdigest()
        while not os.path.isfile(self.dl_file_name) or loc_md5 != self.act_md5:
            if os.path.isfile(self.dl_file_name):
                os.remove(self.dl_file_name)
                print_color("md5 mismatches, redownloading now ....",bcolors.YELLOW)
            loc_md5 = download_file(self.dl_link, self.dl_file_name)
        
    def extract(self):
        print_color("Extracting archive...", bcolors.GREEN)
        print(self.dl_file_name)
        print(self.extract_to)
        with zipfile.ZipFile(self.dl_file_name) as z:
            z.extractall(self.extract_to)
    def copy(self):
        pass
    def install(self):
        # pass
        self.download()
        self.extract()
        self.copy()
