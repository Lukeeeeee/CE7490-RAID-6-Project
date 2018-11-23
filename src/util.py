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

        assert self.block_size % 4 == 0

        self.block_num_per_chunk = 2
        self.chuck_size = self.block_size * self.block_num_per_chunk
        self.char_order_for_zero = 300

        logging.basicConfig(level=logging.DEBUG,
                            filename=self.log_dir + '/test.log',
                            filemode='w')

    def log_out(self):
        Logger.log_str("Disk count is %d" % self.disk_count)
        Logger.log_str("Data disk count is %d" % self.data_disk_count)
        Logger.log_str("Parity disk count is %d" % self.parity_disk_count)
        Logger.log_str("Logical disk size is %d" % self.logical_disk_size)
        Logger.log_str("RAID 6 Disk size is %d" % self.disk_size)
        Logger.log_str("Block size is %d" % self.block_size)
        Logger.log_str("Block number per chunk is %d" % self.block_num_per_chunk)


class Logger(object):
    def __init__(self):
        pass

    @staticmethod
    def log_str(log_str, mode='info'):
        logger = logging.getLogger('RAID-6 log')
        if mode == 'info':
            logger.info(log_str)
        if mode == 'error':
            logger.error(log_str)
        print(log_str + '\n')
