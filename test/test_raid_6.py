from src.raid.raid_6 import RAID_6
from src.file import File
from src.disk import Disk
from src.util import Configuration, Logger


def main():
    # Set up the simulation system

    conf = Configuration()
    disk_list = [Disk(disk_path=conf.disk_dir, id=i, disk_size=conf.disk_size) for i in range(conf.disk_count)]
    raid_6 = RAID_6(disk_list=disk_list,
                    config=conf)
    logical_disk = Disk(disk_path=conf.disk_dir, id=-1, disk_size=conf.logical_disk_size)

    # Random Generate some files
    file = File()
    file.random_generate_string(data_size=conf.logical_disk_size - 11)
    logical_disk.write_to_disk(disk=logical_disk, data=file.file_content)
    data_block_list = logical_disk.set_up_data_block_list(block_size=conf.block_size)

    # Load the files into disks by raid 6

    raid_6.write_file(data_block_list=data_block_list)

    # Start the test of raid 6
    data = raid_6.read_all_data_disks()
    raid_6.check_corruption(disk_data_in_int=data)

    # Start to do the recover test
    raid_6.recover_disk(corrupted_disk_index=(6, 7))


if __name__ == '__main__':
    main()
