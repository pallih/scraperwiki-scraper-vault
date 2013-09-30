################################################################################
#This scraper was adapted from: https://scraperwiki.com/scrapers/advanced-scraping-aspx-pages-1
###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'


Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://locator.moneypass.com/'

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)

data_table = Nokogiri::HTML(page_body).css('table#DataGrid1 tr.ficontent').collect do |row|

    record = {}
    record['loc_name']           = row.css('span#DataGrid1_ctl03_institutionName').inner_text
    record['address']            = row.css('td.ficontent').inner_text
    ScraperWiki.save(['loc_name'],record)
  end
end
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
    scrape_table(page_body)
    link = page.link_with(:text => '[NEXT]')
    if link
      page.form_with(:name => 'form1') do |f|
        f['__EVENTTARGET'] = 'DataGrid1$ctl01$lnkNext',''
        f['__EVENTARGUMENT'] = ''


        page = f.submit()
      end
    scrape_and_look_for_next_link(page)
    end
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

starting_url = BASE_URL + 'postsearch.aspx?zipcode=Detroit%2C+MI'
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Windows IE 7'
}
page = @br.get(starting_url)
puts page.body
# Have a look at 'page': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.

# start scraping
scrape_and_look_for_next_link(page)

################################################################################
#This scraper was adapted from: https://scraperwiki.com/scrapers/advanced-scraping-aspx-pages-1
###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'


Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://locator.moneypass.com/'

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)

data_table = Nokogiri::HTML(page_body).css('table#DataGrid1 tr.ficontent').collect do |row|

    record = {}
    record['loc_name']           = row.css('span#DataGrid1_ctl03_institutionName').inner_text
    record['address']            = row.css('td.ficontent').inner_text
    ScraperWiki.save(['loc_name'],record)
  end
end
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
    scrape_table(page_body)
    link = page.link_with(:text => '[NEXT]')
    if link
      page.form_with(:name => 'form1') do |f|
        f['__EVENTTARGET'] = 'DataGrid1$ctl01$lnkNext',''
        f['__EVENTARGUMENT'] = ''


        page = f.submit()
      end
    scrape_and_look_for_next_link(page)
    end
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

starting_url = BASE_URL + 'postsearch.aspx?zipcode=Detroit%2C+MI'
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Windows IE 7'
}
page = @br.get(starting_url)
puts page.body
# Have a look at 'page': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.

# start scraping
scrape_and_look_for_next_link(page)

################################################################################
#This scraper was adapted from: https://scraperwiki.com/scrapers/advanced-scraping-aspx-pages-1
###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'


Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://locator.moneypass.com/'

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)

data_table = Nokogiri::HTML(page_body).css('table#DataGrid1 tr.ficontent').collect do |row|

    record = {}
    record['loc_name']           = row.css('span#DataGrid1_ctl03_institutionName').inner_text
    record['address']            = row.css('td.ficontent').inner_text
    ScraperWiki.save(['loc_name'],record)
  end
end
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
    scrape_table(page_body)
    link = page.link_with(:text => '[NEXT]')
    if link
      page.form_with(:name => 'form1') do |f|
        f['__EVENTTARGET'] = 'DataGrid1$ctl01$lnkNext',''
        f['__EVENTARGUMENT'] = ''


        page = f.submit()
      end
    scrape_and_look_for_next_link(page)
    end
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

starting_url = BASE_URL + 'postsearch.aspx?zipcode=Detroit%2C+MI'
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Windows IE 7'
}
page = @br.get(starting_url)
puts page.body
# Have a look at 'page': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.

# start scraping
scrape_and_look_for_next_link(page)

################################################################################
#This scraper was adapted from: https://scraperwiki.com/scrapers/advanced-scraping-aspx-pages-1
###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'


Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://locator.moneypass.com/'

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)

data_table = Nokogiri::HTML(page_body).css('table#DataGrid1 tr.ficontent').collect do |row|

    record = {}
    record['loc_name']           = row.css('span#DataGrid1_ctl03_institutionName').inner_text
    record['address']            = row.css('td.ficontent').inner_text
    ScraperWiki.save(['loc_name'],record)
  end
end
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
    scrape_table(page_body)
    link = page.link_with(:text => '[NEXT]')
    if link
      page.form_with(:name => 'form1') do |f|
        f['__EVENTTARGET'] = 'DataGrid1$ctl01$lnkNext',''
        f['__EVENTARGUMENT'] = ''


        page = f.submit()
      end
    scrape_and_look_for_next_link(page)
    end
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

starting_url = BASE_URL + 'postsearch.aspx?zipcode=Detroit%2C+MI'
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Windows IE 7'
}
page = @br.get(starting_url)
puts page.body
# Have a look at 'page': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.

# start scraping
scrape_and_look_for_next_link(page)

