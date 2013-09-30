##################################################################################################
# Third part of the Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe 
##################################################################################################
require 'mechanize'

$id_distrito={}

###################################################################
# These are the two functions we will need to use
###################################################################

# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
  scrape_table(page.body)
  link = page.link_with(:text => '2')
  if link
    page.form_with(:name => 'aspnetForm') do |f|
      f['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$tab21$GVProcesos'
      f['__EVENTARGUMENT'] = 'Page$2'
      page = f.submit()
      p page.body
    end
  scrape_and_look_for_next_link(page)
  end
end

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)
  i=0
  
  data_table = Nokogiri::HTML(page_body).css('table#ctl00_ContentPlaceHolder1_tab21_GVProcesos tr').collect do |row|
    #puts row
    if i==0 then
      i=i+1
    else
      if i<7 and row.css('td')[0].inner_text.include? "/" then
        puts row.css('td')[3].css('a').attr('href')
        record = {}
        record['Fecha']            = row.css('td')[0].inner_text
        record['Proceso']            = row.css('td')[1].inner_text
        record['Comentario']            = row.css('td')[2].inner_text
        record['URL']            = row.css('td')[3].css('a').attr('href')
        ScraperWiki.save_sqlite(["URL"], record)
        i=i+1
      end
    end
  end
end

###########################################################################
# we start downloading the district codes from the first script
###########################################################################

puts "*********************STARTING***************"
puts "*********************Getting list of distritos***************"
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=peru_districts&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)
l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
    $id_distrito[l]=datos.inner_html
  else
    #puts datos.inner_html
    $id_distrito[l]=datos.inner_html
  end
  l=l+1
end

for j in 0..1
  BASE_URL = 'http://www.infogob.com.pe/Localidad/ubigeo.aspx?IdUbigeo='+ $id_distrito[j] +'&IdTab=1'
  puts BASE_URL
  puts j
  
  # ---------------------------------------------------------------------------
  # START HERE: setting up Mechanize We need to set the user-agent header so the page thinks we're a browser,
  # as otherwise it won't show all the fields we need
  # ---------------------------------------------------------------------------
  
  starting_url = BASE_URL
  @br = Mechanize.new do |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
    browser.user_agent_alias = 'Linux Firefox'
  end
  page = @br.get(starting_url)
  p page.body
  
  # start scraping
  scrape_and_look_for_next_link(page)
end




##################################################################################################
# Third part of the Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe 
##################################################################################################
require 'mechanize'

$id_distrito={}

###################################################################
# These are the two functions we will need to use
###################################################################

# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
  scrape_table(page.body)
  link = page.link_with(:text => '2')
  if link
    page.form_with(:name => 'aspnetForm') do |f|
      f['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$tab21$GVProcesos'
      f['__EVENTARGUMENT'] = 'Page$2'
      page = f.submit()
      p page.body
    end
  scrape_and_look_for_next_link(page)
  end
end

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)
  i=0
  
  data_table = Nokogiri::HTML(page_body).css('table#ctl00_ContentPlaceHolder1_tab21_GVProcesos tr').collect do |row|
    #puts row
    if i==0 then
      i=i+1
    else
      if i<7 and row.css('td')[0].inner_text.include? "/" then
        puts row.css('td')[3].css('a').attr('href')
        record = {}
        record['Fecha']            = row.css('td')[0].inner_text
        record['Proceso']            = row.css('td')[1].inner_text
        record['Comentario']            = row.css('td')[2].inner_text
        record['URL']            = row.css('td')[3].css('a').attr('href')
        ScraperWiki.save_sqlite(["URL"], record)
        i=i+1
      end
    end
  end
end

###########################################################################
# we start downloading the district codes from the first script
###########################################################################

puts "*********************STARTING***************"
puts "*********************Getting list of distritos***************"
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=peru_districts&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)
l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
    $id_distrito[l]=datos.inner_html
  else
    #puts datos.inner_html
    $id_distrito[l]=datos.inner_html
  end
  l=l+1
end

for j in 0..1
  BASE_URL = 'http://www.infogob.com.pe/Localidad/ubigeo.aspx?IdUbigeo='+ $id_distrito[j] +'&IdTab=1'
  puts BASE_URL
  puts j
  
  # ---------------------------------------------------------------------------
  # START HERE: setting up Mechanize We need to set the user-agent header so the page thinks we're a browser,
  # as otherwise it won't show all the fields we need
  # ---------------------------------------------------------------------------
  
  starting_url = BASE_URL
  @br = Mechanize.new do |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
    browser.user_agent_alias = 'Linux Firefox'
  end
  page = @br.get(starting_url)
  p page.body
  
  # start scraping
  scrape_and_look_for_next_link(page)
end




##################################################################################################
# Third part of the Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe 
##################################################################################################
require 'mechanize'

$id_distrito={}

###################################################################
# These are the two functions we will need to use
###################################################################

# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
  scrape_table(page.body)
  link = page.link_with(:text => '2')
  if link
    page.form_with(:name => 'aspnetForm') do |f|
      f['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$tab21$GVProcesos'
      f['__EVENTARGUMENT'] = 'Page$2'
      page = f.submit()
      p page.body
    end
  scrape_and_look_for_next_link(page)
  end
end

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)
  i=0
  
  data_table = Nokogiri::HTML(page_body).css('table#ctl00_ContentPlaceHolder1_tab21_GVProcesos tr').collect do |row|
    #puts row
    if i==0 then
      i=i+1
    else
      if i<7 and row.css('td')[0].inner_text.include? "/" then
        puts row.css('td')[3].css('a').attr('href')
        record = {}
        record['Fecha']            = row.css('td')[0].inner_text
        record['Proceso']            = row.css('td')[1].inner_text
        record['Comentario']            = row.css('td')[2].inner_text
        record['URL']            = row.css('td')[3].css('a').attr('href')
        ScraperWiki.save_sqlite(["URL"], record)
        i=i+1
      end
    end
  end
end

###########################################################################
# we start downloading the district codes from the first script
###########################################################################

puts "*********************STARTING***************"
puts "*********************Getting list of distritos***************"
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=peru_districts&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)
l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
    $id_distrito[l]=datos.inner_html
  else
    #puts datos.inner_html
    $id_distrito[l]=datos.inner_html
  end
  l=l+1
end

for j in 0..1
  BASE_URL = 'http://www.infogob.com.pe/Localidad/ubigeo.aspx?IdUbigeo='+ $id_distrito[j] +'&IdTab=1'
  puts BASE_URL
  puts j
  
  # ---------------------------------------------------------------------------
  # START HERE: setting up Mechanize We need to set the user-agent header so the page thinks we're a browser,
  # as otherwise it won't show all the fields we need
  # ---------------------------------------------------------------------------
  
  starting_url = BASE_URL
  @br = Mechanize.new do |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
    browser.user_agent_alias = 'Linux Firefox'
  end
  page = @br.get(starting_url)
  p page.body
  
  # start scraping
  scrape_and_look_for_next_link(page)
end




##################################################################################################
# Third part of the Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe 
##################################################################################################
require 'mechanize'

$id_distrito={}

###################################################################
# These are the two functions we will need to use
###################################################################

# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
  scrape_table(page.body)
  link = page.link_with(:text => '2')
  if link
    page.form_with(:name => 'aspnetForm') do |f|
      f['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$tab21$GVProcesos'
      f['__EVENTARGUMENT'] = 'Page$2'
      page = f.submit()
      p page.body
    end
  scrape_and_look_for_next_link(page)
  end
end

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)
  i=0
  
  data_table = Nokogiri::HTML(page_body).css('table#ctl00_ContentPlaceHolder1_tab21_GVProcesos tr').collect do |row|
    #puts row
    if i==0 then
      i=i+1
    else
      if i<7 and row.css('td')[0].inner_text.include? "/" then
        puts row.css('td')[3].css('a').attr('href')
        record = {}
        record['Fecha']            = row.css('td')[0].inner_text
        record['Proceso']            = row.css('td')[1].inner_text
        record['Comentario']            = row.css('td')[2].inner_text
        record['URL']            = row.css('td')[3].css('a').attr('href')
        ScraperWiki.save_sqlite(["URL"], record)
        i=i+1
      end
    end
  end
end

###########################################################################
# we start downloading the district codes from the first script
###########################################################################

puts "*********************STARTING***************"
puts "*********************Getting list of distritos***************"
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=peru_districts&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)
l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
    $id_distrito[l]=datos.inner_html
  else
    #puts datos.inner_html
    $id_distrito[l]=datos.inner_html
  end
  l=l+1
end

for j in 0..1
  BASE_URL = 'http://www.infogob.com.pe/Localidad/ubigeo.aspx?IdUbigeo='+ $id_distrito[j] +'&IdTab=1'
  puts BASE_URL
  puts j
  
  # ---------------------------------------------------------------------------
  # START HERE: setting up Mechanize We need to set the user-agent header so the page thinks we're a browser,
  # as otherwise it won't show all the fields we need
  # ---------------------------------------------------------------------------
  
  starting_url = BASE_URL
  @br = Mechanize.new do |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
    browser.user_agent_alias = 'Linux Firefox'
  end
  page = @br.get(starting_url)
  p page.body
  
  # start scraping
  scrape_and_look_for_next_link(page)
end




