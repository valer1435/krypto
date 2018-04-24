from random import *
from time import time
import hashlib
ids = input()
letters = 'qwertyuiopasdfghjklzxcvbnm1234567890-'
start = time()
for _ in range(4):
    while True:
        test_string = "".join([choice(letters) for i in range(10)])
        if hashlib.md5((ids+"-"+test_string).encode('utf8')).hexdigest()[:5] == "00000":
            print(ids+"-"+test_string)
            break
print(time() - start)