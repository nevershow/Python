# -*- coding: utf-8 -*-
import myMD5
import hashlib
import platform

if __name__ == '__main__':
  if platform.python_version()[0] == '3':
    print(u'请使用Python2.7 运行程序')
    input()
    quit()
  print('Test string...')
  assert myMD5.md5('') == hashlib.md5('').hexdigest()
  assert myMD5.md5('a') == hashlib.md5('a').hexdigest()
  assert myMD5.md5('test') == hashlib.md5('test').hexdigest()
  assert myMD5.md5('Web security') == hashlib.md5('Web security').hexdigest()
  assert myMD5.md5('longstr'*1000) == hashlib.md5('longstr'*1000).hexdigest()
  print('Pass string test!')
  print('Test binary file...')
  with open('MD5report.pdf', 'rb') as f:
    MD5 = hashlib.md5()
    MD5.update(f.read())
    assert myMD5.md5('MD5report.pdf', isFile = True) == MD5.hexdigest()
  print('Pass file test!')
