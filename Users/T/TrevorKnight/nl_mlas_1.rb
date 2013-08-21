require 'nokogiri' 
require 'open-uri'

BASE_URL = 'http://www.assembly.nl.ca/members/cms/'
# As of the writing, this page contained a table with Member, District, Phone/Fax, Email
source = BASE_URL + "membersdirectlines.htm"
# And this page, a table with Member, District, Party 
partysource = BASE_URL + "membersalpha.htm"
# On 10 December 2011, the top of both pages said:
# **This page is under construction and numbers and emails will be added as they become available.

main_doc = Nokogiri::HTML(open(source))
party_doc = Nokogiri::HTML(open(partysource))


unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

# Loop through tables on page to find the one with
# to find the one with 'Member' in row 0, column 0
def findTable(doc)
  doc.css('table').each do |table|
    if table.css('tr')[0].css('td')[0].text == 'Member'
      return table
    end
  end
  raise "Could not find member table"
end

# Follow link to personal page to get picture url 
# and address                                     
def findPicture(data, doc)
  # Directory to prepend to relative image links:
  image_tag = doc.at_css('img[src^="photos"]')
  if image_tag
    data['photo_url'] = BASE_URL + image_tag['src']
  else
    puts "No image tag for #{data['name']} #{data['url']}\n#{doc.at_css('#content').inner_html}"
  end
end

# Main
table = findTable(main_doc)
party_table = findTable(party_doc)

table.css('tr:gt(1)').each do |row|
  # Get the data from the table
  cols = row.css('td')
  
  next if cols[0].content.include? "Vacant"
  data = {
    'name' => cols[0].content.gsub(/[[:space:]]+/, ' ').gsub(/, (Q\.C\.|Ph\.D)\z/, ''),
    'district_name' => cols[1].content,
    'offices' => [{
      'tel' => cols[2].children[1].text.strip,
      'fax' => cols[2].children[-1].text.strip,
    }].to_json,
    'email' => cols[3].text,
    
    # these are same for all people
    'elected_office' => 'MHA',
    'source_url' => source
  }

  if cols[0].at_css('a') then 
    sub_html = cols[0].at_css('a')['href']
    data['url'] = BASE_URL + sub_html
    sub_doc = Nokogiri::HTML(open(data['url']))
    findPicture(data, sub_doc)  
  end
  
  # Find the party_name on the party_doc:
  party_table.css('tr:gt(1)').each do |row|
    cols = row.css('td')
    if data['name'] == cols[0].text.gsub(/[[:space:]]+/, ' ').gsub(/, (Q\.C\.|Ph\.D)\z/, '').strip
      data['party_name'] = cols[2].text
    end
  end
  ScraperWiki.save_sqlite(unique_keys=['district_name'], data=data)
end

