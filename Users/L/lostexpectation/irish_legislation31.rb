# this is for "Irish Legislation"

require 'nokogiri'
require 'open-uri'
# return the bill info from the fetched page
require 'iconv'


def parse_bill(url)
puts url
 # page = Nokogiri::HTML(ScraperWiki.scrape(url))
#doc = Nokogiri::HTML(Iconv.conv('utf-8//IGNORE', 'ISO-639-1', open(url).read))
page = Nokogiri::HTML(ScraperWiki.scrape(Iconv.conv('utf-8//IGNORE', 'ISO 639-1', url)))

# html = ScraperWiki.scrape(url)
#  page = Nokogiri::HTML(html, nil, 'utf-8')
page.encoding = 'UTF-8'
puts page
#page.encoding = 'ISO 639-1'
  title = page.search("title")
puts tite
  name = title[0].content.sub(/ - Tithe an Oireachtais$/, "").strip if title[0]
puts name
  
  meta = page.search("//meta[@name='Abstract']")
puts meta
  abstract = meta[0]['content'].strip if meta[0]
puts abstract  
  # update the description with full description, since it could be cut off
  # doesn't work right yet, we might have to dive into the hr tags again
  # description = page.search("div.column-center-inner p").map { |p|
  #   p.content.include?(description) ? p.content : nil }.compact[0]
  
  ScraperWiki.save(['name', 'abstract', 'url'], {
    'name' => name,
    'abstract' => abstract,
    'url' => url
  })
  [name, abstract]


=begin
  # OLD METHOD
  # take all the text between the first two <hr> tags
  # for now, don't get the rest, because you'd have to parse word, pdf, etc
  # a lot of it is the debate information
  
  # between first two is name
  # between second and third is description
  node = page.search("hr")[0]
  # need to collect all the nodes until the next hr
  name_nodes = []
  while node = node.next
    break if node.name == "hr"
    name_nodes << node
  end
  
  name = nil
  name_nodes.each do |nn|
    # search for "strong" because that's the markup they use for the name
    if nn.name == "strong" && nn.content && nn.content.strip != ""
      name = nn.content
    else
      strong = nn.search("strong")
      name = strong[0].content.strip if strong[0]
    end
    break if name
  end
    
  node = page.search("hr")[1]
  # collect all nodes until end of description
  desc_nodes = []
  while node = node.next
    break if node.name == "hr"
    desc_nodes << node
  end
  # parse the description into a string of some sort?
  # we could just keep the HTML for now.
=end
end

# goes from year 1997-2010, edit this as needed
years = (2011..2012)
#put year

# collect all the bills in this data structure
bill_info = []

years.each do |year|
#puts year
  base_url = "http://www.oireachtas.ie/viewdoc.asp?DocID=-1&StartDate=1+January+#{year}&CatID=59"
puts base_url

  # are there multiple pages? if so, collect them all
 # page = Nokogiri::HTML(ScraperWiki.scrape(base_url))
page = Nokogiri::HTML(ScraperWiki.scrape(Iconv.conv('utf-8//IGNORE', 'ISO 639-1', base_url)))
#page = Nokogiri::HTML(Iconv.conv('utf-8//IGNORE', 'ISO-639-1', open(base_url).read))
# html = ScraperWiki.scrape(base_url)
#  page = Nokogiri::HTML(html)
#page.encoding = 'ISO 639-1'
#page.encoding = 'UTF-8'
puts page
  page_links = page.search("p.bodytext a.bodytext")
#print page_links
puts page_links
  page_urls = page_links.map { |pl| pl['href'] }
puts page_urls
  # on this page, get all the bill urls
  bill_urls = page.search("div.column-center-inner a").map { |a|
    (a['href'] =~ /DocID=\d+/ && a.content =~ /\[view more\]/) ? a['href'] : nil }.compact

puts bill_urls  
  # on each of the other pages for this year, get all the bills
  page_urls.each do |url|
puts url
#page = Nokogiri::HTML(Iconv.conv('utf-8//IGNORE', 'ISO-639-1', open(url).read))
#page = Nokogiri::HTML(ScraperWiki.scrape(Iconv.conv('utf-8//IGNORE', 'ISO 639-1', base_url)))
pagetest = "http://www.oireachtas.ie/" + url.gsub(" ", "%20")
puts pagetest
   page = Nokogiri::HTML(ScraperWiki.scrape("http://www.oireachtas.ie/" + url.gsub(" ", "%20")))

#    page = Nokogiri::HTML(ScraperWiki.scrape(Iconv.conv('utf-8//IGNORE', 'ISO 639-1',("http://www.oireachtas.ie/" + url.gsub(" ", "%20")))))
    bill_urls = bill_urls + page.search("div.column-center-inner a").map { |a|
      (a['href'] =~ /DocID=\d+/ && a.content =~ /\[view more\]/) ? a['href'] : nil }.compact
  end
  
  # now for each bill, parse its "more info page"
  bill_info = bill_info + bill_urls.map { |bill_url|
    # TODO: save URL
    url = "http://www.oireachtas.ie/" + bill_url.gsub(" ", "%20")
    info = parse_bill(url)
puts info
  }
end

=begin
# replace with scraper wiki api
bill_info.each do |bi|
  # puts(bi.join(","))
  ScraperWiki.save(['name', 'abstract'], {
    'name' => bi[0],
    'abstract' => bi[1]
  })
end
=end
# this is for "Irish Legislation"

require 'nokogiri'
require 'open-uri'
# return the bill info from the fetched page
require 'iconv'


def parse_bill(url)
puts url
 # page = Nokogiri::HTML(ScraperWiki.scrape(url))
#doc = Nokogiri::HTML(Iconv.conv('utf-8//IGNORE', 'ISO-639-1', open(url).read))
page = Nokogiri::HTML(ScraperWiki.scrape(Iconv.conv('utf-8//IGNORE', 'ISO 639-1', url)))

# html = ScraperWiki.scrape(url)
#  page = Nokogiri::HTML(html, nil, 'utf-8')
page.encoding = 'UTF-8'
puts page
#page.encoding = 'ISO 639-1'
  title = page.search("title")
puts tite
  name = title[0].content.sub(/ - Tithe an Oireachtais$/, "").strip if title[0]
puts name
  
  meta = page.search("//meta[@name='Abstract']")
puts meta
  abstract = meta[0]['content'].strip if meta[0]
puts abstract  
  # update the description with full description, since it could be cut off
  # doesn't work right yet, we might have to dive into the hr tags again
  # description = page.search("div.column-center-inner p").map { |p|
  #   p.content.include?(description) ? p.content : nil }.compact[0]
  
  ScraperWiki.save(['name', 'abstract', 'url'], {
    'name' => name,
    'abstract' => abstract,
    'url' => url
  })
  [name, abstract]


=begin
  # OLD METHOD
  # take all the text between the first two <hr> tags
  # for now, don't get the rest, because you'd have to parse word, pdf, etc
  # a lot of it is the debate information
  
  # between first two is name
  # between second and third is description
  node = page.search("hr")[0]
  # need to collect all the nodes until the next hr
  name_nodes = []
  while node = node.next
    break if node.name == "hr"
    name_nodes << node
  end
  
  name = nil
  name_nodes.each do |nn|
    # search for "strong" because that's the markup they use for the name
    if nn.name == "strong" && nn.content && nn.content.strip != ""
      name = nn.content
    else
      strong = nn.search("strong")
      name = strong[0].content.strip if strong[0]
    end
    break if name
  end
    
  node = page.search("hr")[1]
  # collect all nodes until end of description
  desc_nodes = []
  while node = node.next
    break if node.name == "hr"
    desc_nodes << node
  end
  # parse the description into a string of some sort?
  # we could just keep the HTML for now.
=end
end

# goes from year 1997-2010, edit this as needed
years = (2011..2012)
#put year

# collect all the bills in this data structure
bill_info = []

years.each do |year|
#puts year
  base_url = "http://www.oireachtas.ie/viewdoc.asp?DocID=-1&StartDate=1+January+#{year}&CatID=59"
puts base_url

  # are there multiple pages? if so, collect them all
 # page = Nokogiri::HTML(ScraperWiki.scrape(base_url))
page = Nokogiri::HTML(ScraperWiki.scrape(Iconv.conv('utf-8//IGNORE', 'ISO 639-1', base_url)))
#page = Nokogiri::HTML(Iconv.conv('utf-8//IGNORE', 'ISO-639-1', open(base_url).read))
# html = ScraperWiki.scrape(base_url)
#  page = Nokogiri::HTML(html)
#page.encoding = 'ISO 639-1'
#page.encoding = 'UTF-8'
puts page
  page_links = page.search("p.bodytext a.bodytext")
#print page_links
puts page_links
  page_urls = page_links.map { |pl| pl['href'] }
puts page_urls
  # on this page, get all the bill urls
  bill_urls = page.search("div.column-center-inner a").map { |a|
    (a['href'] =~ /DocID=\d+/ && a.content =~ /\[view more\]/) ? a['href'] : nil }.compact

puts bill_urls  
  # on each of the other pages for this year, get all the bills
  page_urls.each do |url|
puts url
#page = Nokogiri::HTML(Iconv.conv('utf-8//IGNORE', 'ISO-639-1', open(url).read))
#page = Nokogiri::HTML(ScraperWiki.scrape(Iconv.conv('utf-8//IGNORE', 'ISO 639-1', base_url)))
pagetest = "http://www.oireachtas.ie/" + url.gsub(" ", "%20")
puts pagetest
   page = Nokogiri::HTML(ScraperWiki.scrape("http://www.oireachtas.ie/" + url.gsub(" ", "%20")))

#    page = Nokogiri::HTML(ScraperWiki.scrape(Iconv.conv('utf-8//IGNORE', 'ISO 639-1',("http://www.oireachtas.ie/" + url.gsub(" ", "%20")))))
    bill_urls = bill_urls + page.search("div.column-center-inner a").map { |a|
      (a['href'] =~ /DocID=\d+/ && a.content =~ /\[view more\]/) ? a['href'] : nil }.compact
  end
  
  # now for each bill, parse its "more info page"
  bill_info = bill_info + bill_urls.map { |bill_url|
    # TODO: save URL
    url = "http://www.oireachtas.ie/" + bill_url.gsub(" ", "%20")
    info = parse_bill(url)
puts info
  }
end

=begin
# replace with scraper wiki api
bill_info.each do |bi|
  # puts(bi.join(","))
  ScraperWiki.save(['name', 'abstract'], {
    'name' => bi[0],
    'abstract' => bi[1]
  })
end
=end
