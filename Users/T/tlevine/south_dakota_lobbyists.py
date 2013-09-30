from scraperwiki.sqlite import save,select,show_tables
from scraperwiki import swimport
from urllib2 import urlopen

URL='http://scraperwiki.googlegroups.com/attach/099c268891118d8b/lobbyist-copy.csv?gda=dN3sHEUAAACaS4Fh0ZJCRC3BojBob2aJbvC7uMekdu4RlfG8XwaJ6NZLWrsOmDHSknbFU_0yOjKO3f1cykW9hbJ1ju6H3kglGu1iLHeqhw4ZZRj3RjJ_-A&part=4'

def main():
  if 'splitnames' in show_tables():
    print "Already finished"
  elif 'lobbyists' in show_tables():
    parsenames()
  else:
    download()
    parsenames()

def download():
  csv=urlopen(URL)
  d=swimport('csv2sw').csv2json(csv)
  save([],d,'lobbyists')

class NameDelimiterError(Exception):
  pass

def parsenames():
  d=select('`Lobbyist_Name` as "full_name" from `lobbyists`')
  for lobbyist in d:
    splitname=lobbyist['full_name'].split(', ')
    l=len(splitname)
    if l==2:
      lobbyist['last_name'],lobbyist['first_name']=splitname
    elif l==3:
      lobbyist['last_name'],lobbyist['suffix'],lobbyist['first_name']=splitname
    else:
      raise NameDelimiterError("This name has %d commas."%l-1)
  save([],d,'splitnames')

main()from scraperwiki.sqlite import save,select,show_tables
from scraperwiki import swimport
from urllib2 import urlopen

URL='http://scraperwiki.googlegroups.com/attach/099c268891118d8b/lobbyist-copy.csv?gda=dN3sHEUAAACaS4Fh0ZJCRC3BojBob2aJbvC7uMekdu4RlfG8XwaJ6NZLWrsOmDHSknbFU_0yOjKO3f1cykW9hbJ1ju6H3kglGu1iLHeqhw4ZZRj3RjJ_-A&part=4'

def main():
  if 'splitnames' in show_tables():
    print "Already finished"
  elif 'lobbyists' in show_tables():
    parsenames()
  else:
    download()
    parsenames()

def download():
  csv=urlopen(URL)
  d=swimport('csv2sw').csv2json(csv)
  save([],d,'lobbyists')

class NameDelimiterError(Exception):
  pass

def parsenames():
  d=select('`Lobbyist_Name` as "full_name" from `lobbyists`')
  for lobbyist in d:
    splitname=lobbyist['full_name'].split(', ')
    l=len(splitname)
    if l==2:
      lobbyist['last_name'],lobbyist['first_name']=splitname
    elif l==3:
      lobbyist['last_name'],lobbyist['suffix'],lobbyist['first_name']=splitname
    else:
      raise NameDelimiterError("This name has %d commas."%l-1)
  save([],d,'splitnames')

main()