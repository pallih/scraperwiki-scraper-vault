# coding: utf-8

require 'nokogiri'        

@year = Date.today.year

def ParseDate(date)
  date =~/((\d+)年)?(\d+)月(\d+)日/
  if $1
    @year = $1.to_i
  end
  Date.new(@year, $3.to_i, $4.to_i)
end

html = ScraperWiki.scrape("http://www.ginreihall.com/schedule/index.html").force_encoding("SHIFT_JIS")
doc = Nokogiri::HTML(html.encode("utf-8"),nil)
for v in doc.search("td[@class='block_link_L']")
  date = v.search('div a').inner_html.split("〜")
  if /'(.+\.html)'/ =~ v.search('div a')[0]["onclick"]
    href="http://www.ginreihall.com/schedule/"+$1
    html2 = ScraperWiki.scrape(href).force_encoding("SHIFT_JIS")
    doc2 = Nokogiri::HTML(html2.encode("utf-8"),nil)
    desc = doc2.search('td[@class="bg_contents"] table')[1]
  end
  data = {
    'href' => href,
    'begin'=> ParseDate(date[0]),
    'end' => ParseDate(date[1]),
    'desc' => desc,
    'program' => []
  }
  for tr in v.search(:tr)
    cells = tr.search('td')
    data["program"].push({
      'title' => cells[0].inner_html,
      '1' => cells[1].search(:div).inner_html,
      '2' => cells[2].search(:div).inner_html,
      '3' => cells[3].search(:div).inner_html,
      '4' => cells[4] ? cells[4].search(:div).inner_html : nil
    })
  end
  puts data
  ScraperWiki.save(['begin'], [data])
end
