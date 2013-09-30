from scraperwiki.sqlite import save_var,execute,commit,show_tables
import os

if "swvariables" in show_tables():
  execute("DROP TABLE swvariables;")

before=set(os.listdir('.'))
save_var('foo','bar')
#os.system('rm *.pyc')
after=set(os.listdir('.'))

#print before-after
#print after
s=[]
for f in after:
  if f[0:4]!='data' and f[-3:-1]!='pyc':
    s.append(f)

print s

baz=[]
baz.append('script.rb')
baz.append('.cache')
for f in baz:
  print open(f).read()
from scraperwiki.sqlite import save_var,execute,commit,show_tables
import os

if "swvariables" in show_tables():
  execute("DROP TABLE swvariables;")

before=set(os.listdir('.'))
save_var('foo','bar')
#os.system('rm *.pyc')
after=set(os.listdir('.'))

#print before-after
#print after
s=[]
for f in after:
  if f[0:4]!='data' and f[-3:-1]!='pyc':
    s.append(f)

print s

baz=[]
baz.append('script.rb')
baz.append('.cache')
for f in baz:
  print open(f).read()
