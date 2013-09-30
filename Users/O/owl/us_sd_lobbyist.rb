require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://apps.sd.gov/applications/ST12ODRS/"

def get_metadata(key, default)
    begin
      ScraperWiki.get_var(key, default)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
        retry
    end
end

def save_metadata(key, value)
    begin
      ScraperWiki.save_var(key, value)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during save_metadata(#{key}) :: #{e.backtrace}"
        retry
    end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\302\240|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end

def scrape(data)
  Nokogiri::HTML(data).xpath("//form[@method='post']/table/tr[position()>1]").each{|tr|
    td = tr.xpath("td")
    records = {
      "YEAR" => text(td[0]),
      "L_NAME" => text(td[1]),
      "L_ADDR" => text(td[2]),
      "L_CITY" => text(td[3]),
      "E_NAME" => text(td[4]),
      "E_ADDR" => text(td[5]),
      "E_CITY" => text(td[6]),
      "DOC"=>Time.now.to_s
    }
    ScraperWiki.save_sqlite(unique_keys=["YEAR","L_NAME","E_NAME"],records,table_name='swdata',verbose=0)
  }
end

def ne(data,path,value)
  return attributes(Nokogiri::HTML(data).xpath(path),value)
end

def action(offset)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }    
    s_url = BASE_URL + "LobbyistViewlist.asp?start=#{offset}"
    ref_url = BASE_URL + "LobbyistViewlist.asp?#{(offset==1)? BASE_URL + 'cmd=resetall' : 'start=(offset-20)'}"
    pg = br.get(s_url,[],BASE_URL+ref_url)
    scrape(pg.body)
    if pg.at("a/img[alt='Next']").nil? 
      save_metadata("OFFSET",1)
    else
      offset = offset+20
      save_metadata("OFFSET",offset)
    end
  rescue Exception=>e
    puts "ERROR: While searching #{offset} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect=~ /Timeout|HTTP|TIME/
      sleep(30)
      retry
    end
  end while(true)

end
action(get_metadata('OFFSET',1))
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://apps.sd.gov/applications/ST12ODRS/"

def get_metadata(key, default)
    begin
      ScraperWiki.get_var(key, default)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
        retry
    end
end

def save_metadata(key, value)
    begin
      ScraperWiki.save_var(key, value)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during save_metadata(#{key}) :: #{e.backtrace}"
        retry
    end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\302\240|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end

def scrape(data)
  Nokogiri::HTML(data).xpath("//form[@method='post']/table/tr[position()>1]").each{|tr|
    td = tr.xpath("td")
    records = {
      "YEAR" => text(td[0]),
      "L_NAME" => text(td[1]),
      "L_ADDR" => text(td[2]),
      "L_CITY" => text(td[3]),
      "E_NAME" => text(td[4]),
      "E_ADDR" => text(td[5]),
      "E_CITY" => text(td[6]),
      "DOC"=>Time.now.to_s
    }
    ScraperWiki.save_sqlite(unique_keys=["YEAR","L_NAME","E_NAME"],records,table_name='swdata',verbose=0)
  }
end

def ne(data,path,value)
  return attributes(Nokogiri::HTML(data).xpath(path),value)
end

def action(offset)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }    
    s_url = BASE_URL + "LobbyistViewlist.asp?start=#{offset}"
    ref_url = BASE_URL + "LobbyistViewlist.asp?#{(offset==1)? BASE_URL + 'cmd=resetall' : 'start=(offset-20)'}"
    pg = br.get(s_url,[],BASE_URL+ref_url)
    scrape(pg.body)
    if pg.at("a/img[alt='Next']").nil? 
      save_metadata("OFFSET",1)
    else
      offset = offset+20
      save_metadata("OFFSET",offset)
    end
  rescue Exception=>e
    puts "ERROR: While searching #{offset} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect=~ /Timeout|HTTP|TIME/
      sleep(30)
      retry
    end
  end while(true)

end
action(get_metadata('OFFSET',1))
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://apps.sd.gov/applications/ST12ODRS/"

def get_metadata(key, default)
    begin
      ScraperWiki.get_var(key, default)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
        retry
    end
end

def save_metadata(key, value)
    begin
      ScraperWiki.save_var(key, value)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during save_metadata(#{key}) :: #{e.backtrace}"
        retry
    end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\302\240|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end

def scrape(data)
  Nokogiri::HTML(data).xpath("//form[@method='post']/table/tr[position()>1]").each{|tr|
    td = tr.xpath("td")
    records = {
      "YEAR" => text(td[0]),
      "L_NAME" => text(td[1]),
      "L_ADDR" => text(td[2]),
      "L_CITY" => text(td[3]),
      "E_NAME" => text(td[4]),
      "E_ADDR" => text(td[5]),
      "E_CITY" => text(td[6]),
      "DOC"=>Time.now.to_s
    }
    ScraperWiki.save_sqlite(unique_keys=["YEAR","L_NAME","E_NAME"],records,table_name='swdata',verbose=0)
  }
end

def ne(data,path,value)
  return attributes(Nokogiri::HTML(data).xpath(path),value)
end

def action(offset)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }    
    s_url = BASE_URL + "LobbyistViewlist.asp?start=#{offset}"
    ref_url = BASE_URL + "LobbyistViewlist.asp?#{(offset==1)? BASE_URL + 'cmd=resetall' : 'start=(offset-20)'}"
    pg = br.get(s_url,[],BASE_URL+ref_url)
    scrape(pg.body)
    if pg.at("a/img[alt='Next']").nil? 
      save_metadata("OFFSET",1)
    else
      offset = offset+20
      save_metadata("OFFSET",offset)
    end
  rescue Exception=>e
    puts "ERROR: While searching #{offset} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect=~ /Timeout|HTTP|TIME/
      sleep(30)
      retry
    end
  end while(true)

end
action(get_metadata('OFFSET',1))
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://apps.sd.gov/applications/ST12ODRS/"

def get_metadata(key, default)
    begin
      ScraperWiki.get_var(key, default)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
        retry
    end
end

def save_metadata(key, value)
    begin
      ScraperWiki.save_var(key, value)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during save_metadata(#{key}) :: #{e.backtrace}"
        retry
    end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\302\240|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end

def scrape(data)
  Nokogiri::HTML(data).xpath("//form[@method='post']/table/tr[position()>1]").each{|tr|
    td = tr.xpath("td")
    records = {
      "YEAR" => text(td[0]),
      "L_NAME" => text(td[1]),
      "L_ADDR" => text(td[2]),
      "L_CITY" => text(td[3]),
      "E_NAME" => text(td[4]),
      "E_ADDR" => text(td[5]),
      "E_CITY" => text(td[6]),
      "DOC"=>Time.now.to_s
    }
    ScraperWiki.save_sqlite(unique_keys=["YEAR","L_NAME","E_NAME"],records,table_name='swdata',verbose=0)
  }
end

def ne(data,path,value)
  return attributes(Nokogiri::HTML(data).xpath(path),value)
end

def action(offset)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }    
    s_url = BASE_URL + "LobbyistViewlist.asp?start=#{offset}"
    ref_url = BASE_URL + "LobbyistViewlist.asp?#{(offset==1)? BASE_URL + 'cmd=resetall' : 'start=(offset-20)'}"
    pg = br.get(s_url,[],BASE_URL+ref_url)
    scrape(pg.body)
    if pg.at("a/img[alt='Next']").nil? 
      save_metadata("OFFSET",1)
    else
      offset = offset+20
      save_metadata("OFFSET",offset)
    end
  rescue Exception=>e
    puts "ERROR: While searching #{offset} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect=~ /Timeout|HTTP|TIME/
      sleep(30)
      retry
    end
  end while(true)

end
action(get_metadata('OFFSET',1))
