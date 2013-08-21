import scraperwiki
import dateutil.parser

print dateutil.parser.parse('21 June 2010').date()
print dateutil.parser.parse('10-Jul-1899').date()

print dateutil.parser.parse('3/2/1999').date()

birth_datetime = dateutil.parser.parse('1/2/1997 9pm')
data = {
    'name':'stilton',
    'birth_datetime' : birth_datetime,
    'birth_date' : birth_datetime.date()
}
scraperwiki.sqlite.save(unique_keys=['name'],data=data)