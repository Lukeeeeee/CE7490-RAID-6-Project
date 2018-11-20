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

    def write_file(self, file_content):
        """
        Write the file to the disks concurrently, firstly computing the parity and concurrently write to all the disks
        :param file_content:
        :return: None
        """
        data = self._split_content_into_data_disks(data_disks_n=self.config.data_disk_count,
                                                   file_content=file_content)
        data_with_parity = np.concatenate([data, self.compute_parity(data=data)], axis=1)

        # We use parallel writing operation to write the file into disks

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.disk_count) as executor:
            executor.map(Disk.write_to_disk,
                         self.disk_list,
                         data_with_parity.tolist())

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
        return self.gf.gen_parity(data=data)

    def check_corruption(self):
        """
        Detect if single disk failed.
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

    def _split_content_into_data_disks(self, data_disks_n, file_content):
        """
        Strip the data into each data disks
        :param data_disks_n: A scalar
        :param file_content: A numpy array with 1 dim or a list
        :return: A numpy arrary with size [data_disks_n, -1]
        """
        file_content = np.reshape(file_content, [-1])
        file_content_length_per_disk = file_content.shape[0] // data_disks_n + \
                                       0 if file_content.shape[0] % data_disks_n == 0 else 1
        data_index = 0
        data_disk_list = [[] for _ in range(data_disks_n)]
        for d in file_content:
            data_disk_list[data_index].append(d if isinstance(d, str) else chr(d))
            data_index = (data_index + 1) % data_disks_n
        if data_index != 0:
            for index in range(data_index, data_disks_n):
                data_disk_list[index].append(0)
        for data in data_disk_list:
            assert len(data) == file_content_length_per_disk
        return np.array(data_disk_list)
