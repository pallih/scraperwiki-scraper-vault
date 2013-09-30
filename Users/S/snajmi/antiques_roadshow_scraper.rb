#encoding: utf-8
require 'nokogiri'
require 'open-uri'

u = "http://www.pbs.org/cgi-registry/wgbh/roadshow/archive_search.cgi?q=&category=&appraiser=&city=&episode=&season=&value_min=&value_max=&x=&y=13"

doc = Nokogiri::HTML(open(u))

#tells the doc to parse the HTML from the url fed into the variable 'html'
for item in doc.search("div[@class=result_item]")
  data = {
    'Link' => "http://www.pbs.org" + item.search("a").first.attribute("href").to_s
  } 
    # => means assign to a hashtable
    # xpath is a way to search xml, // means anything underneath that level
  t = item.search("span[@class=result_title] a").xpath("text()").to_s
  utf = t.encode("US-ASCII", undef: :replace, invalid: :replace)
  data['Title'] = utf 

  for a in item.search("div[@class=summary] span[@class=label]")
    k = a.xpath("text()").to_s.strip.gsub(/:/, '')
    v = a.xpath("following-sibling::text()[1]") #get the text after anything that's the label text
    if v.to_s != " "
      v = a.xpath("following-sibling::text()")
    end
    data[k] = v 
  end

  ScraperWiki.save_sqlite(unique_keys=['Link', 'Title', 'Episode', 'Appraiser', 'Value'], data=data)
end

#encoding: utf-8
require 'nokogiri'
require 'open-uri'

u = "http://www.pbs.org/cgi-registry/wgbh/roadshow/archive_search.cgi?q=&category=&appraiser=&city=&episode=&season=&value_min=&value_max=&x=&y=13"

doc = Nokogiri::HTML(open(u))

#tells the doc to parse the HTML from the url fed into the variable 'html'
for item in doc.search("div[@class=result_item]")
  data = {
    'Link' => "http://www.pbs.org" + item.search("a").first.attribute("href").to_s
  } 
    # => means assign to a hashtable
    # xpath is a way to search xml, // means anything underneath that level
  t = item.search("span[@class=result_title] a").xpath("text()").to_s
  utf = t.encode("US-ASCII", undef: :replace, invalid: :replace)
  data['Title'] = utf 

  for a in item.search("div[@class=summary] span[@class=label]")
    k = a.xpath("text()").to_s.strip.gsub(/:/, '')
    v = a.xpath("following-sibling::text()[1]") #get the text after anything that's the label text
    if v.to_s != " "
      v = a.xpath("following-sibling::text()")
    end
    data[k] = v 
  end

  ScraperWiki.save_sqlite(unique_keys=['Link', 'Title', 'Episode', 'Appraiser', 'Value'], data=data)
end

