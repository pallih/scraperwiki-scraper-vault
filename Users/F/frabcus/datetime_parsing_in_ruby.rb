puts Date.parse('21 June 2010') # 2010-06-21
puts Date.parse('10-Jul-1899')  # 1899-07-10
puts Date.parse('01/01/01')     # 2001-01-01

puts Date.parse('21 June 2010').class # Date


puts Time.parse('Tue 27 Sep 2011 00:25:48 BST') # 2011-09-27 00:25:48 0100
puts Time.parse('21 June 2010 6am').class # Time

puts Date.parse('3/2/1999') # 1999-02-03
puts Date.strptime('3/2/1999', '%m/%d/%Y') # 1999-03-02


birth_date = Date.parse('1/2/1997 9pm')
birth_time = Time.parse('1/2/1997 9pm') 
data = { 
    :name => 'stilton', 
    :birth_datetime => birth_date,
    :birth_date => birth_time
}
ScraperWiki.save_sqlite(unique_keys=['name'], data=data)
puts Date.parse('21 June 2010') # 2010-06-21
puts Date.parse('10-Jul-1899')  # 1899-07-10
puts Date.parse('01/01/01')     # 2001-01-01

puts Date.parse('21 June 2010').class # Date


puts Time.parse('Tue 27 Sep 2011 00:25:48 BST') # 2011-09-27 00:25:48 0100
puts Time.parse('21 June 2010 6am').class # Time

puts Date.parse('3/2/1999') # 1999-02-03
puts Date.strptime('3/2/1999', '%m/%d/%Y') # 1999-03-02


birth_date = Date.parse('1/2/1997 9pm')
birth_time = Time.parse('1/2/1997 9pm') 
data = { 
    :name => 'stilton', 
    :birth_datetime => birth_date,
    :birth_date => birth_time
}
ScraperWiki.save_sqlite(unique_keys=['name'], data=data)
