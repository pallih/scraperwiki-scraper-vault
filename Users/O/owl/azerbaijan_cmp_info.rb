# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
#require 'Date'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://taxes.caspel.com"

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

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where key=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
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
    records = {"DOC"=>Time.now.to_s}
    Nokogiri::HTML(data).xpath(".//table[@width='836']/tbody/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      tmp = text(td[1].xpath("text()")).split(":")
      case tmp[0].strip.gsub(/\s{2,}/,' ')
        when /Kommersiya qurumunun adı/
          ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=0) unless records.length == 1
          records = {"DOC"=>Time.now.to_s}
          records['COMPANY_NAME'],records['TYPE'] = tmp[1].strip.scan(/"([^>]*)" ([^>]*)/)[0]
        when /Qeydiyyat nömrəsi \(VÖEN\)/
          records['COMPANY_NUMBER'] = tmp[1].strip
        when /Təşkilati-hüquqi forması/
          records['FORM'] = tmp[1].strip
        when /Hüquqi ünvanı/
          records['ADDR'] = tmp[1].strip
        when /Maliyyə ili/
          records['FIN_YEAR'] = tmp[1].strip
        when /Dövlət qeydiyyatına alındığı tarix/
          records['REGISTRATION_DT'] = tmp[1].strip
      end
    }
  end
end

def action(day)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    pg = br.get(BASE_URL+"/2009/modules/birpencere/reyestr/melumat.php?ay=#{'%02d' % day.month}&il=#{day.year}&gun=#{'%02d' % day.day}")
    scrape(pg.body,"list")
  end
end

range = (Date.today<<1..Date.today).to_a
range.each{|day|
  action(day)
}

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
#require 'Date'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://taxes.caspel.com"

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

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where key=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
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
    records = {"DOC"=>Time.now.to_s}
    Nokogiri::HTML(data).xpath(".//table[@width='836']/tbody/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      tmp = text(td[1].xpath("text()")).split(":")
      case tmp[0].strip.gsub(/\s{2,}/,' ')
        when /Kommersiya qurumunun adı/
          ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=0) unless records.length == 1
          records = {"DOC"=>Time.now.to_s}
          records['COMPANY_NAME'],records['TYPE'] = tmp[1].strip.scan(/"([^>]*)" ([^>]*)/)[0]
        when /Qeydiyyat nömrəsi \(VÖEN\)/
          records['COMPANY_NUMBER'] = tmp[1].strip
        when /Təşkilati-hüquqi forması/
          records['FORM'] = tmp[1].strip
        when /Hüquqi ünvanı/
          records['ADDR'] = tmp[1].strip
        when /Maliyyə ili/
          records['FIN_YEAR'] = tmp[1].strip
        when /Dövlət qeydiyyatına alındığı tarix/
          records['REGISTRATION_DT'] = tmp[1].strip
      end
    }
  end
end

def action(day)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    pg = br.get(BASE_URL+"/2009/modules/birpencere/reyestr/melumat.php?ay=#{'%02d' % day.month}&il=#{day.year}&gun=#{'%02d' % day.day}")
    scrape(pg.body,"list")
  end
end

range = (Date.today<<1..Date.today).to_a
range.each{|day|
  action(day)
}

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
#require 'Date'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://taxes.caspel.com"

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

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where key=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
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
    records = {"DOC"=>Time.now.to_s}
    Nokogiri::HTML(data).xpath(".//table[@width='836']/tbody/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      tmp = text(td[1].xpath("text()")).split(":")
      case tmp[0].strip.gsub(/\s{2,}/,' ')
        when /Kommersiya qurumunun adı/
          ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=0) unless records.length == 1
          records = {"DOC"=>Time.now.to_s}
          records['COMPANY_NAME'],records['TYPE'] = tmp[1].strip.scan(/"([^>]*)" ([^>]*)/)[0]
        when /Qeydiyyat nömrəsi \(VÖEN\)/
          records['COMPANY_NUMBER'] = tmp[1].strip
        when /Təşkilati-hüquqi forması/
          records['FORM'] = tmp[1].strip
        when /Hüquqi ünvanı/
          records['ADDR'] = tmp[1].strip
        when /Maliyyə ili/
          records['FIN_YEAR'] = tmp[1].strip
        when /Dövlət qeydiyyatına alındığı tarix/
          records['REGISTRATION_DT'] = tmp[1].strip
      end
    }
  end
end

def action(day)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    pg = br.get(BASE_URL+"/2009/modules/birpencere/reyestr/melumat.php?ay=#{'%02d' % day.month}&il=#{day.year}&gun=#{'%02d' % day.day}")
    scrape(pg.body,"list")
  end
end

range = (Date.today<<1..Date.today).to_a
range.each{|day|
  action(day)
}

