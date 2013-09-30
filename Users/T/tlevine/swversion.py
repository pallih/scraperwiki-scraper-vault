from scraperwiki.sqlite import execute,commit,save_var,save as swsave,show_tables,select
from time import time

def save(uniques=None,d=None,table_name=None):
  for row in d:
    row["date_extracted"]=t
  swsave(uniques,d,table_name)

def swversion(table_name='swdata'):
  if table_name in show_tables():
    timestamp=select("max(date_extracted) as m from %s;" % table_name)[0]['m']
    execute("ALTER TABLE `%s` RENAME TO `%s_%d`;"%(table_name,table_name,timestamp))
    commit()

def test():
  save([],{"3":5},'test')
  swversion("test")
  print "SQL to select the most current table:"
  print """SELECT * from (SELECT value_blob FROM `swvariables` WHERE name="test_current");"""

#test()from scraperwiki.sqlite import execute,commit,save_var,save as swsave,show_tables,select
from time import time

def save(uniques=None,d=None,table_name=None):
  for row in d:
    row["date_extracted"]=t
  swsave(uniques,d,table_name)

def swversion(table_name='swdata'):
  if table_name in show_tables():
    timestamp=select("max(date_extracted) as m from %s;" % table_name)[0]['m']
    execute("ALTER TABLE `%s` RENAME TO `%s_%d`;"%(table_name,table_name,timestamp))
    commit()

def test():
  save([],{"3":5},'test')
  swversion("test")
  print "SQL to select the most current table:"
  print """SELECT * from (SELECT value_blob FROM `swvariables` WHERE name="test_current");"""

#test()