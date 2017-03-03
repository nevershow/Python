# -*- coding: utf-8 -*-
import re
import requests
requests.packages.urllib3.disable_warnings() # 禁止访问https时warning提示

headers = {
  'Host': 'www.qcloud.com',
  'Connection': 'keep-alive',
  'Content-Length': '17',
  'Accept': '*/*',
  'Origin': 'https://www.qcloud.com',
  'X-Requested-With': 'XMLHttpRequest',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Referer': 'https://www.qcloud.com/act/campus',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'zh-CN,zh;q=0.8',
  'Cookie': 登录之后的cookie
}

def getCsrfCode(e):
  csrfCode = ""
  if (len(e) > 0):
    n = 5381
    for i in range(len(e)):
      n += (n << 5) + ord(e[i])
      csrfCode = 2147483647 & n
  return csrfCode

def getVoucher(qq):
  skey = re.findall('skey=(.{5,15});', headers['Cookie'])[0]
  csrfCode = getCsrfCode(skey)

  s = requests.Session()
  s.headers = headers
  posturl = 'https://www.qcloud.com/act/campus/ajax/index?uin=%s&csrfCode=%d' % (qq, csrfCode)
  while 1:
    try:
      res = s.post(posturl, data = {'action':'getVoucher'}).json()
      if res.get('code', None) != 20002:
        print(res.get('code', None))
        print(res.get('msg', '').encode('gbk'))
        print(res.get('data', None))
        break        
      else:
        print("waiting...")
    except Exception as e:
      print(e)
      pass

# {"code":10006,"msg":"reach max num limit","data":[]}
# {"code":20002,"msg":"尊敬的用户，抢券时间未到。","data":{}}

if __name__ == '__main__':
  getVoucher(你的QQ号)
