# -*- coding: utf-8 -*-
import time
import random
  
def qsort(L):  
  return L if len(L) <= 1 else qsort([l for l in L[1:] if l < L[0]]) + [L[0]] + qsort([g for g in L[1:] if g >= L[0]])

if __name__ == '__main__':
  L = list(range(1000000))
  random.shuffle(L)
  temp = L[:]

  start = time.time()
  L.sort()
  end = time.time()
  print end - start
  
  start = time.time()
  qsort(temp)
  end = time.time()
  print end - start
