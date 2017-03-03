def fact(n):
   if n < 2:
      return 1
   return n * fact(n - 1)

def power(a, n):
   if n == 0:
      return 1
   return a * power(a, n - 1)

def hanoi(_from, _to, temp, n):
   if n == 1:
      print("move disk %d from %d to %d" % (n, _from, _to))
   else:
      hanoi(_from, temp, _to, n - 1)
      print("move disk %d from %d to %d" % (n, _from, _to))
      hanoi(temp, _to, _from, n - 1)

hanoi(1, 2, 3, 3)
