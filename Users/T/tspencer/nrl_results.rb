require 'nokogiri'
require 'open-uri'
require 'scraperwiki'
require 'pp' 

j = 0

for i in 2008..2012

  html = open("http://live.nrlstats.com/nrl/season#{i}.html")
    
  resultsPage = Nokogiri::HTML(html)
  
  resultsPage.search("//div[@class='c5']/div/div/table/tr[position()>1]").each do |result|

    j += 1

    teams = result.search("td")[1].text.split(" v ")
    scores = result.search("td")[2].text.split("-")

    record = {
      'matchDate' => Date.parse(result.search("td")[0].text + " " + i.to_s),
      'homeTeam' => teams.first,
      'awayTeam'=> teams.last,
      'homeScore' => scores.first,
      'awayScore'=> scores.last,
      'matchID'=> j
    }
      
    #pp record    
  
    ScraperWiki.save_sqlite(unique_keys=["matchID"], data=record)
  
  end

end

require 'nokogiri'
require 'open-uri'
require 'scraperwiki'
require 'pp' 

j = 0

for i in 2008..2012

  html = open("http://live.nrlstats.com/nrl/season#{i}.html")
    
  resultsPage = Nokogiri::HTML(html)
  
  resultsPage.search("//div[@class='c5']/div/div/table/tr[position()>1]").each do |result|

    j += 1

    teams = result.search("td")[1].text.split(" v ")
    scores = result.search("td")[2].text.split("-")

    record = {
      'matchDate' => Date.parse(result.search("td")[0].text + " " + i.to_s),
      'homeTeam' => teams.first,
      'awayTeam'=> teams.last,
      'homeScore' => scores.first,
      'awayScore'=> scores.last,
      'matchID'=> j
    }
      
    #pp record    
  
    ScraperWiki.save_sqlite(unique_keys=["matchID"], data=record)
  
  end

end

