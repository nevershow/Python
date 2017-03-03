# -*- coding: utf-8 -*-
import re
import os
import csv
import sys
import time
import msvcrt
import _winreg
import smtplib
import hashlib
import demjson
import urllib2
import pytesser
import platform
import cookielib
from PIL import Image
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

def get_desktop():
  key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',)
  return _winreg.QueryValueEx(key, "Desktop")[0]

def pwd_input():
  chars = []
  while True:
    newChar = msvcrt.getch()
    if newChar in '\r\n':
      print ''
      break
    elif newChar == ' ':
      continue
    elif newChar == '\b':
      if chars:
        del chars[-1]
        sys.stdout.write('\b')
        sys.stdout.write(' ')
        sys.stdout.write('\b')
    else:
      chars.append(newChar)
      sys.stdout.write('*')
  return ''.join(chars)

class UEMS(object):
  def __init__(self):
    self.coding = 'utf-8'
    self.jxbh2name = {}
    self.canjxbh = []
    self.qiang = []
    self.huan = {}
    if platform.system() == 'Windows':
      self.coding = 'gbk'
    self._user = "719721165@qq.com"
    self._pwd  = "sjgqnbzplyzibbbf"
    self._to   = "huangjw53@mail2.sysu.edu.cn"
    print u'====================================================================\n'
    print u'               Copyright (C) 2016 huangjw'
    print u'               All rights reserved'
    print u'               Contact: huangjw53@mail2.sysu.edu.cn\n'
    print u'====================================================================\n'
    print u'----------------运行过程中按Ctrl C退出或直接关闭窗口----------------'
    print u'--------------点击窗口左上角的白色按钮-->编辑可进行粘贴-------------\n'

    flag = raw_input(u'抢到课后是否进行邮件提醒(y or n): '.encode(self.coding)).strip()
    if flag == 'y' or flag == 'Y':
      self._to = raw_input(u'请输入邮箱: '.encode(self.coding)).strip()

    try:
      user = demjson.decode_file(get_desktop() + '\student.txt')
      for key in user:
        self.stuNum = key
        self.password = user[key]
    except Exception:
      self.stuNum = raw_input(u'请输入学号: '.encode(self.coding)).strip()
      print u'请输入密码: ',
      self.password = pwd_input()
      self.password = hashlib.md5(self.password.encode('utf-8')).hexdigest().upper()

  def login(self):
    # fisrt do url request to get cookie
    # second time do url request, the cookiejar will auto handle the cookie
    print u'连接选课系统...'
    uemsUrl = 'http://uems.sysu.edu.cn/elect/'
    cj = cookielib.CookieJar()
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)));
    firstreq = urllib2.urlopen(uemsUrl)
    self.getCode()

  def getCode(self):
    codeUrl = 'http://uems.sysu.edu.cn/elect/login/code'
    loginUrl = "http://uems.sysu.edu.cn/elect/login"
    print u'加载验证码...'
    while True:
      try:
        open(get_desktop() + "\code.jpeg","wb").write(urllib2.urlopen(codeUrl).read())

        try:
          im = Image.open(get_desktop() + '\code.jpeg').convert('L')
          im = im.point(lambda x:255 if x > 128 else x)
          im = im.point(lambda x:0 if x < 255 else 255)
          box = (2, 2, im.size[0] - 2, im.size[1] - 2)
          im = im.crop(box)
          j_code = pytesser.image_to_string(im).replace(' ', '').replace(']', 'J').replace('0', 'O').strip().upper()
          print u'自动识别验证码...'
        except Exception, e:
          j_code = raw_input(u'请输入桌面的code.jpeg所对应的验证码(不分大小写): '.encode(self.coding)).upper().strip()

        postData = 'username=' + self.stuNum + '&password=' + self.password + '&j_code=' +j_code + '&lt=&_eventId=submit&gateway=true'
        res = urllib2.urlopen(loginUrl, postData)
        html = BeautifulSoup(res.read(), "html.parser")
        self.sid = html.select('input[id=sid]')[0]['value']
        if self.sid != '':
          self.xnd = html.select('input[id=xnd]')[0]['value']
          self.xq = html.select('input[id=xq]')[0]['value']
          print u'登录成功'
          if os.path.exists(get_desktop() + '\student.txt') == False:
            demjson.encode_to_file(get_desktop() + '\student.txt', {self.stuNum : self.password})
            print u'账号密码已存于桌面文件student.txt,下次可直接登录!!!\n'
          break
      except urllib2.HTTPError, e:
        print u'登录失败,重新加载验证码...'
        time.sleep(1.0)

  def getAllCourses(self):
    p = re.compile(r'\d{10,20}')
    try:
      csvfile = file(get_desktop() + u'\教学班号.csv', 'wb')
      writer = csv.writer(csvfile, dialect='excel')
    except IOError, e:
      print u'教学班号.csv已被打开,请先关闭'
      os.system('pause')
      quit()

    print u'\n获取课程信息...'
    writer.writerow([u'教学班号'.encode(self.coding), u'课程名称'.encode(self.coding), u'课程类别'.encode(self.coding), u'时间地点'.encode(self.coding), u'任课教师'.encode(self.coding)])
    for kclb in ['11', '10', '21', '30']:
      writer.writerow(['', '', '', '', ''])
      content = urllib2.urlopen('http://uems.sysu.edu.cn/elect/s/courses?kclb='+kclb+'&xnd='+self.xnd+'&xq='+self.xq+'&fromSearch=false&sid=' + self.sid).read()
      html = BeautifulSoup(content, "html.parser")
      kclb = html.find(id='scrumb').find_all('a')[1].get_text().encode(self.coding)
      allA = html.find_all(href='javascript:void(0)')
      for a in allA:
        jxbh = p.findall(a['onclick'])[0]
        name, number = re.subn(r'<.*?>', '', str(a))
        name = name.decode('utf-8').encode(self.coding)
        td = a.parent.next_sibling.next_sibling
        address, number = re.subn(r'<.*?>', '', str(td))
        address = address.decode('utf-8').encode(self.coding)
        teacher, number = re.subn(r'<.*?>', '', str(td.next_sibling.next_sibling))
        teacher = teacher.decode('utf-8').encode(self.coding)
        self.jxbh2name[jxbh] = name + ' ' + address + ' ' + teacher
        writer.writerow([jxbh, name, kclb, address, teacher])
    csvfile.close()
    self.xqm = html.find(id='xqm')['value']
    print u'所有的课程信息已存入桌面的教学班号.csv中!!!'
    print u'第一列的教学班号默认是用科学计数法表示\n用Excel打开后,选取第一列,右键->设置单元格格式->数值->小数位数设置为0,即可显示正确的教学班号!!!\n'

  def qiangke(self):
    print u'请输入要抢的课在选课系统上对应的教学班号'
    flag = 'y'
    while flag == 'y' :
      s = raw_input(u'请输入要抢的一门课的教学班号: '.encode(self.coding)).strip()
      if len(s) == 13:
        s = '0' + s
      if s in self.jxbh2name.keys():
        self.qiang.append(s)
        print u'要抢的课为 ',
        print self.jxbh2name[s]
        flag = raw_input(u'是否继续输入(y or n): '.encode(self.coding)).strip()
      else:
        print u'该教学班号不存在,请重新输入'

  def huanke(self):
    print u'\nBBB有空位时,退掉AAA换BBB'
    flag = 'y'
    while flag == 'y' :
      s1 = raw_input(u'请输入AAA在选课系统上对应的教学班号: '.encode(self.coding)).strip()
      if len(s1) == 13:
        s1 = '0' + s1
      if s1 not in self.jxbh2name.keys():
        print u'AAA教学班号不存在,请重新输入'
        continue
      print u'AAA为 ',
      print self.jxbh2name[s1]
      s2 = raw_input(u'请输入BBB在选课系统上对应的教学班号: '.encode(self.coding)).strip()
      if len(s2) == 13:
        s2 = '0' + s2
      if s2 not in self.jxbh2name.keys():
        print u'BBB教学班号不存在,请重新输入'
        continue
      print u'BBB为 ',
      print self.jxbh2name[s2]
      self.huan[s1] = s2
      flag = raw_input(u'是否继续输入(y or n): '.encode(self.coding)).strip()

  def inputCourse(self):
    print u'''输入字母代号后回车
    q : 抢课(指定的一门课有空位时直接选课)
    h : 换课(BBB有空位时,退掉AAA换BBB)
    qh: 抢课 + 换课
    '''
    wanted = raw_input(u'请输入您想要的操作: '.encode(self.coding)).strip()
    while wanted not in ['q', 'h', 'qh']:
       wanted = raw_input(u'请重新输入： '.encode(self.coding)).strip()

    if 'q' in wanted:
      self.qiangke()
    if 'h' in wanted:
      self.huanke()

  def getCanJxbh(self):
    p = re.compile(r'\d{10,20}')
    for kclb in ['11', '10', '21', '30']:
      content = urllib2.urlopen('http://uems.sysu.edu.cn/elect/s/courses?kclb='+kclb+'&xqm='+self.xqm+'&sort=&ord=&xnd='+self.xnd+'&xq='+self.xq+'&sid='+self.sid+'&conflict=&blank=1&hides=&fromSearch=false&kcmc=&sjdd=&kkdw=&rkjs=&skyz=&xf1=&xf2=&sfbyb=').read()
      html = BeautifulSoup(content, "html.parser")
      cancourses = html.find_all('a', attrs={'class':'a-elect'})
      for a in cancourses:
        self.canjxbh.append(a['jxbh'])

  def run(self):
    ct = 1
    while (self.qiang != [] or self.huan != {}) :
      i = os.system('cls')
      print  u'---------------第%d次刷课--------------' % ct
      ct = ct + 1

      for jxbh in self.qiang:
        if self.select(jxbh) == True:
          self.qiang.remove(jxbh)

        if self.huan != {}:
          self.getCanJxbh()
          for jxbh1 in self.huan.keys():
            if (self.huan[jxbh1] in self.canjxbh) :
              self.unselect(jxbh1)
            if self.select(self.huan[jxbh1]) == False :
              self.select(jxbh1)
            else :
              del self.huan[jxbh1]
      time.sleep(0.1)

    print u'本次抢课目标已完成!!!请登录选课系统查看结果\a\a'

  def select(self, jxbh) :
    postdata = 'jxbh=' + jxbh + '&sid=' + self.sid
    res = urllib2.urlopen('http://uems.sysu.edu.cn/elect/s/elect', postdata)
    for key in res:
      p = re.compile(r';:(\d)')
      if (p.search(key).group(1) == '0'):
        print self.jxbh2name[jxbh],
        print u' 抢课成功!!!\n\a\a'
        self.sendEmail(self.jxbh2name[jxbh].decode(self.coding).encode('utf-8'))
        return True
      else :
        return False
      # 已选再选<html><body><textarea>{&#034;err&#034;:{&#034;code&#034;:9,&#034;caurse&#034;:null,&#034;message&#034;:null},&#034;code&#034;:0}</textarea></body></html>
      # 上限 <html><body><textarea>{&#034;err&#034;:{&#034;code&#034;:1,&#034;caurse&#034;:null,&#034;message&#034;:null},&#034;code&#034;:0}</textarea></body></html>
      # 成功 <html><body><textarea>{&#034;err&#034;:{&#034;code&#034;:0,&#034;caurse&#034;:null,&#034;message&#034;:null},&#034;code&#034;:0}</textarea></body></html>
      # 没注册 <html><body><textarea>{&#034;err&#034;:{&#034;code&#034;:5,&#034;caurse&#034;:null,&#034;message&#034;:null},&#034;code&#034;:0}</textarea></body></html>

  def unselect(self, jxbh) :
    postdata = 'jxbh=' + jxbh + '&sid=' + self.sid
    res = urllib2.urlopen('http://uems.sysu.edu.cn/elect/s/unelect', postdata)
    for key in res:
      p = re.compile(r';:(\d)')
      if (p.search(key).group(1) == '0'):
        print self.jxbh2name[jxbh],
        print u' 退课成功!!!\n\a\a'
        return True
      else :
        return False

  def sendEmail(self, coursename):
    try:
      msg = MIMEText(coursename + " 抢课成功！！！", "plain", "utf-8")
      msg["Subject"] = "Congratulation！！！"
      msg["From"]    = self._user
      msg["To"]      = self._to

      s = smtplib.SMTP_SSL("smtp.qq.com", 465)
      s.login(self._user, self._pwd)
      s.sendmail(self._user, self._to, msg.as_string())
      s.close()
    except Exception, e:
      pass

if __name__ == "__main__":
  obj = UEMS()
  obj.login()
  obj.getAllCourses()
  obj.inputCourse()

  while True:
    try:
      obj.run()
      break
    except urllib2.HTTPError, e:
      print u'连接已断开,重新登录...'
      obj.getCode()
    except urllib2.URLError, e:
      print u'网络出现问题,连接超时,请重新运行'
      obj.getCode()
  os.system("pause")
