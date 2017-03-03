# -*- coding: utf-8 -*-
import os
import urllib2
import xlsxwriter
import cookielib
from bs4 import BeautifulSoup

def getName():
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  urllib2.install_opener(opener)
  headers = {
    'Host': 'www.yw11.com',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
    'Referer': 'http://www.yw11.com/namelist.php',
    'Accept-Language': 'zh-CN,zh;q=0.8'
  }

  workbook = xlsxwriter.Workbook('name1.xlsx')
  sheet = workbook.add_worksheet('postman')
  index = -1

  for xing in range(5,360):
    for sex in [0, 1]:
      try:
        url = 'http://www.yw11.com/html/mi/3-' + str(xing) + '-' + str(sex) + '-1.htm'
        req = urllib2.Request(url, None, headers)
        res = urllib2.urlopen(req, timeout = 2.0).read()
        soup = BeautifulSoup(res, "html.parser")
        print xing

        lis = soup.select('div[class=listbox1_text]')[0].find_all('li')
        for li in lis:
          index += 1
          sheet.write(index, 0, li.get_text().strip())
          sheet.write(index, 1, u'男' if sex == 0 else u'女')

      except Exception, e:
        continue
  workbook.close()

getName()
