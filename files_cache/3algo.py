import sqlite3
import hashlib
import os
import socket
import paramiko
from time import gmtime, strftime
import random
import time
import psutil
import ping_code as pc
from matplotlib import pyplot as plt
from pyfiglet import Figlet

mec_list = ['10.0.0.10', '10.0.0.20', '10.0.0.30']

colour = {'35.196.51.199/1.html': 'r',
          '35.196.51.199/2.html': 'g',
          '35.196.51.199/3.html': 'c',
          '35.196.51.199/4.html': 'k',
          '35.196.51.199/5.html': 'b',
          '35.196.51.199/6.html': 'm',
          '35.196.51.199/7.html': 'y'}

cache_size = 3
H = 0  # hit counter
M = 0  # miss counter
MH = 0  # cooperative hit counter
re_use = 0  # replacement algorithm use counter
ref = [5, 0, 5, 3, 6, 0, 4, 1, 3, 5, 5, 6, 0, 5, 5, 2, 6, 5, 2, 6, 4, 1, 4, 4, 5, 6, 0, 3, 2, 6]
# ref = [14, 14, 7, 0, 15, 15, 5, 18, 7, 14, 8, 17, 10, 14, 10, 16, 17, 12, 16, 0, 4, 10, 1, 12, 4, 5, 7, 6, 14, 19, 18, 7, 10, 19, 5, 13, 8, 14, 10, 16, 10, 0, 0, 13, 2, 4, 9, 17, 14, 10, 10, 5, 19, 11, 0, 16, 8, 10, 19, 8, 8, 18, 13, 16, 16, 10, 7, 11, 15, 6, 19, 7, 6, 1, 10, 15, 1, 14, 13, 4, 5, 5, 9, 2, 5, 6, 14, 15, 11, 15, 7, 0, 4, 7, 0, 12, 7, 10, 13, 6, 16, 7, 14, 17, 6, 0, 12, 11, 12, 15, 12, 16, 9, 7, 13, 12, 10, 11, 9, 4, 6, 2, 15, 15, 3, 7, 15, 19, 4, 7, 14, 14, 0, 12, 4, 13, 14, 6, 7, 16, 6, 4, 16, 3, 15, 15, 9, 1, 5, 7, 15, 17, 4, 1, 15, 17, 18, 17, 5, 0, 16, 11, 10, 14, 6, 18, 5, 4, 17, 1, 15, 4, 10, 19, 19, 2, 7, 4, 3, 8, 15, 1, 2, 9, 8, 10, 17, 1, 12, 3, 2, 11, 14, 19, 16, 19, 4, 6, 13, 12, 13, 12, 3, 10, 7, 13, 12, 12, 8, 3, 3, 4, 7, 5, 7, 2, 0, 16, 1, 2, 7, 12, 10, 8, 16, 3, 10, 17, 11, 8, 10, 1, 18, 10, 0, 11, 12, 18, 8, 13, 6, 19, 0, 12, 18, 10, 9, 8, 10, 4, 1, 10, 15, 16, 11, 12, 6, 0, 12, 14, 18, 7, 1, 12, 4, 19, 0, 17, 3, 17, 7, 15, 3, 14, 6, 12, 6, 12, 19, 0, 10, 17, 14, 5, 9, 17, 18, 14, 6, 19, 9, 12, 12, 7, 0, 6, 11, 1, 7, 15, 4, 9, 14, 18, 10, 5, 15, 18, 11, 7, 19, 4, 11, 13, 4, 12, 1, 5, 5, 7, 9, 4, 18, 14, 4, 11, 5, 13, 5, 4, 13, 15, 15, 0, 1, 1, 14, 14, 6, 18, 9, 14, 15, 1, 5, 3, 17, 6, 0, 8, 9, 13, 13, 1, 4, 7, 10, 0, 12, 16, 18, 3, 1, 1, 18, 6, 1, 10, 8, 13, 16, 6, 15, 8, 2, 1, 10, 4, 7, 11, 13, 7, 9, 12, 9, 11, 10, 8, 11, 0, 3, 3, 14, 8, 15, 1, 15, 11, 19, 15, 14, 13, 5, 1, 16, 3, 17, 18, 16, 15, 13, 0, 11, 6, 10, 18, 16, 18, 6, 7, 16, 13, 6, 2, 0, 6, 6, 2, 9, 4, 12, 9, 10, 11, 18, 6, 11, 19, 14, 9, 9, 5, 8, 6, 1, 6, 19, 15, 7, 1, 9, 5, 13, 6, 12, 13, 19, 8, 14, 9, 0, 13, 8, 7, 13, 11, 11, 12, 8, 9, 3, 12, 7, 1, 4, 8, 6, 5, 17, 7, 19, 4, 18, 16, 4, 9, 8, 9, 4, 6, 7, 19, 18, 4, 12, 13, 11, 4, 19, 6]

freq = {}
changing_freq = {}
window_size = 0

x_axis = []
y_axis = []


def plot_performance():
    global H
    global M
    global MH
    global re_use

    fig5 = plt.figure('Cache Performance')

    fig5 = plt.clf()

    fig5 = plt.ion()
    name = ['Hits', 'Misses', 'Co-operative-Hits', 'Algo use']
    ypos = ([0, 1, 2, 3])
    values = [H, M, (H + MH), re_use]

    fig5 = plt.xticks(ypos, name)
    fig5 = plt.bar(ypos, values, align='center', color='m')
    fig5 = plt.title('Cache Performance')

    fig5 = plt.ylabel('values')

    fig5 = plt.pause(2)


def update_changing_freq():
    for key in freq.keys():
        x = key
        y = freq[key]
        if x in changing_freq.keys():
            changing_freq[x].append(y)
        else:
            changing_freq[x] = [y]


def plot_changing_freq():
    global changing_freq

    hash_dic = {'35.196.51.199/1.html': '9692a9e4ff9d3fcb79d5b96aa497edf2', 
	'35.196.51.199/2.html': '0133b5a7d8245cc08641e1e5896898d5', 
	'35.196.51.199/3.html': 'ecd701bfea752e7f1e2ef7e6b2084911', 
	'35.196.51.199/4.html': 'c64022b8c9349c07381ef73063eddfb1', 
	'35.196.51.199/5.html': '26cc9799bca4458b326fb5db91940b0f', 
	'35.196.51.199/6.html': 'd0b1193c54e1f3ff4cebe9696fdd22a7', 
	'35.196.51.199/7.html': '872b8422730665964fd706e628f66ac1'}

    plot_dic = {}

    for key in hash_dic:
        if hash_dic[key] not in changing_freq:
            continue
        elif hash_dic[key] in changing_freq:
            rf = changing_freq[hash_dic[key]]
            plot_dic[key] = rf  # converts the dictionary from hash: frequency to web: frequency

    fig3 = plt.figure('Moving Relative Frequency')

    fig3 = plt.clf()
    fig3 = plt.ion()
    fig3 = plt.grid(True, color='k')
    for key in plot_dic.keys():
        fig3 = plt.plot(plot_dic[key], linewidth=5, label=key, color=colour[key])

    fig3 = plt.title('Changing frequency Graph')
    fig3 = plt.ylabel('URL')
    fig3 = plt.xlabel('Time (seconds)')
    fig3 = plt.legend()
    fig3 = plt.pause(2)


def local_cache_frequency():
    ip = ip_address()

    con = sqlite3.connect('cache.db')
    cur = con.cursor()
    cur.execute("select Hash from CacheTable where Host_ip ='" + ip + "'")
    data = cur.fetchall()
    '''
    data format

    [('7e7ea8d98195d1fcf6abe4f77e56730e',), ('26ff04f8463191809dcd9e8605bb952a',), ('d37269610dffb86e4925864b110e4d4e',)]
    '''
    d = []
    if len(data) == 0:
        con.close()
        return 'no items'
        pass
    else:
        for i in data:
            d.append(i[
                         0])  # cleaning data to d = ['7e7ea8d98195d1fcf6abe4f77e56730e', '26ff04f8463191809dcd9e8605bb952a', 'd37269610dffb86e4925864b110e4d4e']
        con.close()
        cache_dic = {}
        for i in d:
            cache_dic[i] = freq[i]  # creates a dictionary and tags the hash with its relative frequency

        hash_dic = {'35.196.51.199/1.html': '9692a9e4ff9d3fcb79d5b96aa497edf2', '35.196.51.199/2.html': '0133b5a7d8245cc08641e1e5896898d5', '35.196.51.199/3.html': 'ecd701bfea752e7f1e2ef7e6b2084911', '35.196.51.199/4.html': 'c64022b8c9349c07381ef73063eddfb1', '35.196.51.199/5.html': '26cc9799bca4458b326fb5db91940b0f', '35.196.51.199/6.html': 'd0b1193c54e1f3ff4cebe9696fdd22a7', '35.196.51.199/7.html': '872b8422730665964fd706e628f66ac1'}

        plot_dic = {}

        for key in hash_dic:
            if hash_dic[key] not in cache_dic:
                continue
            elif hash_dic[key] in cache_dic:
                rf = cache_dic[hash_dic[key]]
                plot_dic[key] = rf  # converts the dictionary from hash: frequency to web: frequency

        return plot_dic


def plot_local_cache_freq():
    global changing_freq

    hash_dic = {'35.196.51.199/1.html': '9692a9e4ff9d3fcb79d5b96aa497edf2', '35.196.51.199/2.html': '0133b5a7d8245cc08641e1e5896898d5', '35.196.51.199/3.html': 'ecd701bfea752e7f1e2ef7e6b2084911', '35.196.51.199/4.html': 'c64022b8c9349c07381ef73063eddfb1', '35.196.51.199/5.html': '26cc9799bca4458b326fb5db91940b0f', '35.196.51.199/6.html': 'd0b1193c54e1f3ff4cebe9696fdd22a7', '35.196.51.199/7.html': '872b8422730665964fd706e628f66ac1'}

    plot_dic = {}

    for key in hash_dic:
        if hash_dic[key] not in changing_freq:
            continue
        elif hash_dic[key] in changing_freq:
            rf = changing_freq[hash_dic[key]]
            plot_dic[key] = rf  # converts the dictionary from hash: frequency to web: frequency

    fig4 = plt.figure('Local Cache Frequency')

    fig4 = plt.clf()
    fig4 = plt.ion()
    fig4 = plt.grid(True, color='k')
    if local_cache_frequency() == 'no items':
        pass
    else:
        for key in plot_dic.keys():
            if key in local_cache_frequency():
                fig4 = plt.plot(plot_dic[key], linewidth=5, label=key, color=colour[key])

            fig4 = plt.title('Local Cache frequency Graph')
            fig4 = plt.ylabel('URL')
            fig4 = plt.xlabel('Time (seconds)')
            fig4 = plt.legend()
            fig4 = plt.pause(2)


def hash_to_web():
    global freq

    hash_dic = {'35.196.51.199/1.html': '9692a9e4ff9d3fcb79d5b96aa497edf2', '35.196.51.199/2.html': '0133b5a7d8245cc08641e1e5896898d5', '35.196.51.199/3.html': 'ecd701bfea752e7f1e2ef7e6b2084911', '35.196.51.199/4.html': 'c64022b8c9349c07381ef73063eddfb1', '35.196.51.199/5.html': '26cc9799bca4458b326fb5db91940b0f', '35.196.51.199/6.html': 'd0b1193c54e1f3ff4cebe9696fdd22a7', '35.196.51.199/7.html': '872b8422730665964fd706e628f66ac1'}

    plot_dic = {}

    for key in hash_dic:
        if hash_dic[key] not in freq:
            continue
        elif hash_dic[key] in freq:
            rf = freq[hash_dic[key]]
            plot_dic[key] = rf

    return plot_dic


def plot_graphs(host='35.196.51.199'):
    prev_t = 0
    rtt = pc.verbose_ping(host)
    next_t = psutil.cpu_percent(percpu=False)
    delta = abs(prev_t - next_t)
    prev_t = next_t
    plot_resource_util(rtt, delta)
    plot_relative_frequency()
    plot_changing_freq()
    plot_local_cache_freq()
    plot_performance()
    plt.show()


def plot_resource_util(x, y):
    fig1 = plt.figure('Resource Utilization')

    fig1 = plt.clf()
    x_axis.append(x)
    y_axis.append(y)
    fig1 = plt.ion()
    fig1 = plt.grid(True, color='k')
    fig1 = plt.plot(x_axis, linewidth=5, label='RTT')
    fig1 = plt.plot(y_axis, linewidth=5, label='CPU')
    fig1 = plt.title('CPU and RTT Utilization over Time')
    fig1 = plt.ylabel('CPU and RTT')
    fig1 = plt.xlabel('Time (seconds)')
    fig1 = plt.legend()
    fig1 = plt.pause(2)

    # plt.show()


def plot_relative_frequency():
    fig2 = plt.figure('Relative Frequency')
    fig2 = plt.clf()
    ret = hash_to_web()

    val = []
    keys = []
    cols = ['r', 'g', 'c', 'k', 'b', 'm', 'y']

    for i in ret.items():
        val.append(i[1])
        keys.append(i[0])

    explode = []
    for i in val:
        if i == max(val):
            explode.append(0.1)
        else:
            explode.append(0)

    fig2 = plt.ion()
    fig2 = plt.pie(val, labels=keys, autopct='%.3f%%', shadow=True, explode=explode, colors=cols)
    fig2 = plt.title('Relative Frequency')
    fig2 = plt.pause(2)


def get_hash(url):
    hash_me = 'get {} HTTP/1.0'.format(url)
    y = str.encode(hash_me)
    ha = hashlib.md5(y)
    hash_no = ha.hexdigest()
    calc_relative_freq(hash_no)
    check_cache(hash_no, url)


def calc_relative_freq(x):
    global freq
    global window_size

    window_size += 1
    alpha = 1 / window_size
    delta = alpha / (len(freq) + 1)
    if x not in freq.keys():
        for k in freq.keys():
            freq[k] -= delta
        freq[x] = alpha
    else:
        for k in freq.keys():
            if k != x:
                freq[k] -= delta
        freq[x] += (len(freq) - 1) * delta

    update_changing_freq()
    plot_graphs()


def get_time():
    y = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return y


def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.0.0.20", 80))
    return s.getsockname()[0]


def check_cache(hash_no, url):
    try:
        global con
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM CacheTable WHERE Hash='" + hash_no + "'")
        d = cur.fetchone()
        r = d[0]
        if r == 0:
            fetch_from_source(hash_no, url)
        else:
            fetch_from_cache(hash_no)

    except sqlite3.Error as e:
        if con:
            con.rollback()
            print('Error in check_cache: {}'.format(e))

    finally:
        if con:
            con.close()


def fetch_from_source(hash_no, url):
    global M
    cmd = "curl {}".format(url)
    os.system(cmd)

    prepare_db()  # CHECKS IF CACHE IS FULL AND ELIMINATES VICTIM

    cmd = "echo `curl {}` > /home/mec/cache/{}.html".format(url, hash_no)  # CACHES DATA FROM SOURCE
    os.system(cmd)
    print('-----------------------------------')
    print('Cache Miss')
    print('-----------------------------------')
    M += 1
    update_local_database(hash_no)


def update_local_database(hash_no):
    try:
        global con

        con = sqlite3.connect('cache.db')
        cur = con.cursor()
        cache_time = get_time()
        ip = ip_address()
        path = '/home/mec/cache/{}.html'.format(hash_no)
        data = (hash_no, path, cache_time, ip)
        cur.execute("INSERT INTO CacheTable VALUES(?, ?, ?, ?)", data)
        con.commit()
        cur.execute("SELECT * FROM CacheTable")
        d = cur.fetchall()

        for row in d:
            print(row)

        update_mec_database(hash_no, path, cache_time, ip)
        con.close()

    except sqlite3.Error as e:
        print('Error in cache_update: {}'.format(e))


def update_mec_database(hash_no, path, cache_time, host_ip):
    ip = ip_address()
    for i in mec_list:
        if i != ip:
            c = paramiko.SSHClient()

            un = 'mec'
            pw = 'password'
            port = 22

            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(i, port, un, pw)
            cmd = 'python3 /home/mec/db_manage.py insert "{}" "{}" "{}" "{}"'.format(hash_no, path, cache_time, host_ip)

            stdin, stdout, stderr = c.exec_command(cmd)


def fetch_from_cache(hash_no):
    try:
        global con
        global H
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("SELECT Host_ip FROM CacheTable WHERE Hash='" + hash_no + "'")
        host_ip_list = cur.fetchall()
        h_list = []
        for i in host_ip_list:
            h_list.append(i[0])

        local_ip = ip_address()
        if local_ip in h_list:
            time = get_time()
            cmd = "cat /home/mec/cache/{}.html".format(hash_no)
            os.system(cmd)
            print('-----------------------------------')
            print('Cache Hit from localhost')
            print('-----------------------------------')
            H += 1
            cur.execute(
                "update CacheTable set DateTime = '" + time + "' where Hash = '" + hash_no + "' and Host_ip = '" + local_ip + "';")
            con.close()
        elif len(host_ip_list) == 1:
            fetch_from_mec(hash_no, host_ip_list[0][0])

        elif len(host_ip_list) > 1:
            max_band_ip = get_max_band()
            fetch_from_mec(hash_no, max_band_ip)

    except sqlite3.Error as e:
        print('Error in cache_update: {}'.format(e))


def frequently_used(hash_no):
    host_ip = ip_address()
    global freq
    try:
        global con
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("SELECT Hash FROM CacheTable WHERE Host_ip ='" + host_ip + "'")
        host_ip_list = cur.fetchall()
        con.close()
        li = []
        for i in range(len(host_ip_list)):
            li.append(host_ip_list[i - 1][0])
        fre_li = []
        for i in li:
            fre_li.append(freq[i])
        min_freq = min(fre_li)

        if min_freq > freq[hash_no]:
            return 'no'
        elif min_freq < freq[hash_no]:
            y = fre_li.index(min_freq)
            delete_least_frequent_mec(li[y], host_ip)
            delete_least_frequent_locally(li[y], host_ip)
            return 'yes'

    except sqlite3.Error as e:
        print('Error in cache_update: {}'.format(e))


def delete_least_frequent_locally(hash_no, host_ip):
    try:
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("DELETE FROM CacheTable WHERE Hash = '" + hash_no + "' AND Host_ip = '" + host_ip + "'")
        con.commit()
        con.close()
        cmd = 'rm /home/mec/cache/{}.html'.format(hash_no)
        os.system(cmd)

    except sqlite3.Error as e:
        print('Error in cache_update: {}'.format(e))


def delete_least_frequent_mec(hash_no, host_ip):
    for i in mec_list:
        if i != host_ip:
            c = paramiko.SSHClient()

            un = 'mec'
            pw = 'password'
            port = 22

            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(i, port, un, pw)
            cmd = 'python3 /home/mec/db_manage.py del "{}" "{}" '.format(hash_no, host_ip)

            stdin, stdout, stderr = c.exec_command(cmd)


def fetch_from_mec(hash_no, host_ip):
    c = paramiko.SSHClient()
    global MH
    global re_use

    un = 'mec'
    pw = 'password'
    port = 22

    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host_ip, port, un, pw)
    cmd = 'cat /home/mec/cache/{}.html'.format(hash_no)

    stdin, stdout, stderr = c.exec_command(cmd)

    con = sqlite3.connect('/home/mec/cache.db')
    cur = con.cursor()

    ip = ip_address()

    cur.execute("SELECT COUNT(*) FROM CacheTable WHERE Host_ip='" + ip + "'")
    d = cur.fetchone()
    r = d[0]  # This value represents how many data entries for host_ip

    if r >= cache_size and frequently_used(hash_no) == 'no':
        for line in stdout:
            q = len(line) - 1
            t = line[:q]
            print(t)
        print('-----------------------------------')
        print('Hit from MEC Not Cached')
        print('-----------------------------------')
        MH += 1
    else:
        for line in stdout:
            q = len(line) - 1
            t = line[:q]
            cmd = "echo '{}' >> /home/mec/cache/{}.html".format(t, hash_no)
            os.system(cmd)
        cmd = 'cat /home/mec/cache/{}.html'.format(hash_no)
        update_local_database(hash_no)
        os.system(cmd)
        print('-----------------------------------')
        print('Cache Hit from MEC')
        print('-----------------------------------')
        MH += 1
        if r >= cache_size:
            re_use += 1
    con.close()


def get_max_band():
    M1 = '10.0.0.10'
    M2 = '10.0.0.20'
    # M3 = '10.3.3.3'
    conn = sqlite3.connect('/home/mec/cache.db')
    curr = conn.cursor()
    sql_cmd = "SELECT M1, M2 FROM Bw_Table ORDER BY Id DESC LIMIT 1;"
    curr.execute(sql_cmd)
    data = curr.fetchone()
    a = data[0]
    b = data[1]
    c = [a, b]
    d = max(c)
    e = c.index(d)
    if e == 0:
        return M1
    elif e == 1:
        return M2


def prepare_db():
    global re_use

    host_ip = ip_address()
    try:
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()

        cur.execute("SELECT COUNT(*) FROM CacheTable WHERE Host_ip='" + host_ip + "'")
        d = cur.fetchone()
        r = d[0]  # This value represents how many data entries for host_ip
        if r >= cache_size:
            cur.execute("SELECT DateTime FROM CacheTable where Host_ip = '" + host_ip + "'")

            data = cur.fetchall()  # returns array that looks like [('2018-08-20 13:23:49',), ('2018-08-20 11:56:04',), ('2018-08-20 13:40:01',)]

            min_time = min(data)[0]  # Return minimum time

            delete_from_mec(min_time, host_ip)

            cur.execute(
                "SELECT Hash FROM CacheTable WHERE DateTime = '" + min_time + "' AND Host_ip = '" + host_ip + "'")
            data = cur.fetchone()

            cmd = 'rm /home/mec/cache/{}.html'.format(data[0])
            os.system(cmd)

            cur.execute("DELETE FROM CacheTable WHERE DateTime = '" + min_time + "' AND Host_ip = '" + host_ip + "'")
            con.commit()
            con.close()
            re_use += 1

            # cur.execute("SELECT * FROM CacheTable")

    except sqlite3.Error as e:
        print('Error Encountered: {}'.format(e))


def delete_from_mec(min_time, host_ip):
    ip = ip_address()
    for i in mec_list:
        if i != ip:
            c = paramiko.SSHClient()

            un = 'mec'
            pw = 'password'
            port = 22

            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(i, port, un, pw)
            cmd = 'python3 /home/mec/db_manage.py delete "{}" "{}" '.format(min_time, host_ip)

            stdin, stdout, stderr = c.exec_command(cmd)


def cache_performance():
    global H
    global M
    global MH
    global window_size
    global re_use
    p = int((H / 30) * 100)
    q = int(((H + MH) / 30) * 100)
    print('----------------------------------------------------------')
    print('                   Cache Performance')
    print('----------------------------------------------------------')
    print('local MEC Performance: {}% | Cooperative Performance: {}% '.format(p, q))
    print('\nLocal Cache hits: {}       | Cache Misses: {}'.format(H, M))
    print('\nMEC Cache hits: {}         | Total Cache hits: {}'.format(MH, H + MH))
    print('----------------------------------------------------------')
    print('         Total use of Replacement Algorithm = {}'.format(re_use))
    print('----------------------------------------------------------')


def run_me():
    os.system('clear')
    g = Figlet(font='bubble')

    print(g.renderText('MEC CACHING PROJECT'))
    print(g.renderText('                      BY     EMEKA'))
    while True:
        print('\n')
        s = input('Enter any key to start and "stop" to exit: ')
        if s == 'stop':
            print('\nProgramme Terminated')
            cache_performance()
            print('\n-----------------------------------------')
            print('RTT plot = {}'.format(x_axis))
            print('\n-----------------------------------------')
            print('\n-----------------------------------------')
            print('CPU plot = {}'.format(y_axis))
            print('\n-----------------------------------------')
            break
        else:
            '''
            for i in range(30):
                fr = open('web_test.txt', 'r')

                t = fr.readlines()

                v = random.randint(0, (len(t) - 1))
                get_hash(t[v])
                fr.close()
                time.sleep(3)
            '''
            for v in ref:
                fr = open('web_test.txt', 'r')

                t = fr.readlines()
                get_hash(t[v])
                fr.close()
                time.sleep(3)


def main():
    run_me()


if __name__ == "__main__":
    main()
