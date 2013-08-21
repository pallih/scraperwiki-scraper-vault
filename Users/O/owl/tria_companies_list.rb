# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.tria.org.tw/en/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

@authors = {}
class String
  def blank?
    self.nil? or self.empty? 
  end
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
  if act == "categories"
    records = []
    Nokogiri::HTML(data).xpath(".//td[@colspan='4']/table[@width='100%']/tr/td[@bgcolor='#E8F4E0']/p/a").each{|a|
      records << {
        "category" => s_text(a.xpath("b/text()")).gsub(/\((.*)\)/,'').strip,
        "tmp_cat_link" => BASE_URL + attributes(a.xpath("."),"href")
      }
    }
    return records
  elsif act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//td[@width='50%']/table[@width='100%']/tr[@height]/td/p/a").each{|a|
      records << {
        "tmp_link" => BASE_URL + attributes(a.xpath("."),"href"),
        "id" => attributes(a.xpath("."),"href").scan(/memberid=(\d+)/).flatten.first,
      }.merge(rec)
    }
    return records
  elsif act == "details"
    doc = Nokogiri::HTML(data).xpath(".//td[@class='table_1']/table[1]/tr")
    r = {}
    r["company_name"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='公司名稱：']]/following-sibling::*[1][self::td]/p/text()"))
    r["estd_yr"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='成立年份：']]/following-sibling::*[1][self::td]/p/text()"))
    r["addr"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='公司地址：']]/following-sibling::*[1][self::td]/p/text()"))
    r["telephone"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='公司電話：']]/following-sibling::*[1][self::td]/p/text()"))
    r["fax"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='公司傳真：']]/following-sibling::*[1][self::td]/p/text()"))
    r["factory_addr"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='工廠地址：']]/following-sibling::*[1][self::td]/p/text()"))
    r["factory_telephone"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='工廠電話：']]/following-sibling::*[1][self::td]/p/text()"))
    r["factory_fax"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='工廠傳真：']]/following-sibling::*[1][self::td]/p/text()"))
    r["contact_person"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='聯絡人：']]/following-sibling::*[1][self::td]/p/text()"))
    r["email"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='電子信箱：']]/following-sibling::*[1][self::td]/p/a/text()"))
    r["products"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='營業項目：']]/following-sibling::*[1][self::td]/p/text()"))
    r["link"] = pg.uri.to_s
    return r.merge(rec)
  end
end


def action()
  cats = scrape(@br.get(BASE_URL + "trade.php"),"categories",{})
  start = get_metadata("start",0)
  cats[start..-1].each{|cat|
    list = scrape(@br.get(cat["tmp_cat_link"]),"list",cat)
    list.each{|rec|
      begin
        record = scrape(@br.get(rec["tmp_link"]),"details",rec.delete_if{|k,v| k=~ /^tmp/ })
        ScraperWiki.save_sqlite(unique_keys=["id"],record,table_name='swdata',verbose=2) 
      end if exists(rec["id"],"swdata","id") == 0
    }
    start = start + 1
    save_metadata("category",start)
  }
  save_metadata("category",0)
end
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.tria.org.tw/en/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

@authors = {}
class String
  def blank?
    self.nil? or self.empty? 
  end
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
  if act == "categories"
    records = []
    Nokogiri::HTML(data).xpath(".//td[@colspan='4']/table[@width='100%']/tr/td[@bgcolor='#E8F4E0']/p/a").each{|a|
      records << {
        "category" => s_text(a.xpath("b/text()")).gsub(/\((.*)\)/,'').strip,
        "tmp_cat_link" => BASE_URL + attributes(a.xpath("."),"href")
      }
    }
    return records
  elsif act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//td[@width='50%']/table[@width='100%']/tr[@height]/td/p/a").each{|a|
      records << {
        "tmp_link" => BASE_URL + attributes(a.xpath("."),"href"),
        "id" => attributes(a.xpath("."),"href").scan(/memberid=(\d+)/).flatten.first,
      }.merge(rec)
    }
    return records
  elsif act == "details"
    doc = Nokogiri::HTML(data).xpath(".//td[@class='table_1']/table[1]/tr")
    r = {}
    r["company_name"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='公司名稱：']]/following-sibling::*[1][self::td]/p/text()"))
    r["estd_yr"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='成立年份：']]/following-sibling::*[1][self::td]/p/text()"))
    r["addr"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='公司地址：']]/following-sibling::*[1][self::td]/p/text()"))
    r["telephone"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='公司電話：']]/following-sibling::*[1][self::td]/p/text()"))
    r["fax"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='公司傳真：']]/following-sibling::*[1][self::td]/p/text()"))
    r["factory_addr"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='工廠地址：']]/following-sibling::*[1][self::td]/p/text()"))
    r["factory_telephone"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='工廠電話：']]/following-sibling::*[1][self::td]/p/text()"))
    r["factory_fax"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='工廠傳真：']]/following-sibling::*[1][self::td]/p/text()"))
    r["contact_person"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='聯絡人：']]/following-sibling::*[1][self::td]/p/text()"))
    r["email"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='電子信箱：']]/following-sibling::*[1][self::td]/p/a/text()"))
    r["products"] = s_text(doc.xpath("./td[@class='table_2' and p[normalize-space(text())='營業項目：']]/following-sibling::*[1][self::td]/p/text()"))
    r["link"] = pg.uri.to_s
    return r.merge(rec)
  end
end


def action()
  cats = scrape(@br.get(BASE_URL + "trade.php"),"categories",{})
  start = get_metadata("start",0)
  cats[start..-1].each{|cat|
    list = scrape(@br.get(cat["tmp_cat_link"]),"list",cat)
    list.each{|rec|
      begin
        record = scrape(@br.get(rec["tmp_link"]),"details",rec.delete_if{|k,v| k=~ /^tmp/ })
        ScraperWiki.save_sqlite(unique_keys=["id"],record,table_name='swdata',verbose=2) 
      end if exists(rec["id"],"swdata","id") == 0
    }
    start = start + 1
    save_metadata("category",start)
  }
  save_metadata("category",0)
end
action()