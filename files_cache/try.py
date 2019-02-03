import hashlib

r = []

def get_hash(url):
    hash_me = 'get {} HTTP/1.0'.format(url)
    y = str.encode(hash_me)
    ha = hashlib.md5(y)
    hash_no = ha.hexdigest()
    r.append(hash_no)


for v in range(7):
  fr = open('web_test.txt', 'r')
  t = fr.readlines()
  get_hash(t[v])
  fr.close()

print(r)

