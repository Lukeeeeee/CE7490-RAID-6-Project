from src.raid.raid_6 import RAID_6
from src.file import File
from src.disk import Disk
from src.util import Configuration as conf, Logger


def main():
    # Set up the simulation system

    conf = Configuration()
    disk_list = [Disk(disk_path=conf.disk_dir, id=i, disk_size=conf.disk_size) for i in range(conf.disk_count)]
    raid_6 = RAID_6(disk_list=disk_list,
                    config=conf)

    # TODO Random Generate some files
    file = File()

    # TODO Load the files into disks by raid 6

    raid_6.write_file(file=file)

    # TODO Start the test of raid 6


def _func(i):
    return i


if __name__ == '__main__':
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        a = list(ex.map(_func, range(10)))
        print(a)
