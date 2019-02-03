import os


def install_me():
    print('upgrading...... \n')
    os.system('apt update && apt upgrade -y')
    os.system('clear')
    print('update done..\n')

    print('setting up environment... \n')
    os.system('apt install sqlite3 -y')

    os.system('apt-get install nano -y')

    os.system('apt-get install curl -y')
    os.system('apt-get install openssh-client -y')
    os.system('apt-get install openssh-server -y')
    os.system('apt-get install wget -y')
    os.system('apt-get install iperf -y')

    os.system('apt-get install python3 -y')
    os.system('apt-get install python3-paramiko -y')
    os.system('apt-get install python3-psutil -y')
    os.system('apt-get install python3-pyfiglet -y')
    os.system('apt-get install python3-matplotlib -y')
    os.system('clear')
    os.system('bash go-ipfs/install.sh')
    os.system('ipfs init')

    from pyfiglet import Figlet

    g = Figlet(font='bubble')

    print(g.renderText('SET UP DONE ...'))


def main():
    install_me()


if __name__ == "__main__":
    main()


