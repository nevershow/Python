# -*- coding: utf-8 -*-
import requests
from lxml import etree
requests.packages.urllib3.disable_warnings() # 禁止访问https时warning提示

def getGoogleFromNet():
  # 从豆瓣页面上提取出谷歌的网址并写入文件
  res = requests.get('https://www.douban.com/note/213070719/').text
  html = etree.HTML(res)
  allA = html.findall('.//div[@id="link-report"]/a')   # 使用xpath提取出超链接
  with open("google.txt", 'w') as fs:
    for a in allA:
      fs.write(a.get('href') + '\n')

def getGoogleFromFile():
  able = []
  with open('google.txt', 'r') as fs:
    for a in fs:
      a = a.strip()  # 去掉每一行末尾的换行符
      try:
        requests.get(a, timeout = 0.2)  # 0.2秒内打不开就默认被墙, 时间根据网速设置
        print(a)                        # 输出未被墙的网址
        able.append(a)
      except Exception as e:
        print('Unable to reach!')

  print('Get %d google' % len(able))
  for a in able:
    print(a)

if __name__ == '__main__':
  getGoogleFromNet()
  getGoogleFromFile()


# https://www.google.je/
# https://www.google.hu/
# https://www.google.rs/
# https://www.google.la/
# https://www.google.dz/
# https://www.google.td/
# https://www.google.cf/
# https://www.google.it.ao/
# https://www.google.co.mz/
