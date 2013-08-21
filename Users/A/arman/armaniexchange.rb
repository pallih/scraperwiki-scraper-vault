require 'nokogiri'

html = ScraperWiki::scrape 'http://www.armaniexchange.com/category/sale.do'

doc = Nokogiri::HTML(html)

BASE_URL = 'http://www.armaniexchange.com'
IMG_URL = 'http://armaniexchange.scene7.com/is/image/armaniexchange/'

menu = doc.css('div.navLeft2Off a')
  .select{|a| !(a.attr('href').to_s =~ /just/) && !(a.attr('href').to_s =~ /accessories/)}
  .map{|a| BASE_URL + a.attr('href').to_s }

def parse_items(items)

  items.each do |item|
    p "Processing #{item}..."
    html = ScraperWiki::scrape item
    doc = Nokogiri::HTML(html)
    p doc.css('a.breadcrumb').map{|a| a.text}
    doc.css('div#prdDescr div.shortDesc b').remove
    data = {

      :category => doc.css('a.breadcrumb').length > 2 ? doc.css('a.breadcrumb')[2].text : doc.css('div.navLeft2On a').text,
      :name => doc.css('div#prdDescr h2').text,
      :color => doc.css('.colorswatches img').map{|img| img.attr('title').to_s}.join(';'),
      :code => doc.css('div.prdCode').text,
      :pricewas => doc.css('div#prdDescr span.pricewas').text,
      :pricesale_red => doc.css('div#prdDescr span.pricesale_red').text,
      :description => doc.css('div#prdDescr div.shortDesc').text,
      :details => doc.css('div#prdDescr.productDtls span.price div[style]').map{|div| div.content}.join(';'),
      :images => doc.css('div[id*="altDiv"] a').each_with_index.map{|i,index| IMG_URL + i.attr('onclick').to_s[/\d+\d{3}+.+\d{3}/] + ".zd#{(index+1)}"}.join(';')
    }
    p data
    ScraperWiki::save_sqlite(["code"], data)
  end

end


def list_items(url)

  @html = ScraperWiki::scrape url
  @doc = Nokogiri::HTML(@html)
  if @doc.css('a#hva').length > 0
    p "going into all view"
    @html = ScraperWiki::scrape(BASE_URL + @doc.css('a#hva').first.attr('href').to_s)
    @doc = Nokogiri::HTML(@html)
  end

  if @doc.css('.thumbbg').length > 0
    #@doc.css('.thumbbg').each {|i| p i.css('.thumbheader a').text }
    items = @doc.css('.thumbbg').map{|item| BASE_URL + item.css('div.thumbheader').css('a').attr('href').to_s}
    p "got #{items.length} items"
    
  end


  items
end


$items = []
menu.each do |m|

  p "processing #{m}"
  items = list_items(m)
  #parse_items(items)
  parse_items(items)
end

p "Collected #{$items.length} items"
require 'nokogiri'

html = ScraperWiki::scrape 'http://www.armaniexchange.com/category/sale.do'

doc = Nokogiri::HTML(html)

BASE_URL = 'http://www.armaniexchange.com'
IMG_URL = 'http://armaniexchange.scene7.com/is/image/armaniexchange/'

menu = doc.css('div.navLeft2Off a')
  .select{|a| !(a.attr('href').to_s =~ /just/) && !(a.attr('href').to_s =~ /accessories/)}
  .map{|a| BASE_URL + a.attr('href').to_s }

def parse_items(items)

  items.each do |item|
    p "Processing #{item}..."
    html = ScraperWiki::scrape item
    doc = Nokogiri::HTML(html)
    p doc.css('a.breadcrumb').map{|a| a.text}
    doc.css('div#prdDescr div.shortDesc b').remove
    data = {

      :category => doc.css('a.breadcrumb').length > 2 ? doc.css('a.breadcrumb')[2].text : doc.css('div.navLeft2On a').text,
      :name => doc.css('div#prdDescr h2').text,
      :color => doc.css('.colorswatches img').map{|img| img.attr('title').to_s}.join(';'),
      :code => doc.css('div.prdCode').text,
      :pricewas => doc.css('div#prdDescr span.pricewas').text,
      :pricesale_red => doc.css('div#prdDescr span.pricesale_red').text,
      :description => doc.css('div#prdDescr div.shortDesc').text,
      :details => doc.css('div#prdDescr.productDtls span.price div[style]').map{|div| div.content}.join(';'),
      :images => doc.css('div[id*="altDiv"] a').each_with_index.map{|i,index| IMG_URL + i.attr('onclick').to_s[/\d+\d{3}+.+\d{3}/] + ".zd#{(index+1)}"}.join(';')
    }
    p data
    ScraperWiki::save_sqlite(["code"], data)
  end

end


def list_items(url)

  @html = ScraperWiki::scrape url
  @doc = Nokogiri::HTML(@html)
  if @doc.css('a#hva').length > 0
    p "going into all view"
    @html = ScraperWiki::scrape(BASE_URL + @doc.css('a#hva').first.attr('href').to_s)
    @doc = Nokogiri::HTML(@html)
  end

  if @doc.css('.thumbbg').length > 0
    #@doc.css('.thumbbg').each {|i| p i.css('.thumbheader a').text }
    items = @doc.css('.thumbbg').map{|item| BASE_URL + item.css('div.thumbheader').css('a').attr('href').to_s}
    p "got #{items.length} items"
    
  end


  items
end


$items = []
menu.each do |m|

  p "processing #{m}"
  items = list_items(m)
  #parse_items(items)
  parse_items(items)
end

p "Collected #{$items.length} items"
