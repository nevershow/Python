# -*- coding: utf-8 -*-
import re # 使用正则表达式进行替换
    
def most_frequent_words(inputfile):
  # 读取文件内容并转为小写
  article = open(inputfile, 'r').read().lower()
  #将所有非字母字符替换为空格, 分离出单词
  words = re.sub('[^a-z]', ' ', article).split(' ')
    
  # 计算每个单词出现的频率
  count = {}
  for word in words:
    if word == '':
      continue
    if word in count:
      count[word] += 1
    else :
      count[word] = 1

  # count.items() 得到的是一个列表，每个元素都是一个元组
  # 对应每一个元组x，x[0]是单词，x[1]是该单词的频率
  # 频率降序排列, 单词按字典序排列，所以key 先x[1]后x[0]
  # sorted默认是升序排列，所以要用-x[1]
  result = sorted(count.items(), key = lambda x : (-x[1], x[0]))

  # 输出频率最高的10个单词, 输出对齐
  for i in range(10):
    print("%-8s%d" % (result[i][0], result[i][1]))
    
most_frequent_words('python.txt')
