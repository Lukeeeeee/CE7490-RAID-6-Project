class RaidController(object):
    """
    Base class for different raid level controllers
    """
    def __init__(self, raid_level, disk_list):
        self.raid_level = raid_level
        self.disk_list = disk_list
        pass

    def write_file(self, *args, **kwargs):
        raise NotImplementedError

    def compute_parity(self, *args, **kwargs):
        raise NotImplementedError

    def check_corruption(self, *args, **kwargs):
        raise NotImplementedError

    def recover_disk(self, *args, **kwargs):
        raise NotImplementedError
