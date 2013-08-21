require 'nokogiri'

CATEGORIES = ['/category/index.jsp?categoryId=3534623','/category/index.jsp?categoryId=3534624']

BASE_URL = 'http://www.aeropostale.com'

menu = []
CATEGORIES.each do |c|

html = ScraperWiki::scrape(BASE_URL + c)

doc = Nokogiri::HTML(html)

menu += doc.css('div.middle li>a').map{|a| BASE_URL + a.attr('href').to_s }

end


def list_items(url)

  @html = ScraperWiki::scrape(url)
  @doc = Nokogiri::HTML(@html)
p @doc.css('div.products')
  #if @doc.css('.viewAll a').length > 0
  #  p "going into all view"
  #  @html = ScraperWiki::scrape(BASE_URL + @doc.css('.viewAll a').attr('href').to_s)
  #  @doc = Nokogiri::HTML(@html)
  #end

  #if @doc.css('div.row div.item').length > 0
    #@doc.css('.thumbbg').each {|i| p i.css('.thumbheader a').text }
  #  items = @doc.css('h4')
  #  p items
    
  #end


  #items
end

menu.each do |m|
  p m
  items = list_items(m)
  #p items.length if items

end
