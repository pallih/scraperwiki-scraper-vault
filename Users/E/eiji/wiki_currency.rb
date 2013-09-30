require 'nokogiri'
require 'uri'

def make_absolute( href, root )
  URI.parse(root).merge(URI.parse(href)).to_s
end

url = 'http://ja.wikipedia.org/wiki/ISO_4217'
html = ScraperWiki.scrape(url)
doc = Nokogiri::HTML(html)

doc.search("/html/body/div[3]/div[3]/div[4]/table[2]/tr").each do |tr|
  cells = tr.search('td')

  if cells.length != 0 then
    if cells[2].search('a')[0] && cells[2].search('a')[0].search('img').length > 0 then
      imgname = cells[2].search('a')[0].search('img')[0].attr('src')
    else
      imgname=nil
    end

    data = {
      'CODE' => cells[0].inner_html,
      'IMGNAME' => imgname && make_absolute(imgname,url)
    }
    
    ScraperWiki.save_sqlite(['CODE'], data)
  end
end

require 'nokogiri'
require 'uri'

def make_absolute( href, root )
  URI.parse(root).merge(URI.parse(href)).to_s
end

url = 'http://ja.wikipedia.org/wiki/ISO_4217'
html = ScraperWiki.scrape(url)
doc = Nokogiri::HTML(html)

doc.search("/html/body/div[3]/div[3]/div[4]/table[2]/tr").each do |tr|
  cells = tr.search('td')

  if cells.length != 0 then
    if cells[2].search('a')[0] && cells[2].search('a')[0].search('img').length > 0 then
      imgname = cells[2].search('a')[0].search('img')[0].attr('src')
    else
      imgname=nil
    end

    data = {
      'CODE' => cells[0].inner_html,
      'IMGNAME' => imgname && make_absolute(imgname,url)
    }
    
    ScraperWiki.save_sqlite(['CODE'], data)
  end
end

