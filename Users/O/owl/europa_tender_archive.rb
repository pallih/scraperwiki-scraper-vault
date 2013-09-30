# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'cgi'
require 'date'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL ="http://ted.europa.eu"


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
    puts "ERROR: #{e.inspect} during save_metadata(#{key}) :: #{e.backtrace}"
   
  end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",key)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key}) :: #{e.backtrace}"
    retry
  end
end

def text(str)
  begin
    ret = ""
    str.each{|s|
      if str.inner_html.nil? or str.inner_html.empty? 
        ret = ret + s.text.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ") + ((s.text.strip.nil? or s.text.strip.empty?)? "" : "|")
      else
        ret = ret + s.inner_html.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ").gsub("<br>","|") + ((s.inner_html.strip.nil? or s.inner_html.strip.empty?)? "" : "|")
      end
    } unless str.nil? 
    return ret.chop
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end

def escape(str)
  return CGI.unescapeHTML(str).gsub(/"/,"&quot;")#.gsub(/"/,"\"")
end

def is_document(url)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where url=?",[url])[data][0][0]
end

def scrape(action,data,url)
  if action == "list"
    links = []
    Nokogiri::HTML(data).xpath(".//*[@id='notice']/tbody/tr").each{|tr|
      td = tr.xpath("td")
      links << BASE_URL + attributes(td[1].xpath("a"),"href")
    }
    return links
  elsif action == "details"
    records = {"DOC"=>Time.now.to_s,"url"=>url}
    Nokogiri::HTML(data).xpath("//table[@class='data']/tr").each{|tr|
      th = tr.xpath("th/text()")
      td = tr.xpath("td[not(div)]")
      records[text(th)] = text(td[1].xpath("text()")) unless td[1].nil? 
    }
    puts records.inspect if @debug
    ScraperWiki.save_sqlite(unique_keys=["ND"],records,table_name="swdata",verbose=0) unless records["ND"].nil? or records["ND"].empty? 
  end
end


def action(pub_dt)
  begin
    @pg = @br.get(BASE_URL + "/TED/search/search.do")
    params = {'action'=>'search', 'Rs.gp.2241457.pid'=>'home', 'lgId'=>'en', 'Rs.gp.2241458.pid'=>'releaseCalendar', 'quickSearchCriteria'=>'', 'searchCriteria.searchScopeId'=>'4', 'searchCriteria.ojs'=>'', 'searchCriteria.freeText'=>'', 'searchCriteria.countryList'=>'', 'searchCriteria.contractList'=>'', 'searchCriteria.documentTypeList'=>'', 'searchCriteria.cpvCodeList'=>'', 'searchCriteria.publicationDateChoice'=>'DEFINITE_PUBLICATION_DATE', 'searchCriteria.publicationDate'=>pub_dt, 'searchCriteria.documentationDate'=>'', 'searchCriteria.typeOfAuthorityList'=>'', 'searchCriteria.place'=>'', 'searchCriteria.procedureList'=>'', 'searchCriteria.regulationList'=>'', 'searchCriteria.nutsCodeList'=>'', 'searchCriteria.documentNumber'=>'', 'searchCriteria.deadline'=>'', 'searchCriteria.authorityName'=>'', 'searchCriteria.mainActivityList'=>'', '_searchCriteria.statisticsMode'=>'on'}
    @pg = @br.post(BASE_URL + "/TED/search/search.do",params)
    nex = get_metadata("offset",nil)
    @pg = @br.get(BASE_URL + "/TED/search/" + nex) unless (nex.nil? or nex.empty? or nex=~ /Next/) 
    scraped = false
    begin
      links = scrape("list",@pg.body,"")
      scraped = true if not (links.nil? or links.empty?)
      links.each{|tender_link|
        begin
          pg_tmp = @br.get(tender_link+"&tabId=3")
          scrape("details",pg_tmp.body,tender_link)
        rescue Exception => e
          puts "ERROR: While processing  #{tender_link} :: #{e.inspect} :: #{e.backtrace}"
          if e.inspect =~ /Timeout|ETIMEDOUT/
            sleep(10)
            retry
          end  
        end #unless is_document(tender_link)>0
      }
      ne = @pg.link_with(:text => "Next")
      break if ne.nil? 
      save_metadata("offset",(ne.nil?) ? "" : ne.href)
      @pg = @pg.link_with(:text => "Next").click unless ne.nil? 
      sleep(30)
    rescue Exception=> e
      puts "ERROR: While processing #{ne} :: #{e.inspect} :: #{e.backtrace}"
      if e.inspect =~ /Timeout|ETIMEDOUT/
        sleep(10)
        retry
      end
    end while not (ne.nil? or @pg.nil?)  or @pg.body =~ /Nothing found to display/
    save_metadata("offset_dt",Date.parse(pub_dt).next.strftime("%d-%m-%Y"))  #if scraped
  rescue Exception=> e
    puts "ERROR: While initializing search :: #{e.inspect} :: #{e.backtrace}"
    #if e.inspect =~ /Timeout|ETIMEDOUT/
      sleep(30)
      retry
    #end
  end
end
@debug = false
if @debug
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
  }
  url="http://ted.europa.eu/udl?uri=TED:NOTICE:261779-2011:DATA:EN:HTML&src=0&tabId=3"
  pg = br.get(url)
  scrape("details",pg.body,url)
end

begin
  @br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout=1200
  }
  @pg = @br.post("http://ted.europa.eu/TED/misc/chooseLanguage.do?lgId=en",{'action'=>'cl'})
rescue Exception=> e
  puts "ERROR: While initializing  :: #{e.inspect} :: #{e.backtrace}"
  if e.inspect =~ /Timeout|ETIMEDOUT/
    sleep(30)
    retry
  end
end unless @debug
#action("10-01-2009")
#save_metadata("offset_dt","01-01-2009")
#save_metadata("offset","searchResult.do?page=41")
strt = Date.parse(get_metadata("offset_dt","01-01-2009"))
endd = Date.parse(Time.now.strftime("%d-%m-%Y"))
(strt..endd).each{|pub_dt|
  action(pub_dt.strftime("%d-%m-%Y")) unless @debug
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'cgi'
require 'date'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL ="http://ted.europa.eu"


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
    puts "ERROR: #{e.inspect} during save_metadata(#{key}) :: #{e.backtrace}"
   
  end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",key)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key}) :: #{e.backtrace}"
    retry
  end
end

def text(str)
  begin
    ret = ""
    str.each{|s|
      if str.inner_html.nil? or str.inner_html.empty? 
        ret = ret + s.text.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ") + ((s.text.strip.nil? or s.text.strip.empty?)? "" : "|")
      else
        ret = ret + s.inner_html.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ").gsub("<br>","|") + ((s.inner_html.strip.nil? or s.inner_html.strip.empty?)? "" : "|")
      end
    } unless str.nil? 
    return ret.chop
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end

def escape(str)
  return CGI.unescapeHTML(str).gsub(/"/,"&quot;")#.gsub(/"/,"\"")
end

def is_document(url)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where url=?",[url])[data][0][0]
end

def scrape(action,data,url)
  if action == "list"
    links = []
    Nokogiri::HTML(data).xpath(".//*[@id='notice']/tbody/tr").each{|tr|
      td = tr.xpath("td")
      links << BASE_URL + attributes(td[1].xpath("a"),"href")
    }
    return links
  elsif action == "details"
    records = {"DOC"=>Time.now.to_s,"url"=>url}
    Nokogiri::HTML(data).xpath("//table[@class='data']/tr").each{|tr|
      th = tr.xpath("th/text()")
      td = tr.xpath("td[not(div)]")
      records[text(th)] = text(td[1].xpath("text()")) unless td[1].nil? 
    }
    puts records.inspect if @debug
    ScraperWiki.save_sqlite(unique_keys=["ND"],records,table_name="swdata",verbose=0) unless records["ND"].nil? or records["ND"].empty? 
  end
end


def action(pub_dt)
  begin
    @pg = @br.get(BASE_URL + "/TED/search/search.do")
    params = {'action'=>'search', 'Rs.gp.2241457.pid'=>'home', 'lgId'=>'en', 'Rs.gp.2241458.pid'=>'releaseCalendar', 'quickSearchCriteria'=>'', 'searchCriteria.searchScopeId'=>'4', 'searchCriteria.ojs'=>'', 'searchCriteria.freeText'=>'', 'searchCriteria.countryList'=>'', 'searchCriteria.contractList'=>'', 'searchCriteria.documentTypeList'=>'', 'searchCriteria.cpvCodeList'=>'', 'searchCriteria.publicationDateChoice'=>'DEFINITE_PUBLICATION_DATE', 'searchCriteria.publicationDate'=>pub_dt, 'searchCriteria.documentationDate'=>'', 'searchCriteria.typeOfAuthorityList'=>'', 'searchCriteria.place'=>'', 'searchCriteria.procedureList'=>'', 'searchCriteria.regulationList'=>'', 'searchCriteria.nutsCodeList'=>'', 'searchCriteria.documentNumber'=>'', 'searchCriteria.deadline'=>'', 'searchCriteria.authorityName'=>'', 'searchCriteria.mainActivityList'=>'', '_searchCriteria.statisticsMode'=>'on'}
    @pg = @br.post(BASE_URL + "/TED/search/search.do",params)
    nex = get_metadata("offset",nil)
    @pg = @br.get(BASE_URL + "/TED/search/" + nex) unless (nex.nil? or nex.empty? or nex=~ /Next/) 
    scraped = false
    begin
      links = scrape("list",@pg.body,"")
      scraped = true if not (links.nil? or links.empty?)
      links.each{|tender_link|
        begin
          pg_tmp = @br.get(tender_link+"&tabId=3")
          scrape("details",pg_tmp.body,tender_link)
        rescue Exception => e
          puts "ERROR: While processing  #{tender_link} :: #{e.inspect} :: #{e.backtrace}"
          if e.inspect =~ /Timeout|ETIMEDOUT/
            sleep(10)
            retry
          end  
        end #unless is_document(tender_link)>0
      }
      ne = @pg.link_with(:text => "Next")
      break if ne.nil? 
      save_metadata("offset",(ne.nil?) ? "" : ne.href)
      @pg = @pg.link_with(:text => "Next").click unless ne.nil? 
      sleep(30)
    rescue Exception=> e
      puts "ERROR: While processing #{ne} :: #{e.inspect} :: #{e.backtrace}"
      if e.inspect =~ /Timeout|ETIMEDOUT/
        sleep(10)
        retry
      end
    end while not (ne.nil? or @pg.nil?)  or @pg.body =~ /Nothing found to display/
    save_metadata("offset_dt",Date.parse(pub_dt).next.strftime("%d-%m-%Y"))  #if scraped
  rescue Exception=> e
    puts "ERROR: While initializing search :: #{e.inspect} :: #{e.backtrace}"
    #if e.inspect =~ /Timeout|ETIMEDOUT/
      sleep(30)
      retry
    #end
  end
end
@debug = false
if @debug
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
  }
  url="http://ted.europa.eu/udl?uri=TED:NOTICE:261779-2011:DATA:EN:HTML&src=0&tabId=3"
  pg = br.get(url)
  scrape("details",pg.body,url)
end

begin
  @br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout=1200
  }
  @pg = @br.post("http://ted.europa.eu/TED/misc/chooseLanguage.do?lgId=en",{'action'=>'cl'})
rescue Exception=> e
  puts "ERROR: While initializing  :: #{e.inspect} :: #{e.backtrace}"
  if e.inspect =~ /Timeout|ETIMEDOUT/
    sleep(30)
    retry
  end
end unless @debug
#action("10-01-2009")
#save_metadata("offset_dt","01-01-2009")
#save_metadata("offset","searchResult.do?page=41")
strt = Date.parse(get_metadata("offset_dt","01-01-2009"))
endd = Date.parse(Time.now.strftime("%d-%m-%Y"))
(strt..endd).each{|pub_dt|
  action(pub_dt.strftime("%d-%m-%Y")) unless @debug
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'cgi'
require 'date'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL ="http://ted.europa.eu"


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
    puts "ERROR: #{e.inspect} during save_metadata(#{key}) :: #{e.backtrace}"
   
  end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",key)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key}) :: #{e.backtrace}"
    retry
  end
end

def text(str)
  begin
    ret = ""
    str.each{|s|
      if str.inner_html.nil? or str.inner_html.empty? 
        ret = ret + s.text.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ") + ((s.text.strip.nil? or s.text.strip.empty?)? "" : "|")
      else
        ret = ret + s.inner_html.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ").gsub("<br>","|") + ((s.inner_html.strip.nil? or s.inner_html.strip.empty?)? "" : "|")
      end
    } unless str.nil? 
    return ret.chop
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end

def escape(str)
  return CGI.unescapeHTML(str).gsub(/"/,"&quot;")#.gsub(/"/,"\"")
end

def is_document(url)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where url=?",[url])[data][0][0]
end

def scrape(action,data,url)
  if action == "list"
    links = []
    Nokogiri::HTML(data).xpath(".//*[@id='notice']/tbody/tr").each{|tr|
      td = tr.xpath("td")
      links << BASE_URL + attributes(td[1].xpath("a"),"href")
    }
    return links
  elsif action == "details"
    records = {"DOC"=>Time.now.to_s,"url"=>url}
    Nokogiri::HTML(data).xpath("//table[@class='data']/tr").each{|tr|
      th = tr.xpath("th/text()")
      td = tr.xpath("td[not(div)]")
      records[text(th)] = text(td[1].xpath("text()")) unless td[1].nil? 
    }
    puts records.inspect if @debug
    ScraperWiki.save_sqlite(unique_keys=["ND"],records,table_name="swdata",verbose=0) unless records["ND"].nil? or records["ND"].empty? 
  end
end


def action(pub_dt)
  begin
    @pg = @br.get(BASE_URL + "/TED/search/search.do")
    params = {'action'=>'search', 'Rs.gp.2241457.pid'=>'home', 'lgId'=>'en', 'Rs.gp.2241458.pid'=>'releaseCalendar', 'quickSearchCriteria'=>'', 'searchCriteria.searchScopeId'=>'4', 'searchCriteria.ojs'=>'', 'searchCriteria.freeText'=>'', 'searchCriteria.countryList'=>'', 'searchCriteria.contractList'=>'', 'searchCriteria.documentTypeList'=>'', 'searchCriteria.cpvCodeList'=>'', 'searchCriteria.publicationDateChoice'=>'DEFINITE_PUBLICATION_DATE', 'searchCriteria.publicationDate'=>pub_dt, 'searchCriteria.documentationDate'=>'', 'searchCriteria.typeOfAuthorityList'=>'', 'searchCriteria.place'=>'', 'searchCriteria.procedureList'=>'', 'searchCriteria.regulationList'=>'', 'searchCriteria.nutsCodeList'=>'', 'searchCriteria.documentNumber'=>'', 'searchCriteria.deadline'=>'', 'searchCriteria.authorityName'=>'', 'searchCriteria.mainActivityList'=>'', '_searchCriteria.statisticsMode'=>'on'}
    @pg = @br.post(BASE_URL + "/TED/search/search.do",params)
    nex = get_metadata("offset",nil)
    @pg = @br.get(BASE_URL + "/TED/search/" + nex) unless (nex.nil? or nex.empty? or nex=~ /Next/) 
    scraped = false
    begin
      links = scrape("list",@pg.body,"")
      scraped = true if not (links.nil? or links.empty?)
      links.each{|tender_link|
        begin
          pg_tmp = @br.get(tender_link+"&tabId=3")
          scrape("details",pg_tmp.body,tender_link)
        rescue Exception => e
          puts "ERROR: While processing  #{tender_link} :: #{e.inspect} :: #{e.backtrace}"
          if e.inspect =~ /Timeout|ETIMEDOUT/
            sleep(10)
            retry
          end  
        end #unless is_document(tender_link)>0
      }
      ne = @pg.link_with(:text => "Next")
      break if ne.nil? 
      save_metadata("offset",(ne.nil?) ? "" : ne.href)
      @pg = @pg.link_with(:text => "Next").click unless ne.nil? 
      sleep(30)
    rescue Exception=> e
      puts "ERROR: While processing #{ne} :: #{e.inspect} :: #{e.backtrace}"
      if e.inspect =~ /Timeout|ETIMEDOUT/
        sleep(10)
        retry
      end
    end while not (ne.nil? or @pg.nil?)  or @pg.body =~ /Nothing found to display/
    save_metadata("offset_dt",Date.parse(pub_dt).next.strftime("%d-%m-%Y"))  #if scraped
  rescue Exception=> e
    puts "ERROR: While initializing search :: #{e.inspect} :: #{e.backtrace}"
    #if e.inspect =~ /Timeout|ETIMEDOUT/
      sleep(30)
      retry
    #end
  end
end
@debug = false
if @debug
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
  }
  url="http://ted.europa.eu/udl?uri=TED:NOTICE:261779-2011:DATA:EN:HTML&src=0&tabId=3"
  pg = br.get(url)
  scrape("details",pg.body,url)
end

begin
  @br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout=1200
  }
  @pg = @br.post("http://ted.europa.eu/TED/misc/chooseLanguage.do?lgId=en",{'action'=>'cl'})
rescue Exception=> e
  puts "ERROR: While initializing  :: #{e.inspect} :: #{e.backtrace}"
  if e.inspect =~ /Timeout|ETIMEDOUT/
    sleep(30)
    retry
  end
end unless @debug
#action("10-01-2009")
#save_metadata("offset_dt","01-01-2009")
#save_metadata("offset","searchResult.do?page=41")
strt = Date.parse(get_metadata("offset_dt","01-01-2009"))
endd = Date.parse(Time.now.strftime("%d-%m-%Y"))
(strt..endd).each{|pub_dt|
  action(pub_dt.strftime("%d-%m-%Y")) unless @debug
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'cgi'
require 'date'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL ="http://ted.europa.eu"


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
    puts "ERROR: #{e.inspect} during save_metadata(#{key}) :: #{e.backtrace}"
   
  end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",key)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key}) :: #{e.backtrace}"
    retry
  end
end

def text(str)
  begin
    ret = ""
    str.each{|s|
      if str.inner_html.nil? or str.inner_html.empty? 
        ret = ret + s.text.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ") + ((s.text.strip.nil? or s.text.strip.empty?)? "" : "|")
      else
        ret = ret + s.inner_html.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ").gsub("<br>","|") + ((s.inner_html.strip.nil? or s.inner_html.strip.empty?)? "" : "|")
      end
    } unless str.nil? 
    return ret.chop
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end

def escape(str)
  return CGI.unescapeHTML(str).gsub(/"/,"&quot;")#.gsub(/"/,"\"")
end

def is_document(url)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where url=?",[url])[data][0][0]
end

def scrape(action,data,url)
  if action == "list"
    links = []
    Nokogiri::HTML(data).xpath(".//*[@id='notice']/tbody/tr").each{|tr|
      td = tr.xpath("td")
      links << BASE_URL + attributes(td[1].xpath("a"),"href")
    }
    return links
  elsif action == "details"
    records = {"DOC"=>Time.now.to_s,"url"=>url}
    Nokogiri::HTML(data).xpath("//table[@class='data']/tr").each{|tr|
      th = tr.xpath("th/text()")
      td = tr.xpath("td[not(div)]")
      records[text(th)] = text(td[1].xpath("text()")) unless td[1].nil? 
    }
    puts records.inspect if @debug
    ScraperWiki.save_sqlite(unique_keys=["ND"],records,table_name="swdata",verbose=0) unless records["ND"].nil? or records["ND"].empty? 
  end
end


def action(pub_dt)
  begin
    @pg = @br.get(BASE_URL + "/TED/search/search.do")
    params = {'action'=>'search', 'Rs.gp.2241457.pid'=>'home', 'lgId'=>'en', 'Rs.gp.2241458.pid'=>'releaseCalendar', 'quickSearchCriteria'=>'', 'searchCriteria.searchScopeId'=>'4', 'searchCriteria.ojs'=>'', 'searchCriteria.freeText'=>'', 'searchCriteria.countryList'=>'', 'searchCriteria.contractList'=>'', 'searchCriteria.documentTypeList'=>'', 'searchCriteria.cpvCodeList'=>'', 'searchCriteria.publicationDateChoice'=>'DEFINITE_PUBLICATION_DATE', 'searchCriteria.publicationDate'=>pub_dt, 'searchCriteria.documentationDate'=>'', 'searchCriteria.typeOfAuthorityList'=>'', 'searchCriteria.place'=>'', 'searchCriteria.procedureList'=>'', 'searchCriteria.regulationList'=>'', 'searchCriteria.nutsCodeList'=>'', 'searchCriteria.documentNumber'=>'', 'searchCriteria.deadline'=>'', 'searchCriteria.authorityName'=>'', 'searchCriteria.mainActivityList'=>'', '_searchCriteria.statisticsMode'=>'on'}
    @pg = @br.post(BASE_URL + "/TED/search/search.do",params)
    nex = get_metadata("offset",nil)
    @pg = @br.get(BASE_URL + "/TED/search/" + nex) unless (nex.nil? or nex.empty? or nex=~ /Next/) 
    scraped = false
    begin
      links = scrape("list",@pg.body,"")
      scraped = true if not (links.nil? or links.empty?)
      links.each{|tender_link|
        begin
          pg_tmp = @br.get(tender_link+"&tabId=3")
          scrape("details",pg_tmp.body,tender_link)
        rescue Exception => e
          puts "ERROR: While processing  #{tender_link} :: #{e.inspect} :: #{e.backtrace}"
          if e.inspect =~ /Timeout|ETIMEDOUT/
            sleep(10)
            retry
          end  
        end #unless is_document(tender_link)>0
      }
      ne = @pg.link_with(:text => "Next")
      break if ne.nil? 
      save_metadata("offset",(ne.nil?) ? "" : ne.href)
      @pg = @pg.link_with(:text => "Next").click unless ne.nil? 
      sleep(30)
    rescue Exception=> e
      puts "ERROR: While processing #{ne} :: #{e.inspect} :: #{e.backtrace}"
      if e.inspect =~ /Timeout|ETIMEDOUT/
        sleep(10)
        retry
      end
    end while not (ne.nil? or @pg.nil?)  or @pg.body =~ /Nothing found to display/
    save_metadata("offset_dt",Date.parse(pub_dt).next.strftime("%d-%m-%Y"))  #if scraped
  rescue Exception=> e
    puts "ERROR: While initializing search :: #{e.inspect} :: #{e.backtrace}"
    #if e.inspect =~ /Timeout|ETIMEDOUT/
      sleep(30)
      retry
    #end
  end
end
@debug = false
if @debug
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
  }
  url="http://ted.europa.eu/udl?uri=TED:NOTICE:261779-2011:DATA:EN:HTML&src=0&tabId=3"
  pg = br.get(url)
  scrape("details",pg.body,url)
end

begin
  @br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout=1200
  }
  @pg = @br.post("http://ted.europa.eu/TED/misc/chooseLanguage.do?lgId=en",{'action'=>'cl'})
rescue Exception=> e
  puts "ERROR: While initializing  :: #{e.inspect} :: #{e.backtrace}"
  if e.inspect =~ /Timeout|ETIMEDOUT/
    sleep(30)
    retry
  end
end unless @debug
#action("10-01-2009")
#save_metadata("offset_dt","01-01-2009")
#save_metadata("offset","searchResult.do?page=41")
strt = Date.parse(get_metadata("offset_dt","01-01-2009"))
endd = Date.parse(Time.now.strftime("%d-%m-%Y"))
(strt..endd).each{|pub_dt|
  action(pub_dt.strftime("%d-%m-%Y")) unless @debug
}