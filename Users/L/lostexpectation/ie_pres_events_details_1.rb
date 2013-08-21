# written by db find http://scraperwiki.com/scrapers/ie_pres_events_details/

require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}
ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS EVENTS(ID INTEGER PRIMARY KEY AUTOINCREMENT,DAY TEXT,TIME_PLACE TEXT,URL TEXT,DETAILS TEXT);")

BASE_URL ="http://president.ie/"

def get_metadata(key, default)
    begin
      ScraperWiki.get_var(key, default)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    end
end

def save_metadata(key, value)
    begin
      ScraperWiki.save_var(key, value)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{default})"
    end
end

def strip(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/[\x80-\xff]|^\s+|:|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def persist_events(records)
  c = ScraperWiki.sqliteexecute("select count(*) from events where day=? and time_place=?",[records['DAY'],records['TIME_PLACE']])['data'][0][0]
  if c == 0
    ScraperWiki.sqliteexecute("insert into events(day,time_place,details,s_url) values(?,?,?,?)",[records['DAY'],records['TIME_PLACE'],records['DETAILS'],records['URL']])
    ScraperWiki.commit()
  else
    puts "Update?"
  end
end

engt = get_metadata("ENGAGEMENT",201101)
s_url = BASE_URL + "index.php?section=6&engagement=#{engt}&lang=eng"

begin
  pg = br.get(s_url)
  doc = Nokogiri::HTML(pg.body)
  scraped = false
  doc.xpath("//dl").each{|dl|
    details = []
    time_place = []
    day = strip(dl.xpath("dt//strong"))
    dl.xpath("dd//strong").each{|a|
      time_place << strip(a) unless strip(a).empty? 
    }
  
    dl.xpath("dd//p[not(descendant::strong)]").each{|a|
      details << strip(a) unless strip(a).empty? 
    }
    len = time_place.length
  #pp day
  #pp time_place
  #pp details
    (0..len).each{|l|
      records ={}
      records["DAY"] = day
      records["TIME_PLACE"] = time_place[l]
      records["DETAILS"] = details[l]
      records["URL"] = s_url
      puts records.inspect unless records["TIME_PLACE"].nil? 
      persist_events(records) unless records["TIME_PLACE"].nil? 
      scraped = true

      #ScraperWiki.sqliteexecute(unique_keys=['TIME_PLACE','DAY'],records,table_name='EVENTS') unless records["TIME_PLACE"].nil? 
    }
    save_metadata("ENGAGEMENT",engt+1) unless scraped
  }
  
rescue Exception => e
  puts e.backtrace
end
# written by db find http://scraperwiki.com/scrapers/ie_pres_events_details/

require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}
ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS EVENTS(ID INTEGER PRIMARY KEY AUTOINCREMENT,DAY TEXT,TIME_PLACE TEXT,URL TEXT,DETAILS TEXT);")

BASE_URL ="http://president.ie/"

def get_metadata(key, default)
    begin
      ScraperWiki.get_var(key, default)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    end
end

def save_metadata(key, value)
    begin
      ScraperWiki.save_var(key, value)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{default})"
    end
end

def strip(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/[\x80-\xff]|^\s+|:|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def persist_events(records)
  c = ScraperWiki.sqliteexecute("select count(*) from events where day=? and time_place=?",[records['DAY'],records['TIME_PLACE']])['data'][0][0]
  if c == 0
    ScraperWiki.sqliteexecute("insert into events(day,time_place,details,s_url) values(?,?,?,?)",[records['DAY'],records['TIME_PLACE'],records['DETAILS'],records['URL']])
    ScraperWiki.commit()
  else
    puts "Update?"
  end
end

engt = get_metadata("ENGAGEMENT",201101)
s_url = BASE_URL + "index.php?section=6&engagement=#{engt}&lang=eng"

begin
  pg = br.get(s_url)
  doc = Nokogiri::HTML(pg.body)
  scraped = false
  doc.xpath("//dl").each{|dl|
    details = []
    time_place = []
    day = strip(dl.xpath("dt//strong"))
    dl.xpath("dd//strong").each{|a|
      time_place << strip(a) unless strip(a).empty? 
    }
  
    dl.xpath("dd//p[not(descendant::strong)]").each{|a|
      details << strip(a) unless strip(a).empty? 
    }
    len = time_place.length
  #pp day
  #pp time_place
  #pp details
    (0..len).each{|l|
      records ={}
      records["DAY"] = day
      records["TIME_PLACE"] = time_place[l]
      records["DETAILS"] = details[l]
      records["URL"] = s_url
      puts records.inspect unless records["TIME_PLACE"].nil? 
      persist_events(records) unless records["TIME_PLACE"].nil? 
      scraped = true

      #ScraperWiki.sqliteexecute(unique_keys=['TIME_PLACE','DAY'],records,table_name='EVENTS') unless records["TIME_PLACE"].nil? 
    }
    save_metadata("ENGAGEMENT",engt+1) unless scraped
  }
  
rescue Exception => e
  puts e.backtrace
end
