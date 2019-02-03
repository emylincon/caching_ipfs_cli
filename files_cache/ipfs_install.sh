
apt update && apt upgrade -y
wget https://dist.ipfs.io/go-ipfs/v0.4.18/go-ipfs_v0.4.18_linux-amd64.tar.gz

tar xvfz go-ipfs_v0.4.18_linux-amd64.tar.gz

cd go-ipfs

bash install.sh
