def save_page(url,table_name="pages")
  text = ScraperWiki.scrape(url)
  d={
    "url" => url,
    "text" => text
  }
  ScraperWiki.save_sqlite(['url'],d,table_name)
end  

def get_page(url,table_name="pages")
  rows=ScraperWiki.select("`text` from "+table_name+" where url=?",[url])
  #Check length, then
  return rows[0]['text']
end



def test()
  save_page('http://scraperwiki.com')
  get_page('http://scraperwiki.com')
end

#test()def save_page(url,table_name="pages")
  text = ScraperWiki.scrape(url)
  d={
    "url" => url,
    "text" => text
  }
  ScraperWiki.save_sqlite(['url'],d,table_name)
end  

def get_page(url,table_name="pages")
  rows=ScraperWiki.select("`text` from "+table_name+" where url=?",[url])
  #Check length, then
  return rows[0]['text']
end



def test()
  save_page('http://scraperwiki.com')
  get_page('http://scraperwiki.com')
end

#test()