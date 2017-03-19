# -*- coding: utf-8 -*-
import math
import struct
F = lambda x, y, z: (x&y)|((~x)&z)   # return z if x == 0 else y
G = lambda x, y, z: (x&z)|(y&(~z))   # return y if z == 0 else x
H = lambda x, y, z: x^y^z
I = lambda x, y, z: y^(x|(~z))
int32 = lambda x: x & 0xffffffff     # 把整数x转为32位整数
rotating = lambda x, s: int32(x << s) | (int32(x) >> (32 - s)) # x循环左移s位
littleEndian = lambda hexs: hexs.decode('hex')[::-1].encode('hex') # 转化为小端
roundOp = lambda a,b,c,d,k,s,i,fun: b + rotating(a+fun(b,c,d)+X[k]+T[i], s)

# 对信息进行位扩展, 每次按一个字节8位扩展添加对应的字符
def extend(msg):
  bitslen = len(msg) << 3
  hexlen = littleEndian(hex(bitslen)[2:].zfill(16))
  extlen = [chr(int(hexlen[i:i+2], 16)) for i in range(0, 16, 2)]
  mod = bitslen % 512
  padding = chr(0x80) + chr(0) * ((mod >= 448) * 64 + 55 - (mod >> 3))
  return msg + padding + ''.join(extlen)

# 将4轮操作统一成一个函数, 通过改变fun调用对应的操作
def Round(kstep, k, ss, i, fun):
  global A, B, C, D
  for j in range(4):
    A = roundOp(A,B,C,D, k, ss[0], i, fun)
    D = roundOp(D,A,B,C, (k + kstep) % 16, ss[1], i + 1, fun)
    C = roundOp(C,D,A,B, (k + kstep * 2) % 16, ss[2], i + 2, fun)
    B = roundOp(B,C,D,A, (k + kstep * 3) % 16, ss[3], i + 3, fun)
    k, i = (k + kstep * 4) % 16, i + 4

def md5(s, isFile = False):
  global X, T, A, B, C, D
  msg = extend(open(s, 'rb').read() if isFile else s)
  # 小端规则 在内存中为01 23 45 67这种形式
  A, B, C, D = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
  T = tuple(int(4294967296*abs(math.sin(x))) for x in range(65))
  for b in range(0, len(msg), 64):  # 每64个字节分为一组
    # 每4个字节转化为一个32位整数存进X
    X = tuple(struct.unpack('i', msg[b+j:b+j+4])[0] for j in range(0, 64, 4))
    AA, BB, CC, DD, i = A, B, C, D, 1
    Round(1, 0, (7, 12, 17, 22), i, F)       # Round 1
    Round(5, 1, (5, 9, 14, 20), i + 16, G)   # Round 2
    Round(3, 5, (4, 11, 16, 23), i + 32, H)  # Round 3
    Round(7, 0, (6, 10, 15, 21), i + 48, I)  # Round 4
    A, B, C, D = int32(A+AA), int32(B+BB), int32(C+CC), int32(D+DD)

  return ''.join(littleEndian(hex(i)[2:-1].zfill(8)) for i in (A,B,C,D))
