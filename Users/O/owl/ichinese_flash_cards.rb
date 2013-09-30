# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.ichineseflashcards.com/"

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

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'')}
      return tmp.delete_if{|a| a.nil? or a.empty? }
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@id='browseContent']//table[@class='browseTable']//tr/td")
    doc.each{|td|
      records << BASE_URL + attributes(td.xpath("a"),"href")
    }
    return records
  elsif act == "details"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@id='flashcardContent']//tr/td[@id='flashcardContainer']")
    doc.each{|td|
      r = {}
      r['ENGLISH'],r['CHINESE'],r['PINYIN'] = text(td.xpath("p[@id='flashcardEnglish']")),text(td.xpath("p[@id='flashcardChinese']")),text(td.xpath("p[@id='flashcardPinyin']"))
      records << r
    }
    ScraperWiki.save_sqlite(unique_keys=['ENGLISH'],records) unless records.length == 0
  end
end

def exists(srch)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where english=?",[srch])['data'][0][0] rescue return 0
end

def action()
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    b.retry_change_requests = true
  }
  pg =  br.get(BASE_URL+"/browse.asp")
  words = scrape(pg.body,"list")
  words.each{|w_lnk|
    pg_tmp = br.get(w_lnk)
    scrape(pg_tmp.body,"details") if exists(w_lnk.split("=").flatten.last) == 0
  }
end
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.ichineseflashcards.com/"

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

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'')}
      return tmp.delete_if{|a| a.nil? or a.empty? }
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@id='browseContent']//table[@class='browseTable']//tr/td")
    doc.each{|td|
      records << BASE_URL + attributes(td.xpath("a"),"href")
    }
    return records
  elsif act == "details"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@id='flashcardContent']//tr/td[@id='flashcardContainer']")
    doc.each{|td|
      r = {}
      r['ENGLISH'],r['CHINESE'],r['PINYIN'] = text(td.xpath("p[@id='flashcardEnglish']")),text(td.xpath("p[@id='flashcardChinese']")),text(td.xpath("p[@id='flashcardPinyin']"))
      records << r
    }
    ScraperWiki.save_sqlite(unique_keys=['ENGLISH'],records) unless records.length == 0
  end
end

def exists(srch)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where english=?",[srch])['data'][0][0] rescue return 0
end

def action()
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    b.retry_change_requests = true
  }
  pg =  br.get(BASE_URL+"/browse.asp")
  words = scrape(pg.body,"list")
  words.each{|w_lnk|
    pg_tmp = br.get(w_lnk)
    scrape(pg_tmp.body,"details") if exists(w_lnk.split("=").flatten.last) == 0
  }
end
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.ichineseflashcards.com/"

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

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'')}
      return tmp.delete_if{|a| a.nil? or a.empty? }
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@id='browseContent']//table[@class='browseTable']//tr/td")
    doc.each{|td|
      records << BASE_URL + attributes(td.xpath("a"),"href")
    }
    return records
  elsif act == "details"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@id='flashcardContent']//tr/td[@id='flashcardContainer']")
    doc.each{|td|
      r = {}
      r['ENGLISH'],r['CHINESE'],r['PINYIN'] = text(td.xpath("p[@id='flashcardEnglish']")),text(td.xpath("p[@id='flashcardChinese']")),text(td.xpath("p[@id='flashcardPinyin']"))
      records << r
    }
    ScraperWiki.save_sqlite(unique_keys=['ENGLISH'],records) unless records.length == 0
  end
end

def exists(srch)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where english=?",[srch])['data'][0][0] rescue return 0
end

def action()
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    b.retry_change_requests = true
  }
  pg =  br.get(BASE_URL+"/browse.asp")
  words = scrape(pg.body,"list")
  words.each{|w_lnk|
    pg_tmp = br.get(w_lnk)
    scrape(pg_tmp.body,"details") if exists(w_lnk.split("=").flatten.last) == 0
  }
end
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.ichineseflashcards.com/"

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

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'')}
      return tmp.delete_if{|a| a.nil? or a.empty? }
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@id='browseContent']//table[@class='browseTable']//tr/td")
    doc.each{|td|
      records << BASE_URL + attributes(td.xpath("a"),"href")
    }
    return records
  elsif act == "details"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@id='flashcardContent']//tr/td[@id='flashcardContainer']")
    doc.each{|td|
      r = {}
      r['ENGLISH'],r['CHINESE'],r['PINYIN'] = text(td.xpath("p[@id='flashcardEnglish']")),text(td.xpath("p[@id='flashcardChinese']")),text(td.xpath("p[@id='flashcardPinyin']"))
      records << r
    }
    ScraperWiki.save_sqlite(unique_keys=['ENGLISH'],records) unless records.length == 0
  end
end

def exists(srch)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where english=?",[srch])['data'][0][0] rescue return 0
end

def action()
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    b.retry_change_requests = true
  }
  pg =  br.get(BASE_URL+"/browse.asp")
  words = scrape(pg.body,"list")
  words.each{|w_lnk|
    pg_tmp = br.get(w_lnk)
    scrape(pg_tmp.body,"details") if exists(w_lnk.split("=").flatten.last) == 0
  }
end
action()