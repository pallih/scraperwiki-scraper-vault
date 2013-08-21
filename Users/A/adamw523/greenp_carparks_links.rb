require "hpricot"

html = ScraperWiki.scrape("http://parking.greenp.com/parking-info/carpark-info.html")

name_re = /(.*)\<span/
doc = Hpricot(html)

number_of_pages = doc.search("a.pagenum").last.inner_text.to_i

1.upto(number_of_pages) do |page_num|
  list_url = "http://parking.greenp.com/parking-info/carpark-info.html?page=#{page_num}"

  html = ScraperWiki.scrape(list_url)
  doc = Hpricot(html)

  doc.search(".carparks-list").each do |cp|
    #<h1 class="carpark-name"><a  href="/parking-info/carpark-info/20_101-cedarvale-avenue.html">Carpark  20  <span>101 Cedarvale Avenue</span></a></h1>      

    item = {}
item['street_address'] = cp.search("span").inner_html
    item['name'] = cp.search("a")[0].inner_html.match(name_re)[1].strip
    item['url'] = "http://parking.greenp.com#{cp.search("a")[0]['href']}"
    ScraperWiki.save(['url'], item)
  end

end
