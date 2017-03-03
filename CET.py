# -*- coding:utf-8 -*-
import time
import requests

# south 440010
# north 440011
# zhu 440012
# east 440013
class CET():
   def __init__(self):
      self.stuId = ''
      self.year = 2016
      self.mon = 12
      print u'----------查询 %d 年 %d 月四六级成绩----------\n' % (self.year, self.mon)

   def printScore(self, res):
      cet = {'1' : u'英语四级', '2' : u'英语六级'}
      L = res.split(',')
      print u'\n考生姓名:   ', L[6]
      print u'学校:       ', L[5]
      print u'考试类别:   ', cet[self.stuId[9]]
      print u'准考证号:   ', self.stuId
      print u'\n总分:       ', L[4]
      print u'听力:       ', L[1]
      print u'阅读:       ', L[2]
      print u'写作和翻译: ', L[3]


   def tryQuery(self):
      print u'\n尝试暴力查询中,请耐心等待...'
      s = requests.Session()
      school = '440013'
      four_six = '2'
      stuId = school + '162' + four_six
      for room in range(1,250):
         print u'尝试第 %d 考场...' % room
         for num in range(1,31):
            Id = (stuId + '%03d' + '%02d') % (room, num)
            try:
               res = s.post('http://cet.99sushe.com/getscore' + Id, data = {'id':Id, 'name': '%CB%D5%CF%FE'}).content
               print "here", res
               raw_input()
               if res[0] != '3':
                  print u'\n----------查询到相似考生成绩!!!----------\a',
                  self.stuId = Id
                  self.printScore(res)
                  print u'-----------------------------------------'
                  print u'\n可能为同名考生,是否继续查询(y or n):',
                  flag = raw_input()
                  if flag != 'y' and flag != 'Y':
                     return
            except Exception, e:
               print e

obj = CET()
obj.tryQuery()
