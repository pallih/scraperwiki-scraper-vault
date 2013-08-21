import os


f = open('floo.r', 'w')
f.write('#!/usr/bin/env Rscript\nprint(rnorm(100))')
f.close()

os.system('Rscript floo.r')
