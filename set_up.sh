clear
echo 'preparing your machine . . .'
sleep 2
apt update && apt upgrade -y
clear

echo 'setting up environment... '
sleep 3
apt install sqlite3 -y

apt-get install nano -y

apt-get install curl -y
apt-get install openssh-client -y
apt-get install openssh-server -y
apt-get install wget -y
apt-get install iperf3 -y
apt-get install python3 -y
apt-get install python3-paramiko -y
apt-get install python3-psutil -y
apt-get install python3-pyfiglet -y
apt-get install python3-matplotlib -y

wget https://dist.ipfs.io/go-ipfs/v0.4.18/go-ipfs_v0.4.18_linux-amd64.tar.gz

tar xvfz go-ipfs_v0.4.18_linux-amd64.tar.gz

cd go-ipfs

bash install.sh
