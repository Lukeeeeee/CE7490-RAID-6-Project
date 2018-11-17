# Date: 11/17/18
# Author: Luke
# Project: CE7490-RAID-6-Project

from src.raid.raid_controller import RaidController


class RAID_6(RaidController):
    def __init__(self, raid_level, disk_list, file_path, config):
        super().__init__(raid_level, disk_list, file_path)
        self.config = config

    def read_file(self):
        pass

    def compute_parity(self):
        pass

    def check_corruption(self):
        pass

    def recover_disk(self):
        pass
