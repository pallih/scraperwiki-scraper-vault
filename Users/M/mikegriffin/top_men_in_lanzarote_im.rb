require 'yaml'

ScraperWiki.attach("parse_pdf")
data = ScraperWiki.select( "* from parse_pdf.swdata LIMIT 100" )
puts "<table>"
puts "<tr><th>Place</th><th>Bib #</th><th>Name</th><th>Category</th></tr>"
data.each { |d|
  line = d["line"]
  if out1 = /^\[\(\d+, '(\d+)'\), \(\d+, '(\d+)'\), \(\d+, '(.+?)'\), \(\d+, '(\w+)'\), \(\d+, '(.+?)'\)/.match(line)
    puts "<tr><td>" + out1[1] + "</td><td>" + out1[2] + "</td><td>" + out1[3] + "</td><td>" + out1[5] + "</td></tr>"
  end
}
puts "</table>"
