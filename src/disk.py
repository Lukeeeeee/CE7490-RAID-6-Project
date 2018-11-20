import os
import sys
from src.util import *


class Disk(object):
    """
    Class to hold the entity of the disk, currently we use the naive way with a folder and a data file in the file
    system to represent the disk entity.
    """

    def __init__(self, disk_path, id, disk_size, disk_type='data', override_path=False):
        self.id = id
        self.disk_size = disk_size
        self.disk_type = disk_type
        self.disk_path = self.create_disk_folder(disk_path=os.path.join(disk_path, 'disk_%d' % id),
                                                 override_path=override_path)
        self.data_file_path = None

    def create_disk_folder(self, disk_path, override_path=False):
        if os.path.isdir(disk_path) and override_path is False:
            raise ValueError('Disk %s already existed' % disk_path)
        os.mkdir(disk_path)
        Logger.log_str(log_str=str('Disk %d is created at %s' % (self.id, disk_path)))
        return disk_path

    def load_file_from_disk(self):
        return None

    def detect_corruption(self):
        return False

    @staticmethod
    def write_to_disk(disk, data):
        with open(os.path.join(disk.disk_path, 'data'), 'wb') as f:
            f.write(data)
            disk.data_file_path = os.path.join(disk.disk_path, 'data')

    @staticmethod
    def read_from_disk(disk):
        with open(disk.data_file_path, 'r') as f:
            return f.read()
