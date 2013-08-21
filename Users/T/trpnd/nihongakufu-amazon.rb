require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.amazon.co.jp/'

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  data = page.css('span.lrg bold').each do |link|
    #p 'link: ' + link['href']
    item_url = BASE_URL + link['href']
    #p 'item_url: ' + item_url
    row = Nokogiri::HTML(open(item_url))

    #p 'Title: ' + row.css('h1.page_title').inner_text
    #p 'SizePage: ' + row.css('#container_items_view div.view_cart td')[0].inner_text
    #p 'JANCode: ' + row.css('#container_items_view div.view_cart td')[1].inner_text
    #p 'ISBNCode: ' + row.css('#container_items_view div.view_cart td')[2].inner_text
    #p 'Price: ' + row.css('#container_items_view div.view_cart td')[3].inner_text
    #p 'Description: ' + row.css('div.explanation p').inner_text

    record = {
      Title: row.css('h1.page_title').inner_text,
      SizePage: row.css('#container_items_view div.view_cart td')[0].inner_text,
      JANCode: row.css('#container_items_view div.view_cart td')[1].inner_text,
      ISBNCode: row.css('#container_items_view div.view_cart td')[2].inner_text,
      Price: row.css('#container_items_view div.view_cart td')[3].inner_text,
      Description: row.css('div.explanation p').inner_text,
      ItemURL: item_url
    }

    # Print out the data we've gathered
    #p record

    # Finally, save the record to the datastore - 'Product' is our unique key
    ScraperWiki.save_sqlite([:ISBNCode], record)
  end
end

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape_table(page)
  next_link = page.at_css('a.next')
  if next_link 
    #p 'next_link: ' + next_link['href']
    next_url = BASE_URL + next_link['href']
    p 'next_url: ' + next_url
    scrape_and_look_for_next_link(next_url)
  end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL + 's/ref=nb_sb_noss_1?__mk_ja_JP=%83J%83^%83J%83i&url=search-alias%3Dstripbooks&field-keywords=%93%FA%96{%8Ay%95%88%8Fo%94%C5%8E%D0+No&rh=n%3A465392%2Ck%3A%93%FA%96{%8Ay%95%88%8Fo%94%C5%8E%D0+No'
p 'starting_url: ' + starting_url
scrape_and_look_for_next_link(starting_url)