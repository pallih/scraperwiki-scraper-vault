# Blank Ruby

require 'mechanize'

a = Mechanize.new()
a.user_agent_alias = "Windows IE 8"

labs_url = 'http://www.scripps.org/services/laboratory-services'
labs = {}
count = 0

page = a.get(labs_url)

page.links_with({ :text => 'Directions' }).each do |p|
  p = p.node.parent()
  tmp = {}
 
  tmp['type'] = p.parent.at_xpath('h3').text
  tmp['area'] = p.parent.at_xpath('h4').text
  tmp['phone'] = p.at_xpath('strong').text.strip

  p.search('text()').each_with_index do |line,index|
    line = line.text.strip
    tmp['name'] = line if index == 0
    tmp['addr1'] = line if index == 2
    tmp['addr2'] = line if index == 3
    tmp['hours'] = line if index == 4
  end
  labs[count] = tmp.clone
  count +=1
end

ScraperWiki::save_sqlite(unique_keys=['phone'], data=labs.values)# Blank Ruby

require 'mechanize'

a = Mechanize.new()
a.user_agent_alias = "Windows IE 8"

labs_url = 'http://www.scripps.org/services/laboratory-services'
labs = {}
count = 0

page = a.get(labs_url)

page.links_with({ :text => 'Directions' }).each do |p|
  p = p.node.parent()
  tmp = {}
 
  tmp['type'] = p.parent.at_xpath('h3').text
  tmp['area'] = p.parent.at_xpath('h4').text
  tmp['phone'] = p.at_xpath('strong').text.strip

  p.search('text()').each_with_index do |line,index|
    line = line.text.strip
    tmp['name'] = line if index == 0
    tmp['addr1'] = line if index == 2
    tmp['addr2'] = line if index == 3
    tmp['hours'] = line if index == 4
  end
  labs[count] = tmp.clone
  count +=1
end

ScraperWiki::save_sqlite(unique_keys=['phone'], data=labs.values)