###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
require 'mechanize'

BASE_URL = 'http://recognition.ncqa.org/'

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)
  data_table = Nokogiri::HTML(page_body).css('table#ProviderSearchResultsTable1_ProvidersGrid tr.SearchResultsRow').collect do |row|
    record = {}
    record['Clinician']           = row.css('td')[0].inner_text
    record['Location']            = row.css('td')[1].inner_text
    record['CurrentRecognitions'] = row.css('td')[2].inner_text.gsub('&nbsp;',' ').rstrip
    ScraperWiki.save_sqlite(["Clinician"], record)
  end
end
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
  scrape_table(page.body)
  link = page.link_with(:text => 'Next Page >>')
  if link
    page.form_with(:name => 'ctl00') do |f|
      f['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
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

starting_url = BASE_URL + 'PSearchResults.aspx?state=NY&rp='
@br = Mechanize.new do |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
end
page = @br.get(starting_url)
p page.body
# Have a look at 'page': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.

# start scraping
scrape_and_look_for_next_link(page)

###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
require 'mechanize'

BASE_URL = 'http://recognition.ncqa.org/'

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)
  data_table = Nokogiri::HTML(page_body).css('table#ProviderSearchResultsTable1_ProvidersGrid tr.SearchResultsRow').collect do |row|
    record = {}
    record['Clinician']           = row.css('td')[0].inner_text
    record['Location']            = row.css('td')[1].inner_text
    record['CurrentRecognitions'] = row.css('td')[2].inner_text.gsub('&nbsp;',' ').rstrip
    ScraperWiki.save_sqlite(["Clinician"], record)
  end
end
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
  scrape_table(page.body)
  link = page.link_with(:text => 'Next Page >>')
  if link
    page.form_with(:name => 'ctl00') do |f|
      f['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
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

starting_url = BASE_URL + 'PSearchResults.aspx?state=NY&rp='
@br = Mechanize.new do |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
end
page = @br.get(starting_url)
p page.body
# Have a look at 'page': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.

# start scraping
scrape_and_look_for_next_link(page)

