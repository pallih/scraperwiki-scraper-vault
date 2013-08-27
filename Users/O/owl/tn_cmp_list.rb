# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.registre-commerce.tn"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
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
  def pretty
    self.collect{|a|a.strip}
  end
end


def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//td/table[@class='tbl-measurement']/tr[position()>1]").each{|tr|
      records << {
        "column1" => s_text(tr.xpath("./td[1]/text()")),
        "column2" => s_text(tr.xpath("./td[3]/text()")),
        "column3" => s_text(tr.xpath("./td[5]/text()")),
        "column4" => s_text(tr.xpath("./td[7]/text()")),
        "column5" => attributes(tr.xpath("./td[9]/a"),"href")
      }.merge(rec) 
    }
    return records
  elsif act == "det"
    return s_text(Nokogiri::HTML(data).xpath(".//td[@width='949']/table[@class='tbl-measurement']/tr[1]/td[3]/text()"))
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    r = {}
    r["company_number"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Numéro du registre')]/following-sibling::*[2][self::td]/text()"))
    r["status_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Etat du registre')]/following-sibling::*[2][self::td]/text()"))
    r["status_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'الوضع القانوني')]/preceding-sibling::*[2][self::td]/text()"))
    r["legal_form_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Forme juridique')]/following-sibling::*[2][self::td]/text()"))
    r["legal_form_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'حالة السجل التجاري')]/preceding-sibling::*[2][self::td]/text()"))
    r["company_name_1_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Dénomination sociale')]/following-sibling::*[2][self::td]/text()"))
    r["company_name_1_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'إسم الشركة الجماعي')]/preceding-sibling::*[2][self::td]/text()"))
    r["company_name_2_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Nom Commercial')]/following-sibling::*[2][self::td]/text()"))
    r["company_name_2_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'الإسم التجاري للشركة')]/preceding-sibling::*[2][self::td]/text()"))
    r["address_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Adresse du Siège')]/following-sibling::*[2][self::td]/text()"))
    r["address_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'المقر الإجتماعي')]/preceding-sibling::*[2][self::td]/text()"))
    
    return r.merge(rec)
  end
end

def action()
  @br.get(BASE_URL + "/search/RCCSearch.do?action=getPage&rg_type=PM&search_mode=NORMAL")
  pg = @br.post(BASE_URL + "/search/RCCSearch.do?action=search",{'registreType'=>'PM', 'searchMode'=>'NORMAL', 'searchRegistrePmRcc.numRegistre'=>'', 'searchRegistrePmRcc.registrePm.numPatente'=>'', 'searchRegistrePmRcc.nomSocieteFr'=>'_', 'searchRegistrePmRcc.registrePm.nomSociete'=>'', 'searchRegistrePmRcc.nomCommercialFr'=>'', 'searchRegistrePmRcc.registrePm.nomCommercial'=>''})
  pg_no = get_metadata("page_no",1)
  begin
    pg = @br.get("http://www.registre-commerce.tn/search/RCCSearch.do?action=search&page=#{pg_no}")
    list = scrape(pg,"list",{})
    list.each_with_index{|rec,idx|
      pg_tmp = @br.get("http://www.registre-commerce.tn/search/RCCSearch.do?action=chooseDocuments&numRegistreIndex=#{idx}") 
      cid = scrape(pg_tmp,"det",{"doc"=>Time.now})
      raise "Invalid company number for index #{pg_no} <-> #{idx} <-> #{cid}" if cid.nil? or cid.empty? 
      next if cid.nil? or cid.empty? 
      r = scrape(pg_tmp,"details",{"doc"=>Time.now})
      ScraperWiki.save_sqlite(['company_number'],r)
    }
    break if list.length == 0
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
  end while(true)
  delete_metadata("page_no")
end

action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.registre-commerce.tn"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
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
  def pretty
    self.collect{|a|a.strip}
  end
end


def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//td/table[@class='tbl-measurement']/tr[position()>1]").each{|tr|
      records << {
        "column1" => s_text(tr.xpath("./td[1]/text()")),
        "column2" => s_text(tr.xpath("./td[3]/text()")),
        "column3" => s_text(tr.xpath("./td[5]/text()")),
        "column4" => s_text(tr.xpath("./td[7]/text()")),
        "column5" => attributes(tr.xpath("./td[9]/a"),"href")
      }.merge(rec) 
    }
    return records
  elsif act == "det"
    return s_text(Nokogiri::HTML(data).xpath(".//td[@width='949']/table[@class='tbl-measurement']/tr[1]/td[3]/text()"))
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    r = {}
    r["company_number"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Numéro du registre')]/following-sibling::*[2][self::td]/text()"))
    r["status_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Etat du registre')]/following-sibling::*[2][self::td]/text()"))
    r["status_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'الوضع القانوني')]/preceding-sibling::*[2][self::td]/text()"))
    r["legal_form_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Forme juridique')]/following-sibling::*[2][self::td]/text()"))
    r["legal_form_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'حالة السجل التجاري')]/preceding-sibling::*[2][self::td]/text()"))
    r["company_name_1_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Dénomination sociale')]/following-sibling::*[2][self::td]/text()"))
    r["company_name_1_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'إسم الشركة الجماعي')]/preceding-sibling::*[2][self::td]/text()"))
    r["company_name_2_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Nom Commercial')]/following-sibling::*[2][self::td]/text()"))
    r["company_name_2_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'الإسم التجاري للشركة')]/preceding-sibling::*[2][self::td]/text()"))
    r["address_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Adresse du Siège')]/following-sibling::*[2][self::td]/text()"))
    r["address_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'المقر الإجتماعي')]/preceding-sibling::*[2][self::td]/text()"))
    
    return r.merge(rec)
  end
end

def action()
  @br.get(BASE_URL + "/search/RCCSearch.do?action=getPage&rg_type=PM&search_mode=NORMAL")
  pg = @br.post(BASE_URL + "/search/RCCSearch.do?action=search",{'registreType'=>'PM', 'searchMode'=>'NORMAL', 'searchRegistrePmRcc.numRegistre'=>'', 'searchRegistrePmRcc.registrePm.numPatente'=>'', 'searchRegistrePmRcc.nomSocieteFr'=>'_', 'searchRegistrePmRcc.registrePm.nomSociete'=>'', 'searchRegistrePmRcc.nomCommercialFr'=>'', 'searchRegistrePmRcc.registrePm.nomCommercial'=>''})
  pg_no = get_metadata("page_no",1)
  begin
    pg = @br.get("http://www.registre-commerce.tn/search/RCCSearch.do?action=search&page=#{pg_no}")
    list = scrape(pg,"list",{})
    list.each_with_index{|rec,idx|
      pg_tmp = @br.get("http://www.registre-commerce.tn/search/RCCSearch.do?action=chooseDocuments&numRegistreIndex=#{idx}") 
      cid = scrape(pg_tmp,"det",{"doc"=>Time.now})
      raise "Invalid company number for index #{pg_no} <-> #{idx} <-> #{cid}" if cid.nil? or cid.empty? 
      next if cid.nil? or cid.empty? 
      r = scrape(pg_tmp,"details",{"doc"=>Time.now})
      ScraperWiki.save_sqlite(['company_number'],r)
    }
    break if list.length == 0
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
  end while(true)
  delete_metadata("page_no")
end

action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.registre-commerce.tn"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
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
  def pretty
    self.collect{|a|a.strip}
  end
end


def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//td/table[@class='tbl-measurement']/tr[position()>1]").each{|tr|
      records << {
        "column1" => s_text(tr.xpath("./td[1]/text()")),
        "column2" => s_text(tr.xpath("./td[3]/text()")),
        "column3" => s_text(tr.xpath("./td[5]/text()")),
        "column4" => s_text(tr.xpath("./td[7]/text()")),
        "column5" => attributes(tr.xpath("./td[9]/a"),"href")
      }.merge(rec) 
    }
    return records
  elsif act == "det"
    return s_text(Nokogiri::HTML(data).xpath(".//td[@width='949']/table[@class='tbl-measurement']/tr[1]/td[3]/text()"))
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    r = {}
    r["company_number"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Numéro du registre')]/following-sibling::*[2][self::td]/text()"))
    r["status_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Etat du registre')]/following-sibling::*[2][self::td]/text()"))
    r["status_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'الوضع القانوني')]/preceding-sibling::*[2][self::td]/text()"))
    r["legal_form_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Forme juridique')]/following-sibling::*[2][self::td]/text()"))
    r["legal_form_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'حالة السجل التجاري')]/preceding-sibling::*[2][self::td]/text()"))
    r["company_name_1_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Dénomination sociale')]/following-sibling::*[2][self::td]/text()"))
    r["company_name_1_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'إسم الشركة الجماعي')]/preceding-sibling::*[2][self::td]/text()"))
    r["company_name_2_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Nom Commercial')]/following-sibling::*[2][self::td]/text()"))
    r["company_name_2_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'الإسم التجاري للشركة')]/preceding-sibling::*[2][self::td]/text()"))
    r["address_fr"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'Adresse du Siège')]/following-sibling::*[2][self::td]/text()"))
    r["address_ar"] = s_text(doc.xpath(".//td[@class='title-tbl-t' and contains(text(),'المقر الإجتماعي')]/preceding-sibling::*[2][self::td]/text()"))
    
    return r.merge(rec)
  end
end

def action()
  @br.get(BASE_URL + "/search/RCCSearch.do?action=getPage&rg_type=PM&search_mode=NORMAL")
  pg = @br.post(BASE_URL + "/search/RCCSearch.do?action=search",{'registreType'=>'PM', 'searchMode'=>'NORMAL', 'searchRegistrePmRcc.numRegistre'=>'', 'searchRegistrePmRcc.registrePm.numPatente'=>'', 'searchRegistrePmRcc.nomSocieteFr'=>'_', 'searchRegistrePmRcc.registrePm.nomSociete'=>'', 'searchRegistrePmRcc.nomCommercialFr'=>'', 'searchRegistrePmRcc.registrePm.nomCommercial'=>''})
  pg_no = get_metadata("page_no",1)
  begin
    pg = @br.get("http://www.registre-commerce.tn/search/RCCSearch.do?action=search&page=#{pg_no}")
    list = scrape(pg,"list",{})
    list.each_with_index{|rec,idx|
      pg_tmp = @br.get("http://www.registre-commerce.tn/search/RCCSearch.do?action=chooseDocuments&numRegistreIndex=#{idx}") 
      cid = scrape(pg_tmp,"det",{"doc"=>Time.now})
      raise "Invalid company number for index #{pg_no} <-> #{idx} <-> #{cid}" if cid.nil? or cid.empty? 
      next if cid.nil? or cid.empty? 
      r = scrape(pg_tmp,"details",{"doc"=>Time.now})
      ScraperWiki.save_sqlite(['company_number'],r)
    }
    break if list.length == 0
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
  end while(true)
  delete_metadata("page_no")
end

action()
