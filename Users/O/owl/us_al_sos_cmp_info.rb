require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://arc-sos.state.al.us"


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
      puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
      retry
    end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
    retry
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@width='780']/tr[position()>1 and position()<last()]").each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NUMBER"=>text(td[0].xpath("a/text()")),
        "URL"=>BASE_URL+attributes(td[0].xpath("a"),"href"),
        "COMPANY_NAME"=>text(td[1].xpath("a/text()")),
        #"CITY"=>text(td[2].xpath("text()")),
        #"TYPE"=>text(td[3].xpath("text()")),
        #"STATUS"=>text(td[4].xpath("text()")),
        "DOC"=>Time.now
      }
      status = text(td[4].xpath("text()"))
      #puts records.inspect
      records << r unless status =~ /Previous Name|Name Reservation/i
    }
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=2) unless records.length == 0
  end
end

def ne(data)
  return Nokogiri::HTML(data).xpath(".//a[@class='cgiPageLink' and contains(text(),'Next')]")
end

def action(srch,pgno)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL+"/cgi/corpname.mbr/output?s=#{pgno}&search=#{srch}&type=ALL&status=ALL&place=ALL&city=&order=default&hld=&dir=&page=Y"
    pg = br.get(s_url)
    scrape(pg.body,"list")
    pgno = pgno+25
    nex = ne(pg.body)
    if nex.nil? or nex.empty? 
      delete_metadata("PGNO")
      break
    else
      save_metadata("PGNO",pgno)
    end
  end while(true)

end

range = ('A'..'ZZ').to_a+ (0..9).to_a + ['$','@','#','(','"','-','\'','.']
#save_metadata("PGNO",976)
#save_metadata("OFFSET",0)
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index{|srch,index|
  next if index<offset
  action(srch,get_metadata("PGNO",1))
  save_metadata("OFFSET",index.next)
}require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://arc-sos.state.al.us"


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
      puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
      retry
    end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
    retry
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@width='780']/tr[position()>1 and position()<last()]").each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NUMBER"=>text(td[0].xpath("a/text()")),
        "URL"=>BASE_URL+attributes(td[0].xpath("a"),"href"),
        "COMPANY_NAME"=>text(td[1].xpath("a/text()")),
        #"CITY"=>text(td[2].xpath("text()")),
        #"TYPE"=>text(td[3].xpath("text()")),
        #"STATUS"=>text(td[4].xpath("text()")),
        "DOC"=>Time.now
      }
      status = text(td[4].xpath("text()"))
      #puts records.inspect
      records << r unless status =~ /Previous Name|Name Reservation/i
    }
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=2) unless records.length == 0
  end
end

def ne(data)
  return Nokogiri::HTML(data).xpath(".//a[@class='cgiPageLink' and contains(text(),'Next')]")
end

def action(srch,pgno)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL+"/cgi/corpname.mbr/output?s=#{pgno}&search=#{srch}&type=ALL&status=ALL&place=ALL&city=&order=default&hld=&dir=&page=Y"
    pg = br.get(s_url)
    scrape(pg.body,"list")
    pgno = pgno+25
    nex = ne(pg.body)
    if nex.nil? or nex.empty? 
      delete_metadata("PGNO")
      break
    else
      save_metadata("PGNO",pgno)
    end
  end while(true)

end

range = ('A'..'ZZ').to_a+ (0..9).to_a + ['$','@','#','(','"','-','\'','.']
#save_metadata("PGNO",976)
#save_metadata("OFFSET",0)
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index{|srch,index|
  next if index<offset
  action(srch,get_metadata("PGNO",1))
  save_metadata("OFFSET",index.next)
}require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://arc-sos.state.al.us"


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
      puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
      retry
    end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
    retry
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@width='780']/tr[position()>1 and position()<last()]").each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NUMBER"=>text(td[0].xpath("a/text()")),
        "URL"=>BASE_URL+attributes(td[0].xpath("a"),"href"),
        "COMPANY_NAME"=>text(td[1].xpath("a/text()")),
        #"CITY"=>text(td[2].xpath("text()")),
        #"TYPE"=>text(td[3].xpath("text()")),
        #"STATUS"=>text(td[4].xpath("text()")),
        "DOC"=>Time.now
      }
      status = text(td[4].xpath("text()"))
      #puts records.inspect
      records << r unless status =~ /Previous Name|Name Reservation/i
    }
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=2) unless records.length == 0
  end
end

def ne(data)
  return Nokogiri::HTML(data).xpath(".//a[@class='cgiPageLink' and contains(text(),'Next')]")
end

def action(srch,pgno)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL+"/cgi/corpname.mbr/output?s=#{pgno}&search=#{srch}&type=ALL&status=ALL&place=ALL&city=&order=default&hld=&dir=&page=Y"
    pg = br.get(s_url)
    scrape(pg.body,"list")
    pgno = pgno+25
    nex = ne(pg.body)
    if nex.nil? or nex.empty? 
      delete_metadata("PGNO")
      break
    else
      save_metadata("PGNO",pgno)
    end
  end while(true)

end

range = ('A'..'ZZ').to_a+ (0..9).to_a + ['$','@','#','(','"','-','\'','.']
#save_metadata("PGNO",976)
#save_metadata("OFFSET",0)
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index{|srch,index|
  next if index<offset
  action(srch,get_metadata("PGNO",1))
  save_metadata("OFFSET",index.next)
}require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://arc-sos.state.al.us"


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
      puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
      retry
    end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
    retry
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@width='780']/tr[position()>1 and position()<last()]").each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NUMBER"=>text(td[0].xpath("a/text()")),
        "URL"=>BASE_URL+attributes(td[0].xpath("a"),"href"),
        "COMPANY_NAME"=>text(td[1].xpath("a/text()")),
        #"CITY"=>text(td[2].xpath("text()")),
        #"TYPE"=>text(td[3].xpath("text()")),
        #"STATUS"=>text(td[4].xpath("text()")),
        "DOC"=>Time.now
      }
      status = text(td[4].xpath("text()"))
      #puts records.inspect
      records << r unless status =~ /Previous Name|Name Reservation/i
    }
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=2) unless records.length == 0
  end
end

def ne(data)
  return Nokogiri::HTML(data).xpath(".//a[@class='cgiPageLink' and contains(text(),'Next')]")
end

def action(srch,pgno)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL+"/cgi/corpname.mbr/output?s=#{pgno}&search=#{srch}&type=ALL&status=ALL&place=ALL&city=&order=default&hld=&dir=&page=Y"
    pg = br.get(s_url)
    scrape(pg.body,"list")
    pgno = pgno+25
    nex = ne(pg.body)
    if nex.nil? or nex.empty? 
      delete_metadata("PGNO")
      break
    else
      save_metadata("PGNO",pgno)
    end
  end while(true)

end

range = ('A'..'ZZ').to_a+ (0..9).to_a + ['$','@','#','(','"','-','\'','.']
#save_metadata("PGNO",976)
#save_metadata("OFFSET",0)
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index{|srch,index|
  next if index<offset
  action(srch,get_metadata("PGNO",1))
  save_metadata("OFFSET",index.next)
}