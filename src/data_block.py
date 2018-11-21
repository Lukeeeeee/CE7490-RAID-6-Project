class DataBlock(object):
    """
    Abstraction for data block in the RAID 6
    """

    def __init__(self, data, disk=None):
        self.data = data
        self.disk = disk

    def assign_to_disk(self, disk):
        self.disk = disk
