require 'nokogiri'
require('date')


sources = {
  'aluminium' => "http://www.lme.com/aluminium.asp",
  'copper' => "http://www.lme.com/copper.asp",
  'lead' => "http://www.lme.com/lead.asp",
  'nickel' => "http://www.lme.com/nickel.asp",
  'zinc' => "http://www.lme.com/zinc.asp"
}

sources.each_pair do |future, url|
  doc = Nokogiri::HTML(ScraperWiki.scrape(url) ) 

#  doc.css("b.primaryHeader")[0].parent.parent.next.css("tr").each do |l| # positionnement au debut du tableau
  doc.css("h3.primaryHeader")[0].parent.parent.next.css("tr").each do |l| # positionnement au debut du tableau
    line = l.css("td")

    begin
      close = (line[2].content.gsub(/,/, "").to_f + line[3].content.gsub(/,/, "").to_f) / 2 # prix mid
    rescue
      close = nil      
    end

    begin
      future_name = line[0].content
      future_date = Date.parse(line[1].content) 
    rescue
      future_date = nil     
    end

    data = { 
      :context => 'prod_lme', 
      :future => future,
      :future_date => future_date,
      :future_name => future_name, 
      :snapshot_date => Date.today,
      :quote_prior_close => close
    }

    ScraperWiki.save_sqlite(unique_keys=['context', 'future', 'future_date', 'snapshot_date'], data=data) unless data[:future_date].nil? 
  
  end

end
#doc2 = doc.search("table[@class='fe_quotes']")



