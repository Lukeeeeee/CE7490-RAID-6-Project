# CE7490-RAID-6-PROJECT

This repository holds the RAID 6 project for CE7490 Advanced Topics in Distributed Systems for Fall 2018 NTU.

### Installation Guide
The code was developed under Ubuntu and some of the installation configurations may not applicable on Windows.
We give the installation guide on Ubuntu 16.04 system, for others, a similar process can be applied.
Firstly, install [Anaconda 3.7](https://www.anaconda.com/download/#linux) in your PC. 
Then clone this repo and create the environment by:
```
git clone https://github.com/Lukeeeeee/CE7490-RAID-6-Project
cd CE7490-RAID-6-Project
conda env create -f environment.yml
```
Test if you create the environment correctly:
```
source activate raid6
```

### Run the test
The source code is placed at `/src`, and the test script is placed at `/test`.
To test the raid 6: 
```
cd /path/to/CE7490-RAID-6-Project
source activate raid6
python test/test_raid_6.py
```
The log will be printed to the console, also a log directory will be created at `/log` with a timestamp 
(e.g., `/log/2018-11-23_10-51-30`). And in the log directory, the `disk` is the virtual representation of the real disks
and `test.log` contains the same output of the console for recording.
