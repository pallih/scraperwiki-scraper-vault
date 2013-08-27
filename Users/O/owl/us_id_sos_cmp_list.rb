require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.accessidaho.org/public/sos/corp/"

def get_metadata(key, default)
    begin
      ret = ScraperWiki.get_var(key, default)
      return (ret.nil? or ret=="")? default : ret
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

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip }
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

def scrape(data,action)
  if action == "list"
    cnt = 0
    r = []
    records = {}
    begin
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+1]")
      td = tr.xpath("td")
      return if td.length < 1
      records["COMPANY_NAME"] = text(td[0].xpath("p/span/a"))
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+3]")
      td = tr.xpath("td")
      records["COMPANY_NUMBER"] = text(td[0]).split(":")[1]
      records["CREATION_DT"] = text(td[1]).gsub("Filed ","")
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+4]")
      td = tr.xpath("td")
      #records["ADDR"] = text(td[0])
      records["TYPE"] = text(td[1])
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+5]")
      td = tr.xpath("td")
      records["STATUS"] = text(td[0])
      records["DOC"] = Time.now
      cnt = cnt + 6
      r << records unless records['TYPE'] =~ /NAME/i
      #ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name='swdata',verbose=0)
      #puts records.inspect if records['TYPE'] =~ /NAME RESERVATION/
      #ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name='swdata',verbose=2) unless records['TYPE'] =~ /NAME/i
    end until cnt == 120
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],r,table_name='swdata',verbose=2) unless r.empty? 
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='[ Next >>> ]']"),"href")
end

def action()
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200  
    b.max_history = 0
  }
  offset = get_metadata("offset",0)
  begin
    #params ="search.html?p=#{offset}&crit.name=&crit.city=&crit.fileNumber=&crit.raName=&crit.raCity=&crit.startDay=1&crit.startMonth=1&crit.startYear=1000&crit.endDay=1&crit.endMonth=1&crit.endYear=2099&search=true"
    params = "search.html?p=#{offset}&crit.name=&crit.city=&crit.fileNumber=&crit.raName=&crit.raCity=&crit.startDay=1&crit.startMonth=#{Time.now.month}&crit.startYear=#{Time.now.year}&crit.endDay=&crit.endMonth=&crit.endYear=&search=true"
    pg = br.get(BASE_URL+params,nil,BASE_URL+"search.html")
    scrape(pg.body,"list")
    params = ne(pg.body)
    #puts params.inspect
    if params.nil? or params.empty? 
      save_metadata("offset",0)
      break
    else
      offset = offset +1
      save_metadata("offset",offset)
    end
    @cnt = @cnt +1
    if @cnt == 10
      sleep(30)
      @cnt = 0
    end
  rescue Exception => e
    puts "ERROR: While processing #{offset} :: #{e.inspect} :: #{e.backtrace}"
    #if e.inspect =~ /Timeout|TIMED|HTTP/
      retry
    #end
  end while(true)
end
#save_metadata("offset",0)
@cnt = 0
action()

#puts ScraperWiki.sqliteexecute("delete from swdata where type='NAME RESERVATION'")
#puts ScraperWiki.commit()
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.accessidaho.org/public/sos/corp/"

def get_metadata(key, default)
    begin
      ret = ScraperWiki.get_var(key, default)
      return (ret.nil? or ret=="")? default : ret
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

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip }
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

def scrape(data,action)
  if action == "list"
    cnt = 0
    r = []
    records = {}
    begin
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+1]")
      td = tr.xpath("td")
      return if td.length < 1
      records["COMPANY_NAME"] = text(td[0].xpath("p/span/a"))
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+3]")
      td = tr.xpath("td")
      records["COMPANY_NUMBER"] = text(td[0]).split(":")[1]
      records["CREATION_DT"] = text(td[1]).gsub("Filed ","")
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+4]")
      td = tr.xpath("td")
      #records["ADDR"] = text(td[0])
      records["TYPE"] = text(td[1])
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+5]")
      td = tr.xpath("td")
      records["STATUS"] = text(td[0])
      records["DOC"] = Time.now
      cnt = cnt + 6
      r << records unless records['TYPE'] =~ /NAME/i
      #ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name='swdata',verbose=0)
      #puts records.inspect if records['TYPE'] =~ /NAME RESERVATION/
      #ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name='swdata',verbose=2) unless records['TYPE'] =~ /NAME/i
    end until cnt == 120
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],r,table_name='swdata',verbose=2) unless r.empty? 
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='[ Next >>> ]']"),"href")
end

def action()
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200  
    b.max_history = 0
  }
  offset = get_metadata("offset",0)
  begin
    #params ="search.html?p=#{offset}&crit.name=&crit.city=&crit.fileNumber=&crit.raName=&crit.raCity=&crit.startDay=1&crit.startMonth=1&crit.startYear=1000&crit.endDay=1&crit.endMonth=1&crit.endYear=2099&search=true"
    params = "search.html?p=#{offset}&crit.name=&crit.city=&crit.fileNumber=&crit.raName=&crit.raCity=&crit.startDay=1&crit.startMonth=#{Time.now.month}&crit.startYear=#{Time.now.year}&crit.endDay=&crit.endMonth=&crit.endYear=&search=true"
    pg = br.get(BASE_URL+params,nil,BASE_URL+"search.html")
    scrape(pg.body,"list")
    params = ne(pg.body)
    #puts params.inspect
    if params.nil? or params.empty? 
      save_metadata("offset",0)
      break
    else
      offset = offset +1
      save_metadata("offset",offset)
    end
    @cnt = @cnt +1
    if @cnt == 10
      sleep(30)
      @cnt = 0
    end
  rescue Exception => e
    puts "ERROR: While processing #{offset} :: #{e.inspect} :: #{e.backtrace}"
    #if e.inspect =~ /Timeout|TIMED|HTTP/
      retry
    #end
  end while(true)
end
#save_metadata("offset",0)
@cnt = 0
action()

#puts ScraperWiki.sqliteexecute("delete from swdata where type='NAME RESERVATION'")
#puts ScraperWiki.commit()
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.accessidaho.org/public/sos/corp/"

def get_metadata(key, default)
    begin
      ret = ScraperWiki.get_var(key, default)
      return (ret.nil? or ret=="")? default : ret
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

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip }
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

def scrape(data,action)
  if action == "list"
    cnt = 0
    r = []
    records = {}
    begin
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+1]")
      td = tr.xpath("td")
      return if td.length < 1
      records["COMPANY_NAME"] = text(td[0].xpath("p/span/a"))
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+3]")
      td = tr.xpath("td")
      records["COMPANY_NUMBER"] = text(td[0]).split(":")[1]
      records["CREATION_DT"] = text(td[1]).gsub("Filed ","")
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+4]")
      td = tr.xpath("td")
      #records["ADDR"] = text(td[0])
      records["TYPE"] = text(td[1])
      tr = Nokogiri::HTML(data).xpath("html/body/table[2]/tr[4]/td[2]/table/tr[#{cnt}+5]")
      td = tr.xpath("td")
      records["STATUS"] = text(td[0])
      records["DOC"] = Time.now
      cnt = cnt + 6
      r << records unless records['TYPE'] =~ /NAME/i
      #ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name='swdata',verbose=0)
      #puts records.inspect if records['TYPE'] =~ /NAME RESERVATION/
      #ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name='swdata',verbose=2) unless records['TYPE'] =~ /NAME/i
    end until cnt == 120
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],r,table_name='swdata',verbose=2) unless r.empty? 
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='[ Next >>> ]']"),"href")
end

def action()
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200  
    b.max_history = 0
  }
  offset = get_metadata("offset",0)
  begin
    #params ="search.html?p=#{offset}&crit.name=&crit.city=&crit.fileNumber=&crit.raName=&crit.raCity=&crit.startDay=1&crit.startMonth=1&crit.startYear=1000&crit.endDay=1&crit.endMonth=1&crit.endYear=2099&search=true"
    params = "search.html?p=#{offset}&crit.name=&crit.city=&crit.fileNumber=&crit.raName=&crit.raCity=&crit.startDay=1&crit.startMonth=#{Time.now.month}&crit.startYear=#{Time.now.year}&crit.endDay=&crit.endMonth=&crit.endYear=&search=true"
    pg = br.get(BASE_URL+params,nil,BASE_URL+"search.html")
    scrape(pg.body,"list")
    params = ne(pg.body)
    #puts params.inspect
    if params.nil? or params.empty? 
      save_metadata("offset",0)
      break
    else
      offset = offset +1
      save_metadata("offset",offset)
    end
    @cnt = @cnt +1
    if @cnt == 10
      sleep(30)
      @cnt = 0
    end
  rescue Exception => e
    puts "ERROR: While processing #{offset} :: #{e.inspect} :: #{e.backtrace}"
    #if e.inspect =~ /Timeout|TIMED|HTTP/
      retry
    #end
  end while(true)
end
#save_metadata("offset",0)
@cnt = 0
action()

#puts ScraperWiki.sqliteexecute("delete from swdata where type='NAME RESERVATION'")
#puts ScraperWiki.commit()
