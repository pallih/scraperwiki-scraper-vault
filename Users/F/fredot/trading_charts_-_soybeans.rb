# Blank Ruby

require 'nokogiri'
require('date')

sources = {
  'soybeans_pit' => "http://data.tradingcharts.com/futures/quotes/S.html",
  'wheat_kansas_elec' => "http://data.tradingcharts.com/futures/quotes/KE.html",
  'corn_pit' => "http://data.tradingcharts.com/futures/quotes/C.html",
  'wheat_elec' => "http://data.tradingcharts.com/futures/quotes/ZW.html",
  'light_crude_oil_nymex' => "http://data.tradingcharts.com/futures/quotes/CL.html",
  'copper_pit' => "http://data.tradingcharts.com/futures/quotes/HG.html"
}

sources.each_pair do |future, url|

  doc = Nokogiri::HTML(ScraperWiki.scrape(url) ) 

  doc.css("tr.qdata").each do |l|
  
    line = l.css("td")

    begin
      tmp = line[9].content.split(" ")
      puts tmp.inspect
      close = tmp[0].to_f + (tmp[1].nil? ? 0 : eval(tmp[1]+".0")) # conversion des 4/8, 6/8 etc..
    rescue
      close = nil      
    end

    begin
      future_date = Date.parse(line[0].content).next_month.prev_day # dernier jour du mois
    rescue
      future_date = nil     
    end

    begin
      quote_date = Date.parse(line[5].content)
      quote_time = Time.parse(line[5].content)
    rescue
      quote_date = nil
      quote_time = nil
    end

    data = { 
      :context => 'test', 
      :future => future,
      :future_date => future_date,
      :future_name => line[0].content, 
      :quote_date => quote_date,
      :quote_time => quote_time,
      :snapshot_date => Date.today,
      :quote_prior_close => close
    }
    ScraperWiki.save_sqlite(unique_keys=['context', 'future', 'future_date', 'snapshot_date'], data=data)
  
  end

end
#doc2 = doc.search("table[@class='fe_quotes']")



# Blank Ruby

require 'nokogiri'
require('date')

sources = {
  'soybeans_pit' => "http://data.tradingcharts.com/futures/quotes/S.html",
  'wheat_kansas_elec' => "http://data.tradingcharts.com/futures/quotes/KE.html",
  'corn_pit' => "http://data.tradingcharts.com/futures/quotes/C.html",
  'wheat_elec' => "http://data.tradingcharts.com/futures/quotes/ZW.html",
  'light_crude_oil_nymex' => "http://data.tradingcharts.com/futures/quotes/CL.html",
  'copper_pit' => "http://data.tradingcharts.com/futures/quotes/HG.html"
}

sources.each_pair do |future, url|

  doc = Nokogiri::HTML(ScraperWiki.scrape(url) ) 

  doc.css("tr.qdata").each do |l|
  
    line = l.css("td")

    begin
      tmp = line[9].content.split(" ")
      puts tmp.inspect
      close = tmp[0].to_f + (tmp[1].nil? ? 0 : eval(tmp[1]+".0")) # conversion des 4/8, 6/8 etc..
    rescue
      close = nil      
    end

    begin
      future_date = Date.parse(line[0].content).next_month.prev_day # dernier jour du mois
    rescue
      future_date = nil     
    end

    begin
      quote_date = Date.parse(line[5].content)
      quote_time = Time.parse(line[5].content)
    rescue
      quote_date = nil
      quote_time = nil
    end

    data = { 
      :context => 'test', 
      :future => future,
      :future_date => future_date,
      :future_name => line[0].content, 
      :quote_date => quote_date,
      :quote_time => quote_time,
      :snapshot_date => Date.today,
      :quote_prior_close => close
    }
    ScraperWiki.save_sqlite(unique_keys=['context', 'future', 'future_date', 'snapshot_date'], data=data)
  
  end

end
#doc2 = doc.search("table[@class='fe_quotes']")



