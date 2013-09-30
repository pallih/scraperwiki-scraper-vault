# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://ucc.state.ri.us/CorpSearch/"
Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
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

def scrape(data,action)
  if action == "list"
    records = []
    begin
      Nokogiri::HTML(data,nil,'ISO-8859-1').xpath("//tr[@bgcolor='#C0C0C0']/following-sibling::tr[1]/td/table/tr[position()>1]").each{|tr| 
      td = tr.xpath("td")
      records << {
        "company_name" => s_text(td[0].xpath("./font/a/text()")),
        "link" => BASE_URL + attributes(td[0].xpath("./font/a"),"href"),
        "company_number" => s_text(td[1].xpath("./font/text()")),
        "charter" => s_text(td[2].xpath("./font/text()")),
        "status" => s_text(td[3].xpath("./font/text()")),
        "type" => s_text(td[4].xpath("./font/text()")),
        "doc" => Time.now
      }
    }
    end
    return records
  end
end

def action(srch)
  begin
    pg_num = 1#get_metadata("#{srch}_PG_NUM",1).to_i
    params = {
      "EntityName" => srch, 
      "SearchType" => "E", 
      "LastName" => "", 
      "FirstName" => "", 
      "MiddleName" => "", 
      "iPageNum" => pg_num, 
      "lstDisplay" => "5000", 
      "TotalPageCount" => "", 
      "TotalRecords" => "", 
      "SearchMethod" => "B", 
      "Purpose" => "", 
      "AgentName" => "", 
      "Address" => "", 
      "ActiveFlagCrit" => "Y", 
      "ActiveFlag" => ""
    }
    s_url = BASE_URL+"CorpSearchEntityList.asp?ReadFromDB=True&UpdateAllowed="
    pg = @br.post(s_url,params)
    begin
      records = scrape(pg.body,"list")
      ScraperWiki.save_sqlite(unique_keys=['company_number'],records)
      pg.form_with(:name => "frmCorpSearch") do |f|
        params.each{|k,v|
          f[k] = v
        }
        pg =  f.submit
      end
      pg_num = pg_num +1
      params["iPageNum"] = pg_num
      sleep(3)
    end while pg.at("input[@name='cmdNext']")
  end
end

@br.get(BASE_URL + "CorpSearchInput.asp")

delete_metadata("list")
list = ('A'..'ZZZ').to_a + (0..99).to_a
lstart = get_metadata("list",0)
list[lstart..-1].each{|srch|
  action(srch)
  lstart = lstart + 1
  save_metadata("list",lstart)
}
delete_metadata("list")
#ScraperWiki.sqliteexecute("drop table tmp")
#ScraperWiki.sqliteexecute("CREATE TABLE tmp (status text, charter text, doc timestamp, company_number text, link text, company_name text, type text)")
#ScraperWiki.sqliteexecute("insert into tmp select status, charter, datetime(strftime('%s',replace(doc,'+0000','')),'unixepoch'), company_number, link, company_name, type from swdata")
#ScraperWiki.commit()
#ScraperWiki.sqliteexecute("drop table swdata")
#ScraperWiki.sqliteexecute("alter table tmp rename to swdata")
# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://ucc.state.ri.us/CorpSearch/"
Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
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

def scrape(data,action)
  if action == "list"
    records = []
    begin
      Nokogiri::HTML(data,nil,'ISO-8859-1').xpath("//tr[@bgcolor='#C0C0C0']/following-sibling::tr[1]/td/table/tr[position()>1]").each{|tr| 
      td = tr.xpath("td")
      records << {
        "company_name" => s_text(td[0].xpath("./font/a/text()")),
        "link" => BASE_URL + attributes(td[0].xpath("./font/a"),"href"),
        "company_number" => s_text(td[1].xpath("./font/text()")),
        "charter" => s_text(td[2].xpath("./font/text()")),
        "status" => s_text(td[3].xpath("./font/text()")),
        "type" => s_text(td[4].xpath("./font/text()")),
        "doc" => Time.now
      }
    }
    end
    return records
  end
end

def action(srch)
  begin
    pg_num = 1#get_metadata("#{srch}_PG_NUM",1).to_i
    params = {
      "EntityName" => srch, 
      "SearchType" => "E", 
      "LastName" => "", 
      "FirstName" => "", 
      "MiddleName" => "", 
      "iPageNum" => pg_num, 
      "lstDisplay" => "5000", 
      "TotalPageCount" => "", 
      "TotalRecords" => "", 
      "SearchMethod" => "B", 
      "Purpose" => "", 
      "AgentName" => "", 
      "Address" => "", 
      "ActiveFlagCrit" => "Y", 
      "ActiveFlag" => ""
    }
    s_url = BASE_URL+"CorpSearchEntityList.asp?ReadFromDB=True&UpdateAllowed="
    pg = @br.post(s_url,params)
    begin
      records = scrape(pg.body,"list")
      ScraperWiki.save_sqlite(unique_keys=['company_number'],records)
      pg.form_with(:name => "frmCorpSearch") do |f|
        params.each{|k,v|
          f[k] = v
        }
        pg =  f.submit
      end
      pg_num = pg_num +1
      params["iPageNum"] = pg_num
      sleep(3)
    end while pg.at("input[@name='cmdNext']")
  end
end

@br.get(BASE_URL + "CorpSearchInput.asp")

delete_metadata("list")
list = ('A'..'ZZZ').to_a + (0..99).to_a
lstart = get_metadata("list",0)
list[lstart..-1].each{|srch|
  action(srch)
  lstart = lstart + 1
  save_metadata("list",lstart)
}
delete_metadata("list")
#ScraperWiki.sqliteexecute("drop table tmp")
#ScraperWiki.sqliteexecute("CREATE TABLE tmp (status text, charter text, doc timestamp, company_number text, link text, company_name text, type text)")
#ScraperWiki.sqliteexecute("insert into tmp select status, charter, datetime(strftime('%s',replace(doc,'+0000','')),'unixepoch'), company_number, link, company_name, type from swdata")
#ScraperWiki.commit()
#ScraperWiki.sqliteexecute("drop table swdata")
#ScraperWiki.sqliteexecute("alter table tmp rename to swdata")
# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://ucc.state.ri.us/CorpSearch/"
Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
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

def scrape(data,action)
  if action == "list"
    records = []
    begin
      Nokogiri::HTML(data,nil,'ISO-8859-1').xpath("//tr[@bgcolor='#C0C0C0']/following-sibling::tr[1]/td/table/tr[position()>1]").each{|tr| 
      td = tr.xpath("td")
      records << {
        "company_name" => s_text(td[0].xpath("./font/a/text()")),
        "link" => BASE_URL + attributes(td[0].xpath("./font/a"),"href"),
        "company_number" => s_text(td[1].xpath("./font/text()")),
        "charter" => s_text(td[2].xpath("./font/text()")),
        "status" => s_text(td[3].xpath("./font/text()")),
        "type" => s_text(td[4].xpath("./font/text()")),
        "doc" => Time.now
      }
    }
    end
    return records
  end
end

def action(srch)
  begin
    pg_num = 1#get_metadata("#{srch}_PG_NUM",1).to_i
    params = {
      "EntityName" => srch, 
      "SearchType" => "E", 
      "LastName" => "", 
      "FirstName" => "", 
      "MiddleName" => "", 
      "iPageNum" => pg_num, 
      "lstDisplay" => "5000", 
      "TotalPageCount" => "", 
      "TotalRecords" => "", 
      "SearchMethod" => "B", 
      "Purpose" => "", 
      "AgentName" => "", 
      "Address" => "", 
      "ActiveFlagCrit" => "Y", 
      "ActiveFlag" => ""
    }
    s_url = BASE_URL+"CorpSearchEntityList.asp?ReadFromDB=True&UpdateAllowed="
    pg = @br.post(s_url,params)
    begin
      records = scrape(pg.body,"list")
      ScraperWiki.save_sqlite(unique_keys=['company_number'],records)
      pg.form_with(:name => "frmCorpSearch") do |f|
        params.each{|k,v|
          f[k] = v
        }
        pg =  f.submit
      end
      pg_num = pg_num +1
      params["iPageNum"] = pg_num
      sleep(3)
    end while pg.at("input[@name='cmdNext']")
  end
end

@br.get(BASE_URL + "CorpSearchInput.asp")

delete_metadata("list")
list = ('A'..'ZZZ').to_a + (0..99).to_a
lstart = get_metadata("list",0)
list[lstart..-1].each{|srch|
  action(srch)
  lstart = lstart + 1
  save_metadata("list",lstart)
}
delete_metadata("list")
#ScraperWiki.sqliteexecute("drop table tmp")
#ScraperWiki.sqliteexecute("CREATE TABLE tmp (status text, charter text, doc timestamp, company_number text, link text, company_name text, type text)")
#ScraperWiki.sqliteexecute("insert into tmp select status, charter, datetime(strftime('%s',replace(doc,'+0000','')),'unixepoch'), company_number, link, company_name, type from swdata")
#ScraperWiki.commit()
#ScraperWiki.sqliteexecute("drop table swdata")
#ScraperWiki.sqliteexecute("alter table tmp rename to swdata")
# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://ucc.state.ri.us/CorpSearch/"
Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
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

def scrape(data,action)
  if action == "list"
    records = []
    begin
      Nokogiri::HTML(data,nil,'ISO-8859-1').xpath("//tr[@bgcolor='#C0C0C0']/following-sibling::tr[1]/td/table/tr[position()>1]").each{|tr| 
      td = tr.xpath("td")
      records << {
        "company_name" => s_text(td[0].xpath("./font/a/text()")),
        "link" => BASE_URL + attributes(td[0].xpath("./font/a"),"href"),
        "company_number" => s_text(td[1].xpath("./font/text()")),
        "charter" => s_text(td[2].xpath("./font/text()")),
        "status" => s_text(td[3].xpath("./font/text()")),
        "type" => s_text(td[4].xpath("./font/text()")),
        "doc" => Time.now
      }
    }
    end
    return records
  end
end

def action(srch)
  begin
    pg_num = 1#get_metadata("#{srch}_PG_NUM",1).to_i
    params = {
      "EntityName" => srch, 
      "SearchType" => "E", 
      "LastName" => "", 
      "FirstName" => "", 
      "MiddleName" => "", 
      "iPageNum" => pg_num, 
      "lstDisplay" => "5000", 
      "TotalPageCount" => "", 
      "TotalRecords" => "", 
      "SearchMethod" => "B", 
      "Purpose" => "", 
      "AgentName" => "", 
      "Address" => "", 
      "ActiveFlagCrit" => "Y", 
      "ActiveFlag" => ""
    }
    s_url = BASE_URL+"CorpSearchEntityList.asp?ReadFromDB=True&UpdateAllowed="
    pg = @br.post(s_url,params)
    begin
      records = scrape(pg.body,"list")
      ScraperWiki.save_sqlite(unique_keys=['company_number'],records)
      pg.form_with(:name => "frmCorpSearch") do |f|
        params.each{|k,v|
          f[k] = v
        }
        pg =  f.submit
      end
      pg_num = pg_num +1
      params["iPageNum"] = pg_num
      sleep(3)
    end while pg.at("input[@name='cmdNext']")
  end
end

@br.get(BASE_URL + "CorpSearchInput.asp")

delete_metadata("list")
list = ('A'..'ZZZ').to_a + (0..99).to_a
lstart = get_metadata("list",0)
list[lstart..-1].each{|srch|
  action(srch)
  lstart = lstart + 1
  save_metadata("list",lstart)
}
delete_metadata("list")
#ScraperWiki.sqliteexecute("drop table tmp")
#ScraperWiki.sqliteexecute("CREATE TABLE tmp (status text, charter text, doc timestamp, company_number text, link text, company_name text, type text)")
#ScraperWiki.sqliteexecute("insert into tmp select status, charter, datetime(strftime('%s',replace(doc,'+0000','')),'unixepoch'), company_number, link, company_name, type from swdata")
#ScraperWiki.commit()
#ScraperWiki.sqliteexecute("drop table swdata")
#ScraperWiki.sqliteexecute("alter table tmp rename to swdata")
