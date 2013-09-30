# encoding: UTF-8
###############################################################################
# Parafie InPost Scraper 
###############################################################################

require 'nokogiri'
require 'open-uri'

@woj = ['22','32','28','20','08','30','04','14','06','10','02','16','24','12','26','18']
#@woj = ['22']

PAR_URL = 'http://www.usc.pl/parafie;'
WOJ_URL = 'http://www.usc.pl/parafie;;'

def scrape_woj(i)
  woj = @woj[i]
  p woj

  page = Nokogiri::HTML(open(WOJ_URL+woj), nil, 'utf-8')
  page.encoding = 'utf-8'

  data_table = page.css('.szukaj_firm_wyniki_ul a').collect do |row|
    # Ex. row['href'] = "/parafie;1073"
    id = row['href'].sub('/parafie;', '')
    if id
      record = {
        ID: id,
        City: row['title'].capitalize,
        Name: row.css('h4').inner_text
      }
  
      # Print out the data we've gathered
      #p page
  
      # Finally, save the record to the datastore - 'Product' is our unique key
      p record
      ScraperWiki.save_sqlite([:ID], record)
    end
  end  

  if @woj[i] != @woj.last
    i += 1
    scrape_woj(i)
  end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
scrape_woj(0)# encoding: UTF-8
###############################################################################
# Parafie InPost Scraper 
###############################################################################

require 'nokogiri'
require 'open-uri'

@woj = ['22','32','28','20','08','30','04','14','06','10','02','16','24','12','26','18']
#@woj = ['22']

PAR_URL = 'http://www.usc.pl/parafie;'
WOJ_URL = 'http://www.usc.pl/parafie;;'

def scrape_woj(i)
  woj = @woj[i]
  p woj

  page = Nokogiri::HTML(open(WOJ_URL+woj), nil, 'utf-8')
  page.encoding = 'utf-8'

  data_table = page.css('.szukaj_firm_wyniki_ul a').collect do |row|
    # Ex. row['href'] = "/parafie;1073"
    id = row['href'].sub('/parafie;', '')
    if id
      record = {
        ID: id,
        City: row['title'].capitalize,
        Name: row.css('h4').inner_text
      }
  
      # Print out the data we've gathered
      #p page
  
      # Finally, save the record to the datastore - 'Product' is our unique key
      p record
      ScraperWiki.save_sqlite([:ID], record)
    end
  end  

  if @woj[i] != @woj.last
    i += 1
    scrape_woj(i)
  end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
scrape_woj(0)