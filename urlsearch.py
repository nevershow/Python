# -*- coding: utf-8 -*-
import time
import requests
from lxml import etree
from Queue import Queue
requests.packages.urllib3.disable_warnings() # 禁止访问https时warning提示
    
# 输出路径
def printPath(url1, url2, parents):
  print "\nThe path from %s to %s: " % (url1, url2)
  path = [url2]
  parent = parents[url2]
  while bool(parent):  # 路径回溯
    path.append(parent)
    parent = parents[parent]
  path = path[::-1]    # 路径反转
  print "\n-> ".join(path)
    
# 广搜, 并记录每个url的父亲, 以便输出路径
def search(url1, url2):
  visited = set()
  parents = dict()
  parents[url1] = None
  s = requests.Session()
  q = Queue()
  q.put(url1)
  while q.empty() == False:
    currentUrl = q.get()
    try:
      res = s.get(currentUrl)
      print('Search in %s ...' % currentUrl)
      visited.add(currentUrl)
      visited.add(res.url)            # 链接可能会进行重定向
      html = etree.HTML(res.text)
      newurls = html.findall('.//a')  # 找出所有的超链接
      for url in newurls:
        href = url.get('href')
        if href == url2:
          parents[href] = currentUrl
          print('\nFind %s successfully!!!' % url2)
          printPath(url1, url2, parents)
          return
        if href not in visited:
          parents[href] = currentUrl
          q.put(href)
    except Exception as e:
      pass
    
if __name__ == '__main__':
  start = time.time()
  search('http://helpdesk.sysu.edu.cn/', 'http://tv.sysu.edu.cn/')
  print "\nCost time: %f s" % (time.time() - start)
