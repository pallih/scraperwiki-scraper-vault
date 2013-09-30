require 'rubygems'
require 'open-uri'
require 'nokogiri'
require 'mechanize'

def vendor_scrape (new_table)
  trs = new_table.search('tr')

  for tr in trs[5..-3]
    cells = tr.search('td,th')
    values = cells.map{|cell| cell.text}
    data = Hash[COLNAMES.zip(values)]
    #puts data
    ScraperWiki.save([],data)
  end
end

COLNAMES = [
    'name','entity','address'
]

agent = Mechanize.new
page = agent.get('http://slnx-prd-web.nyc.gov/cfb/cfbSearch.nyc?method=search')

vendor_form = page.form('cfbSearchForm')

# search term
vendor_form.lastName = 'd'

page = agent.submit(vendor_form)

tables = page.search('table')


# grabbing the number of pages
last_table = tables[-1].search('.table_text').text()

regex = /of [\d]+/
mtch = last_table.match(regex)
total_pages = mtch[0].gsub(/of[\s]+/, "")
total_pages = total_pages.to_i 


# store data from page 1 of the results
table = tables[2]

vendor_scrape(table)



# scrape pages if more than 1

(2..total_pages).each do |page_num|
  if (page_num % 5 == 1)
    new_page = agent.page.link_with(:text => "next>>" ).click
    puts page_num
    new_tables = new_page.search('table')

    # store data from each of the results
    table = tables[2]
    vendor_scrape(table)
  else
    new_page = agent.page.link_with(:text => page_num.to_s ).click
    puts page_num
    new_tables = new_page.search('table')

    # store data from each of the results
    table = tables[2]
    vendor_scrape(table)
  end
end
require 'rubygems'
require 'open-uri'
require 'nokogiri'
require 'mechanize'

def vendor_scrape (new_table)
  trs = new_table.search('tr')

  for tr in trs[5..-3]
    cells = tr.search('td,th')
    values = cells.map{|cell| cell.text}
    data = Hash[COLNAMES.zip(values)]
    #puts data
    ScraperWiki.save([],data)
  end
end

COLNAMES = [
    'name','entity','address'
]

agent = Mechanize.new
page = agent.get('http://slnx-prd-web.nyc.gov/cfb/cfbSearch.nyc?method=search')

vendor_form = page.form('cfbSearchForm')

# search term
vendor_form.lastName = 'd'

page = agent.submit(vendor_form)

tables = page.search('table')


# grabbing the number of pages
last_table = tables[-1].search('.table_text').text()

regex = /of [\d]+/
mtch = last_table.match(regex)
total_pages = mtch[0].gsub(/of[\s]+/, "")
total_pages = total_pages.to_i 


# store data from page 1 of the results
table = tables[2]

vendor_scrape(table)



# scrape pages if more than 1

(2..total_pages).each do |page_num|
  if (page_num % 5 == 1)
    new_page = agent.page.link_with(:text => "next>>" ).click
    puts page_num
    new_tables = new_page.search('table')

    # store data from each of the results
    table = tables[2]
    vendor_scrape(table)
  else
    new_page = agent.page.link_with(:text => page_num.to_s ).click
    puts page_num
    new_tables = new_page.search('table')

    # store data from each of the results
    table = tables[2]
    vendor_scrape(table)
  end
end
