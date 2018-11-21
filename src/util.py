# Date: 11/17/18
# Author: Luke
# Project: CE7490-RAID-6-Project
import logging
import config
import time
from log import LOG_PATH
import os

__all__ = ['Configuration', 'Logger']


class Configuration(object):
    def __init__(self):
        self.disk_count = 8
        self.data_disk_count = 6
        self.parity_disk_count = 2
        self.log_dir = os.path.join(LOG_PATH, time.strftime("%Y-%m-%d_%H-%M-%S"))
        while os.path.exists(self.log_dir):
            self.log_dir = os.path.join(LOG_PATH, time.strftime("%Y-%m-%d_%H-%M-%S"))
        os.mkdir(self.log_dir)
        os.mkdir(os.path.join(self.log_dir, 'disk'))
        self.disk_dir = os.path.join(self.log_dir, 'disk')
        Logger.log_str(log_str='Experiment log created at %s' % self.log_dir)
        assert self.data_disk_count + self.parity_disk_count == self.disk_count

        # Disk size means
        self.disk_size = 10
        self.logical_disk_size = self.disk_size * self.data_disk_count
        # Block size better set to be 4 * k
        self.block_size = 4
        self.block_num_per_chunk = 1
        self.chuck_size = self.block_size * self.block_num_per_chunk


class Logger(object):
    def __init__(self):
        pass

    @staticmethod
    def log_str(log_str):
        logging.info(log_str)
        print(log_str + '\n')
