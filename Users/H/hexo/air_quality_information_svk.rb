require 'nokogiri'
html = ScraperWiki.scrape("http://www.shmu.sk/sk/?page=991")

data = {}
headers = []

doc = Nokogiri::HTML(html)

to_scrape = []
doc.xpath("//select[@class='w150']/option/@value").each do |val|
  p val.value
  begin
    res = ScraperWiki.select("count(*) from swdata where timestamp is ?", val.value).first
    to_scrape << val.value if res["count(*)"] == 0
  rescue
    to_scrape << val.value
  end
end
#puts "to_scrape = #{to_scrape.inspect}"


to_scrape.each do |current_ts|
  html = ScraperWiki.scrape("http://www.shmu.sk/sk/?page=991", "t=#{current_ts}")
  
  data = {}
  headers = []
  
  doc = Nokogiri::HTML(html)  


  doc.xpath("//table/tr/th").each do |th|
    headers << th.content.to_s
  end
  
  tstamp = doc.at_xpath('//select[@class="w150"]/option[@selected="selected"]/@value').to_s
  
  doc.xpath("//table/tr/td").each_slice(headers.size) do |tds|
    data = headers.zip(tds).map do |td|
      cont = td[1].content.to_s
      cont = case cont
              when "\u00A0"
               then nil
              when '*'
               then 'N/A'
              else cont
             end
              
      {td[0] => cont}
    end.reduce(Hash.new) do |r,s|
      r.merge(s)
    end
    data.merge!("timestamp" => tstamp)
    ScraperWiki.save_sqlite(unique_keys = [], data = data)
  end
end

#p ScraperWiki.show_tables()
