require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://ad-networks.findthebest.com/'
starting_url = BASE_URL + 'collections/237-Storm-Front'

ScraperWiki.save_var('data_columns',['keywords','title'])


def scrape_table(page,url)
  if url[url.length-2,url.length]=="HD"
    class_suffix="hd"
  else
    class_suffix="sd"
  end
  page.css('table[@class="clip thumbnail_large_' + class_suffix +'"]').each do |item|
    record={}
    name=item.css('tr.info td.title a')[0].inner_text
    keywords=item.css('div.info_hover p').inner_text
    keywords=keywords[10,keywords.length-10]
    #converting keywords to an array would be easy: keywords=keywords.split(/,/)
    record['title'] = name + '.mov'
    record['keywords'] = keywords
    #ScraperWiki.save_sqlite(unique_keys=["a"], data={"a"=>1, "bbb"=>"Hi there"})
    ScraperWiki.save_sqlite(unique_keys=["title"],data=record)
  end
end

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    scrape_table(page,url)
    next_link = page.at_css('a.next_page')
    if next_link 
      # puts next_link
      next_url = BASE_URL + next_link['href']
      # puts next_url
      scrape_and_look_for_next_link(next_url)
    end
end



# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
scrape_and_look_for_next_link(starting_url)

