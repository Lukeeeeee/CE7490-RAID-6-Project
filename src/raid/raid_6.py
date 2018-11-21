# Date: 11/17/18
# Author: Luke
# Project: CE7490-RAID-6-Project

from src.raid.raid_controller import RaidController
from src.disk import Disk
from src.galois_field import GaloisField
import numpy as np
import functools
import os
import concurrent.futures


class RAID_6(RaidController):
    def __init__(self, disk_list, config, gf=None):
        super().__init__(6, disk_list)
        self.config = config
        assert self.raid_level == 6
        if not gf:
            self.gf = GaloisField(num_data_disk=self.config.data_disk_count,
                                  num_checksum=self.config.parity_disk_count)
        else:
            self.gf = gf
        self.encode_matrix = self._generate_encode_matrix(identity_num=self.config.data_disk_count,
                                                          check_sum_matrix=self.gf.vandermond)

    def write_file(self, data_block_list):
        """
        Write the file to the disks concurrently, firstly computing the parity and concurrently write to all the disks
        :param file_content:
        :return: None
        """
        data = self._split_block_into_data_disks(data_disks_n=self.config.data_disk_count,
                                                 data_block=data_block_list,
                                                 block_count_per_chunk=self.config.block_num_per_chunk)
        data_with_parity = np.concatenate([data, self.compute_parity(data=data)], axis=0)

        # We use parallel writing operation to write the file into disks

        # with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.disk_count) as executor:
        #     executor.map(Disk.write_to_disk,
        #                  self.disk_list,
        #                  data_with_parity.tolist())
        for disk, data in zip(self.disk_list, data_with_parity.tolist()):
            disk.write_to_disk(disk=disk, data="".join(val for val in data), mode='w')

    def read_all_data_disks(self, excluded_list=None):
        """
        Read the disks concurrently to a numpy array.
        :return: Data from all the disks
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.disk_count) as executor:
            res = np.array(executor.map(Disk.read_from_disk, self.disk_list))

        non_padding_length = min(np.count_nonzero(np.array(res), axis=1))
        non_padding_res = np.array([res[i][0:non_padding_length] for i in range(res.shape[0])])
        return non_padding_res

    def compute_parity(self, data):
        res = self.gf.gen_parity(data=data)
        return res


    def check_corruption(self):
        """
        Detect if single disk occurred silent corruption.
        :return: A boolean, True for failed, False for not.
        """
        pass

    def recover_disk(self):
        pass

    def update_data(self):
        # TODO
        pass

    def _gaussian_elimination(self, corrupted_disk_index):
        """
        Function to recover the disks using the gaussian elimination method
        :param corrupted_disk_index: the disks' index list that were corrupted which should be less than m
        :return: recovered data disks content
        """
        # matrix_a_new, vector_e_new = self.gf.recover_matrix(mat_A=)

    def _generate_encode_matrix(self, identity_num, check_sum_matrix):
        # check_sum_matrix = np.asarray(check_sum_matrix)
        # assert check_sum_matrix.shape[0] == self.config.parity_disk_count
        # assert check_sum_matrix.shape[1] == self.config.data_disk_count
        #
        # encode_matrix = np.zeros([identity_num, self.config.data_disk_count])
        # for i in range(self.config.data_disk_count):
        #     encode_matrix[i][i] = 1
        # encode_matrix = np.concatenate([encode_matrix, check_sum_matrix], axis=1)
        # return encode_matrix
        return self.gf.gen_matrix_A()

    def _split_block_into_data_disks(self, data_disks_n, data_block, block_count_per_chunk):
        """
        Split the data block from logical disk into raid data disks
        :param data_disks_n: total number of data disks in raid 6
        :param data_block: data blocks from logical disk that will be stripped into raid 6
        :param block_count_per_chunk: assign how many data blocks to one data disk before moving to the next
        :return:
        """
        disk_index = 0
        data_disk_list = [[] for _ in range(data_disks_n)]
        data_block_per_disk = len(data_block) / data_disks_n

        for i, block_i in enumerate(data_block):
            data_disk_list[disk_index].append(self._str_to_order(block_i) if isinstance(block_i, str) else block_i)
            if (i + 1) % block_count_per_chunk == 0:
                disk_index = (disk_index + 1) % data_disks_n

        padding_block = self.generate_padding_block(byte_length=len(data_block[0]))
        assert len(padding_block) == len(data_block[0])
        assert isinstance(padding_block, type(data_block[0]))
        if disk_index != 0:
            for index in range(disk_index, data_disks_n):
                for _ in range(block_count_per_chunk):
                    data_disk_list[index].append(padding_block)
        for data in data_disk_list:
            assert len(data) == data_block_per_disk
        return np.array(data_disk_list)

    @staticmethod
    def _str_to_order(str):
        res = [ord(str[i]) for i in range(len(str))]
        return np.array(res)

    @staticmethod
    def generate_padding_block(byte_length):
        return bytes([0 for _ in range(byte_length)])
