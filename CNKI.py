# -*- coding: utf-8 -*-
import re              # 正则表达式的包,用来匹配字符串
import requests        # 访问网络
import xlsxwriter      # 写xlsx的包
from lxml import html  # 处理html

if __name__ == '__main__': 
  workbook = xlsxwriter.Workbook('paper.xlsx')  # 新建文件
  sheet = workbook.add_worksheet()              # 添加一个表格
  row = 0                                       # 光标停在第一行,下标从0开始

  s = requests.Session()   # 记住cookie,通过s访问网络

  # 访问网络时带着header
  headers = {
    'Cookie':'ASP.NET_SessionId=iqoga0w3y255xp1hms0yachd; kc_cnki_net_uid=f5b5959a-ce5d-3301-99e0-11a1f20816a5; Ecp_ClientId=2161102231602607984; LID=WEEvREcwSlJHSldRa1FhdkJkdjAzb1J6bnhtYlE2UVZ0Ky80R1pyVDIrND0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4ggI8Fm4gTkoUKaID8j8gFw!!; KNS_DisplayModel=listmode; RsPerPage=50'
  }
  
  for page in range(1,6):
    url = 'http://epub.cnki.net/kns/brief/brief.aspx?curpage=' + str(page) + '&RecordsPerPage=50&QueryID=18&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&ctl=27258ba4-65b5-48ee-8bac-6947a89ad10d#J_ORDER'
    res = s.get(url, headers = headers).content  # 获取网页的内容

    root = html.fromstring(res)                  # 转成html
    papers = root.find_class('fz14')             # 找出类名为fz14的元素
    tdrigtxt = root.findall('.//td[@class="tdrigtxt"]')  # 找出所有类名为tdrigtxt的td元素
    index = 2   # 第一个引用次数的下标
    for paper in papers:
      print 'row', row
      href = paper.get('href')                # 获取关键字页面的链接
      href = href.replace('/kns', 'http://www.cnki.net/KCMS/') # 替换
      text =  re.findall(r"'(.*)'", paper.text_content())[0]  
      name, n = re.subn(r"(<.+?>)", "", text, 5)   # 替换<>标签为空串,替换5次,默认论文题目中会计档案的次数不超过5
      print name.encode('gbk')              # 在cmd输出论文的名字
      sheet.write(row, 0, name)             # 在excel坐标[row, 0]写入论文名
      
      res = s.get(href, headers = headers).content # 获取关键字页面的内容
      root = html.fromstring(res)

      try:  # 这里用try是因为有些论文没有关键字
        keywords = root.find('.//span[@id="ChDivKeyWord"]').findall('a') # 找出所有关键字,每个关键字都是<a>
        keywordList =[keyword.text_content() for keyword in keywords] # 关键字列表
        sheet.write(row, 1, ";".join(keywordList))   # 每个关键字用;分隔,写入excel
      except Exception as e:
        pass

      a = tdrigtxt[index].find('a') # 获取引用次数
      if a != None:
        sheet.write(row, 2, a.text_content())

      index += 3
      row += 1

  workbook.close()  # 关闭表格,保存
