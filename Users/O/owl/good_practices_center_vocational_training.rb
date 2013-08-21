# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://good-practice.bibb.de/adb/"

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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def text(str)
  begin
    return (str.nil? or str.text.nil?) ? "" : str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,records)
  if act == "list"
    holder = []
    Nokogiri::HTML(data).xpath(".//table[@border='1']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      r = {
        "NAME" => text(td[0].xpath("font/a/text()")),
        "ANSPRECHPARTNER" => text(td[1].xpath("font/text()")),
        "STRASSE" =>text(td[2].xpath("font/text()")),
        "PLZ-ORT" =>text(td[3].xpath("font/text()")),
        "TEL" =>text(td[4].xpath("font/text()")),
        "FAX" =>text(td[5].xpath("font/text()")),
        "EMAIL" =>text(td[6].xpath("font/text()")),
        "DOC" =>Time.now.to_s,
        "URL"=>BASE_URL+attributes(td[0].xpath("font/a"),"href")
      }
      holder << r
    }
    #ScraperWiki.save_sqlite(unique_keys=['NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
    return holder
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    #records = {'NAME'=>text(doc.xpath(".//h3[@class='Title']/text()"))}
    doc.xpath(".//div[@id='content_table' and preceding-sibling::div[h3[text()='Eines unserer Projekte']]][1]/table/tr").each{|tr|
      td = tr.xpath("td")
      tmp_key = text(td[0].xpath("p/text()"))
      key = nil
      key = "DESCRIPTION" if tmp_key.nil? or tmp_key.empty? 
      #puts tmp_key.inspect
      case tmp_key 
        when tmp_key = "Gegenstand/Ziele des Projekts:"
          key = "PURPOSE"
        when tmp_key = "Informationen zur Zielgruppe:"
          key = "INFO"
        when tmp_key = "Finanzierende Stellen, Rechtsgrundlagen:"
          key = "FIN_AGENCY"
        when tmp_key = "Kooperationspartner:"
          key = "PARTNER"
        when tmp_key = "Teil-/Abschlüsse:"
          key = "TEIL"
        when tmp_key = "Förderzeitraum:"
          key = "FIN_PERIOD"
        else
          key = tmp_key.upcase
      end unless tmp_key.nil? or tmp_key.empty? 
      records[key] = text(td[1].xpath("p/text()|p/b/text()")) unless key.nil? or key.empty? 
    }
    records['WEBSITE']=text(doc.xpath(".//td[text()='Internet:']/following-sibling::td[1]/a/text()"))
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['NAME'],records,table_name='swdata',verbose=2) unless records['NAME'].nil? or records['NAME'].empty? 
  end
end

def exists(name)
  begin
    return ScraperWiki.sqliteexecute("select count(*) from swdata where name=?",[name])['data'][0][0]
  rescue Exception => e
    puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
    return 0
  end
end

def action()
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "suche.php?action=result&searchid=3&adressliste=1"
    pg = br.get(s_url)
    lst = scrape(pg.body,"list",nil)
    lst.each{|records|
      begin
        pg_tmp = br.get(records['URL'])
        scrape(pg_tmp.body,"details",records)
      #break
      rescue Exception => e
        retry if e.inspect =~ /Timeout|TIME|HTTP/
      end unless exists(records['NAME'])>=1
    }
  rescue Exception => e
    puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
    sleep(30)
    retry if e.inspect =~ /Timeout|TIME|HTTP/
  end
end

#def action(s_url)
#  scrape(Mechanize.new.get(s_url).body,"details",s_url)  
#end
#action("https://good-practice.bibb.de/adb/suche.php?action=view&id=3314")
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://good-practice.bibb.de/adb/"

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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def text(str)
  begin
    return (str.nil? or str.text.nil?) ? "" : str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,records)
  if act == "list"
    holder = []
    Nokogiri::HTML(data).xpath(".//table[@border='1']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      r = {
        "NAME" => text(td[0].xpath("font/a/text()")),
        "ANSPRECHPARTNER" => text(td[1].xpath("font/text()")),
        "STRASSE" =>text(td[2].xpath("font/text()")),
        "PLZ-ORT" =>text(td[3].xpath("font/text()")),
        "TEL" =>text(td[4].xpath("font/text()")),
        "FAX" =>text(td[5].xpath("font/text()")),
        "EMAIL" =>text(td[6].xpath("font/text()")),
        "DOC" =>Time.now.to_s,
        "URL"=>BASE_URL+attributes(td[0].xpath("font/a"),"href")
      }
      holder << r
    }
    #ScraperWiki.save_sqlite(unique_keys=['NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
    return holder
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    #records = {'NAME'=>text(doc.xpath(".//h3[@class='Title']/text()"))}
    doc.xpath(".//div[@id='content_table' and preceding-sibling::div[h3[text()='Eines unserer Projekte']]][1]/table/tr").each{|tr|
      td = tr.xpath("td")
      tmp_key = text(td[0].xpath("p/text()"))
      key = nil
      key = "DESCRIPTION" if tmp_key.nil? or tmp_key.empty? 
      #puts tmp_key.inspect
      case tmp_key 
        when tmp_key = "Gegenstand/Ziele des Projekts:"
          key = "PURPOSE"
        when tmp_key = "Informationen zur Zielgruppe:"
          key = "INFO"
        when tmp_key = "Finanzierende Stellen, Rechtsgrundlagen:"
          key = "FIN_AGENCY"
        when tmp_key = "Kooperationspartner:"
          key = "PARTNER"
        when tmp_key = "Teil-/Abschlüsse:"
          key = "TEIL"
        when tmp_key = "Förderzeitraum:"
          key = "FIN_PERIOD"
        else
          key = tmp_key.upcase
      end unless tmp_key.nil? or tmp_key.empty? 
      records[key] = text(td[1].xpath("p/text()|p/b/text()")) unless key.nil? or key.empty? 
    }
    records['WEBSITE']=text(doc.xpath(".//td[text()='Internet:']/following-sibling::td[1]/a/text()"))
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['NAME'],records,table_name='swdata',verbose=2) unless records['NAME'].nil? or records['NAME'].empty? 
  end
end

def exists(name)
  begin
    return ScraperWiki.sqliteexecute("select count(*) from swdata where name=?",[name])['data'][0][0]
  rescue Exception => e
    puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
    return 0
  end
end

def action()
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "suche.php?action=result&searchid=3&adressliste=1"
    pg = br.get(s_url)
    lst = scrape(pg.body,"list",nil)
    lst.each{|records|
      begin
        pg_tmp = br.get(records['URL'])
        scrape(pg_tmp.body,"details",records)
      #break
      rescue Exception => e
        retry if e.inspect =~ /Timeout|TIME|HTTP/
      end unless exists(records['NAME'])>=1
    }
  rescue Exception => e
    puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
    sleep(30)
    retry if e.inspect =~ /Timeout|TIME|HTTP/
  end
end

#def action(s_url)
#  scrape(Mechanize.new.get(s_url).body,"details",s_url)  
#end
#action("https://good-practice.bibb.de/adb/suche.php?action=view&id=3314")
action()