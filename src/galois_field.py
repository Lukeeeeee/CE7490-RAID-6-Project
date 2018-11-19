# Date: 11/17/18
# Author: Luke
# Project: CE7490-RAID-6-Project


class GaloisField(object):
    """
    Galois field module
    """
    __shared_state = {}

    def __init__(self, N=8):
        self.__dict__ = self.__shared_state
        self.N = N
        # mask1, mask2 are two masks unsed internall; polyred is the "polynomial base"
        self.mask1 = 1 << self.N
        self.mask2 = self.mask1 - 1
        self.polyred = reduce(lambda x, y: (x << 1) + y, self.i2P(self.modulus)[1:])
        # circle in GF2^N, 255 in GF2^8
        self.circle = 2 ** self.N - 1

    def multiply(self, p1, p2):
        """Multiply two polynomials in GF(2^N)/g(x)
        :param p1: multipler
        :param p2: multiplier
        """
        p = 0
        while p2:
            if p2 & 1:
                p ^= p1
            p1 <<= 1
            if p1 & self.mask1:
                p1 ^= self.polyred
            p2 >>= 1
        return p & self.mask2

    def power(self, a, n):
        """
        compute a^n
        """
        n %= self.circle  # n is guaranteed >=0 after modular
        res = 1
        while True:
            if n == 0:
                return res
            n -= 1
            res = self.multiply(res, a)

    def gen_vandermond(self, n, m):
        '''
        input: n = data disk number, m = parity disk number
        '''
        self.n = n
        self.m = m
        self.vandermond = np.zeros((m, n), dtype=int)
        for i in range(m):
            for j in range(n):
                self.vandermond[i][j] = self.power(j, i)

    def gen_parity(self, data):
        result = []
        for i in range(self.m):
            vector = []
            for j in range(self.n):
                vector.append(self.multiply(data[j], self.vandermond[i][j]))
            result.append(np.bitwise_xor.reduce(vector))
        return result

    def gen_matrix_A(self, corrupt_index):
        A = np.concatenate((np.eye(self.n, self.n, dtype=int), self.vandermond), axis=0)
        A = np.delete(A, corrupt_index, axis=0)
        return A

    def recover(self, A, E):
        pass

    @staticmethod
    def i2P(sInt):
        """Convert an integer into a polynomial"""
        return [(sInt >> i) & 1 for i in reversed(range(sInt.bit_length()))]