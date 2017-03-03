# -*- coding: utf-8 -*-
import os
import urllib2
import multiprocessing
from bs4 import BeautifulSoup
from multiprocessing import cpu_count

headers = {
  'Host': 'www.sysu.edu.cn',
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
  'Accept-Language': 'zh-CN,zh;q=0.8'
}

def main():
  headers['Referer'] = 'http//www.sysu.edu.cn/2012/en/news/news06/index.htm'
  req = urllib2.Request('http://www.sysu.edu.cn/2012/en/news/index.htm', None, headers)
  res = urllib2.urlopen(req).read()
  soup = BeautifulSoup(res, "html.parser")
  h5s = soup.find_all('h5')
  h5s.pop()
  #维持执行的进程总数为cpu_count,当一个进程执行完毕后会添加新的进程进去
  pool = multiprocessing.Pool(processes = cpu_count())
  for h5 in h5s:
    pool.apply_async(subprocess, (h5,))

  pool.close()
  pool.join()   #join函数等待所有子进程结束

def getNews(folder, Referer, url):
  headers['Referer'] = Referer
  req = urllib2.Request(Referer[:Referer.rindex('/')] + '/' + url, None, headers)
  res = urllib2.urlopen(req).read()
  soup = BeautifulSoup(res, 'html.parser')
  news = soup.select('div[class=encont]')[0]

  with open(folder + '/' + url.replace('htm', 'txt'), 'w') as fs:
    fs.write(news.get_text().encode('utf8'))

def subprocess(h5):
  folder = h5.get_text().replace('more', '')
  if os.path.exists(folder) == False:
    os.mkdir(folder)
  href = h5.find_all('a')[0]['href']

  index = href[:href.index('.')]
  i = 0
  while True:
    try:
      if i == 0:
        Referer = 'http://www.sysu.edu.cn/2012/en/news/' + index + '.htm'
      else:
        Referer = 'http://www.sysu.edu.cn/2012/en/news/' + index + str(i) + '.htm'

      res = urllib2.urlopen(Referer).read()
      soup = BeautifulSoup(res, "html.parser")
      newslist = soup.select('li')
      for li in newslist:
        url = li.select('a')[0]['href']
        print folder, url
        getNews(folder, Referer, url)

      i += 1
    except urllib2.HTTPError, e:
      if e.code == 404:
        break

if __name__ == '__main__':
  multiprocessing.freeze_support()
  main()
