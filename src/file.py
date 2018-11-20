import os
import sys
import glob


class File(object):
    """
    A class that represent a real file that need to be stored in the RAID 6 system.
    """
    def __init__(self):
        self.file_content = None

    def random_generate(self, data_size):
        pass

    def read_from_path(self, data_path):
        pass
