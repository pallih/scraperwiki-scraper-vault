# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.jucap.ap.gov.br"


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
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip
    elsif str.children().length == 0
      return ""
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip unless st.text.nil? or st.text.empty?}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act)
  if act == "details"
    records = []
    Nokogiri::HTML(data).xpath(".//div/fieldset").each{|fs|
      div=fs.xpath("div")
      return if div.nil? 
      idx = 3
      3.times{
        break if idx>=div.length
        r = {'COMPANY_NUMBER'=>text(div[idx].xpath('.')),'COMPANY_NAME'=>text(div[idx+1].xpath('.')),'STATUS'=>text(div[idx+2].xpath('.')),'DOC'=>Time.now}
        records << r
        idx = idx+3
      } while idx < div.length
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length==0
  end
end



def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
      #b.log = Logger.new(STDERR)
    }
    params = {'nome'=>srch,'enviar'=>'Buscar','estatus'=>'OK'}
    s_url = BASE_URL+"/apps/consultane.php"
    pg = br.post(s_url,params,{'Referer'=>BASE_URL,'Cookie'=>'acf9520a2c865db7c27e3f8355100a44=ih7h03pih8pa51cndtb8lasgi1; PHPSESSID=fcgbq7nbdlrlhfltkug4t3eni6'})
    scrape(pg.body,"details")
  end
end
range = ('A'..'Z').to_a + (0..9).to_a + ['#','%',' ','*'].to_a
offset = get_metadata('OFFSET',0)
offset =0 if offset>=range.length
range.each_with_index{|srch,idx|
  next if idx <= offset
  action(srch)
  save_metadata('OFFSET',idx.next)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.jucap.ap.gov.br"


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
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip
    elsif str.children().length == 0
      return ""
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip unless st.text.nil? or st.text.empty?}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act)
  if act == "details"
    records = []
    Nokogiri::HTML(data).xpath(".//div/fieldset").each{|fs|
      div=fs.xpath("div")
      return if div.nil? 
      idx = 3
      3.times{
        break if idx>=div.length
        r = {'COMPANY_NUMBER'=>text(div[idx].xpath('.')),'COMPANY_NAME'=>text(div[idx+1].xpath('.')),'STATUS'=>text(div[idx+2].xpath('.')),'DOC'=>Time.now}
        records << r
        idx = idx+3
      } while idx < div.length
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length==0
  end
end



def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
      #b.log = Logger.new(STDERR)
    }
    params = {'nome'=>srch,'enviar'=>'Buscar','estatus'=>'OK'}
    s_url = BASE_URL+"/apps/consultane.php"
    pg = br.post(s_url,params,{'Referer'=>BASE_URL,'Cookie'=>'acf9520a2c865db7c27e3f8355100a44=ih7h03pih8pa51cndtb8lasgi1; PHPSESSID=fcgbq7nbdlrlhfltkug4t3eni6'})
    scrape(pg.body,"details")
  end
end
range = ('A'..'Z').to_a + (0..9).to_a + ['#','%',' ','*'].to_a
offset = get_metadata('OFFSET',0)
offset =0 if offset>=range.length
range.each_with_index{|srch,idx|
  next if idx <= offset
  action(srch)
  save_metadata('OFFSET',idx.next)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.jucap.ap.gov.br"


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
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip
    elsif str.children().length == 0
      return ""
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip unless st.text.nil? or st.text.empty?}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act)
  if act == "details"
    records = []
    Nokogiri::HTML(data).xpath(".//div/fieldset").each{|fs|
      div=fs.xpath("div")
      return if div.nil? 
      idx = 3
      3.times{
        break if idx>=div.length
        r = {'COMPANY_NUMBER'=>text(div[idx].xpath('.')),'COMPANY_NAME'=>text(div[idx+1].xpath('.')),'STATUS'=>text(div[idx+2].xpath('.')),'DOC'=>Time.now}
        records << r
        idx = idx+3
      } while idx < div.length
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length==0
  end
end



def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
      #b.log = Logger.new(STDERR)
    }
    params = {'nome'=>srch,'enviar'=>'Buscar','estatus'=>'OK'}
    s_url = BASE_URL+"/apps/consultane.php"
    pg = br.post(s_url,params,{'Referer'=>BASE_URL,'Cookie'=>'acf9520a2c865db7c27e3f8355100a44=ih7h03pih8pa51cndtb8lasgi1; PHPSESSID=fcgbq7nbdlrlhfltkug4t3eni6'})
    scrape(pg.body,"details")
  end
end
range = ('A'..'Z').to_a + (0..9).to_a + ['#','%',' ','*'].to_a
offset = get_metadata('OFFSET',0)
offset =0 if offset>=range.length
range.each_with_index{|srch,idx|
  next if idx <= offset
  action(srch)
  save_metadata('OFFSET',idx.next)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.jucap.ap.gov.br"


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
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip
    elsif str.children().length == 0
      return ""
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip unless st.text.nil? or st.text.empty?}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act)
  if act == "details"
    records = []
    Nokogiri::HTML(data).xpath(".//div/fieldset").each{|fs|
      div=fs.xpath("div")
      return if div.nil? 
      idx = 3
      3.times{
        break if idx>=div.length
        r = {'COMPANY_NUMBER'=>text(div[idx].xpath('.')),'COMPANY_NAME'=>text(div[idx+1].xpath('.')),'STATUS'=>text(div[idx+2].xpath('.')),'DOC'=>Time.now}
        records << r
        idx = idx+3
      } while idx < div.length
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length==0
  end
end



def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
      #b.log = Logger.new(STDERR)
    }
    params = {'nome'=>srch,'enviar'=>'Buscar','estatus'=>'OK'}
    s_url = BASE_URL+"/apps/consultane.php"
    pg = br.post(s_url,params,{'Referer'=>BASE_URL,'Cookie'=>'acf9520a2c865db7c27e3f8355100a44=ih7h03pih8pa51cndtb8lasgi1; PHPSESSID=fcgbq7nbdlrlhfltkug4t3eni6'})
    scrape(pg.body,"details")
  end
end
range = ('A'..'Z').to_a + (0..9).to_a + ['#','%',' ','*'].to_a
offset = get_metadata('OFFSET',0)
offset =0 if offset>=range.length
range.each_with_index{|srch,idx|
  next if idx <= offset
  action(srch)
  save_metadata('OFFSET',idx.next)
}