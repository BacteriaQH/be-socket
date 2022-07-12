from passlib.hash import sha256_crypt
from datetime import datetime
import pytz
time = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
password = sha256_crypt.hash('password')
password2 = sha256_crypt.hash('password')
print(time)
print(password)
print(password2)

dt = datetime.now()
print(dt)
print(datetime.timestamp(dt))
if sha256_crypt.verify('password', password):
    print('true')