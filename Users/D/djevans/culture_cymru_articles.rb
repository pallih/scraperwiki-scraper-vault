# Blank Ruby

require 'nokogiri'
require 'xsl'

BASE = "http://cymruculture.co.uk"
ARTICLES = "#{BASE}/featuredarticles.html"
INTERVIEWS = "#{BASE}/cymruculturecelebrityinterviews.html"
html = ScraperWiki.scrape(ARTICLES)
doc = Nokogiri::HTML(html,nil,'ISO-8859-1')

paras = doc.xpath("//td[@id='wdk_content-maincontentcontainer']/div/p")
paras.each do |para| 
  date = para.xpath('descendant::span[1]').inner_html
  para.xpath('descendant::a[1]').each do |link|
    title = link.inner_html
    href = link['href']
    url = "#{BASE}/#{href}"
    unless href[/^http/]
      id = href[/\d+/]
      article_page = ScraperWiki.scrape "#{BASE}/#{href}"
      article_doc = Nokogiri::HTML(article_page,nil,'ISO-8859-1')
      body = article_doc.xpath("//td[@id='wdk_content-maincontentcontainer']").inner_html
      data = {
        'id' => id,
        'title' => title,
        'body' => body,
        'date' => Date.parse(date).to_s
      }
      data.each {|key,val| val.encode!('UTF-8')}
      ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
    else
      p "No Way Jos"
    end
  end
end# Blank Ruby

require 'nokogiri'
require 'xsl'

BASE = "http://cymruculture.co.uk"
ARTICLES = "#{BASE}/featuredarticles.html"
INTERVIEWS = "#{BASE}/cymruculturecelebrityinterviews.html"
html = ScraperWiki.scrape(ARTICLES)
doc = Nokogiri::HTML(html,nil,'ISO-8859-1')

paras = doc.xpath("//td[@id='wdk_content-maincontentcontainer']/div/p")
paras.each do |para| 
  date = para.xpath('descendant::span[1]').inner_html
  para.xpath('descendant::a[1]').each do |link|
    title = link.inner_html
    href = link['href']
    url = "#{BASE}/#{href}"
    unless href[/^http/]
      id = href[/\d+/]
      article_page = ScraperWiki.scrape "#{BASE}/#{href}"
      article_doc = Nokogiri::HTML(article_page,nil,'ISO-8859-1')
      body = article_doc.xpath("//td[@id='wdk_content-maincontentcontainer']").inner_html
      data = {
        'id' => id,
        'title' => title,
        'body' => body,
        'date' => Date.parse(date).to_s
      }
      data.each {|key,val| val.encode!('UTF-8')}
      ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
    else
      p "No Way Jos"
    end
  end
end