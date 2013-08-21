# this is for "Irish Legislation" to understand and improve it orignal copy here http://scraperwiki.com/scrapers/irish-legislation/edit/
# can i figure out the rate of change, scrape data into doc first and try to detect change in columns
# http://www.oireachtas.ie/members-hist/default.asp?housetype=0
#http://www.oireachtas.ie/members-hist/default.asp?housetype=0&HouseNum=28&disp=mem
require 'nokogiri'

# return the bill info from the fetched page
def parse_bill(url)
  page = Nokogiri::HTML(ScraperWiki.scrape(url))
  title = page.search("title")
  name = title[0].content.sub(/ - Tithe an Oireachtais$/, "").strip if title[0]
  
  meta = page.search("//meta[@name='Abstract']")
  abstract = meta[0]['content'].strip if meta[0]

 
  # update the description with full description, since it could be cut off
  # doesn't work right yet, we might have to dive into the hr tags again
  # description = page.search("div.column-center-inner p").map { |p|
  #   p.content.include?(description) ? p.content : nil }.compact[0]
  
  ScraperWiki.save(['name', 'abstract', 'url'], {
    'name' => name,
    'abstract' => abstract,

    'url' => url
  })
  [name, abstract, url]
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
dails = (1..30)

# collect all the bills in this data structure
bill_info = []

dails.each do |dail|
#http://www.oireachtas.ie/members-hist/default.asp?housetype=0&HouseNum=28&disp=mem
  base_url = "http://www.oireachtas.ie/members-hist/default.asp?housetype=0&HouseNum=#{dail}&disp=mem"
  # are there multiple pages? if so, collect them all
  page = Nokogiri::HTML(ScraperWiki.scrape(base_url))
  page_links = page.search("p.bodytext a.bodytext")
  page_urls = page_links.map { |pl| pl['href'] }
  
  # on this page, get all the bill urls
  bill_urls = page.search("div.column-center-inner a").map { |a|
    (a['href'] =~ /default.asp?\d+/ && a.content =~ /\<img src\=\"\/images\/members-details.gif\" width\=\"16\" height\=\"16\" alt\=\"Display by Constituencies\" /\>/) ? a['href'] : nil }.compact
  
  # on each of the other pages for this year, get all the bills
  #page_urls.each do |url|
  #  page = Nokogiri::HTML(ScraperWiki.scrape("http://www.oireachtas.ie/" + url.gsub(" ", "%20")))
  #  bill_urls = bill_urls + page.search("div.column-center-inner a").map { |a|
  #    (a['href'] =~ /DocID=\d+/ && a.content =~ /\[view more\]/) ? a['href'] : nil }.compact
  #end
  
  # now for each bill, parse its "more info page"
  bill_info = bill_info + bill_urls.map { |bill_url|
    # TODO: save URL
    url = "http://www.oireachtas.ie/" + bill_url.gsub(" ", "%20")
    info = parse_bill(url)
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
# this is for "Irish Legislation" to understand and improve it orignal copy here http://scraperwiki.com/scrapers/irish-legislation/edit/
# can i figure out the rate of change, scrape data into doc first and try to detect change in columns
# http://www.oireachtas.ie/members-hist/default.asp?housetype=0
#http://www.oireachtas.ie/members-hist/default.asp?housetype=0&HouseNum=28&disp=mem
require 'nokogiri'

# return the bill info from the fetched page
def parse_bill(url)
  page = Nokogiri::HTML(ScraperWiki.scrape(url))
  title = page.search("title")
  name = title[0].content.sub(/ - Tithe an Oireachtais$/, "").strip if title[0]
  
  meta = page.search("//meta[@name='Abstract']")
  abstract = meta[0]['content'].strip if meta[0]

 
  # update the description with full description, since it could be cut off
  # doesn't work right yet, we might have to dive into the hr tags again
  # description = page.search("div.column-center-inner p").map { |p|
  #   p.content.include?(description) ? p.content : nil }.compact[0]
  
  ScraperWiki.save(['name', 'abstract', 'url'], {
    'name' => name,
    'abstract' => abstract,

    'url' => url
  })
  [name, abstract, url]
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
dails = (1..30)

# collect all the bills in this data structure
bill_info = []

dails.each do |dail|
#http://www.oireachtas.ie/members-hist/default.asp?housetype=0&HouseNum=28&disp=mem
  base_url = "http://www.oireachtas.ie/members-hist/default.asp?housetype=0&HouseNum=#{dail}&disp=mem"
  # are there multiple pages? if so, collect them all
  page = Nokogiri::HTML(ScraperWiki.scrape(base_url))
  page_links = page.search("p.bodytext a.bodytext")
  page_urls = page_links.map { |pl| pl['href'] }
  
  # on this page, get all the bill urls
  bill_urls = page.search("div.column-center-inner a").map { |a|
    (a['href'] =~ /default.asp?\d+/ && a.content =~ /\<img src\=\"\/images\/members-details.gif\" width\=\"16\" height\=\"16\" alt\=\"Display by Constituencies\" /\>/) ? a['href'] : nil }.compact
  
  # on each of the other pages for this year, get all the bills
  #page_urls.each do |url|
  #  page = Nokogiri::HTML(ScraperWiki.scrape("http://www.oireachtas.ie/" + url.gsub(" ", "%20")))
  #  bill_urls = bill_urls + page.search("div.column-center-inner a").map { |a|
  #    (a['href'] =~ /DocID=\d+/ && a.content =~ /\[view more\]/) ? a['href'] : nil }.compact
  #end
  
  # now for each bill, parse its "more info page"
  bill_info = bill_info + bill_urls.map { |bill_url|
    # TODO: save URL
    url = "http://www.oireachtas.ie/" + bill_url.gsub(" ", "%20")
    info = parse_bill(url)
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
