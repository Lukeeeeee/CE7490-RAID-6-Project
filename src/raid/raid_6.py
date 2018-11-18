# Date: 11/17/18
# Author: Luke
# Project: CE7490-RAID-6-Project

from src.raid.raid_controller import RaidController
from src.disk import Disk
from src.file import File


class RAID_6(RaidController):
    def __init__(self, disk_list, file_path, config):
        super().__init__(6, disk_list, file_path)
        self.config = config
        assert self.raid_level == 6

    def read_file(self, file):
        pass

    def compute_parity(self):
        pass

    def check_corruption(self):
        pass

    def recover_disk(self):
        pass
