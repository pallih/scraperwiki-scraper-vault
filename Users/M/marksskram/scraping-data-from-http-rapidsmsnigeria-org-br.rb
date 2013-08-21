require 'nokogiri'           

STATES = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37"]

MONTHS = ["2013/5","2013/4","2013/3","2013/2","2013/1","2012/12","2012/11","2012/10","2012/9","2012/8","2012/7","2012/6","2012/5","2012/4","2012/3","2012/2","2012/1","2011/12","2011/11","2011/10","2011/9","2011/8","2011/7","2011/6","2011/5","2011/4","2011/3","2011/2","2011/1"]

STATES.each do |state_id|
  MONTHS.each do |month_id|
    url = "http://rapidsmsnigeria.org/br/19/#{month_id}"
    puts "analyzing #{url}"

    html = ScraperWiki::scrape(url)
    doc = Nokogiri::HTML(html)
    
    lga_totals = doc.css("tr.totals td:last").map do |total_row|
      total_row.inner_text.gsub(",","").to_i
    end
    
    page_total = lga_totals.inject{|sum,x| sum + x }
    
    puts "page_total for #{url} is #{page_total}"
  end
end