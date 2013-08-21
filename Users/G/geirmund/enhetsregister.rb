###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page.  We use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://hotell.difi.no/api/html/brreg/enhetsregisteret'
pagenum = 0


# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  data_table = page.css('table tr').collect {|x| x.css('td')}.reject{ |x| x.length == 0}.collect do |row|
    record = {
      Orgnr: row[0].inner_text,
      Navn: row[1].inner_text,
      Organisasjonsform: row[2].inner_text,
      Forretningsadr: row[3].inner_text,
      Forradr_postnr: row[4].inner_text,
      Forradr_poststed: row[5].inner_text,
      Forradr_kommnr: row[6].inner_text,
      Postadresse: row[7].inner_text,
      Ppostnr: row[8].inner_text,
      Ppoststed: row[9].inner_text,
      Ppost_land: row[10].inner_text,
      Reg_i_FR: row[11].inner_text
    }

    # Print out the data we've gathered
    # p record

    # Finally, save the record to the datastore - 'Orgnr' is our unique key
    ScraperWiki.save_sqlite([:Orgnr], record)
  end
end

# scrape_and_set_next_page
def scrape_and_set_next_link(url,pagenum)
  page = Nokogiri::HTML(open(url))
  scrape_table(page)
  next_url = BASE_URL + '?page=' + pagenum.to_s()
  pagenum = pagenum + 1
  scrape_and_set_next_link(next_url,pagenum)
end



# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------

starting_url = BASE_URL + '?page=1'
scrape_and_set_next_link(starting_url,2)

