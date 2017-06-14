import os
from pyPdf2 import PdfFileReader, PdfFileWriter

ofs = PdfFileWriter()

for x in os.listdir('.'):
  if x.endswith('.pdf'):
    print x,

    """Example:
      if pages == '1-3 5 7 10-15'
      it will merge page [1,2,3,5,7,10,11,12,13,14,15]
    """
    pages = raw_input('pages to merge')
    L = pages.strip().split(' ')
    add = []
    for l in L:
      if '-' in l:
        begin, end = map(int, l.split('-'))
        add.extend(list(range(begin, end + 1)))
      else:
        add.append(int(l))

    ifs = PdfFileReader(file(x, "rb"))
    for i in add:
      ofs.addPage(ifs.getPage(i - 1))

ofs.write(file('merge.pdf', 'wb'))
