class RaidController(object):
    def __init__(self, raid_level, disk_list, file_path):
        self.raid_level = raid_level
        pass

    def read_file(self, *args, **kwargs):
        raise NotImplementedError

    def compute_parity(self, *args, **kwargs):
        raise NotImplementedError

    def check_corruption(self, *args, **kwargs):
        raise NotImplementedError

    def recover_disk(self, *args, **kwargs):
        raise NotImplementedError
