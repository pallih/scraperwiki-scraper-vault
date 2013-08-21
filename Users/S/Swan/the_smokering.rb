require 'nokogiri'

@counter = 0
@continue = true

while @continue
  html = ScraperWiki.scrape('http://www.thesmokering.com/index.php?option=com_webring&task=browse&limitstart='+(@counter * 20).to_s)

  @counter += 1

  if html
    doc = Nokogiri::HTML(html)
    doc.search("td[class='tablehov']").each do |v|
      @regex = /.*?<a.*href="(.*)".*>(.*)<\/a>.*<br>(.*)/
      data = {
        'raw' => v.inner_html,
        'title' => @regex.match(v.inner_html)[2],
        'url' => @regex.match(v.inner_html)[1],
        'text' => @regex.match(v.inner_html)[3]
      }
      puts data.to_json
      ScraperWiki.save_sqlite(unique_keys=['title'], data=data)
    end
  else
    @continue = false
  end
end