# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


BASE_URL = "https://ems.ms.gov.pl"

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

class String
  def pretty
    self.strip.gsub(/(\s)+/,' ').strip
  end  
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(data,act,rec)
  if act == "details"
    r = {}
    doc = Nokogiri::HTML(data).xpath(".")
    r["company_name"] = s_text(doc.xpath(".//td[normalize-space(text())='Nazwa']/following-sibling::*[1][self::td]/text()"))  
    r["register"] = s_text(doc.xpath(".//td[normalize-space(text())='Rejestr']/following-sibling::*[1][self::td]/text()"))  
    r["company_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Numer KRS']/following-sibling::*[1][self::td]/text()"))
    r["nip"] = s_text(doc.xpath(".//td[normalize-space(text())='NIP']/following-sibling::*[1][self::td]/text()"))
    r["type"] = s_text(doc.xpath(".//td[normalize-space(text())='Forma prawna']/following-sibling::*[1][self::td]/text()"))
    r["register"] = "Rejestr Stowarzyszeń" if r["type"] == "STOWARZYSZENIE"
    r["inc_dt_roe"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wpisu do Rejestru Przedsiębiorców']/following-sibling::*[1][self::td]/text()"))  
    r["inc_dt_roa"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wpisu do Rejestru Stowarzyszeń']/following-sibling::*[1][self::td]/text()"))  
    r["rem_dt_roe"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wykreślenia z Rejestru Przedsiębiorców']/following-sibling::*[1][self::td]/text()"))  
    r["rem_dt_roa"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wykreślenia z Rejestru Stowarzyszeń']/following-sibling::*[1][self::td]/text()"))  
    r["rem_dt_krs"] = s_text(doc.xpath(".//td[normalize-space(text())='Data uprawomocnienia wykreślenia z KRS']/following-sibling::*[1][self::td]/text()"))  
    r["susp_dt"] = s_text(doc.xpath(".//td[normalize-space(text())='Data zawieszenia działalności']/following-sibling::*[1][self::td]/text()"))  
    r["resp_dt"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wznowienia działalności']/following-sibling::*[1][self::td]/text()"))  
    r["province"] = s_text(doc.xpath(".//td[normalize-space(text())='Województwo']/following-sibling::*[1][self::td]/text()"))  
    r["district"] = s_text(doc.xpath(".//td[normalize-space(text())='Powiat']/following-sibling::*[1][self::td]/text()"))  
    r["community"] = s_text(doc.xpath(".//td[normalize-space(text())='Gmina']/following-sibling::*[1][self::td]/text()"))  
    r["place"] = s_text(doc.xpath(".//td[normalize-space(text())='Miejscowość']/following-sibling::*[1][self::td]/text()"))  
    r["address"] = s_text(doc.xpath(".//td[normalize-space(text())='Adres']/following-sibling::*[1][self::td]/text()"))  
    r["zipcode"] = s_text(doc.xpath(".//td[normalize-space(text())='Kod pocztowy']/following-sibling::*[1][self::td]/text()"))  
    r["website"] = a_text(doc.xpath(".//td[normalize-space(text())='Adres WWW']/following-sibling::*[1][self::td]/text()")).join(" ").pretty
    r["email"] = a_text(doc.xpath(".//td[normalize-space(text())='Email']/following-sibling::*[1][self::td]/text()")).join(" ").pretty
 
    tmp = []
    doc.xpath(".//table[@class='czlonkowieReprezentacji']/tbody/tr").each{|tr|
      tmp << {
        "name" => s_text(tr.xpath("./td[@class='nazwanazwiskoLubNazwa']/text()")),
        "second" => s_text(tr.xpath("./td[@class='nazwanazwiskoDrugie']/text()")),
        "first_name" => s_text(tr.xpath("./td[@class='nazwaimiePierwsze']/text()")),
        "second_name" => s_text(tr.xpath("./td[@class='nazwaimieDrugie']/text()")),
        "function" => s_text(tr.xpath("./td[@class='funkcja']/text()"))
      }
    }
    r["members"] = JSON.generate tmp unless tmp.empty? 
    r["doc"] = Time.now
  
    return r.merge(rec).delete_if{|k,v| k=~ /^tmp_/} unless r['company_number'].nil? or r['company_number'].strip.empty? 
  end

end

def action(id)
  records = []
  pg = @br.get("https://ems.ms.gov.pl/krs/wyszukiwaniepodmiotu.podmiotdaneszczegolowe/RP/#{'%010d' % id}") rescue retry
  return if pg.nil? 
  tmp = scrape(pg.body,"details",{})
  records << tmp unless tmp.nil? or tmp["company_name"].nil? or tmp["company_name"].empty? 

  ScraperWiki.save_sqlite(unique_keys=["company_number"],records) unless records.empty? 
end


strt = get_metadata("start",432165)
(strt..strt+1000).each{|id|
  ret = action(id)
  save_metadata("start",id) unless ret.nil? 
  sleep(5)
}


#puts scrape(@br.get("https://ems.ms.gov.pl/krs/wyszukiwaniepodmiotu.podmiotdaneszczegolowe/RP/#{'%010d' % 240611}").body,"details",{}).inspect
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


BASE_URL = "https://ems.ms.gov.pl"

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

class String
  def pretty
    self.strip.gsub(/(\s)+/,' ').strip
  end  
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(data,act,rec)
  if act == "details"
    r = {}
    doc = Nokogiri::HTML(data).xpath(".")
    r["company_name"] = s_text(doc.xpath(".//td[normalize-space(text())='Nazwa']/following-sibling::*[1][self::td]/text()"))  
    r["register"] = s_text(doc.xpath(".//td[normalize-space(text())='Rejestr']/following-sibling::*[1][self::td]/text()"))  
    r["company_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Numer KRS']/following-sibling::*[1][self::td]/text()"))
    r["nip"] = s_text(doc.xpath(".//td[normalize-space(text())='NIP']/following-sibling::*[1][self::td]/text()"))
    r["type"] = s_text(doc.xpath(".//td[normalize-space(text())='Forma prawna']/following-sibling::*[1][self::td]/text()"))
    r["register"] = "Rejestr Stowarzyszeń" if r["type"] == "STOWARZYSZENIE"
    r["inc_dt_roe"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wpisu do Rejestru Przedsiębiorców']/following-sibling::*[1][self::td]/text()"))  
    r["inc_dt_roa"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wpisu do Rejestru Stowarzyszeń']/following-sibling::*[1][self::td]/text()"))  
    r["rem_dt_roe"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wykreślenia z Rejestru Przedsiębiorców']/following-sibling::*[1][self::td]/text()"))  
    r["rem_dt_roa"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wykreślenia z Rejestru Stowarzyszeń']/following-sibling::*[1][self::td]/text()"))  
    r["rem_dt_krs"] = s_text(doc.xpath(".//td[normalize-space(text())='Data uprawomocnienia wykreślenia z KRS']/following-sibling::*[1][self::td]/text()"))  
    r["susp_dt"] = s_text(doc.xpath(".//td[normalize-space(text())='Data zawieszenia działalności']/following-sibling::*[1][self::td]/text()"))  
    r["resp_dt"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wznowienia działalności']/following-sibling::*[1][self::td]/text()"))  
    r["province"] = s_text(doc.xpath(".//td[normalize-space(text())='Województwo']/following-sibling::*[1][self::td]/text()"))  
    r["district"] = s_text(doc.xpath(".//td[normalize-space(text())='Powiat']/following-sibling::*[1][self::td]/text()"))  
    r["community"] = s_text(doc.xpath(".//td[normalize-space(text())='Gmina']/following-sibling::*[1][self::td]/text()"))  
    r["place"] = s_text(doc.xpath(".//td[normalize-space(text())='Miejscowość']/following-sibling::*[1][self::td]/text()"))  
    r["address"] = s_text(doc.xpath(".//td[normalize-space(text())='Adres']/following-sibling::*[1][self::td]/text()"))  
    r["zipcode"] = s_text(doc.xpath(".//td[normalize-space(text())='Kod pocztowy']/following-sibling::*[1][self::td]/text()"))  
    r["website"] = a_text(doc.xpath(".//td[normalize-space(text())='Adres WWW']/following-sibling::*[1][self::td]/text()")).join(" ").pretty
    r["email"] = a_text(doc.xpath(".//td[normalize-space(text())='Email']/following-sibling::*[1][self::td]/text()")).join(" ").pretty
 
    tmp = []
    doc.xpath(".//table[@class='czlonkowieReprezentacji']/tbody/tr").each{|tr|
      tmp << {
        "name" => s_text(tr.xpath("./td[@class='nazwanazwiskoLubNazwa']/text()")),
        "second" => s_text(tr.xpath("./td[@class='nazwanazwiskoDrugie']/text()")),
        "first_name" => s_text(tr.xpath("./td[@class='nazwaimiePierwsze']/text()")),
        "second_name" => s_text(tr.xpath("./td[@class='nazwaimieDrugie']/text()")),
        "function" => s_text(tr.xpath("./td[@class='funkcja']/text()"))
      }
    }
    r["members"] = JSON.generate tmp unless tmp.empty? 
    r["doc"] = Time.now
  
    return r.merge(rec).delete_if{|k,v| k=~ /^tmp_/} unless r['company_number'].nil? or r['company_number'].strip.empty? 
  end

end

def action(id)
  records = []
  pg = @br.get("https://ems.ms.gov.pl/krs/wyszukiwaniepodmiotu.podmiotdaneszczegolowe/RP/#{'%010d' % id}") rescue retry
  return if pg.nil? 
  tmp = scrape(pg.body,"details",{})
  records << tmp unless tmp.nil? or tmp["company_name"].nil? or tmp["company_name"].empty? 

  ScraperWiki.save_sqlite(unique_keys=["company_number"],records) unless records.empty? 
end


strt = get_metadata("start",432165)
(strt..strt+1000).each{|id|
  ret = action(id)
  save_metadata("start",id) unless ret.nil? 
  sleep(5)
}


#puts scrape(@br.get("https://ems.ms.gov.pl/krs/wyszukiwaniepodmiotu.podmiotdaneszczegolowe/RP/#{'%010d' % 240611}").body,"details",{}).inspect
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


BASE_URL = "https://ems.ms.gov.pl"

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

class String
  def pretty
    self.strip.gsub(/(\s)+/,' ').strip
  end  
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(data,act,rec)
  if act == "details"
    r = {}
    doc = Nokogiri::HTML(data).xpath(".")
    r["company_name"] = s_text(doc.xpath(".//td[normalize-space(text())='Nazwa']/following-sibling::*[1][self::td]/text()"))  
    r["register"] = s_text(doc.xpath(".//td[normalize-space(text())='Rejestr']/following-sibling::*[1][self::td]/text()"))  
    r["company_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Numer KRS']/following-sibling::*[1][self::td]/text()"))
    r["nip"] = s_text(doc.xpath(".//td[normalize-space(text())='NIP']/following-sibling::*[1][self::td]/text()"))
    r["type"] = s_text(doc.xpath(".//td[normalize-space(text())='Forma prawna']/following-sibling::*[1][self::td]/text()"))
    r["register"] = "Rejestr Stowarzyszeń" if r["type"] == "STOWARZYSZENIE"
    r["inc_dt_roe"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wpisu do Rejestru Przedsiębiorców']/following-sibling::*[1][self::td]/text()"))  
    r["inc_dt_roa"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wpisu do Rejestru Stowarzyszeń']/following-sibling::*[1][self::td]/text()"))  
    r["rem_dt_roe"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wykreślenia z Rejestru Przedsiębiorców']/following-sibling::*[1][self::td]/text()"))  
    r["rem_dt_roa"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wykreślenia z Rejestru Stowarzyszeń']/following-sibling::*[1][self::td]/text()"))  
    r["rem_dt_krs"] = s_text(doc.xpath(".//td[normalize-space(text())='Data uprawomocnienia wykreślenia z KRS']/following-sibling::*[1][self::td]/text()"))  
    r["susp_dt"] = s_text(doc.xpath(".//td[normalize-space(text())='Data zawieszenia działalności']/following-sibling::*[1][self::td]/text()"))  
    r["resp_dt"] = s_text(doc.xpath(".//td[normalize-space(text())='Data wznowienia działalności']/following-sibling::*[1][self::td]/text()"))  
    r["province"] = s_text(doc.xpath(".//td[normalize-space(text())='Województwo']/following-sibling::*[1][self::td]/text()"))  
    r["district"] = s_text(doc.xpath(".//td[normalize-space(text())='Powiat']/following-sibling::*[1][self::td]/text()"))  
    r["community"] = s_text(doc.xpath(".//td[normalize-space(text())='Gmina']/following-sibling::*[1][self::td]/text()"))  
    r["place"] = s_text(doc.xpath(".//td[normalize-space(text())='Miejscowość']/following-sibling::*[1][self::td]/text()"))  
    r["address"] = s_text(doc.xpath(".//td[normalize-space(text())='Adres']/following-sibling::*[1][self::td]/text()"))  
    r["zipcode"] = s_text(doc.xpath(".//td[normalize-space(text())='Kod pocztowy']/following-sibling::*[1][self::td]/text()"))  
    r["website"] = a_text(doc.xpath(".//td[normalize-space(text())='Adres WWW']/following-sibling::*[1][self::td]/text()")).join(" ").pretty
    r["email"] = a_text(doc.xpath(".//td[normalize-space(text())='Email']/following-sibling::*[1][self::td]/text()")).join(" ").pretty
 
    tmp = []
    doc.xpath(".//table[@class='czlonkowieReprezentacji']/tbody/tr").each{|tr|
      tmp << {
        "name" => s_text(tr.xpath("./td[@class='nazwanazwiskoLubNazwa']/text()")),
        "second" => s_text(tr.xpath("./td[@class='nazwanazwiskoDrugie']/text()")),
        "first_name" => s_text(tr.xpath("./td[@class='nazwaimiePierwsze']/text()")),
        "second_name" => s_text(tr.xpath("./td[@class='nazwaimieDrugie']/text()")),
        "function" => s_text(tr.xpath("./td[@class='funkcja']/text()"))
      }
    }
    r["members"] = JSON.generate tmp unless tmp.empty? 
    r["doc"] = Time.now
  
    return r.merge(rec).delete_if{|k,v| k=~ /^tmp_/} unless r['company_number'].nil? or r['company_number'].strip.empty? 
  end

end

def action(id)
  records = []
  pg = @br.get("https://ems.ms.gov.pl/krs/wyszukiwaniepodmiotu.podmiotdaneszczegolowe/RP/#{'%010d' % id}") rescue retry
  return if pg.nil? 
  tmp = scrape(pg.body,"details",{})
  records << tmp unless tmp.nil? or tmp["company_name"].nil? or tmp["company_name"].empty? 

  ScraperWiki.save_sqlite(unique_keys=["company_number"],records) unless records.empty? 
end


strt = get_metadata("start",432165)
(strt..strt+1000).each{|id|
  ret = action(id)
  save_metadata("start",id) unless ret.nil? 
  sleep(5)
}


#puts scrape(@br.get("https://ems.ms.gov.pl/krs/wyszukiwaniepodmiotu.podmiotdaneszczegolowe/RP/#{'%010d' % 240611}").body,"details",{}).inspect
