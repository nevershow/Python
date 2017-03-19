# -*- coding: utf-8 -*-
import math
import random

# 扩展欧几里得算法
gcd = lambda a, b: gcd(b, a % b) if b else a
def exGCD(a, b, x, y):
  if b == 0:
    return a, 1, 0
  r, t, y = exGCD(b, a % b, x, y)
  x, y = y, t - a / b * y
  return r, x, y

# 快速幂取模
def quickPowMod(a, n, m):
  ans = 1
  while n:
    if n & 1:
      ans = ans * a % m
    a = a * a % m
    n >>= 1
  return ans   # a^n % m

# 米勒-罗宾算法
def Miller_Rabin(n):
  r, d = 0, n - 1
  while d & 1 == 0:
    r += 1
    d >>= 1
  
  for k in range(5):
    a = random.randint(2, n-2)
    x = quickPowMod(a, d, n)
    if x == 1 or x + 1 == n:
      continue
    for i in range(r - 1):
      x = x * x % n
      if x == 1:
        return False
      if x + 1 == n:
         break

    if x + 1 != n:
      return False
  
  return True

# 米勒-罗宾算法求大质数
def getBigPrime(n):
  while 1:
    if Miller_Rabin(n):
      return n
    n += 2

if __name__ == '__main__':
  p = getBigPrime(random.randrange(10,30,2)**random.randint(150,160) + 1)
  q = getBigPrime(p + 2)
  N = p * q
  fN = (p - 1) * (q - 1)
  e = random.randrange(100,1000,2) + 1
  while 1:
    if gcd(fN, e) == 1:
      break
    e += 2
  d = (exGCD(e, fN, 1, 0)[1] + fN) % fN

  # plain = open('myRSA.py', 'r').read()
  plain = u"test RSA"
  a = map(ord, plain)
  b = [quickPowMod(i, e, N) for i in a]
  print ''.join(map(chr, [quickPowMod(i, d, N) for i in b]))
