require 'nokogiri'

urls = []
u = {}
u[:address] = "http://state.hi.us/dot/administration/contracts/bidopening/bidcurrent.htm"
u[:fy] = 2011
u[:q] = 0
urls << u

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
    attribute = attribute.gsub(/\s{2,}/,' ').gsub(/\n/,'')
    attribute = attribute.split(' ').collect{|x| x.capitalize }.join(' ') if attr_name.include?("projecttitle")
    attribute = attribute.gsub(/\s*:\s*/,'') if attr_name.include?("estimate")
    curr_id = attribute if attr_name.include?("projectno")
    if attr_name.include?("bidopening")
      attribute = attribute.gsub('\302\240','').gsub(/^\s*,/,'').strip unless attribute.nil? 
    end
    all_bids["#{curr_id}"] = {} if all_bids["#{curr_id}"].nil? 
    if attribute =~ /\W*2\W*00\W*P\W*M\W*/
      time = attribute.scan(/\W*2\W*00\W*P\W*M\W*/).join('').gsub(/[\n,]/,'').strip.gsub('P. M.','P.M.')
      time.gsub!(/\s*[.]\s*/,'')
      time.gsub!(/^\W*/,'')
      date = attribute.split(/\W*2\W*00\W*P\W*M\W*/).join('').gsub(/[\n.]/,'').strip
      date = date.split(' ').collect {|x| x.capitalize }.join(' ')
      date.gsub!(/^\W*/,'')
      all_bids["#{curr_id}"]["time"] = time
      all_bids["#{curr_id}"]["date"] = date
    else
      if attr_name == "bidopening"
        attr_name = "date"
        attribute = attribute.split(' ').collect {|x| x.capitalize}.join(' ')
      end
      all_bids["#{curr_id}"]["#{attr_name}"] = attribute
    end
    all_bids["#{curr_id}"]["fy"] = url[:fy]
    all_bids["#{curr_id}"]["q"] = url[:q]
  end

  all_bids.each do |bid|
    bidinfo = bid[1]
    p bidinfo
    ScraperWiki.save_sqlite(unique_keys=['projectno'], data=bidinfo)
  end

end

require 'nokogiri'

urls = []
u = {}
u[:address] = "http://state.hi.us/dot/administration/contracts/bidopening/bidcurrent.htm"
u[:fy] = 2011
u[:q] = 0
urls << u

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
    attribute = attribute.gsub(/\s{2,}/,' ').gsub(/\n/,'')
    attribute = attribute.split(' ').collect{|x| x.capitalize }.join(' ') if attr_name.include?("projecttitle")
    attribute = attribute.gsub(/\s*:\s*/,'') if attr_name.include?("estimate")
    curr_id = attribute if attr_name.include?("projectno")
    if attr_name.include?("bidopening")
      attribute = attribute.gsub('\302\240','').gsub(/^\s*,/,'').strip unless attribute.nil? 
    end
    all_bids["#{curr_id}"] = {} if all_bids["#{curr_id}"].nil? 
    if attribute =~ /\W*2\W*00\W*P\W*M\W*/
      time = attribute.scan(/\W*2\W*00\W*P\W*M\W*/).join('').gsub(/[\n,]/,'').strip.gsub('P. M.','P.M.')
      time.gsub!(/\s*[.]\s*/,'')
      time.gsub!(/^\W*/,'')
      date = attribute.split(/\W*2\W*00\W*P\W*M\W*/).join('').gsub(/[\n.]/,'').strip
      date = date.split(' ').collect {|x| x.capitalize }.join(' ')
      date.gsub!(/^\W*/,'')
      all_bids["#{curr_id}"]["time"] = time
      all_bids["#{curr_id}"]["date"] = date
    else
      if attr_name == "bidopening"
        attr_name = "date"
        attribute = attribute.split(' ').collect {|x| x.capitalize}.join(' ')
      end
      all_bids["#{curr_id}"]["#{attr_name}"] = attribute
    end
    all_bids["#{curr_id}"]["fy"] = url[:fy]
    all_bids["#{curr_id}"]["q"] = url[:q]
  end

  all_bids.each do |bid|
    bidinfo = bid[1]
    p bidinfo
    ScraperWiki.save_sqlite(unique_keys=['projectno'], data=bidinfo)
  end

end

