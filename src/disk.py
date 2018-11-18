import os
import sys
from src.util import *


class Disk(object):
    """
    Class to hold the entity of the disk, currently we use the naive way with a folder and a data file in the file
    system to represent the disk entity.
    """

    def __init__(self, disk_path, id, disk_size, override_path=False):
        self.id = id
        self.disk_size = disk_size
        self.disk_path = self.create_disk_folder(disk_path=os.path.join(disk_path, 'disk_%d' % id),
                                                 override_path=override_path)

    def create_disk_folder(self, disk_path, override_path=False):
        if os.path.isdir(disk_path) and override_path is False:
            raise ValueError('Disk %s already existed' % disk_path)
        os.mkdir(disk_path)
        Logger.log_str(log_str=str('Disk %d is created at %s' % (self.id, disk_path)))
        return disk_path

    def write_file_to_disk(self, data):
        pass

    def load_file_from_disk(self):
        return None

    def detect_corruption(self):
        return False
