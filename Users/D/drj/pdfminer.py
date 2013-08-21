import os

import pdfminer
d=os.path.dirname(pdfminer.__file__)
f=os.path.join(d, 'pdfparser.py')

for i,line in enumerate(open(f), start=1):
    if 420 < i < 426:
        print i, line.rstrip()
