# this is for "Irish Legislation" to understand and improve it orignal copy here http://scraperwiki.com/scrapers/irish-legislation/edit/
# http://www.oireachtas.ie/ViewDoc.asp?DocId=-1&CatID=59&m=b
require 'nokogiri'

# return the bill info from the fetched page
def parse_bill(url)
  page = Nokogiri::HTML(ScraperWiki.scrape(url))
  doc.search('dd').each do |dd|
#    ScraperWiki.save(['data'], {'data' => td.inner_html})

 
  # update the description with full description, since it could be cut off
  # doesn't work right yet, we might have to dive into the hr tags again
  # description = page.search("div.column-center-inner p").map { |p|
  #   p.content.include?(description) ? p.content : nil }.compact[0]
  
  ScraperWiki.save(['dd', 'url'], {
    'dd' => dd,
    'url' => url
  })
  [name, url]
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
#end

# goes from year 1997-2010, edit this as needed
years = (1997..2011)
#weeks = (01..52)
# collect all the bills in this data structure
bill_info = []
years.each do |year|
#weeks.each do |week|
  base_url = "http://president.ie/index.php?section=6&engagement={year}&lang=eng"
#  base_url = "http://president.ie/index.php?section=6&engagement={year}{week}&lang=eng"
  # are there multiple pages? if so, collect them all
  page = Nokogiri::HTML(ScraperWiki.scrape(base_url))
  page_links = page.search("p.bodytext a.bodytext")

  
  # on this page, get all the bill urls
  bill_urls = page.search("div.column-center-inner a").map { |a|
    (a['href'] =~ /section=6\&amp;engagement=\d+/ && a.content =~ /Week beginning/) ? a['href'] : nil }.compact
  
  # on each of the other pages for this year, get all the bills
 

  # now for each bill, parse its "more info page"
  bill_info = bill_info + bill_urls.map { |bill_url|
    # TODO: save URL
    url = "http://president.ie/" + bill_url.gsub(" ", "%20")
    info = parse_bill(url)
  }
end# this is for "Irish Legislation" to understand and improve it orignal copy here http://scraperwiki.com/scrapers/irish-legislation/edit/
# http://www.oireachtas.ie/ViewDoc.asp?DocId=-1&CatID=59&m=b
require 'nokogiri'

# return the bill info from the fetched page
def parse_bill(url)
  page = Nokogiri::HTML(ScraperWiki.scrape(url))
  doc.search('dd').each do |dd|
#    ScraperWiki.save(['data'], {'data' => td.inner_html})

 
  # update the description with full description, since it could be cut off
  # doesn't work right yet, we might have to dive into the hr tags again
  # description = page.search("div.column-center-inner p").map { |p|
  #   p.content.include?(description) ? p.content : nil }.compact[0]
  
  ScraperWiki.save(['dd', 'url'], {
    'dd' => dd,
    'url' => url
  })
  [name, url]
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
#end

# goes from year 1997-2010, edit this as needed
years = (1997..2011)
#weeks = (01..52)
# collect all the bills in this data structure
bill_info = []
years.each do |year|
#weeks.each do |week|
  base_url = "http://president.ie/index.php?section=6&engagement={year}&lang=eng"
#  base_url = "http://president.ie/index.php?section=6&engagement={year}{week}&lang=eng"
  # are there multiple pages? if so, collect them all
  page = Nokogiri::HTML(ScraperWiki.scrape(base_url))
  page_links = page.search("p.bodytext a.bodytext")

  
  # on this page, get all the bill urls
  bill_urls = page.search("div.column-center-inner a").map { |a|
    (a['href'] =~ /section=6\&amp;engagement=\d+/ && a.content =~ /Week beginning/) ? a['href'] : nil }.compact
  
  # on each of the other pages for this year, get all the bills
 

  # now for each bill, parse its "more info page"
  bill_info = bill_info + bill_urls.map { |bill_url|
    # TODO: save URL
    url = "http://president.ie/" + bill_url.gsub(" ", "%20")
    info = parse_bill(url)
  }
end# this is for "Irish Legislation" to understand and improve it orignal copy here http://scraperwiki.com/scrapers/irish-legislation/edit/
# http://www.oireachtas.ie/ViewDoc.asp?DocId=-1&CatID=59&m=b
require 'nokogiri'

# return the bill info from the fetched page
def parse_bill(url)
  page = Nokogiri::HTML(ScraperWiki.scrape(url))
  doc.search('dd').each do |dd|
#    ScraperWiki.save(['data'], {'data' => td.inner_html})

 
  # update the description with full description, since it could be cut off
  # doesn't work right yet, we might have to dive into the hr tags again
  # description = page.search("div.column-center-inner p").map { |p|
  #   p.content.include?(description) ? p.content : nil }.compact[0]
  
  ScraperWiki.save(['dd', 'url'], {
    'dd' => dd,
    'url' => url
  })
  [name, url]
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
#end

# goes from year 1997-2010, edit this as needed
years = (1997..2011)
#weeks = (01..52)
# collect all the bills in this data structure
bill_info = []
years.each do |year|
#weeks.each do |week|
  base_url = "http://president.ie/index.php?section=6&engagement={year}&lang=eng"
#  base_url = "http://president.ie/index.php?section=6&engagement={year}{week}&lang=eng"
  # are there multiple pages? if so, collect them all
  page = Nokogiri::HTML(ScraperWiki.scrape(base_url))
  page_links = page.search("p.bodytext a.bodytext")

  
  # on this page, get all the bill urls
  bill_urls = page.search("div.column-center-inner a").map { |a|
    (a['href'] =~ /section=6\&amp;engagement=\d+/ && a.content =~ /Week beginning/) ? a['href'] : nil }.compact
  
  # on each of the other pages for this year, get all the bills
 

  # now for each bill, parse its "more info page"
  bill_info = bill_info + bill_urls.map { |bill_url|
    # TODO: save URL
    url = "http://president.ie/" + bill_url.gsub(" ", "%20")
    info = parse_bill(url)
  }
end