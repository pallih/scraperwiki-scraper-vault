#
# View od DL courses at UoL
# Author: Craig Russell <craig@craig-russell.co.uk>
#

ScraperWiki::attach('dlcourses') 

data = ScraperWiki::select('* FROM dlcourses.swdata')

html = '<table>'

data.each do |course|
  row = '<tr>'
  row += "<td class=\"title\">#{course['title']}</td>"
  row += "<td class=\"level\">#{course['level']}</td>"
  row += "<td class=\"start_dates\">#{course['start_dates']}</td>"
  row += "<td class=\"url\"><a href=\"#{course['url']}\">#{course['url']}</a></td>"
  row += '</tr>'
  html += row
end

html += '</table>'

puts html#
# View od DL courses at UoL
# Author: Craig Russell <craig@craig-russell.co.uk>
#

ScraperWiki::attach('dlcourses') 

data = ScraperWiki::select('* FROM dlcourses.swdata')

html = '<table>'

data.each do |course|
  row = '<tr>'
  row += "<td class=\"title\">#{course['title']}</td>"
  row += "<td class=\"level\">#{course['level']}</td>"
  row += "<td class=\"start_dates\">#{course['start_dates']}</td>"
  row += "<td class=\"url\"><a href=\"#{course['url']}\">#{course['url']}</a></td>"
  row += '</tr>'
  html += row
end

html += '</table>'

puts html