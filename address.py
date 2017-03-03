# -*- coding: utf-8 -*-
import os
import urllib2
import xlsxwriter
import cookielib
import threading
from bs4 import BeautifulSoup

people = 1
xlsx = 'address' + str(people) + '.xlsx'

headers = {
  'Host': 'sh.city8.com',
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
  'Accept-Language': 'zh-CN,zh;q=0.8'
}

class myThread (threading.Thread):   #继承父类threading.Thread
  def __init__(self, threadID):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.sheet = workbook.add_worksheet('postman' + str(self.threadID))

  def run(self):  #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
    global people
    global workbook
    global headers

    index = -1
    start = (people - 1) * 100 + 1 + (self.threadID - 1) * 25
    end = start + 25
    for s in range(start, end):
      for p in range(1,10):
        print 's' + str(s) + 'p' + str(p)
        try:
          url = 'http://sh.city8.com/address/s' + str(s) + 'p' + str(p) + '/'
          req = urllib2.Request(url, None, headers)
          res = urllib2.urlopen(req, timeout = 5.0).read()
          soup = BeautifulSoup(res, "html.parser")

          spans = soup.select('div[class=zixun_lista]')[0].find_all('a')
          for span in spans:
            address = span['title']
            if u'号' in address or u'弄' in address:
              index += 1
              self.sheet.write(index, 0, address[:address.index(' ')])
        except Exception, e:
          print e
          continue

if __name__ == "__main__":
  if os.path.exists(xlsx):
    print xlsx + u' 已存在, 请使用新的名字！'
    exit()
  global workbook
  workbook = xlsxwriter.Workbook(xlsx)
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  urllib2.install_opener(opener)

  threads = []

  # 创建新线程
  thread1 = myThread(1)
  thread2 = myThread(2)
  thread3 = myThread(3)
  thread4 = myThread(4)

  # 开启线程
  thread1.start()
  thread2.start()
  thread3.start()
  thread4.start()

  # 添加线程到线程列表
  threads.append(thread1)
  threads.append(thread2)
  threads.append(thread3)
  threads.append(thread4)

  # 等待所有线程完成
  for thread in threads:
      thread.join()

  workbook.close()
  print u"完成\a\a"

  raw_input()
