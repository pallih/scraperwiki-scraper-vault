# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.tasi.org/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


@authors = {}
class String
  def pretty
    self.gsub(/\n|\t|\r/,' ').gsub(/\s+/," ").gsub(/${##}|^{##}|;$|^;|,$|^,/,'').gsub(/\u2013/,'-').strip.gsub(/(\u00A1@)+/,'').strip
  end
  def join(str)
    self + str
  end
  def append_base(str)
    return nil if self.nil? or self.empty? 
    return BASE_URL + str + self
  end
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
end


def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}"
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@width='878']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records << {
        "id" => a_text(td[1].xpath(".")).join("").strip,
        "link" => attributes(td[1].xpath(".//a"),"href"),
        "class" => s_text(td[0].xpath("./font/text()")),
        "website" => attributes(td[2].xpath(".//a"),"href"),
        "company_name" =>a_text(td[2].xpath(".")).join(" ").strip,
        "incharge" => a_text(td[3].xpath(".")).join(" ").strip,
        "email" => attributes(td[3].xpath(".//a"),"href").gsub("mailto:","").strip,
        "telephone" => s_text(td[4].xpath("./font/text()")),
        "fax" => s_text(td[5].xpath("./font/text()")),
        "addr" => s_text(td[6].xpath("./font/text()")),
      }
    }
    return records
  elsif act == "details"
    doc = Nokogiri::HTML(data).xpath(".//td[@width='349']")
    r = {}
    r["company_name"] = s_text(doc.xpath("strong/font[@size='2']/text()|font[@size='2'][1]/strong/text()"))
    
    tmp = a_text(doc.xpath("p"))#.each_slice(3)
  
    puts tmp.inspect
    if tmp.first =~ /\uFF1A/
      r["person_in_charge"] = tmp[tmp.index{|a| a=~ /^Person in charge/}].split(/\uFF1A/).last rescue nil
      r["position"] = tmp[tmp.index{|a| a=~ /^Position/}].split(/\uFF1A/).last rescue nil
      r["addr"] = tmp[tmp.index{|a| a=~ /^Address/}].split(/\uFF1A/).last rescue nil
      r["factory_addr"] = tmp[tmp.index{|a| a=~ /^Factory/}].split(/\uFF1A/).last rescue nil
      r["telephone"] = tmp[tmp.index{|a| a=~ /^Tel/}].split(/\uFF1A/).last rescue nil
      r["fax"] = tmp[tmp.index{|a| a=~ /^Fax/}].split(/\uFF1A/).last rescue nil
      r["email"] = tmp[tmp.index{|a| a=~ /^Email|^E-mail/i}+1] rescue nil
      r["website"] = tmp[tmp.index{|a| a=~ /^Web/i}+1] rescue nil
      r["products"] = tmp[tmp.index{|a| a=~ /^Product/i}].split(/\uFF1A/).last rescue nil
      r["brand"] = tmp[tmp.index{|a| a=~ /^Brand/i}].split(/\uFF1A/).last rescue nil
      r["profile"] = tmp[tmp.index{|a| a=~ /^Profile/i}].split(/\uFF1A/).last rescue nil
      r["capital"] = tmp[tmp.index{|a| a=~ /^Capital/i}].split(/\uFF1A/).last rescue nil
      r["turnover"] = tmp[tmp.index{|a| a=~ /^Turnover/i}].split(/\uFF1A/).last rescue nil
      r["estd_yr"] = tmp[tmp.index{|a| a=~ /^Date established/i}].split(/\uFF1A/).last rescue nil
      r["employees"] = tmp[tmp.index{|a| a=~ /^Personnel/i}].split(/\uFF1A/).last rescue nil
    else
      tm = tmp.each_slice(3)
      tm.each{|t|
        case t.first.strip
          when "Person in charge"
            r["person_in_charge"] = t.last
          when "Postion"
            r["position"] = t.last
          when "Address"
            r["addr"] = t.last
          when "Factory"
            r["factory_addr"] = t.last
          when "Tel"
            r["telephone"] = t.last
          when "Fax"
            r["fax"] = t.last
          when "Web"
            r["website"] = t.last
          when /email|e-mail/i
            r["email"] = t.last
          when "Product"
            r["product"] = t.last
          when "Brand"
            r["brand"] = t.last
          when "Profile"
            r["profile"] = t.last
          when "Capital"
            r["capital"] = t.last
          when "Turnover"
            r["turnover"] = t.last
          when "Date established"
            r["estd_dt"] = t.last
          when "Personnel"
            r["employees"] = t.last
        end
      }
    end
    return r.merge(rec)
  end
end


def action()
  list = scrape(@br.get(BASE_URL + "ememberlist.htm"),"list",{})
  ScraperWiki.save_sqlite(unique_keys=['id'],list,table_name='swdata',verbose=2)
end

action()
#puts scrape(@br.get("http://www.tasi.org/member/1006.htm"),"details",{}).inspect
#puts scrape(@br.get("http://www.tasi.org/member/1001.htm"),"details",{}).inspect
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.tasi.org/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


@authors = {}
class String
  def pretty
    self.gsub(/\n|\t|\r/,' ').gsub(/\s+/," ").gsub(/${##}|^{##}|;$|^;|,$|^,/,'').gsub(/\u2013/,'-').strip.gsub(/(\u00A1@)+/,'').strip
  end
  def join(str)
    self + str
  end
  def append_base(str)
    return nil if self.nil? or self.empty? 
    return BASE_URL + str + self
  end
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
end


def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}"
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@width='878']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records << {
        "id" => a_text(td[1].xpath(".")).join("").strip,
        "link" => attributes(td[1].xpath(".//a"),"href"),
        "class" => s_text(td[0].xpath("./font/text()")),
        "website" => attributes(td[2].xpath(".//a"),"href"),
        "company_name" =>a_text(td[2].xpath(".")).join(" ").strip,
        "incharge" => a_text(td[3].xpath(".")).join(" ").strip,
        "email" => attributes(td[3].xpath(".//a"),"href").gsub("mailto:","").strip,
        "telephone" => s_text(td[4].xpath("./font/text()")),
        "fax" => s_text(td[5].xpath("./font/text()")),
        "addr" => s_text(td[6].xpath("./font/text()")),
      }
    }
    return records
  elsif act == "details"
    doc = Nokogiri::HTML(data).xpath(".//td[@width='349']")
    r = {}
    r["company_name"] = s_text(doc.xpath("strong/font[@size='2']/text()|font[@size='2'][1]/strong/text()"))
    
    tmp = a_text(doc.xpath("p"))#.each_slice(3)
  
    puts tmp.inspect
    if tmp.first =~ /\uFF1A/
      r["person_in_charge"] = tmp[tmp.index{|a| a=~ /^Person in charge/}].split(/\uFF1A/).last rescue nil
      r["position"] = tmp[tmp.index{|a| a=~ /^Position/}].split(/\uFF1A/).last rescue nil
      r["addr"] = tmp[tmp.index{|a| a=~ /^Address/}].split(/\uFF1A/).last rescue nil
      r["factory_addr"] = tmp[tmp.index{|a| a=~ /^Factory/}].split(/\uFF1A/).last rescue nil
      r["telephone"] = tmp[tmp.index{|a| a=~ /^Tel/}].split(/\uFF1A/).last rescue nil
      r["fax"] = tmp[tmp.index{|a| a=~ /^Fax/}].split(/\uFF1A/).last rescue nil
      r["email"] = tmp[tmp.index{|a| a=~ /^Email|^E-mail/i}+1] rescue nil
      r["website"] = tmp[tmp.index{|a| a=~ /^Web/i}+1] rescue nil
      r["products"] = tmp[tmp.index{|a| a=~ /^Product/i}].split(/\uFF1A/).last rescue nil
      r["brand"] = tmp[tmp.index{|a| a=~ /^Brand/i}].split(/\uFF1A/).last rescue nil
      r["profile"] = tmp[tmp.index{|a| a=~ /^Profile/i}].split(/\uFF1A/).last rescue nil
      r["capital"] = tmp[tmp.index{|a| a=~ /^Capital/i}].split(/\uFF1A/).last rescue nil
      r["turnover"] = tmp[tmp.index{|a| a=~ /^Turnover/i}].split(/\uFF1A/).last rescue nil
      r["estd_yr"] = tmp[tmp.index{|a| a=~ /^Date established/i}].split(/\uFF1A/).last rescue nil
      r["employees"] = tmp[tmp.index{|a| a=~ /^Personnel/i}].split(/\uFF1A/).last rescue nil
    else
      tm = tmp.each_slice(3)
      tm.each{|t|
        case t.first.strip
          when "Person in charge"
            r["person_in_charge"] = t.last
          when "Postion"
            r["position"] = t.last
          when "Address"
            r["addr"] = t.last
          when "Factory"
            r["factory_addr"] = t.last
          when "Tel"
            r["telephone"] = t.last
          when "Fax"
            r["fax"] = t.last
          when "Web"
            r["website"] = t.last
          when /email|e-mail/i
            r["email"] = t.last
          when "Product"
            r["product"] = t.last
          when "Brand"
            r["brand"] = t.last
          when "Profile"
            r["profile"] = t.last
          when "Capital"
            r["capital"] = t.last
          when "Turnover"
            r["turnover"] = t.last
          when "Date established"
            r["estd_dt"] = t.last
          when "Personnel"
            r["employees"] = t.last
        end
      }
    end
    return r.merge(rec)
  end
end


def action()
  list = scrape(@br.get(BASE_URL + "ememberlist.htm"),"list",{})
  ScraperWiki.save_sqlite(unique_keys=['id'],list,table_name='swdata',verbose=2)
end

action()
#puts scrape(@br.get("http://www.tasi.org/member/1006.htm"),"details",{}).inspect
#puts scrape(@br.get("http://www.tasi.org/member/1001.htm"),"details",{}).inspect
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.tasi.org/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


@authors = {}
class String
  def pretty
    self.gsub(/\n|\t|\r/,' ').gsub(/\s+/," ").gsub(/${##}|^{##}|;$|^;|,$|^,/,'').gsub(/\u2013/,'-').strip.gsub(/(\u00A1@)+/,'').strip
  end
  def join(str)
    self + str
  end
  def append_base(str)
    return nil if self.nil? or self.empty? 
    return BASE_URL + str + self
  end
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
end


def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}"
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@width='878']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records << {
        "id" => a_text(td[1].xpath(".")).join("").strip,
        "link" => attributes(td[1].xpath(".//a"),"href"),
        "class" => s_text(td[0].xpath("./font/text()")),
        "website" => attributes(td[2].xpath(".//a"),"href"),
        "company_name" =>a_text(td[2].xpath(".")).join(" ").strip,
        "incharge" => a_text(td[3].xpath(".")).join(" ").strip,
        "email" => attributes(td[3].xpath(".//a"),"href").gsub("mailto:","").strip,
        "telephone" => s_text(td[4].xpath("./font/text()")),
        "fax" => s_text(td[5].xpath("./font/text()")),
        "addr" => s_text(td[6].xpath("./font/text()")),
      }
    }
    return records
  elsif act == "details"
    doc = Nokogiri::HTML(data).xpath(".//td[@width='349']")
    r = {}
    r["company_name"] = s_text(doc.xpath("strong/font[@size='2']/text()|font[@size='2'][1]/strong/text()"))
    
    tmp = a_text(doc.xpath("p"))#.each_slice(3)
  
    puts tmp.inspect
    if tmp.first =~ /\uFF1A/
      r["person_in_charge"] = tmp[tmp.index{|a| a=~ /^Person in charge/}].split(/\uFF1A/).last rescue nil
      r["position"] = tmp[tmp.index{|a| a=~ /^Position/}].split(/\uFF1A/).last rescue nil
      r["addr"] = tmp[tmp.index{|a| a=~ /^Address/}].split(/\uFF1A/).last rescue nil
      r["factory_addr"] = tmp[tmp.index{|a| a=~ /^Factory/}].split(/\uFF1A/).last rescue nil
      r["telephone"] = tmp[tmp.index{|a| a=~ /^Tel/}].split(/\uFF1A/).last rescue nil
      r["fax"] = tmp[tmp.index{|a| a=~ /^Fax/}].split(/\uFF1A/).last rescue nil
      r["email"] = tmp[tmp.index{|a| a=~ /^Email|^E-mail/i}+1] rescue nil
      r["website"] = tmp[tmp.index{|a| a=~ /^Web/i}+1] rescue nil
      r["products"] = tmp[tmp.index{|a| a=~ /^Product/i}].split(/\uFF1A/).last rescue nil
      r["brand"] = tmp[tmp.index{|a| a=~ /^Brand/i}].split(/\uFF1A/).last rescue nil
      r["profile"] = tmp[tmp.index{|a| a=~ /^Profile/i}].split(/\uFF1A/).last rescue nil
      r["capital"] = tmp[tmp.index{|a| a=~ /^Capital/i}].split(/\uFF1A/).last rescue nil
      r["turnover"] = tmp[tmp.index{|a| a=~ /^Turnover/i}].split(/\uFF1A/).last rescue nil
      r["estd_yr"] = tmp[tmp.index{|a| a=~ /^Date established/i}].split(/\uFF1A/).last rescue nil
      r["employees"] = tmp[tmp.index{|a| a=~ /^Personnel/i}].split(/\uFF1A/).last rescue nil
    else
      tm = tmp.each_slice(3)
      tm.each{|t|
        case t.first.strip
          when "Person in charge"
            r["person_in_charge"] = t.last
          when "Postion"
            r["position"] = t.last
          when "Address"
            r["addr"] = t.last
          when "Factory"
            r["factory_addr"] = t.last
          when "Tel"
            r["telephone"] = t.last
          when "Fax"
            r["fax"] = t.last
          when "Web"
            r["website"] = t.last
          when /email|e-mail/i
            r["email"] = t.last
          when "Product"
            r["product"] = t.last
          when "Brand"
            r["brand"] = t.last
          when "Profile"
            r["profile"] = t.last
          when "Capital"
            r["capital"] = t.last
          when "Turnover"
            r["turnover"] = t.last
          when "Date established"
            r["estd_dt"] = t.last
          when "Personnel"
            r["employees"] = t.last
        end
      }
    end
    return r.merge(rec)
  end
end


def action()
  list = scrape(@br.get(BASE_URL + "ememberlist.htm"),"list",{})
  ScraperWiki.save_sqlite(unique_keys=['id'],list,table_name='swdata',verbose=2)
end

action()
#puts scrape(@br.get("http://www.tasi.org/member/1006.htm"),"details",{}).inspect
#puts scrape(@br.get("http://www.tasi.org/member/1001.htm"),"details",{}).inspect
