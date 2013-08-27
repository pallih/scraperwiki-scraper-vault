# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.icab.cat"

class String
  def join(str)
    self+str
  end
  def pretty
    self.gsub(/\n|\t|\r/,'').gsub(/,$/,'').strip
  end

end
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
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip}
      return tmp.delete_if{|a| a.nil? or a.empty?}
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,rec)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//ul[@class='dstyleList']/li/a")
    doc.collect {|rec|
      records << attributes(rec.xpath("."),"href")
    }
    return records
  elsif act == "details"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//div[@class='personalData']/div[@class='left']")
    r = {}
    tmp = text(doc.xpath("p"))
    r["NAME"]= tmp[0]
    r["ID"],r["EXCERCENT"] = tmp[1].scan(/Nº de col·legiat (.*)\. (.*)/).flatten
    r["INC_DT"] = tmp[2].scan(/Data d'incorporació: (.*)/).flatten.first

    para = Nokogiri::HTML(data).xpath(".//div[not(@class or @id or @style)]")
    begin
      r["ADDRESS"] = text(para.xpath("p[strong[text()='Adreça: ']]/span")).join(",").pretty
      r["TELEPHONE"] = text(para.xpath("p[strong[text()='Telèfon: ']]/span")).join(",").pretty
      r["MOBILE"] = text(para.xpath("p[strong[text()='Telèfon mòbil: ']]/span")).join(",").pretty
      r["EMAIL"] = text(para.xpath("p[strong[text()='Correu Electrònic: ']]/span")).join(",").pretty
      r["SECTIONS"] = text(para.xpath("p[strong[text()='Seccions: ']]/span")).join(",").pretty
      r["PREFERENCES"] = text(para.xpath("p[strong[text()='Dedicacions preferents']]/span")).join(",").pretty
      r["LANGUAGES"] = text(para.xpath("p[strong[text()='Idiomes: ']]/span")).join(",").pretty
    end
    r["URL"] = rec["URL"]
    r["DOC"]=Time.now
    records << r unless r['ID'].nil? or r['ID'].empty? 
    ScraperWiki.save_sqlite(unique_keys=['ID'],records,table_name='swdata',verbose=2) unless records.length == 0
    return records.length
  end
end

def init()
  @br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }

end
def action()
  begin
    init() if @br.nil? 
    param = get_metadata("PARAM","eaf9d1a0ec5f1dc58757ad6cffdacedb1a58854a600312ccc87f484313450d19276f8592ea512941")
    s_url = BASE_URL + "/?go=#{param}"
    pg = @br.get(s_url)
    raise "captcha" if pg.body =~ /captcha/i
    urls = scrape(pg.body,"list",nil)
    urls.each{|url|
      s_url = BASE_URL + url
      pg_tmp = @br.get(s_url)
      raise "captcha" if pg_tmp.body =~ /captcha/i
      scrape(pg_tmp.body,"details",{"URL"=>s_url})
    }
    param = attributes(Nokogiri::HTML(pg.body).xpath(".//ul[@class='paginador']/li/a[@class='current']/following::a[1]"),"href").split(/=/).last
    break if param.nil? or param.empty? 
    save_metadata("PARAM",param)
    @br = nil
    init()
    sleep(25)
  rescue Exception => e
   puts [s_url,e,e.backtrace,].inspect
   raise e if e.inspect =~ /captcha/i
  end while(true)
  delete_metadata("PARAM")
end

action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.icab.cat"

class String
  def join(str)
    self+str
  end
  def pretty
    self.gsub(/\n|\t|\r/,'').gsub(/,$/,'').strip
  end

end
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
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip}
      return tmp.delete_if{|a| a.nil? or a.empty?}
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,rec)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//ul[@class='dstyleList']/li/a")
    doc.collect {|rec|
      records << attributes(rec.xpath("."),"href")
    }
    return records
  elsif act == "details"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//div[@class='personalData']/div[@class='left']")
    r = {}
    tmp = text(doc.xpath("p"))
    r["NAME"]= tmp[0]
    r["ID"],r["EXCERCENT"] = tmp[1].scan(/Nº de col·legiat (.*)\. (.*)/).flatten
    r["INC_DT"] = tmp[2].scan(/Data d'incorporació: (.*)/).flatten.first

    para = Nokogiri::HTML(data).xpath(".//div[not(@class or @id or @style)]")
    begin
      r["ADDRESS"] = text(para.xpath("p[strong[text()='Adreça: ']]/span")).join(",").pretty
      r["TELEPHONE"] = text(para.xpath("p[strong[text()='Telèfon: ']]/span")).join(",").pretty
      r["MOBILE"] = text(para.xpath("p[strong[text()='Telèfon mòbil: ']]/span")).join(",").pretty
      r["EMAIL"] = text(para.xpath("p[strong[text()='Correu Electrònic: ']]/span")).join(",").pretty
      r["SECTIONS"] = text(para.xpath("p[strong[text()='Seccions: ']]/span")).join(",").pretty
      r["PREFERENCES"] = text(para.xpath("p[strong[text()='Dedicacions preferents']]/span")).join(",").pretty
      r["LANGUAGES"] = text(para.xpath("p[strong[text()='Idiomes: ']]/span")).join(",").pretty
    end
    r["URL"] = rec["URL"]
    r["DOC"]=Time.now
    records << r unless r['ID'].nil? or r['ID'].empty? 
    ScraperWiki.save_sqlite(unique_keys=['ID'],records,table_name='swdata',verbose=2) unless records.length == 0
    return records.length
  end
end

def init()
  @br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }

end
def action()
  begin
    init() if @br.nil? 
    param = get_metadata("PARAM","eaf9d1a0ec5f1dc58757ad6cffdacedb1a58854a600312ccc87f484313450d19276f8592ea512941")
    s_url = BASE_URL + "/?go=#{param}"
    pg = @br.get(s_url)
    raise "captcha" if pg.body =~ /captcha/i
    urls = scrape(pg.body,"list",nil)
    urls.each{|url|
      s_url = BASE_URL + url
      pg_tmp = @br.get(s_url)
      raise "captcha" if pg_tmp.body =~ /captcha/i
      scrape(pg_tmp.body,"details",{"URL"=>s_url})
    }
    param = attributes(Nokogiri::HTML(pg.body).xpath(".//ul[@class='paginador']/li/a[@class='current']/following::a[1]"),"href").split(/=/).last
    break if param.nil? or param.empty? 
    save_metadata("PARAM",param)
    @br = nil
    init()
    sleep(25)
  rescue Exception => e
   puts [s_url,e,e.backtrace,].inspect
   raise e if e.inspect =~ /captcha/i
  end while(true)
  delete_metadata("PARAM")
end

action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.icab.cat"

class String
  def join(str)
    self+str
  end
  def pretty
    self.gsub(/\n|\t|\r/,'').gsub(/,$/,'').strip
  end

end
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
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip}
      return tmp.delete_if{|a| a.nil? or a.empty?}
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,rec)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//ul[@class='dstyleList']/li/a")
    doc.collect {|rec|
      records << attributes(rec.xpath("."),"href")
    }
    return records
  elsif act == "details"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//div[@class='personalData']/div[@class='left']")
    r = {}
    tmp = text(doc.xpath("p"))
    r["NAME"]= tmp[0]
    r["ID"],r["EXCERCENT"] = tmp[1].scan(/Nº de col·legiat (.*)\. (.*)/).flatten
    r["INC_DT"] = tmp[2].scan(/Data d'incorporació: (.*)/).flatten.first

    para = Nokogiri::HTML(data).xpath(".//div[not(@class or @id or @style)]")
    begin
      r["ADDRESS"] = text(para.xpath("p[strong[text()='Adreça: ']]/span")).join(",").pretty
      r["TELEPHONE"] = text(para.xpath("p[strong[text()='Telèfon: ']]/span")).join(",").pretty
      r["MOBILE"] = text(para.xpath("p[strong[text()='Telèfon mòbil: ']]/span")).join(",").pretty
      r["EMAIL"] = text(para.xpath("p[strong[text()='Correu Electrònic: ']]/span")).join(",").pretty
      r["SECTIONS"] = text(para.xpath("p[strong[text()='Seccions: ']]/span")).join(",").pretty
      r["PREFERENCES"] = text(para.xpath("p[strong[text()='Dedicacions preferents']]/span")).join(",").pretty
      r["LANGUAGES"] = text(para.xpath("p[strong[text()='Idiomes: ']]/span")).join(",").pretty
    end
    r["URL"] = rec["URL"]
    r["DOC"]=Time.now
    records << r unless r['ID'].nil? or r['ID'].empty? 
    ScraperWiki.save_sqlite(unique_keys=['ID'],records,table_name='swdata',verbose=2) unless records.length == 0
    return records.length
  end
end

def init()
  @br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }

end
def action()
  begin
    init() if @br.nil? 
    param = get_metadata("PARAM","eaf9d1a0ec5f1dc58757ad6cffdacedb1a58854a600312ccc87f484313450d19276f8592ea512941")
    s_url = BASE_URL + "/?go=#{param}"
    pg = @br.get(s_url)
    raise "captcha" if pg.body =~ /captcha/i
    urls = scrape(pg.body,"list",nil)
    urls.each{|url|
      s_url = BASE_URL + url
      pg_tmp = @br.get(s_url)
      raise "captcha" if pg_tmp.body =~ /captcha/i
      scrape(pg_tmp.body,"details",{"URL"=>s_url})
    }
    param = attributes(Nokogiri::HTML(pg.body).xpath(".//ul[@class='paginador']/li/a[@class='current']/following::a[1]"),"href").split(/=/).last
    break if param.nil? or param.empty? 
    save_metadata("PARAM",param)
    @br = nil
    init()
    sleep(25)
  rescue Exception => e
   puts [s_url,e,e.backtrace,].inspect
   raise e if e.inspect =~ /captcha/i
  end while(true)
  delete_metadata("PARAM")
end

action()