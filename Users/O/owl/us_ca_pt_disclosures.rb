# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.ptsearch.ss.ca.gov"
  
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

def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='details']/tbody/tr[position()>1]/td[1]/a").each{|a|
      tmp = append_base(BASE_URL,attributes(a.xpath("."),"href"))
      records << {"link"=>tmp} unless tmp =~ /help/
    }
    return records
  elsif act == "details"
    r = {}
    doc = Nokogiri::HTML(data).xpath(".")
    
    #CORPORATION
    r["company_name"] = s_text(doc.xpath(".//td[normalize-space(text())='Corporation Name:']/following-sibling::*[1][self::td]/text()"))
    r["company_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Corporation Number:']/following-sibling::*[1][self::td]/text()"))
    r["document_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Document Number:']/following-sibling::*[1][self::td]/text()"))
    r["filing_dt"] = s_text(doc.xpath(".//td[normalize-space(text())='Disclosure Filing Date:']/following-sibling::*[1][self::td]/text()"))
    r["bankruptcy"] = s_text(doc.xpath(".//td[normalize-space(text())='Bankruptcy:']/following-sibling::*[1][self::td]/text()"))
    r["legal_proceedings"] = a_text(doc.xpath(".//td[normalize-space(text())='Legal Proceedings:']/following-sibling::*[1][self::td]/text()")).join("\n").pretty
    
    #INDEPENDENT AUDITOR
    tmp = {}
    doc.xpath(".//table[@class='details' and tbody/tr[1]/td[normalize-space(text())='INDEPENDENT AUDITOR']]/tbody/tr[position()>1]").each{|tr|
      tmp[s_text(tr.xpath("./td[1]/text()"))] = s_text(tr.xpath("./td[2]/text()"))
    }
    r["independent_auditor"] = JSON.generate tmp unless tmp.empty? 

    #DIRECTORS AND EXECUTIVE OFFICERS
    tmp = []
    doc.xpath(".//table[@class='details' and tbody/tr[1]/td[normalize-space(text())='DIRECTORS AND EXECUTIVE OFFICERS']]/tbody/tr[position()>2]").each{|tr|
      tmp << {
        "name" => s_text(tr.xpath("./td[1]/text()")),
        "title" => s_text(tr.xpath("./td[2]/text()")),
        "compensation" => s_text(tr.xpath("./td[3]/text()")),
        "shares" => s_text(tr.xpath("./td[4]/text()")),
        "options" => s_text(tr.xpath("./td[5]/text()")),
        "bankruptcy" => s_text(tr.xpath("./td[5]/text()")),
        "fraud" => s_text(tr.xpath("./td[6]/text()")),
      }
    }
    r["people"] = JSON.generate tmp unless tmp.empty? 

    return r.merge(rec)
  end
end

def action()
  pg = @br.get("http://www.ptsearch.ss.ca.gov/app/advanced_search_results.html")
  pg.form_with(:name=>"form1") do |f|
    pg = f.submit
  end
  pg_no = get_metadata("page_no",1)
  begin
    list = scrape(pg.body,"list",{})
    puts ["list",list.length,list].inspect
    list.each{|rec|
      pg_tmp = @br.get(rec["link"]) rescue nil
      next if pg_tmp.nil? 
      record = scrape(pg_tmp.body,"details",rec)
      ScraperWiki.save_sqlite(unique_keys=['company_number','document_number'],record)
    }
    break if list.empty? or list.length < 15

    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)

    pg = @br.post(BASE_URL+"/app/advanced_search_results.html",{"goToPageNumber"=>"#{pg_no}","nextPage"=>"Next%A0%3E%3E"})
  end while(true)
end

action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.ptsearch.ss.ca.gov"
  
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

def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='details']/tbody/tr[position()>1]/td[1]/a").each{|a|
      tmp = append_base(BASE_URL,attributes(a.xpath("."),"href"))
      records << {"link"=>tmp} unless tmp =~ /help/
    }
    return records
  elsif act == "details"
    r = {}
    doc = Nokogiri::HTML(data).xpath(".")
    
    #CORPORATION
    r["company_name"] = s_text(doc.xpath(".//td[normalize-space(text())='Corporation Name:']/following-sibling::*[1][self::td]/text()"))
    r["company_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Corporation Number:']/following-sibling::*[1][self::td]/text()"))
    r["document_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Document Number:']/following-sibling::*[1][self::td]/text()"))
    r["filing_dt"] = s_text(doc.xpath(".//td[normalize-space(text())='Disclosure Filing Date:']/following-sibling::*[1][self::td]/text()"))
    r["bankruptcy"] = s_text(doc.xpath(".//td[normalize-space(text())='Bankruptcy:']/following-sibling::*[1][self::td]/text()"))
    r["legal_proceedings"] = a_text(doc.xpath(".//td[normalize-space(text())='Legal Proceedings:']/following-sibling::*[1][self::td]/text()")).join("\n").pretty
    
    #INDEPENDENT AUDITOR
    tmp = {}
    doc.xpath(".//table[@class='details' and tbody/tr[1]/td[normalize-space(text())='INDEPENDENT AUDITOR']]/tbody/tr[position()>1]").each{|tr|
      tmp[s_text(tr.xpath("./td[1]/text()"))] = s_text(tr.xpath("./td[2]/text()"))
    }
    r["independent_auditor"] = JSON.generate tmp unless tmp.empty? 

    #DIRECTORS AND EXECUTIVE OFFICERS
    tmp = []
    doc.xpath(".//table[@class='details' and tbody/tr[1]/td[normalize-space(text())='DIRECTORS AND EXECUTIVE OFFICERS']]/tbody/tr[position()>2]").each{|tr|
      tmp << {
        "name" => s_text(tr.xpath("./td[1]/text()")),
        "title" => s_text(tr.xpath("./td[2]/text()")),
        "compensation" => s_text(tr.xpath("./td[3]/text()")),
        "shares" => s_text(tr.xpath("./td[4]/text()")),
        "options" => s_text(tr.xpath("./td[5]/text()")),
        "bankruptcy" => s_text(tr.xpath("./td[5]/text()")),
        "fraud" => s_text(tr.xpath("./td[6]/text()")),
      }
    }
    r["people"] = JSON.generate tmp unless tmp.empty? 

    return r.merge(rec)
  end
end

def action()
  pg = @br.get("http://www.ptsearch.ss.ca.gov/app/advanced_search_results.html")
  pg.form_with(:name=>"form1") do |f|
    pg = f.submit
  end
  pg_no = get_metadata("page_no",1)
  begin
    list = scrape(pg.body,"list",{})
    puts ["list",list.length,list].inspect
    list.each{|rec|
      pg_tmp = @br.get(rec["link"]) rescue nil
      next if pg_tmp.nil? 
      record = scrape(pg_tmp.body,"details",rec)
      ScraperWiki.save_sqlite(unique_keys=['company_number','document_number'],record)
    }
    break if list.empty? or list.length < 15

    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)

    pg = @br.post(BASE_URL+"/app/advanced_search_results.html",{"goToPageNumber"=>"#{pg_no}","nextPage"=>"Next%A0%3E%3E"})
  end while(true)
end

action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.ptsearch.ss.ca.gov"
  
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

def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='details']/tbody/tr[position()>1]/td[1]/a").each{|a|
      tmp = append_base(BASE_URL,attributes(a.xpath("."),"href"))
      records << {"link"=>tmp} unless tmp =~ /help/
    }
    return records
  elsif act == "details"
    r = {}
    doc = Nokogiri::HTML(data).xpath(".")
    
    #CORPORATION
    r["company_name"] = s_text(doc.xpath(".//td[normalize-space(text())='Corporation Name:']/following-sibling::*[1][self::td]/text()"))
    r["company_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Corporation Number:']/following-sibling::*[1][self::td]/text()"))
    r["document_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Document Number:']/following-sibling::*[1][self::td]/text()"))
    r["filing_dt"] = s_text(doc.xpath(".//td[normalize-space(text())='Disclosure Filing Date:']/following-sibling::*[1][self::td]/text()"))
    r["bankruptcy"] = s_text(doc.xpath(".//td[normalize-space(text())='Bankruptcy:']/following-sibling::*[1][self::td]/text()"))
    r["legal_proceedings"] = a_text(doc.xpath(".//td[normalize-space(text())='Legal Proceedings:']/following-sibling::*[1][self::td]/text()")).join("\n").pretty
    
    #INDEPENDENT AUDITOR
    tmp = {}
    doc.xpath(".//table[@class='details' and tbody/tr[1]/td[normalize-space(text())='INDEPENDENT AUDITOR']]/tbody/tr[position()>1]").each{|tr|
      tmp[s_text(tr.xpath("./td[1]/text()"))] = s_text(tr.xpath("./td[2]/text()"))
    }
    r["independent_auditor"] = JSON.generate tmp unless tmp.empty? 

    #DIRECTORS AND EXECUTIVE OFFICERS
    tmp = []
    doc.xpath(".//table[@class='details' and tbody/tr[1]/td[normalize-space(text())='DIRECTORS AND EXECUTIVE OFFICERS']]/tbody/tr[position()>2]").each{|tr|
      tmp << {
        "name" => s_text(tr.xpath("./td[1]/text()")),
        "title" => s_text(tr.xpath("./td[2]/text()")),
        "compensation" => s_text(tr.xpath("./td[3]/text()")),
        "shares" => s_text(tr.xpath("./td[4]/text()")),
        "options" => s_text(tr.xpath("./td[5]/text()")),
        "bankruptcy" => s_text(tr.xpath("./td[5]/text()")),
        "fraud" => s_text(tr.xpath("./td[6]/text()")),
      }
    }
    r["people"] = JSON.generate tmp unless tmp.empty? 

    return r.merge(rec)
  end
end

def action()
  pg = @br.get("http://www.ptsearch.ss.ca.gov/app/advanced_search_results.html")
  pg.form_with(:name=>"form1") do |f|
    pg = f.submit
  end
  pg_no = get_metadata("page_no",1)
  begin
    list = scrape(pg.body,"list",{})
    puts ["list",list.length,list].inspect
    list.each{|rec|
      pg_tmp = @br.get(rec["link"]) rescue nil
      next if pg_tmp.nil? 
      record = scrape(pg_tmp.body,"details",rec)
      ScraperWiki.save_sqlite(unique_keys=['company_number','document_number'],record)
    }
    break if list.empty? or list.length < 15

    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)

    pg = @br.post(BASE_URL+"/app/advanced_search_results.html",{"goToPageNumber"=>"#{pg_no}","nextPage"=>"Next%A0%3E%3E"})
  end while(true)
end

action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.ptsearch.ss.ca.gov"
  
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

def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='details']/tbody/tr[position()>1]/td[1]/a").each{|a|
      tmp = append_base(BASE_URL,attributes(a.xpath("."),"href"))
      records << {"link"=>tmp} unless tmp =~ /help/
    }
    return records
  elsif act == "details"
    r = {}
    doc = Nokogiri::HTML(data).xpath(".")
    
    #CORPORATION
    r["company_name"] = s_text(doc.xpath(".//td[normalize-space(text())='Corporation Name:']/following-sibling::*[1][self::td]/text()"))
    r["company_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Corporation Number:']/following-sibling::*[1][self::td]/text()"))
    r["document_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Document Number:']/following-sibling::*[1][self::td]/text()"))
    r["filing_dt"] = s_text(doc.xpath(".//td[normalize-space(text())='Disclosure Filing Date:']/following-sibling::*[1][self::td]/text()"))
    r["bankruptcy"] = s_text(doc.xpath(".//td[normalize-space(text())='Bankruptcy:']/following-sibling::*[1][self::td]/text()"))
    r["legal_proceedings"] = a_text(doc.xpath(".//td[normalize-space(text())='Legal Proceedings:']/following-sibling::*[1][self::td]/text()")).join("\n").pretty
    
    #INDEPENDENT AUDITOR
    tmp = {}
    doc.xpath(".//table[@class='details' and tbody/tr[1]/td[normalize-space(text())='INDEPENDENT AUDITOR']]/tbody/tr[position()>1]").each{|tr|
      tmp[s_text(tr.xpath("./td[1]/text()"))] = s_text(tr.xpath("./td[2]/text()"))
    }
    r["independent_auditor"] = JSON.generate tmp unless tmp.empty? 

    #DIRECTORS AND EXECUTIVE OFFICERS
    tmp = []
    doc.xpath(".//table[@class='details' and tbody/tr[1]/td[normalize-space(text())='DIRECTORS AND EXECUTIVE OFFICERS']]/tbody/tr[position()>2]").each{|tr|
      tmp << {
        "name" => s_text(tr.xpath("./td[1]/text()")),
        "title" => s_text(tr.xpath("./td[2]/text()")),
        "compensation" => s_text(tr.xpath("./td[3]/text()")),
        "shares" => s_text(tr.xpath("./td[4]/text()")),
        "options" => s_text(tr.xpath("./td[5]/text()")),
        "bankruptcy" => s_text(tr.xpath("./td[5]/text()")),
        "fraud" => s_text(tr.xpath("./td[6]/text()")),
      }
    }
    r["people"] = JSON.generate tmp unless tmp.empty? 

    return r.merge(rec)
  end
end

def action()
  pg = @br.get("http://www.ptsearch.ss.ca.gov/app/advanced_search_results.html")
  pg.form_with(:name=>"form1") do |f|
    pg = f.submit
  end
  pg_no = get_metadata("page_no",1)
  begin
    list = scrape(pg.body,"list",{})
    puts ["list",list.length,list].inspect
    list.each{|rec|
      pg_tmp = @br.get(rec["link"]) rescue nil
      next if pg_tmp.nil? 
      record = scrape(pg_tmp.body,"details",rec)
      ScraperWiki.save_sqlite(unique_keys=['company_number','document_number'],record)
    }
    break if list.empty? or list.length < 15

    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)

    pg = @br.post(BASE_URL+"/app/advanced_search_results.html",{"goToPageNumber"=>"#{pg_no}","nextPage"=>"Next%A0%3E%3E"})
  end while(true)
end

action()
