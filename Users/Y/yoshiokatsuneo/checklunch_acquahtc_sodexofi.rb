# Blank Ruby

require 'open-uri'

(0..10).each{|day_to_add|
  day = Date.today + day_to_add
  body = open("http://www.sodexo.fi/ruokalistat/output/daily_json/399/#{day.year}/#{day.month}/#{day.day}/en").read
  doc = JSON.parse(body);


  doc["courses"].each{|course|
          date = day
          title = course["title_en"]
          title += course["properties"].to_s if course["properties"]
          price = course["price"]
          doc = {
            :date => date,
            :title => title,
            :price => price
          }
          ScraperWiki::save_sqlite(['date','title'], doc) 
  
  }

}
# Blank Ruby

require 'open-uri'

(0..10).each{|day_to_add|
  day = Date.today + day_to_add
  body = open("http://www.sodexo.fi/ruokalistat/output/daily_json/399/#{day.year}/#{day.month}/#{day.day}/en").read
  doc = JSON.parse(body);


  doc["courses"].each{|course|
          date = day
          title = course["title_en"]
          title += course["properties"].to_s if course["properties"]
          price = course["price"]
          doc = {
            :date => date,
            :title => title,
            :price => price
          }
          ScraperWiki::save_sqlite(['date','title'], doc) 
  
  }

}
# Blank Ruby

require 'open-uri'

(0..10).each{|day_to_add|
  day = Date.today + day_to_add
  body = open("http://www.sodexo.fi/ruokalistat/output/daily_json/399/#{day.year}/#{day.month}/#{day.day}/en").read
  doc = JSON.parse(body);


  doc["courses"].each{|course|
          date = day
          title = course["title_en"]
          title += course["properties"].to_s if course["properties"]
          price = course["price"]
          doc = {
            :date => date,
            :title => title,
            :price => price
          }
          ScraperWiki::save_sqlite(['date','title'], doc) 
  
  }

}
