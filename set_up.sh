clear
echo 'preparing your machine . . .'
sleep 2
apt update && apt upgrade -y
clear

echo 'setting up environment... '
sleep 2
apt install sqlite3 -y

apt install nano -y

apt install curl -y
apt install openssh-client -y
apt install openssh-server -y
apt install wget -y
apt install iperf3 -y
apt install python3 -y
apt install python3-paramiko -y
apt install python3-psutil -y
apt install python3-pyfiglet -y
apt install python3-matplotlib -y
apt install nmap -y

clear

echo 'database done!'
echo 'setting up ipfs'
sleep 1.5

wget https://dist.ipfs.io/go-ipfs/v0.4.18/go-ipfs_v0.4.18_linux-amd64.tar.gz

tar xvfz go-ipfs_v0.4.18_linux-amd64.tar.gz

cd go-ipfs

bash install.sh

clear
echo 'IPFS done..'

sleep 1.5
clear
echo 'Preparing database'
sleep 2

mv * ..
python3 /home/mec/files_cache/refresh_db.py
/etc/init.d/ssh start

#rm -r /home/mec/caching_ipfs_cli
