# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://sccefile.scc.virginia.gov/BusinessEntity/"

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

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,url)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='ctl00_DefaultContent_EntitySearchDataList']/tr[position()>1 and position()<last()]").each{|tr|
      td=tr.xpath("td")
      r = {
        'COMPANY_NUMBER'=>td[1].xpath("a/text()|span/text()"),
        'COMPANY_NAME'=>td[2].xpath("a/text()|span/text()"),
        'TYPE'=>td[3].xpath("span/text()"),
        'STATUS'=>td[4].xpath("span/text()"),
        'URL'=>BASE_URL+attributes(td[1].xpath("a"),"href"),
        'DOC'=>Time.now.to_s,
      }
      records << r if r['STATUS']='Active'
    }
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER','TYPE'],records,table_name='SWDATA',verbose=2) unless records.length==0
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    records={
      "COMPANY_NUMBER"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblNumber']/text()")),
      "COMPANY_NAME"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblName']/text()")),
      "ADDR"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblAddress1']/text()")),
      "CITY"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblCity']/text()")),
      "STATE"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblState']/text()")),
      "ZIP"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblZip']/text()")),
      "PHONE"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblPhone']/text()")),
      "DOMICILE"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblDomState']/text()"))
    }
    #puts records.inspect
    records['URL']=url
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
      #b.log = Logger.new(STDERR)
    }
    params = {'ctl00$DefaultContent$BusinessName'=>srch,'ctl00$DefaultContent$EntitySearch'=>'Search'}
    pg = br.get(BASE_URL+"BusinessEntitySearch.aspx")
    pgno = 1
    dmp = []
    begin
      pg.form_with(:name => "aspnetForm") do|f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      len = Nokogiri::HTML(pg.body).xpath(".//table[@id='ctl00_DefaultContent_EntitySearchDataList']/tr").length
      break if pg.body =~ /An error has occurred/ or len == 2
      scrape(pg.body,"list",nil)
      pgno = pgno.next
      params={'__EVENTTARGET'=>'ctl00$DefaultContent$EntitySearchDataList','__EVENTARGUMENT'=>"Page$#{pgno}"}
    rescue Exception => e
      puts "ERROR: While processing #{srch}-looping :: #{e.inspect} :: #{e.backtrace}"
      retry if e.inspect =~ /Timeout|TIME|HTTP/i
    exit if e.inspect =~ /reset|refused/
    end while(true)
  rescue Exception => e
    puts "ERROR: While establishing session for #{srch}:: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /Timeout|TIME|HTTP/i
    exit if e.inspect =~ /reset|refused|HTTPServerException/i
  end
end


#save_metadata('OFFSET',104)
range = (0..100).to_a + ('A'..'ZZZZ').sort.to_a
offset = get_metadata("OFFSET",0).to_i
offset = 0 if offset>=range.length
range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch)
  save_metadata("OFFSET",idx.next)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://sccefile.scc.virginia.gov/BusinessEntity/"

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

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,url)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='ctl00_DefaultContent_EntitySearchDataList']/tr[position()>1 and position()<last()]").each{|tr|
      td=tr.xpath("td")
      r = {
        'COMPANY_NUMBER'=>td[1].xpath("a/text()|span/text()"),
        'COMPANY_NAME'=>td[2].xpath("a/text()|span/text()"),
        'TYPE'=>td[3].xpath("span/text()"),
        'STATUS'=>td[4].xpath("span/text()"),
        'URL'=>BASE_URL+attributes(td[1].xpath("a"),"href"),
        'DOC'=>Time.now.to_s,
      }
      records << r if r['STATUS']='Active'
    }
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER','TYPE'],records,table_name='SWDATA',verbose=2) unless records.length==0
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    records={
      "COMPANY_NUMBER"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblNumber']/text()")),
      "COMPANY_NAME"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblName']/text()")),
      "ADDR"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblAddress1']/text()")),
      "CITY"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblCity']/text()")),
      "STATE"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblState']/text()")),
      "ZIP"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblZip']/text()")),
      "PHONE"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblPhone']/text()")),
      "DOMICILE"=>text(doc.xpath(".//span[@id='ctl00_MainContent_lblDomState']/text()"))
    }
    #puts records.inspect
    records['URL']=url
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
      #b.log = Logger.new(STDERR)
    }
    params = {'ctl00$DefaultContent$BusinessName'=>srch,'ctl00$DefaultContent$EntitySearch'=>'Search'}
    pg = br.get(BASE_URL+"BusinessEntitySearch.aspx")
    pgno = 1
    dmp = []
    begin
      pg.form_with(:name => "aspnetForm") do|f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      len = Nokogiri::HTML(pg.body).xpath(".//table[@id='ctl00_DefaultContent_EntitySearchDataList']/tr").length
      break if pg.body =~ /An error has occurred/ or len == 2
      scrape(pg.body,"list",nil)
      pgno = pgno.next
      params={'__EVENTTARGET'=>'ctl00$DefaultContent$EntitySearchDataList','__EVENTARGUMENT'=>"Page$#{pgno}"}
    rescue Exception => e
      puts "ERROR: While processing #{srch}-looping :: #{e.inspect} :: #{e.backtrace}"
      retry if e.inspect =~ /Timeout|TIME|HTTP/i
    exit if e.inspect =~ /reset|refused/
    end while(true)
  rescue Exception => e
    puts "ERROR: While establishing session for #{srch}:: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /Timeout|TIME|HTTP/i
    exit if e.inspect =~ /reset|refused|HTTPServerException/i
  end
end


#save_metadata('OFFSET',104)
range = (0..100).to_a + ('A'..'ZZZZ').sort.to_a
offset = get_metadata("OFFSET",0).to_i
offset = 0 if offset>=range.length
range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch)
  save_metadata("OFFSET",idx.next)
}
