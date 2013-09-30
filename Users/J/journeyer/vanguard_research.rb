def extract_link(itemrow)
  itemrow.at("a")[:href]
end

def extract_headline(i)
  ""
end

def extract_description(i)
  ""
end

def extract_datetime(i)
  Date.parse(i.at("div.dt").inner_text.split.join(' ')).strftime("%Y-%m-%dT00:01:00+05:30")
end

require 'nokogiri'
url="https://institutional.vanguard.com/VGApp/iip/site/institutional/researchandcomm"
data=ScraperWiki.scrape(url)
doc=Nokogiri(data)
items = doc/"table.summaryTable tr"

#(doc/("table#iamResearchForm:researchSummaryTable")).search("tr#iamResearchForm:researchSummaryTabletbody0")
r=%r{^.*/videos/(\d+)/.*}
items.each{|i|
  data={}
  data['link'] = extract_link(i)
  data['headline'] = extract_headline(i)
  data['description'] = extract_headline(i)
  data['time'] = extract_datetime(i)
  m = r.match(data['link'])
  if m
    data['videoid'] = (m)[1]
    puts data.to_json
    ScraperWiki.save_sqlite(unique_keys=['videoid'], data=data)
  end
}
def extract_link(itemrow)
  itemrow.at("a")[:href]
end

def extract_headline(i)
  ""
end

def extract_description(i)
  ""
end

def extract_datetime(i)
  Date.parse(i.at("div.dt").inner_text.split.join(' ')).strftime("%Y-%m-%dT00:01:00+05:30")
end

require 'nokogiri'
url="https://institutional.vanguard.com/VGApp/iip/site/institutional/researchandcomm"
data=ScraperWiki.scrape(url)
doc=Nokogiri(data)
items = doc/"table.summaryTable tr"

#(doc/("table#iamResearchForm:researchSummaryTable")).search("tr#iamResearchForm:researchSummaryTabletbody0")
r=%r{^.*/videos/(\d+)/.*}
items.each{|i|
  data={}
  data['link'] = extract_link(i)
  data['headline'] = extract_headline(i)
  data['description'] = extract_headline(i)
  data['time'] = extract_datetime(i)
  m = r.match(data['link'])
  if m
    data['videoid'] = (m)[1]
    puts data.to_json
    ScraperWiki.save_sqlite(unique_keys=['videoid'], data=data)
  end
}
