###############################################################################
# START HERE: scrap Zoho Books (needs your account user + pwd)
###############################################################################
require 'nokogiri'
require 'open-uri'
require 'mechanize'

BASE_URL = 'http://www.zoho.com/books/'
BASE_LOGIN ='https://accounts.zoho.com/login?servicename=ZohoBooks&hide_signup=true&serviceurl=http%3A%2F%2Fbooks.zoho.com%3A80'

m = Mechanize.new
m.history.max_size = 0
m.user_agent_alias = 'Mac Safari'
page = m.get(BASE_LOGIN)
puts page

login_form = page.form('login')
login_form.fields.each do |f|
  puts f.name
end

login_form.field_with(:name => "lid").value = "abeauvois@entropic-synergies.com"
login_form.field_with(:name => 'pwd').value = "xela06"

page = m.submit(login_form)
page.links.each do |link|
  puts link.text
end
puts page.body
#puts login_form.(:name => "lid").value


=begin
# define the order our columns are displayed in the datastore
ScraperWiki.save_var('data_columns', ['ID','model','power', 'version', 'price', 'mileage','year'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  i=0
  data_table = page.css('table#TabAnn').collect do |row|
  while (i<19) 
    i=i+1
    sel="tr#ul_"+"#{i}"
    selv="tr#ul_"+"#{i}b"
    record = {}
    record ['model'] = 'Lotus Exige'
    record['version'] = row.css(selv).css('td.lcversion').inner_text.strip() #gsub(/\s/,'')
    record['power'] = record['version'].scan(/[^\s]*(280|260|243|221|192|179)[^@]*/).flatten[0]
    row_data = row.css(sel)
    
    record['mileage']     = row_data.css('td.lcmileage').inner_text.strip().gsub(/\s/,'')
    record['price']  = row_data.css('td.lcprice').inner_text.strip().gsub(/\u20AC/,'').gsub(/\s/,'')
    record['year'] = row_data.css('td.lcyear').inner_text.strip()
    record ['ID'] = record['version'] + record['price']
    # Print out the data we've gathered
    puts record
  end

    # Finally, save the record to the datastore - 'Artist' is our unique key
    #ScraperWiki.save("ID", record)
    ScraperWiki.save_sqlite(unique_keys=["ID"], record)
p ScraperWiki.show_tables()


  end
end

#        scrape_and_look_for_next_link(starting_url)

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    scrape_table(page)
    next_link = page.at_css('a.next')
    if next_link 
      puts next_link
      next_url = BASE_URL + next_link['href']
      puts next_url
      scrape_and_look_for_next_link(next_url)
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL #+ 'example_table_1.html'
#scrape_and_look_for_next_link(starting_url)
scrape_table(Nokogiri::HTML(open(starting_url)))
=end###############################################################################
# START HERE: scrap Zoho Books (needs your account user + pwd)
###############################################################################
require 'nokogiri'
require 'open-uri'
require 'mechanize'

BASE_URL = 'http://www.zoho.com/books/'
BASE_LOGIN ='https://accounts.zoho.com/login?servicename=ZohoBooks&hide_signup=true&serviceurl=http%3A%2F%2Fbooks.zoho.com%3A80'

m = Mechanize.new
m.history.max_size = 0
m.user_agent_alias = 'Mac Safari'
page = m.get(BASE_LOGIN)
puts page

login_form = page.form('login')
login_form.fields.each do |f|
  puts f.name
end

login_form.field_with(:name => "lid").value = "abeauvois@entropic-synergies.com"
login_form.field_with(:name => 'pwd').value = "xela06"

page = m.submit(login_form)
page.links.each do |link|
  puts link.text
end
puts page.body
#puts login_form.(:name => "lid").value


=begin
# define the order our columns are displayed in the datastore
ScraperWiki.save_var('data_columns', ['ID','model','power', 'version', 'price', 'mileage','year'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  i=0
  data_table = page.css('table#TabAnn').collect do |row|
  while (i<19) 
    i=i+1
    sel="tr#ul_"+"#{i}"
    selv="tr#ul_"+"#{i}b"
    record = {}
    record ['model'] = 'Lotus Exige'
    record['version'] = row.css(selv).css('td.lcversion').inner_text.strip() #gsub(/\s/,'')
    record['power'] = record['version'].scan(/[^\s]*(280|260|243|221|192|179)[^@]*/).flatten[0]
    row_data = row.css(sel)
    
    record['mileage']     = row_data.css('td.lcmileage').inner_text.strip().gsub(/\s/,'')
    record['price']  = row_data.css('td.lcprice').inner_text.strip().gsub(/\u20AC/,'').gsub(/\s/,'')
    record['year'] = row_data.css('td.lcyear').inner_text.strip()
    record ['ID'] = record['version'] + record['price']
    # Print out the data we've gathered
    puts record
  end

    # Finally, save the record to the datastore - 'Artist' is our unique key
    #ScraperWiki.save("ID", record)
    ScraperWiki.save_sqlite(unique_keys=["ID"], record)
p ScraperWiki.show_tables()


  end
end

#        scrape_and_look_for_next_link(starting_url)

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    scrape_table(page)
    next_link = page.at_css('a.next')
    if next_link 
      puts next_link
      next_url = BASE_URL + next_link['href']
      puts next_url
      scrape_and_look_for_next_link(next_url)
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL #+ 'example_table_1.html'
#scrape_and_look_for_next_link(starting_url)
scrape_table(Nokogiri::HTML(open(starting_url)))
=end