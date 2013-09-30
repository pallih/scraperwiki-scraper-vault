# 
sourcescraper = "money_of_akb48_sosenkyo_3"
limit = 100
offset = 0

# connect to the source database giving it the name src
ScraperWiki.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = ScraperWiki.select("* from src.swdata order by 'order' asc limit ? offset ?", [limit, offset])
#p sdata

class Fixnum
  def to_money
    self.to_s.gsub(/(\d)(?=(?:\d\d\d)+(?!\d))/, '\1,')
  end
end

print '<h2>money of AKB sosenkyo 3</h2>'
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>"
print "<th>money(yen)</th>"
print "<th>order</th>"
print "<th>name</th>"
print "<th>votes</th>"
print "</tr>\n"

# rows
sdata.each do |row| 
    print "<tr>"
    print "<td align='right'>", row['money'].to_money, "</td>"
    print "<td align='right'>", row['order'].to_s, "</td>"
    print "<td>", row['name'].to_s, "</td>"
    print "<td align='right'>", row['votes'].to_money, "</td>"
    print "</tr>\n"
end
    
print "</table>"
# 
sourcescraper = "money_of_akb48_sosenkyo_3"
limit = 100
offset = 0

# connect to the source database giving it the name src
ScraperWiki.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = ScraperWiki.select("* from src.swdata order by 'order' asc limit ? offset ?", [limit, offset])
#p sdata

class Fixnum
  def to_money
    self.to_s.gsub(/(\d)(?=(?:\d\d\d)+(?!\d))/, '\1,')
  end
end

print '<h2>money of AKB sosenkyo 3</h2>'
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>"
print "<th>money(yen)</th>"
print "<th>order</th>"
print "<th>name</th>"
print "<th>votes</th>"
print "</tr>\n"

# rows
sdata.each do |row| 
    print "<tr>"
    print "<td align='right'>", row['money'].to_money, "</td>"
    print "<td align='right'>", row['order'].to_s, "</td>"
    print "<td>", row['name'].to_s, "</td>"
    print "<td align='right'>", row['votes'].to_money, "</td>"
    print "</tr>\n"
end
    
print "</table>"
