# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "https://www.corporations.state.pa.us"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  b.retry_change_requests = true
}


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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'') }
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

def scrape(data,action,num,url)
  if action == "details"
      doc = Nokogiri::HTML(data).xpath("//table[@width='98%']/tr")
      records = {
        "COMPANY_NAME"=> text(doc.xpath("td[following::td[1][font/text()='Current Name']]")),
        "COMPANY_NUMBER"=> text(doc.xpath("td[font/b/text()='Entity Number:']/following::td[1]")),
        "URL"=>url,"DOC"=>Time.now
      }
      #puts records.inspect
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
      return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0 
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='>']"),"href")
end

def action(num)
  begin
    init() if @pg.nil? 
    @pg = @br.post(BASE_URL+"/corp/soskb/searchbycharternumber.asp",{'CharterNumber'=>num,'SearchBtn'=>'Search'})
    re = scrape(@pg.body,"details",num,@pg.uri.to_s)
    save_metadata("OFFSET",num.next) unless re.nil? 
  end
end

def init()
  begin
    @pg = @br.get(BASE_URL+"/corp/soskb/searchbycharternumber.asp?dtm=898113425925926")
  end
end

#save_metadata("INDEX",2973413)
strt = get_metadata("OFFSET",2973413).to_i
(strt..strt+50).each{|num|
  action(num)
  sleep(10)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "https://www.corporations.state.pa.us"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  b.retry_change_requests = true
}


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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'') }
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

def scrape(data,action,num,url)
  if action == "details"
      doc = Nokogiri::HTML(data).xpath("//table[@width='98%']/tr")
      records = {
        "COMPANY_NAME"=> text(doc.xpath("td[following::td[1][font/text()='Current Name']]")),
        "COMPANY_NUMBER"=> text(doc.xpath("td[font/b/text()='Entity Number:']/following::td[1]")),
        "URL"=>url,"DOC"=>Time.now
      }
      #puts records.inspect
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
      return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0 
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='>']"),"href")
end

def action(num)
  begin
    init() if @pg.nil? 
    @pg = @br.post(BASE_URL+"/corp/soskb/searchbycharternumber.asp",{'CharterNumber'=>num,'SearchBtn'=>'Search'})
    re = scrape(@pg.body,"details",num,@pg.uri.to_s)
    save_metadata("OFFSET",num.next) unless re.nil? 
  end
end

def init()
  begin
    @pg = @br.get(BASE_URL+"/corp/soskb/searchbycharternumber.asp?dtm=898113425925926")
  end
end

#save_metadata("INDEX",2973413)
strt = get_metadata("OFFSET",2973413).to_i
(strt..strt+50).each{|num|
  action(num)
  sleep(10)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "https://www.corporations.state.pa.us"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  b.retry_change_requests = true
}


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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'') }
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

def scrape(data,action,num,url)
  if action == "details"
      doc = Nokogiri::HTML(data).xpath("//table[@width='98%']/tr")
      records = {
        "COMPANY_NAME"=> text(doc.xpath("td[following::td[1][font/text()='Current Name']]")),
        "COMPANY_NUMBER"=> text(doc.xpath("td[font/b/text()='Entity Number:']/following::td[1]")),
        "URL"=>url,"DOC"=>Time.now
      }
      #puts records.inspect
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
      return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0 
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='>']"),"href")
end

def action(num)
  begin
    init() if @pg.nil? 
    @pg = @br.post(BASE_URL+"/corp/soskb/searchbycharternumber.asp",{'CharterNumber'=>num,'SearchBtn'=>'Search'})
    re = scrape(@pg.body,"details",num,@pg.uri.to_s)
    save_metadata("OFFSET",num.next) unless re.nil? 
  end
end

def init()
  begin
    @pg = @br.get(BASE_URL+"/corp/soskb/searchbycharternumber.asp?dtm=898113425925926")
  end
end

#save_metadata("INDEX",2973413)
strt = get_metadata("OFFSET",2973413).to_i
(strt..strt+50).each{|num|
  action(num)
  sleep(10)
}
