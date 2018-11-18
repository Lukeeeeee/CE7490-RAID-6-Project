from src.raid.raid_6 import RAID_6
from src.file import File
from src.disk import Disk
from src.util import Configuration as conf, Logger

if __name__ == '__main__':
    # Set up the simulation system

    conf = conf()
    disk_list = [Disk(disk_path=conf.disk_dir, id=i, disk_size=conf.disk_size) for i in range(conf.disk_count)]
    raid_6 = RAID_6(disk_list=disk_list,
                    file_path=conf.log_dir,
                    config=conf)

    # TODO Random Generate some files
    file = File()

    # TODO Load the files into disks by raid 6

    raid_6.read_file(file=file)

    # TODO Start the test of raid 6
