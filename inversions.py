import math

def MergeAndCount(A, B):
  count = 0
  res = []
  while len(A) and len(B):
    if A[0] > B[0]:
      count += len(A)
      res.append(B.pop(0))
    else:
      res.append(A.pop(0))
  res += A + B
  return count, res

def SortAndCount(L):
  if len(L) < 2:
    return 0, L
  n = int(math.ceil(len(L) / 2.0))
  A = L[:n]
  B = L[n:]
  ra, A = SortAndCount(A)
  rb, B = SortAndCount(B)
  r, L = MergeAndCount(A, B)
  return ra + rb + r, L

if __name__ == '__main__':
  print SortAndCount([2,4,1,3,5])
