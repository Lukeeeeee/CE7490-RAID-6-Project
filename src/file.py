import os
import sys
import glob
import numpy as np
import string
from src.util import Logger, Configuration


class File(object):
    """
    A class that represent a real file that need to be stored in the RAID 6 system.
    """

    def __init__(self):
        self._file_content = None

    @property
    def file_content(self):
        return np.array(self._file_content).tostring()

    @file_content.setter
    def file_content(self, val):
        self._file_content = val

    def random_generate_string(self, data_size):
        self.file_content = np.random.choice(list(string.ascii_letters), size=data_size)
        Logger.log_str(log_str='Random generate a string: {}'.format(self.file_content.decode('utf-8')))

    def read_from_path(self, data_path):
        pass

    @staticmethod
    def byte_to_string(bytes_data):
        assert isinstance(bytes_data, bytes)
        return str(bytes_data.decode('utf-8'))
