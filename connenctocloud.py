import requests
import json
from tan_token import *
pin_num=5
on_off=1

r = requests.get('https://cloud.arest.io/{dorm}/digital/{pin}/{turn}'.format(dorm=dorm_id,pin=pin_num,turn=on_off))

data = json.loads(r.content)
for k,v in data:
    print(k,v)

#if input==blue: pin_num=13
#if input==red: pin_num=12
#if input==green: pin_num=5