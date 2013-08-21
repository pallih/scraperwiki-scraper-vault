# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'httpclient'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://business.abudhabi.ae"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
#@br = HTTPClient.new


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

def scrape(cn,data,url)
  doc = Nokogiri::HTML(data).xpath(".//div[@id='T4801647921215097862967']//div[@class='fragment introModul']")
  return nil if doc.length <= 0
  r = {
    "company_number"=>cn,
    "company_name"=>s_text(doc.xpath(".//h4[@class='subheadline']"))
  }

  doc = Nokogiri::HTML(data).xpath(".")
  r["company_type"] = s_text(doc.xpath(".//dt[normalize-space(text())='Company Type']/following-sibling::*[1][self::dd]/text()"))
  r["legal_form"]=s_text(doc.xpath(".//dt[normalize-space(text())='Legal Form']/following-sibling::*[1][self::dd]/text()"))
  r["established_dt"]=s_text(doc.xpath(".//dt[normalize-space(text())='Established']/following-sibling::*[1][self::dd]/text()"))
  r["expiry_dt"]=s_text(doc.xpath(".//dt[normalize-space(text())='Expiry Date']/following-sibling::*[1][self::dd]/text()"))
  r["address"]=s_text(doc.xpath(".//dt[normalize-space(text())='Address']/following-sibling::*[1][self::dd]/text()"))
  r["city"]=s_text(doc.xpath(".//dt[normalize-space(text())='City']/following-sibling::*[1][self::dd]/text()"))
  r["telephone"]=s_text(doc.xpath(".//dt[normalize-space(text())='Telephone']/following-sibling::*[1][self::dd]/text()"))
  r["fax"]=s_text(doc.xpath(".//dt[normalize-space(text())='Fax']/following-sibling::*[1][self::dd]/text()"))
  r["email"]=s_text(doc.xpath(".//dt[normalize-space(text())='Email']/following-sibling::*[1][self::dd]/a/text()"))
  r["website"]=s_text(doc.xpath(".//dt[normalize-space(text())='Website']/following-sibling::*[1][self::dd]/text()"))
  r["link"]=url
  r["doc"] = Time.now
  
  puts r.inspect
  ScraperWiki.save_sqlite(unique_keys=['company_number'],r,table_name='swdata',verbose=2) unless r['company_name'].nil? or r['company_name'].empty? 
  return (r['company_name'].nil? or r['company_name'].empty?)? nil : 0
end

def action(srch)
  begin
    s_url = BASE_URL + "/egovPoolPortal_WAR/appmanager/ADeGP/Business?_nfpb=true&_windowLabel=T4801647921215097862967&T4801647921215097862967_actionOverride=%2Fae%2Fabudhabi%2Fportal%2Fportlet%2Fdepartment%2Fadcci%2FcommercialDirectory%2FshowDetails&T4801647921215097862967legalFormId=0&T4801647921215097862967searchExpression=____&T4801647921215097862967companyId=#{srch}&T4801647921215097862967cityId=0&T4801647921215097862967source=searchCompanies&T4801647921215097862967companyTypeId=0&T4801647921215097862967activityId=&_pageLabel=P2800547921215097790384&lang=en"
    pg = @br.get(s_url)
    resp = scrape(srch,pg.body,s_url)  
  end
end

strt = ScraperWiki.select("max(company_number) as cnt from swdata")[0]['cnt']
(strt..(strt+2000)).each{|srch|
  action(srch)
}

#puts scrape(nil,@br.get("https://business.abudhabi.ae/egovPoolPortal_WAR/appmanager/ADeGP/Business?_nfpb=true&_windowLabel=T4801647921215097862967&T4801647921215097862967_actionOverride=%2Fae%2Fabudhabi%2Fportal%2Fportlet%2Fdepartment%2Fadcci%2FcommercialDirectory%2FshowDetails&T4801647921215097862967legalFormId=0&T4801647921215097862967searchExpression=____&T4801647921215097862967companyId=214450&T4801647921215097862967cityId=0&T4801647921215097862967source=searchCompanies&T4801647921215097862967companyTypeId=0&T4801647921215097862967activityId=&_pageLabel=P2800547921215097790384&lang=en").body,"")# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'httpclient'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://business.abudhabi.ae"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
#@br = HTTPClient.new


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

def scrape(cn,data,url)
  doc = Nokogiri::HTML(data).xpath(".//div[@id='T4801647921215097862967']//div[@class='fragment introModul']")
  return nil if doc.length <= 0
  r = {
    "company_number"=>cn,
    "company_name"=>s_text(doc.xpath(".//h4[@class='subheadline']"))
  }

  doc = Nokogiri::HTML(data).xpath(".")
  r["company_type"] = s_text(doc.xpath(".//dt[normalize-space(text())='Company Type']/following-sibling::*[1][self::dd]/text()"))
  r["legal_form"]=s_text(doc.xpath(".//dt[normalize-space(text())='Legal Form']/following-sibling::*[1][self::dd]/text()"))
  r["established_dt"]=s_text(doc.xpath(".//dt[normalize-space(text())='Established']/following-sibling::*[1][self::dd]/text()"))
  r["expiry_dt"]=s_text(doc.xpath(".//dt[normalize-space(text())='Expiry Date']/following-sibling::*[1][self::dd]/text()"))
  r["address"]=s_text(doc.xpath(".//dt[normalize-space(text())='Address']/following-sibling::*[1][self::dd]/text()"))
  r["city"]=s_text(doc.xpath(".//dt[normalize-space(text())='City']/following-sibling::*[1][self::dd]/text()"))
  r["telephone"]=s_text(doc.xpath(".//dt[normalize-space(text())='Telephone']/following-sibling::*[1][self::dd]/text()"))
  r["fax"]=s_text(doc.xpath(".//dt[normalize-space(text())='Fax']/following-sibling::*[1][self::dd]/text()"))
  r["email"]=s_text(doc.xpath(".//dt[normalize-space(text())='Email']/following-sibling::*[1][self::dd]/a/text()"))
  r["website"]=s_text(doc.xpath(".//dt[normalize-space(text())='Website']/following-sibling::*[1][self::dd]/text()"))
  r["link"]=url
  r["doc"] = Time.now
  
  puts r.inspect
  ScraperWiki.save_sqlite(unique_keys=['company_number'],r,table_name='swdata',verbose=2) unless r['company_name'].nil? or r['company_name'].empty? 
  return (r['company_name'].nil? or r['company_name'].empty?)? nil : 0
end

def action(srch)
  begin
    s_url = BASE_URL + "/egovPoolPortal_WAR/appmanager/ADeGP/Business?_nfpb=true&_windowLabel=T4801647921215097862967&T4801647921215097862967_actionOverride=%2Fae%2Fabudhabi%2Fportal%2Fportlet%2Fdepartment%2Fadcci%2FcommercialDirectory%2FshowDetails&T4801647921215097862967legalFormId=0&T4801647921215097862967searchExpression=____&T4801647921215097862967companyId=#{srch}&T4801647921215097862967cityId=0&T4801647921215097862967source=searchCompanies&T4801647921215097862967companyTypeId=0&T4801647921215097862967activityId=&_pageLabel=P2800547921215097790384&lang=en"
    pg = @br.get(s_url)
    resp = scrape(srch,pg.body,s_url)  
  end
end

strt = ScraperWiki.select("max(company_number) as cnt from swdata")[0]['cnt']
(strt..(strt+2000)).each{|srch|
  action(srch)
}

#puts scrape(nil,@br.get("https://business.abudhabi.ae/egovPoolPortal_WAR/appmanager/ADeGP/Business?_nfpb=true&_windowLabel=T4801647921215097862967&T4801647921215097862967_actionOverride=%2Fae%2Fabudhabi%2Fportal%2Fportlet%2Fdepartment%2Fadcci%2FcommercialDirectory%2FshowDetails&T4801647921215097862967legalFormId=0&T4801647921215097862967searchExpression=____&T4801647921215097862967companyId=214450&T4801647921215097862967cityId=0&T4801647921215097862967source=searchCompanies&T4801647921215097862967companyTypeId=0&T4801647921215097862967activityId=&_pageLabel=P2800547921215097790384&lang=en").body,"")