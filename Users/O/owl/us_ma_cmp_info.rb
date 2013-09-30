# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://corp.sec.state.ma.us/corp/corpsearch/"

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

def scrape(data)
  records = []
  Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//table[@width='100%' and @border='1' and not(@bordercolor) and @cellpadding='4']/tr[position()>1]").each{|tr|
    td=tr.xpath("td")
    r={
      'COMPANY_NAME'=> s_text(td[0].xpath("font/a/text()")),
      'COMPANY_NUMBER'=> s_text(td[1].xpath("font/text()")),
      'ADDR'=> s_text(td[3].xpath("font/text()")),
      'URL'=>BASE_URL+attributes(td[0].xpath("font/a"),"href"),
      'DOC'=>Time.now
    }
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length==0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    pg = br.get(BASE_URL+"CorpSearchInput.asp")
    params = {'SearchType'=>'E', 'EntityName'=>srch, 'EntitySearchMethod'=>'B', 'IndividualSearchMethod'=>'B', 'lstDisplay'=>'5000', 'FormCode'=>'0000160', 'FilingMethod'=>'I', 'ReadFromDB'=>'False', 'Refreshed'=>'True'}
    pginfo = eval(get_metadata("PGINFO",""))
    params['iPageNum'],params['TotalPageCount'],params['TotalRecords'] = pginfo unless pginfo.nil? or pginfo.empty? 
    begin
      f = pg.forms[0]
      begin
        params.each{|k,v| f[k] = v }
        f.action="CorpSearchEntityList.asp?ReadFromDB=True&UpdateAllowed=" unless f.action=~ /entitylist/i
        pg = f.submit
      end unless f.nil? 
      scrape(pg.body)
      break if pg.body =~ /No Records Matched/
      nex = pg.at("input[@name='cmdNext']")
      if nex.nil? 
        break
      else
        val = nex.attr('onclick').to_s
        if val.nil? or val.empty? 
          break
        else
          params['iPageNum'],params['TotalPageCount'],params['TotalRecords'] = val.scan(/fGoto_Page\((.*),(.*),(.*)\)/)[0]
          save_metadata("PGINFO",val.scan(/fGoto_Page\((.*),(.*),(.*)\)/)[0].to_s)
        end
      end
      sleep(2)
    end while(true)
    delete_metadata("PGINFO")
  end
end

#action("GOOG")
#exit
range =  (0..9).to_a + ('A'..'Z').sort.to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next  if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)
      sleep(2)
end

# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://corp.sec.state.ma.us/corp/corpsearch/"

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

def scrape(data)
  records = []
  Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//table[@width='100%' and @border='1' and not(@bordercolor) and @cellpadding='4']/tr[position()>1]").each{|tr|
    td=tr.xpath("td")
    r={
      'COMPANY_NAME'=> s_text(td[0].xpath("font/a/text()")),
      'COMPANY_NUMBER'=> s_text(td[1].xpath("font/text()")),
      'ADDR'=> s_text(td[3].xpath("font/text()")),
      'URL'=>BASE_URL+attributes(td[0].xpath("font/a"),"href"),
      'DOC'=>Time.now
    }
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length==0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    pg = br.get(BASE_URL+"CorpSearchInput.asp")
    params = {'SearchType'=>'E', 'EntityName'=>srch, 'EntitySearchMethod'=>'B', 'IndividualSearchMethod'=>'B', 'lstDisplay'=>'5000', 'FormCode'=>'0000160', 'FilingMethod'=>'I', 'ReadFromDB'=>'False', 'Refreshed'=>'True'}
    pginfo = eval(get_metadata("PGINFO",""))
    params['iPageNum'],params['TotalPageCount'],params['TotalRecords'] = pginfo unless pginfo.nil? or pginfo.empty? 
    begin
      f = pg.forms[0]
      begin
        params.each{|k,v| f[k] = v }
        f.action="CorpSearchEntityList.asp?ReadFromDB=True&UpdateAllowed=" unless f.action=~ /entitylist/i
        pg = f.submit
      end unless f.nil? 
      scrape(pg.body)
      break if pg.body =~ /No Records Matched/
      nex = pg.at("input[@name='cmdNext']")
      if nex.nil? 
        break
      else
        val = nex.attr('onclick').to_s
        if val.nil? or val.empty? 
          break
        else
          params['iPageNum'],params['TotalPageCount'],params['TotalRecords'] = val.scan(/fGoto_Page\((.*),(.*),(.*)\)/)[0]
          save_metadata("PGINFO",val.scan(/fGoto_Page\((.*),(.*),(.*)\)/)[0].to_s)
        end
      end
      sleep(2)
    end while(true)
    delete_metadata("PGINFO")
  end
end

#action("GOOG")
#exit
range =  (0..9).to_a + ('A'..'Z').sort.to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next  if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)
      sleep(2)
end

# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://corp.sec.state.ma.us"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
PER_PAGE=100

class String
  def pretty
    self.strip
  end
end


class Array
  def strip
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  records = []
  doc = Nokogiri::HTML(data)
  doc.xpath(".//table[@id='MainContent_SearchControl_grdSearchResultsEntity']/tr[@class='GridRow' or @class='GridAltRow']").each{|tr|
    r = {}
    r["company_name"] = s_text(tr.xpath("./td[1]/a/text()"))
    r["company_number"] = s_text(tr.xpath("./td[2]/text()"))
    r["old_company_number"] = s_text(tr.xpath("./td[3]/text()"))
    r["address"] = a_text(tr.xpath("./td[4]")).join("\n").strip

    records << r.merge(rec)
  }
  tmp = attributes(doc.xpath(".//table[@id='MainContent_SearchControl_grdSearchResultsEntity']/tr[@class='link']/td/table/tr/td[span]/following-sibling::*[1][self::td]/a"),"href").split("'")[3]
  return records,tmp
end

def init()
  @pg = @br.get(BASE_URL + "/CorpWeb/CorpSearch/CorpSearch.aspx")
  @pg.form_with(:id=>"Form1") do |f|
    f['__EVENTTARGET'] = "ctl00$MainContent$rdoByEntityName"
    @pg = f.submit
  end
end

def action()
  list =  (0..9).to_a + ('A'..'Z').sort.to_a
  lstart = get_metadata("list",0)
  list[lstart..-1].each_with_index{|srch,idx|
    params = JSON.parse(get_metadata("form",JSON.generate({'__EVENTTARGET'=>'ctl00$MainContent$ddRecordsPerPage', 'ctl00$MainContent$CorpSearch'=>'rdoByEntityName', 'ctl00$MainContent$txtEntityName'=>srch, 'ctl00$MainContent$ddRecordsPerPage'=>PER_PAGE})))
    begin
      init() if @pg.nil? 
      @pg.form_with(:id=>"Form1") do |f|
        params.each{|k,v| f[k] = v}
        @pg = f.submit
      end
      records,nex = scrape(@pg,"list",{"doc"=>Time.now})
      ScraperWiki.save_sqlite(['company_number'],records,'ocdata')
      break if records.nil? or records.length < PER_PAGE or nex.nil? or nex.empty? 
    
      params = {'__EVENTTARGET'=>'ctl00$MainContent$SearchControl$grdSearchResultsEntity', '__EVENTARGUMENT'=>nex, '__ASYNCPOST'=>'false'}

      
      #tmp_f = {}
      #@pg.form_with(:id=>"Form1").fields.each{|f|
      #  tmp_f[f.name] = f.value
      #}
      #save_metadata("form",JSON.generate(tmp_f))
    end while(true)
    @pg = nil
    delete_metadata("form")
    lstart = lstart + 1
    save_metadata("list",lstart)
  }
  delete_metadata("list")
end

action()
# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://corp.sec.state.ma.us"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
PER_PAGE=100

class String
  def pretty
    self.strip
  end
end


class Array
  def strip
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  records = []
  doc = Nokogiri::HTML(data)
  doc.xpath(".//table[@id='MainContent_SearchControl_grdSearchResultsEntity']/tr[@class='GridRow' or @class='GridAltRow']").each{|tr|
    r = {}
    r["company_name"] = s_text(tr.xpath("./td[1]/a/text()"))
    r["company_number"] = s_text(tr.xpath("./td[2]/text()"))
    r["old_company_number"] = s_text(tr.xpath("./td[3]/text()"))
    r["address"] = a_text(tr.xpath("./td[4]")).join("\n").strip

    records << r.merge(rec)
  }
  tmp = attributes(doc.xpath(".//table[@id='MainContent_SearchControl_grdSearchResultsEntity']/tr[@class='link']/td/table/tr/td[span]/following-sibling::*[1][self::td]/a"),"href").split("'")[3]
  return records,tmp
end

def init()
  @pg = @br.get(BASE_URL + "/CorpWeb/CorpSearch/CorpSearch.aspx")
  @pg.form_with(:id=>"Form1") do |f|
    f['__EVENTTARGET'] = "ctl00$MainContent$rdoByEntityName"
    @pg = f.submit
  end
end

def action()
  list =  (0..9).to_a + ('A'..'Z').sort.to_a
  lstart = get_metadata("list",0)
  list[lstart..-1].each_with_index{|srch,idx|
    params = JSON.parse(get_metadata("form",JSON.generate({'__EVENTTARGET'=>'ctl00$MainContent$ddRecordsPerPage', 'ctl00$MainContent$CorpSearch'=>'rdoByEntityName', 'ctl00$MainContent$txtEntityName'=>srch, 'ctl00$MainContent$ddRecordsPerPage'=>PER_PAGE})))
    begin
      init() if @pg.nil? 
      @pg.form_with(:id=>"Form1") do |f|
        params.each{|k,v| f[k] = v}
        @pg = f.submit
      end
      records,nex = scrape(@pg,"list",{"doc"=>Time.now})
      ScraperWiki.save_sqlite(['company_number'],records,'ocdata')
      break if records.nil? or records.length < PER_PAGE or nex.nil? or nex.empty? 
    
      params = {'__EVENTTARGET'=>'ctl00$MainContent$SearchControl$grdSearchResultsEntity', '__EVENTARGUMENT'=>nex, '__ASYNCPOST'=>'false'}

      
      #tmp_f = {}
      #@pg.form_with(:id=>"Form1").fields.each{|f|
      #  tmp_f[f.name] = f.value
      #}
      #save_metadata("form",JSON.generate(tmp_f))
    end while(true)
    @pg = nil
    delete_metadata("form")
    lstart = lstart + 1
    save_metadata("list",lstart)
  }
  delete_metadata("list")
end

action()
