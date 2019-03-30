***********************************************************************************************************************************
WARNINING! THIS WORK IS A COPY RIGHT OF LONDON SOUTH BANK UNIVERSITY AND IT HAS BEEN LICENSED UNDER CREATIVE COMMONS CC BY NC CA
***********************************************************************************************************************************

This is a hybrid caching algorithm using LRU, LFU and Cooperative Caching.
IPFS is used in cooperative caching platform.

please run the set_up.py  file first

*************************************************************************************************************************************
## Working With IPFS

* ipfs uses DHT(distributed Hash technique) to store data
* MerkleDAG to give it structure
* it uses bittorrent mechanism to exchange data

### IPFS installation
The setup file install IPFS buyt if you want to do it manually follow the steps below:
```
apt update && apt upgrade -y  
wget https://dist.ipfs.io/go-ipfs/v0.4.18/go-ipfs_v0.4.18_linux-amd64.tar.gz  
tar xvfz go-ipfs_v0.4.18_linux-amd64.tar.gz  
cd go-ipfs  
bash install.sh #(moves ipfs to /usr/local/bin) or mv ./ipfs /usr/local/bin  
```

------------------------------------------
### checking installation
------------------------------------------

`ipfs help`

----------------------------------------------
### initializing ipfs
----------------------------------------------

`ipfs init`

------------------------
running the ipfs daemon
------------------------

`ipfs daemon`

# to run in background
ctrl z
bg
#######################

or 

`ipfs daemon &`

........................
### Add file to IPFS
........................

`ipfs add <file name>`

........................
### delete a file
........................

`ipfs pin rm -r <hash id>`  
`ipfs repo gc`

---------------------------------
see the files added in ipfs
---------------------------------

`ipfs pin ls --type=all`

