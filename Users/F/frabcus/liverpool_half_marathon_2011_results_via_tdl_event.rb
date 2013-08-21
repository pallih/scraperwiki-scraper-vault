# TDL Event Services - the results of chips in your bibs

require 'nokogiri'

race_id = 623 # Liverpool Half Marathon 2011

# Parse one page of TDL results for one particular race
def get_one_page(race_id, page)
  url = "http://www.tdl.ltd.uk/results.php?checked=1&race_id=" +race_id.to_s + "&submit=sent&page=" + page.to_s
  html = ScraperWiki.scrape(url)

  doc = Nokogiri::HTML(html)
  headings = nil
  saved = 0
  datas = []
  doc.search('tr').each do |tr|
    tds = tr.search('td')
    if tr["style"] == "color:White;background-color:#CC0000;":
      # get headings to use as keys
      headings = tds.map { |x| x.inner_html().gsub("<b>", "").gsub("</b>", "") }
      next
    end

    raise "length of line differs from headings" if tds.size != headings.size
    data = { 'Race ID' => race_id, 'Source' => url }
    headings.zip(tds).each do |heading, td|
      data[heading] = td.inner_html
    end
    datas.push data
    #ScraperWiki.save(unique_keys=['Race Number',], data=data)
    saved = saved + 1
  end
  # XXX this should make it faster but doesn't work
  #puts datas.to_yaml
  if datas.size > 0 
    ScraperWiki.save(unique_keys=['Race Number',], data=datas)
  end

  # Return if there was nothing on this page (beyond end)
  puts "saved records: " + saved.to_s
  return saved != 0
end

# Go through every page until there are no rows on one
page = 1
saved = true
while saved
  puts "page " + page.to_s
  saved = get_one_page(623, page)
  page = page + 1
end

