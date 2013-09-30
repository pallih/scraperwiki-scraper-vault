#!/usr/bin/ruby
#
# Beware - there are some page encoding issues yet to be dealt with here

require 'nokogiri'

starting_url = 'http://www.parliament.uk/mps-lords-and-offices/government-and-opposition1/her-majestys-government/'

html = ScraperWiki.scrape(starting_url)
doc = Nokogiri::HTML(html)

skippable = ['The Cabinet', 'Also attending Cabinet meetings', 'Also invited to attend Cabinet meetings when required',
'HM Household', 'Second Church Estates Commissioner, representing Church Commissioners', 'Key']

doc.search('#ctl00_ctl00_SiteSpecificPlaceholder_PageContent_ctlMainBody_wrapperDiv h3').each do |title|
  department = title.content.gsub(/^\W+(.*)\W+$/, '$1').gsub(/^[\302\240|\s]*|[\302\240|\s]*$/, '')
  next if skippable.include?(department)

  potential_table = title
  
  begin 
    potential_table = potential_table.next_sibling 
  end while potential_table.name != 'table'
  
  potential_table.search('tbody tr').each do |row|
    cells = row.search('td')
    if cells.length == 2
      result = {
        'department' => department,
        'title' => row.search('td').first.content.strip,
        'minister' => row.search('td').last.content.gsub(/\(.*\)/, '').gsub('*', '').strip
      }
      ScraperWiki.save(result.keys, result)
    end
  end
  
  
end


#!/usr/bin/ruby
#
# Beware - there are some page encoding issues yet to be dealt with here

require 'nokogiri'

starting_url = 'http://www.parliament.uk/mps-lords-and-offices/government-and-opposition1/her-majestys-government/'

html = ScraperWiki.scrape(starting_url)
doc = Nokogiri::HTML(html)

skippable = ['The Cabinet', 'Also attending Cabinet meetings', 'Also invited to attend Cabinet meetings when required',
'HM Household', 'Second Church Estates Commissioner, representing Church Commissioners', 'Key']

doc.search('#ctl00_ctl00_SiteSpecificPlaceholder_PageContent_ctlMainBody_wrapperDiv h3').each do |title|
  department = title.content.gsub(/^\W+(.*)\W+$/, '$1').gsub(/^[\302\240|\s]*|[\302\240|\s]*$/, '')
  next if skippable.include?(department)

  potential_table = title
  
  begin 
    potential_table = potential_table.next_sibling 
  end while potential_table.name != 'table'
  
  potential_table.search('tbody tr').each do |row|
    cells = row.search('td')
    if cells.length == 2
      result = {
        'department' => department,
        'title' => row.search('td').first.content.strip,
        'minister' => row.search('td').last.content.gsub(/\(.*\)/, '').gsub('*', '').strip
      }
      ScraperWiki.save(result.keys, result)
    end
  end
  
  
end


