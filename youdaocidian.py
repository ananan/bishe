import sys
from pprint import pprint
import requests
import hashlib
import random
import time

def get_data(word):
    salt = str(int(time.time()*1000) + random.randint(1,10))
    A = "rY0D^0'nM0}g5Mm1z%1G4"
    sign = hashlib.md5(("fanyideskweb" + word + salt + A).encode('utf8')).hexdigest()   # Create hash sign
    
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    
    data = {}
    data['i'] = word
    data['salt'] = salt
    data['sign'] = sign
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_REALTIME'
    data['typoResult'] = 'true'

    headers = {
         'Accept':'application/json, text/javascript, */*; q=0.01',
         'Accept-Encoding':'gzip, deflate',
         'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
         'Connection':'keep-alive',
         'Content-Length':'205',
         'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
         'Cookie':'OUTFOX_SEARCH_USER_ID=-1952769096@123.58.182.243; OUTFOX_SEARCH_USER_ID_NCOO=299132983.56201506; _ntes_nnid=2be06273f9a84c503694b14e705dc9d4,1503010352270; JSESSIONID=aaaOR3Z_jEmnuc7ysuQ8v; UM_distinctid=15f2c092692501-0bc916153c00d5-1227170b-13c680-15f2c09269354a; NTES_SESS=MV6x1csO53ep_nKOlpk_yAn.Yg.1fkWwAntD7bKMMPGBbX4tbOxW2SkdxGmK6Xu_.IeBeM87MpQplZBbZL.Zy3xK5YmsDdjgqdobLzpn2hra0a5PnssQkR6S4r5eI.1ln19IA0nLHPh6U3fCvgYnPa5YVImypa0q9WrnsmVgVcHjyb_FVGBXWnFiR0I8wmk4E; S_INFO=1508243941|0|3&100##|m15917916221_1; P_INFO=m15917916221_1@163.com|1508243941|0|search|00&99|gud&1508235466&search#gud&440100#10#0#0|159221&1|search&mail163|15917916221@163.com; ___rl__test__cookies=1508281766130',
         'Host':'fanyi.youdao.com',
         'Origin':'http://fanyi.youdao.com',
         'Referer':'http://fanyi.youdao.com/',
         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
         'X-Requested-With':'XMLHttpRequest',
         }
    try:
        res = requests.post(url=url,data=data,headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print('Raise Error...',e)

    
if __name__ == "__main__":
    word = 'Python is a beautiful language'
    input_data = sys.argv[1]
    pprint(get_data(input_data))
