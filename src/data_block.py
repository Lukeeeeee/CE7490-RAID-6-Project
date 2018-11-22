class DataBlock(object):
    """
    Abstraction for data block in the RAID 6
    """
    DATA_TYPE_DATA_BLOCK = 0
    PARITY_TYPE_DATA_BLOCK = 1

    def __init__(self, data, data_type, file_id):
        self.data = data
        self.type = data_type
        self.file_id = file_id

    def __call__(self, *args, **kwargs):
        return self.data
