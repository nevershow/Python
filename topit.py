# -*- coding: utf-8 -*-
import os
import requests
from lxml import etree

s = requests.Session()
s.cookies['is_click'] = '1'

def download(pagenum):
  root = etree.HTML(s.get('http://www.topit.me/tag/%E6%83%85%E4%BE%A3?p=' + str(pagenum)).content)
  allA = root.findall('.//div[@class="e m"]/a/img')
  for a in allA:
    src = a.get('data-original')
    if src == None:
      src = a.get('src')
    name = src[src.rfind('/')+1:]
    open("cp\%s" % name, 'wb').write(s.get(src).content)

if __name__ == '__main__':
  if os.path.exists('cp') == False:
    os.mkdir('cp')
  try:
    for pagenum in range(1,4044):
      print(u'第 %d 页' % pagenum)
      download(pagenum)    
  except Exception as e:
    pass
