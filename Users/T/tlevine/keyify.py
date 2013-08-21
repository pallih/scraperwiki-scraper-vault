"Make a key nice to the sqlite datastore"
JUNK=('\t','\n','\r','$',':','.','*',',','(',')',';')
SPACES=(' ',u'\xa0')
import re

def keyify(key):
  #Long spaces
  key=re.sub(r'  +',' ',key)

  #Spaces
  for s in SPACES:
    key=key.replace(s,'_')

  #Junk
  for j in JUNK:
    key=key.replace(j,'')

  key=key.replace('#','num').replace('/','_or_').replace('&','and')

  return key