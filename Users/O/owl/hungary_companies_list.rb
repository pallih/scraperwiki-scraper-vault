require 'nokogiri'
require 'mechanize'
require 'pp'
require 'logger'
# encoding: UTF-8

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.e-cegjegyzek.hu/"

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/:|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data)

  Nokogiri::HTML(data).xpath(".//*[@style='TABLE-LAYOUT:fixed;']/tr[@valign='TOP']").each{|tr|
    td = tr.xpath("td")
    records = {}
    records["COMPANY_NUMBER"] = text(td[1])
    records["COMPANY_STR"] = text(td[2].xpath("span[@id='cegnev']/text()"))
    records["STATUS"] = text(td[2].xpath("span[@id='cegnev']/i/text()")).gsub(/\(|\)/,"")
    records["ADDR"] = text(td[2].xpath("span[@id='szekhely']/text()"))
    records["TAXID"] = text(td[2].xpath("span[@id='adoszam']/text()"))
    records["DOC"]=Time.now.to_s
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER","COMPANY_STR","STATUS"],records,table_name='swdata',verbose=0) unless (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?)
    }
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.log = Logger.new("mechanize.log")
      b.read_timeout = 12000

    }
    params = {
      'recaptcha_challenge_field'=>'03AHJ_VuskjgRSz7yY-1NHBP2Ttkkyodh-i8Bw2lwhh8sKcKZM32XuNq5wqI5StANECNv38BkYVIpDTfUc_ue-iaJd1nWy4j4gwDpNHD5dMjaDXDPat2ACE1E',
      'recaptcha_response_field'=>'hgytu iop', 'stype'=>'CgnevKeres', 'doku'=>'', 'adoszam'=>'', 'nev'=>'', 'bs'=>'', 'cf'=>'', 'n'=>'', 'cegnev'=>"#{srch}___", 'tlist'=>'', 'key'=>'', 'tipus'=>'', 'outformat'=>'html', 'reqtip'=>'adatokat', 'alairt'=>'', 'maxnum'=>'50000', 'vantlist'=>'', 'fcode'=>'', 'VDAT'=>'', 'do'=>'Mehet'
    }
    s_url = BASE_URL + "IMOnline"
    pg = br.post(s_url,params)
    puts pg.body
    scrape(pg.body)
  rescue Exception => e
     puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
     sleep(30)
     retry
  end
end
action("A")
puts IO.read("mechanize.log")
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'logger'
# encoding: UTF-8

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.e-cegjegyzek.hu/"

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/:|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data)

  Nokogiri::HTML(data).xpath(".//*[@style='TABLE-LAYOUT:fixed;']/tr[@valign='TOP']").each{|tr|
    td = tr.xpath("td")
    records = {}
    records["COMPANY_NUMBER"] = text(td[1])
    records["COMPANY_STR"] = text(td[2].xpath("span[@id='cegnev']/text()"))
    records["STATUS"] = text(td[2].xpath("span[@id='cegnev']/i/text()")).gsub(/\(|\)/,"")
    records["ADDR"] = text(td[2].xpath("span[@id='szekhely']/text()"))
    records["TAXID"] = text(td[2].xpath("span[@id='adoszam']/text()"))
    records["DOC"]=Time.now.to_s
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER","COMPANY_STR","STATUS"],records,table_name='swdata',verbose=0) unless (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?)
    }
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.log = Logger.new("mechanize.log")
      b.read_timeout = 12000

    }
    params = {
      'recaptcha_challenge_field'=>'03AHJ_VuskjgRSz7yY-1NHBP2Ttkkyodh-i8Bw2lwhh8sKcKZM32XuNq5wqI5StANECNv38BkYVIpDTfUc_ue-iaJd1nWy4j4gwDpNHD5dMjaDXDPat2ACE1E',
      'recaptcha_response_field'=>'hgytu iop', 'stype'=>'CgnevKeres', 'doku'=>'', 'adoszam'=>'', 'nev'=>'', 'bs'=>'', 'cf'=>'', 'n'=>'', 'cegnev'=>"#{srch}___", 'tlist'=>'', 'key'=>'', 'tipus'=>'', 'outformat'=>'html', 'reqtip'=>'adatokat', 'alairt'=>'', 'maxnum'=>'50000', 'vantlist'=>'', 'fcode'=>'', 'VDAT'=>'', 'do'=>'Mehet'
    }
    s_url = BASE_URL + "IMOnline"
    pg = br.post(s_url,params)
    puts pg.body
    scrape(pg.body)
  rescue Exception => e
     puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
     sleep(30)
     retry
  end
end
action("A")
puts IO.read("mechanize.log")
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'logger'
# encoding: UTF-8

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.e-cegjegyzek.hu/"

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/:|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data)

  Nokogiri::HTML(data).xpath(".//*[@style='TABLE-LAYOUT:fixed;']/tr[@valign='TOP']").each{|tr|
    td = tr.xpath("td")
    records = {}
    records["COMPANY_NUMBER"] = text(td[1])
    records["COMPANY_STR"] = text(td[2].xpath("span[@id='cegnev']/text()"))
    records["STATUS"] = text(td[2].xpath("span[@id='cegnev']/i/text()")).gsub(/\(|\)/,"")
    records["ADDR"] = text(td[2].xpath("span[@id='szekhely']/text()"))
    records["TAXID"] = text(td[2].xpath("span[@id='adoszam']/text()"))
    records["DOC"]=Time.now.to_s
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER","COMPANY_STR","STATUS"],records,table_name='swdata',verbose=0) unless (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?)
    }
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.log = Logger.new("mechanize.log")
      b.read_timeout = 12000

    }
    params = {
      'recaptcha_challenge_field'=>'03AHJ_VuskjgRSz7yY-1NHBP2Ttkkyodh-i8Bw2lwhh8sKcKZM32XuNq5wqI5StANECNv38BkYVIpDTfUc_ue-iaJd1nWy4j4gwDpNHD5dMjaDXDPat2ACE1E',
      'recaptcha_response_field'=>'hgytu iop', 'stype'=>'CgnevKeres', 'doku'=>'', 'adoszam'=>'', 'nev'=>'', 'bs'=>'', 'cf'=>'', 'n'=>'', 'cegnev'=>"#{srch}___", 'tlist'=>'', 'key'=>'', 'tipus'=>'', 'outformat'=>'html', 'reqtip'=>'adatokat', 'alairt'=>'', 'maxnum'=>'50000', 'vantlist'=>'', 'fcode'=>'', 'VDAT'=>'', 'do'=>'Mehet'
    }
    s_url = BASE_URL + "IMOnline"
    pg = br.post(s_url,params)
    puts pg.body
    scrape(pg.body)
  rescue Exception => e
     puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
     sleep(30)
     retry
  end
end
action("A")
puts IO.read("mechanize.log")
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'logger'
# encoding: UTF-8

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.e-cegjegyzek.hu/"

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/:|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data)

  Nokogiri::HTML(data).xpath(".//*[@style='TABLE-LAYOUT:fixed;']/tr[@valign='TOP']").each{|tr|
    td = tr.xpath("td")
    records = {}
    records["COMPANY_NUMBER"] = text(td[1])
    records["COMPANY_STR"] = text(td[2].xpath("span[@id='cegnev']/text()"))
    records["STATUS"] = text(td[2].xpath("span[@id='cegnev']/i/text()")).gsub(/\(|\)/,"")
    records["ADDR"] = text(td[2].xpath("span[@id='szekhely']/text()"))
    records["TAXID"] = text(td[2].xpath("span[@id='adoszam']/text()"))
    records["DOC"]=Time.now.to_s
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER","COMPANY_STR","STATUS"],records,table_name='swdata',verbose=0) unless (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?)
    }
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.log = Logger.new("mechanize.log")
      b.read_timeout = 12000

    }
    params = {
      'recaptcha_challenge_field'=>'03AHJ_VuskjgRSz7yY-1NHBP2Ttkkyodh-i8Bw2lwhh8sKcKZM32XuNq5wqI5StANECNv38BkYVIpDTfUc_ue-iaJd1nWy4j4gwDpNHD5dMjaDXDPat2ACE1E',
      'recaptcha_response_field'=>'hgytu iop', 'stype'=>'CgnevKeres', 'doku'=>'', 'adoszam'=>'', 'nev'=>'', 'bs'=>'', 'cf'=>'', 'n'=>'', 'cegnev'=>"#{srch}___", 'tlist'=>'', 'key'=>'', 'tipus'=>'', 'outformat'=>'html', 'reqtip'=>'adatokat', 'alairt'=>'', 'maxnum'=>'50000', 'vantlist'=>'', 'fcode'=>'', 'VDAT'=>'', 'do'=>'Mehet'
    }
    s_url = BASE_URL + "IMOnline"
    pg = br.post(s_url,params)
    puts pg.body
    scrape(pg.body)
  rescue Exception => e
     puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
     sleep(30)
     retry
  end
end
action("A")
puts IO.read("mechanize.log")
