# Date: 11/17/18
# Author: Luke
# Project: CE7490-RAID-6-Project
import numpy as np
from functools import reduce

GF_W = 8
PRIM_POLY = 285


class GaloisField(object):
    """
    Galois field module
    :param num_data_disk: the number of data disks
    :param num_checksum: the number of checksums
    """

    def __init__(self, num_data_disk, num_checksum):
        self.GF_W = GF_W
        self.prim_poly = PRIM_POLY
        self.n_data_disk = num_data_disk
        self.n_checksum = num_checksum
        self.x_to_w = 1 << self.GF_W
        self.gflog = np.zeros((self.x_to_w,), dtype=int)
        self.gfilog = np.zeros((self.x_to_w,), dtype=int)
        self.vandermond = np.zeros((self.n_checksum, self.n_data_disk), dtype=int)
        self.gen_log_table()
        self.gen_vandermond()

    def gen_log_table(self):
        """
        Function to generate log table and inverse log table in GF
        :return: None
        """
        b = 1
        for alog in range(self.x_to_w - 1):
            self.gflog[b] = alog
            self.gfilog[alog] = b
            b = b << 1
            if b & self.x_to_w:
                b = b ^ self.prim_poly

    def multiply(self, a, b):
        """
        Function to multiply a and b in GF by log table
        :param a: multiplier
        :param b: multiplier
        :return: a x b in GF
        """

        if a == 0 or b == 0:
            return 0
        sum_log = self.gflog[a] + self.gflog[b]
        if sum_log >= self.x_to_w - 1:
            sum_log -= self.x_to_w - 1
        return self.gfilog[sum_log]

    def devide(self, a, b):
        """
        Function to devide a by b in GF by log table
        :param a: devisor
        :param b: devidend
        :return: a/b in GF
        """
        if a == 0:
            return 0
        if b == 0:
            return -1  # Can’t divide by 0
        diff_log = self.gflog[a] - self.gflog[b]
        if diff_log < 0:
            diff_log += self.x_to_w - 1
        return self.gfilog[diff_log]

    def add(self, add_list):
        """
        Function to perform add or minus operation in GF
        :param add_list: list of numbers to be added
        :return: the bitwise XOR result of the input list
        """
        return np.bitwise_xor.reduce(add_list)

    def power(self, a, n):
        """
        Function to compute a^n
        :param a: base
        :param n: power
        :return: a^n in GF
        """
        n %= self.x_to_w - 1  # n is guaranteed >=0 after modular
        res = 1
        while True:
            if n == 0:
                return res
            n -= 1
            res = self.multiply(res, a)

    def gen_vandermond(self):
        """
        Function to generate the vandermond matrix
        :return: None
        """
        for i in range(self.n_checksum):
            for j in range(self.n_data_disk):
                self.vandermond[i][j] = self.power(j, i)

    def gen_parity(self, data):
        """
        Function to generate the parity bytes in checksums
        :param data: 1d array of data bytes
        :return:  1d array of checksums
        """

        result = []
        for i in range(self.n_checksum):
            vector = []
            for j in range(self.n_data_disk):
                vector.append(self.multiply(data[j], self.vandermond[i][j]))
            result.append(self.add(vector))
        return np.array(result)

    def gen_matrix_A(self):
        """
        generate matrix A concatenated by n x n identity matrix and vandermond matrix
        :return: the concatenated matrix A
        """

        mat_a = np.concatenate((np.eye(self.n_data_disk, self.n_data_disk, dtype=int), self.vandermond), axis=0)
        return mat_a

    def recover_matrix(self, mat_a, vec_e, corrupt_index):
        """
        Function to delete rows in A and E to get new matrix for recovery
        :param mat_a: atrix A concatenated by n x n identity matrix and vandermond matrix
        :param vec_e: concatenated vector by byte in data disks and checksums
        :param corrupt_index: the index of disks which are corrupted
        :return: reduced matrix A and vector E
        """

        if len(corrupt_index) > self.n_checksum:
            raise ValueError('corrupted disk number can not be greater than checksum number')
        mat_a = np.delete(mat_a, corrupt_index, axis=0)
        vec_e = np.delete(vec_e, corrupt_index)
        if len(corrupt_index) == self.n_checksum:
            return mat_a, vec_e
        else:
            for i in range(self.n_checksum - len(corrupt_index)):
                rand_index = np.random.randint(len(vec_e))
                mat_a = np.delete(mat_a, rand_index, axis=0)
                vec_e = np.delete(vec_e, rand_index)
            return mat_a, vec_e

    @staticmethod
    def i2P(sInt):
        """
        Convert an integer into a polynomia
        :param sInt: integer
        :return: polynomial patameters
        """
        return [(sInt >> i) & 1 for i in reversed(range(sInt.bit_length()))]