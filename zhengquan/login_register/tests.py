# import random
# char_list = [str(random.randint(1,10)) for i in range(4)]
# code = ''.join(char_list)
# import redis, time
# red = redis.Redis()
# red.set('name', 'cao', 1)
# # time.sleep(2)
# data = red.get('name')
# if data and data.decode() == 'cao':
#     print(data)
# else:
#     print(11)
import hashlib


def data_enc(data, salt):
    md5 = hashlib.md5()
    md5.update(data.encode())
    data = md5.hexdigest() + salt
    md5 = hashlib.md5()
    md5.update(data.encode())
    return md5.hexdigest()

data = 'cao'
salt = 'cao'
# 83bb37cf679f00264880126ddc020be6
# 83bb37cf679f00264880126ddc020be6
print(data_enc(data, salt))
print(data_enc(data, salt))
