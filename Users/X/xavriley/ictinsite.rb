# Blank Ruby
puts "Starting Scrape of Total Pages"
html = ScraperWiki.scrape("http://stores.ebay.co.uk/UK-Screen-Specialists/_i.html")

require 'nokogiri'           

doc = Nokogiri::HTML(html)

catList = doc.css('div.lcat ul li a')

for catpage in catList
  curURI = "http://stores.ebay.co.uk" + catpage.attr('href').gsub(/&_sid[0-9a-zA-Z\=\&\.\_]+/,'')
  html = ScraperWiki.scrape(curURI)
  docCat = Nokogiri::HTML(html)
  pageSummary = docCat.search('td.l span.page').inner_html.split(' ')
  totalPages = pageSummary.last.to_i
  currentPage = pageSummary[1].to_i

  while currentPage != totalPages
    html = ScraperWiki.scrape(curURI + '&_pgn=' + currentPage.to_s)
    docCat2 = Nokogiri::HTML(html)
    pageSummaryInner = docCat2.search('td.l span.page').inner_html.split(' ')
    currentPage = pageSummaryInner[1].to_i

    for v in docCat2.search("table.gallery td.details")
      prodLink = v.search('div.ttl a').attr('href')
      prodName = v.search('div.ttl a').text()
      prodPrice = v.search('span.bin').text().gsub("£", '')
      data = {
        'prodLink' => prodLink,
        'prodName' => prodName,
        'prodPrice' => prodPrice
      }
    ScraperWiki.save_sqlite(unique_keys=['prodLink'], data=data)
    end
    currentPage += 1
  end
end# Blank Ruby
puts "Starting Scrape of Total Pages"
html = ScraperWiki.scrape("http://stores.ebay.co.uk/UK-Screen-Specialists/_i.html")

require 'nokogiri'           

doc = Nokogiri::HTML(html)

catList = doc.css('div.lcat ul li a')

for catpage in catList
  curURI = "http://stores.ebay.co.uk" + catpage.attr('href').gsub(/&_sid[0-9a-zA-Z\=\&\.\_]+/,'')
  html = ScraperWiki.scrape(curURI)
  docCat = Nokogiri::HTML(html)
  pageSummary = docCat.search('td.l span.page').inner_html.split(' ')
  totalPages = pageSummary.last.to_i
  currentPage = pageSummary[1].to_i

  while currentPage != totalPages
    html = ScraperWiki.scrape(curURI + '&_pgn=' + currentPage.to_s)
    docCat2 = Nokogiri::HTML(html)
    pageSummaryInner = docCat2.search('td.l span.page').inner_html.split(' ')
    currentPage = pageSummaryInner[1].to_i

    for v in docCat2.search("table.gallery td.details")
      prodLink = v.search('div.ttl a').attr('href')
      prodName = v.search('div.ttl a').text()
      prodPrice = v.search('span.bin').text().gsub("£", '')
      data = {
        'prodLink' => prodLink,
        'prodName' => prodName,
        'prodPrice' => prodPrice
      }
    ScraperWiki.save_sqlite(unique_keys=['prodLink'], data=data)
    end
    currentPage += 1
  end
end