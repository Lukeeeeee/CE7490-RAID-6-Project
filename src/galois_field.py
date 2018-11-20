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
        '''
            generate log table and inverse log table in GF
        '''
        b = 1
        for alog in range(self.x_to_w - 1):
            self.gflog[b] = alog
            self.gfilog[alog] = b
            b = b << 1
            if b & self.x_to_w:
                b = b ^ self.prim_poly

    def multiply(self, a, b):
        '''
            multiply in GF by log table
            return a x b
        '''
        if a == 0 or b == 0:
            return 0
        sum_log = self.gflog[a] + self.gflog[b]
        if sum_log >= self.x_to_w - 1:
            sum_log -= self.x_to_w - 1
        return self.gfilog[sum_log]

    def devide(self, a, b):
        '''
            multiply in GF by log table
            return a / b
        '''
        if a == 0:
            return 0
        if b == 0:
            return -1  # Can’t divide by 0
        diff_log = self.gflog[a] - self.gflog[b]
        if diff_log < 0:
            diff_log += self.x_to_w - 1
        return self.gfilog[diff_log]

    def add(self, add_list):
        '''
            input: add_list: list of numbers to be added
            Add or minus operation in GF
            return the XOR result of the input list
        '''
        return np.bitwise_xor.reduce(add_list)

    def power(self, a, n):
        """
        compute a^n
        """
        n %= self.x_to_w - 1  # n is guaranteed >=0 after modular
        res = 1
        while True:
            if n == 0:
                return res
            n -= 1
            res = self.multiply(res, a)

    def gen_vandermond(self):
        '''
        input: n = data disk number, m = parity disk number
        '''
        for i in range(self.n_checksum):
            for j in range(self.n_data_disk):
                self.vandermond[i][j] = self.power(j, i)

    def gen_parity(self, data):
        '''
        input: data: [n,1] a row of data bytes
        output: an 1d array of checksums
        '''
        result = []
        for i in range(self.n_checksum):
            vector = []
            for j in range(self.n_data_disk):
                vector.append(self.multiply(data[j], self.vandermond[i][j]))
            result.append(np.bitwise_xor.reduce(vector))
        return np.array(result)

    def gen_matrix_A(self):
        '''
        generate matrix A concatenated by n x n identity matrix and vandermond matrix
        '''
        mat_a = np.concatenate((np.eye(self.n_data_disk, self.n_data_disk, dtype=int), self.vandermond), axis=0)
        return mat_a

    def recover_matrix(self, mat_a, vec_e, corrupt_index):
        '''
        delete rows in A and E to get new matrix for recovery
        A : concatenated matrix
        E : concatenated vector by byte in data disks and checksums
        '''
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
        """Convert an integer into a polynomial"""
        return [(sInt >> i) & 1 for i in reversed(range(sInt.bit_length()))]