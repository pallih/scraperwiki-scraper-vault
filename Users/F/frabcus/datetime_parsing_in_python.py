import dateutil.parser
print dateutil.parser.parse('21 June 2010').date() # 2010-06-21
print dateutil.parser.parse('10-Jul-1899').date()  # 1899-07-10
print dateutil.parser.parse('01/01/01').date()     # 2001-01-01

print dateutil.parser.parse('21 June 2010').date().__class__ # <type 'datetime.date'>



print dateutil.parser.parse('Tue 27 Sep 2011 00:25:48') # 2011-09-27 00:25:48
print dateutil.parser.parse('21 June 2010 6am').__class__ # <type 'datetime.datetime'>


print dateutil.parser.parse('3/2/1999').date() # 1999-03-02
print dateutil.parser.parse('3/2/1999', dayfirst=True).date() # 1999-02-03
import datetime
print datetime.datetime.strptime('3/2/1999', '%d/%m/%Y').date() # 1999-02-03


import scraperwiki
birth_datetime = dateutil.parser.parse('1/2/1997 9pm') 
data = { 
    'name':'stilton', 
    'birth_datetime' : birth_datetime,
    'birth_date' : birth_datetime.date()
}
scraperwiki.sqlite.save(unique_keys=['name'], data=data)

