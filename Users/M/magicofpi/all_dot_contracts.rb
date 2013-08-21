require 'nokogiri'

urls = []
years = ["98","99","00","01","02","03","04","05","06","07","08","09","10"]
years.each do |year|
  (1..4).each do |q|
    u = {}
    u[:address] = "http://www6.hawaii.gov/dot/administration/contracts/bidopening/fy#{year}/q#{q}/index.htm"
    u[:fy] = year
    u[:q] = q 
    urls << u
  end
end

p urls

urls.each do |url|

  html = ScraperWiki.scrape(url[:address])
  doc = Nokogiri::HTML(html)
  all_bids = {}
  curr_id = ""

  doc.css('table tr table tr table tr').each do |row|
    cells = row.css('td')
    attr_name = cells[0].inner_text.strip.downcase.gsub(/[^a-zA-Z]/, '').delete(':')
    attribute = cells[1].inner_text.strip
    curr_id = attribute if attr_name.include?("projectno")
    if attr_name.include?("bidopening")
      attribute = attribute.gsub('\302\240','').gsub(/2:00\s*P.\s*M.\s*/,'').gsub(/^\s*,/,'').strip unless attribute.nil? 
    end
    # puts curr_id
    # puts "#{attr_name} = #{attribute}"
    all_bids["#{curr_id}"] = {} if all_bids["#{curr_id}"].nil? 
    all_bids["#{curr_id}"]["#{attr_name}"] = attribute
    all_bids["#{curr_id}"]["fy"] = url[:fy]
    all_bids["#{curr_id}"]["q"] = url[:q]
  end

  all_bids.each do |bid|
    bidinfo = bid[1]
    p bidinfo
    ScraperWiki.save_sqlite(unique_keys=['projectno'], data=bidinfo)
  end

end

