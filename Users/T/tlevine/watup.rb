require "open-uri"
require "nokogiri"

page = open ("http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm")
puts page.read

n=Nokogiri::HTML(page)
tables=n.search('table')
table=tables[2]

rows=table.search('tr')
row=rows[6]

cells=row.search('td p')
for cell in cells
  celltext=cell.text

  puts cell
  puts celltext
end

ScraperWiki.save([],{"o"=>4})require "open-uri"
require "nokogiri"

page = open ("http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm")
puts page.read

n=Nokogiri::HTML(page)
tables=n.search('table')
table=tables[2]

rows=table.search('tr')
row=rows[6]

cells=row.search('td p')
for cell in cells
  celltext=cell.text

  puts cell
  puts celltext
end

ScraperWiki.save([],{"o"=>4})