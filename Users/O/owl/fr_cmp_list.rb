# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "http://www.infogreffe.fr"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end

class Array
  def strip
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue data
  if act == "list"
    records = []
    Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//td[@class='entreprise']/a[@class='company']").each{|a|
      records << {
        "company_name" => s_text(a.xpath("./text()")),
        "link" => append_base(BASE_URL,attributes(a.xpath("."),"href")),
        "doc" => Time.now
      }.merge(rec)
    }
    return records
  end
end

def action(srch)
  strt = 10
  @br.get(BASE_URL + "/infogreffe/entrepNewRech.do")
  pg = @br.get(BASE_URL + "/infogreffe/listeRegCom.xml?denomination=#{srch}")
  begin
    list = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['link'],list)
    break if list.nil? or list.empty? or list.length < 10
    strt = strt + 10
    pg = @br.get(BASE_URL + "/infogreffe/includeEntrepListe.do?index=rcs&tri=PERTINENCE&entrepGlobalIndex=#{strt}&_=")
  end while(true)
  return srch,strt
end


trail = get_metadata("trail","A").split(">>")
srch = trail.last
MAX_T = 100
begin
  prev,ret = action(srch)
  if ret >= MAX_T
    srch = srch + "A"
    trail << srch
  else
    tmp = ''
    begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
      if tmp.nil? 
        trail == ["A"]
      else
        srch = (tmp == 'Z')? "A" : tmp.next
        trail << srch
    end
  end
  puts [ret,prev,srch,trail.join(">>")].inspect
  save_metadata("trail",trail.join(">>"))
end while(true)
# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "http://www.infogreffe.fr"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end

class Array
  def strip
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue data
  if act == "list"
    records = []
    Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//td[@class='entreprise']/a[@class='company']").each{|a|
      records << {
        "company_name" => s_text(a.xpath("./text()")),
        "link" => append_base(BASE_URL,attributes(a.xpath("."),"href")),
        "doc" => Time.now
      }.merge(rec)
    }
    return records
  end
end

def action(srch)
  strt = 10
  @br.get(BASE_URL + "/infogreffe/entrepNewRech.do")
  pg = @br.get(BASE_URL + "/infogreffe/listeRegCom.xml?denomination=#{srch}")
  begin
    list = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['link'],list)
    break if list.nil? or list.empty? or list.length < 10
    strt = strt + 10
    pg = @br.get(BASE_URL + "/infogreffe/includeEntrepListe.do?index=rcs&tri=PERTINENCE&entrepGlobalIndex=#{strt}&_=")
  end while(true)
  return srch,strt
end


trail = get_metadata("trail","A").split(">>")
srch = trail.last
MAX_T = 100
begin
  prev,ret = action(srch)
  if ret >= MAX_T
    srch = srch + "A"
    trail << srch
  else
    tmp = ''
    begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
      if tmp.nil? 
        trail == ["A"]
      else
        srch = (tmp == 'Z')? "A" : tmp.next
        trail << srch
    end
  end
  puts [ret,prev,srch,trail.join(">>")].inspect
  save_metadata("trail",trail.join(">>"))
end while(true)
# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "http://www.infogreffe.fr"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end

class Array
  def strip
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue data
  if act == "list"
    records = []
    Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//td[@class='entreprise']/a[@class='company']").each{|a|
      records << {
        "company_name" => s_text(a.xpath("./text()")),
        "link" => append_base(BASE_URL,attributes(a.xpath("."),"href")),
        "doc" => Time.now
      }.merge(rec)
    }
    return records
  end
end

def action(srch)
  strt = 10
  @br.get(BASE_URL + "/infogreffe/entrepNewRech.do")
  pg = @br.get(BASE_URL + "/infogreffe/listeRegCom.xml?denomination=#{srch}")
  begin
    list = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['link'],list)
    break if list.nil? or list.empty? or list.length < 10
    strt = strt + 10
    pg = @br.get(BASE_URL + "/infogreffe/includeEntrepListe.do?index=rcs&tri=PERTINENCE&entrepGlobalIndex=#{strt}&_=")
  end while(true)
  return srch,strt
end


trail = get_metadata("trail","A").split(">>")
srch = trail.last
MAX_T = 100
begin
  prev,ret = action(srch)
  if ret >= MAX_T
    srch = srch + "A"
    trail << srch
  else
    tmp = ''
    begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
      if tmp.nil? 
        trail == ["A"]
      else
        srch = (tmp == 'Z')? "A" : tmp.next
        trail << srch
    end
  end
  puts [ret,prev,srch,trail.join(">>")].inspect
  save_metadata("trail",trail.join(">>"))
end while(true)
