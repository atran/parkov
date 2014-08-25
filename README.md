# Parkov

Installation using Raspberry Pis to create Markov Chains; making algorithms physical.

## Setup

Manually install pexpect
```
wget http://pexpect.sourceforge.net/pexpect-2.3.tar.gz
tar xzf pexpect-2.3.tar.gz
cd pexpect-2.3
sudo python ./setup.py install
cd ..
sudo rm -r pexpect-2.3
```

## Use

Partition a FAT32 portion on the SD Card. Mount it on `/mnt/storage`. Place files to be played there.
