# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://web.prc.newmexico.gov"


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

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//table[@id='ctl00_CPHLogin_CorpGrid']/tr[position()>2 and position()<last()]").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=>text(td[1].xpath(".")),
      "COMPANY_NAME"=>text(td[2].xpath(".")),
      "TYPE"=>text(td[3].xpath(".")),
      "STATUS"=>text(td[4].xpath(".")),
      "DOC"=>Time.now
    }
    records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    pg = br.get(BASE_URL+"/Corplookup/CorpSearch.aspx")
    params = {
      "ctl00$JsCheck1$hfClientJSEnabled"=>"True",
      "ctl00$CPHLogin$txtcorpnam"=>srch,
      "ctl00$CPHLogin$DropDownList1"=>"B",
      "ctl00$CPHLogin$txtnmscc"=>"",
      "ctl00$CPHLogin$btnsearch"=>"Search"
    }
    pg.form_with(:id => "aspnetForm") do |f|
      params.each{|k,v| f[k]=v}
      pg = f.submit
    end
    scrape(pg.body.gsub(/id="__VIEWSTATE" value=(.*)>/,">"))
    pgno = 2
    begin
      ne = Nokogiri::HTML(pg.body).xpath(".//table[@border='0' and not(@width or @style)]/tr/td[font/span]/following-sibling::td/font/a")
      if ne.nil? or ne.empty?       
        break
      else
        begin
          params={"__EVENTTARGET"=>"ctl00$CPHLogin$CorpGrid","__EVENTARGUMENT"=>"Page$#{pgno}"}
          pg.form_with(:id=>'aspnetForm') do |f|
            params.each{|k,v| f[k]=v}
            pg = f.submit
          end
          scrape(pg.body.gsub(/id="__VIEWSTATE" value=(.*)>/,">"))
          pgno = pgno + 1
        rescue Exception => e
          puts "ERROR: While processing subsequent pages #{srch} :: #{e.inspect} :: #{e.backtrace}"      
        end
      end
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time|locked/i
  end
end

action("%")# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://web.prc.newmexico.gov"


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

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//table[@id='ctl00_CPHLogin_CorpGrid']/tr[position()>2 and position()<last()]").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=>text(td[1].xpath(".")),
      "COMPANY_NAME"=>text(td[2].xpath(".")),
      "TYPE"=>text(td[3].xpath(".")),
      "STATUS"=>text(td[4].xpath(".")),
      "DOC"=>Time.now
    }
    records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    pg = br.get(BASE_URL+"/Corplookup/CorpSearch.aspx")
    params = {
      "ctl00$JsCheck1$hfClientJSEnabled"=>"True",
      "ctl00$CPHLogin$txtcorpnam"=>srch,
      "ctl00$CPHLogin$DropDownList1"=>"B",
      "ctl00$CPHLogin$txtnmscc"=>"",
      "ctl00$CPHLogin$btnsearch"=>"Search"
    }
    pg.form_with(:id => "aspnetForm") do |f|
      params.each{|k,v| f[k]=v}
      pg = f.submit
    end
    scrape(pg.body.gsub(/id="__VIEWSTATE" value=(.*)>/,">"))
    pgno = 2
    begin
      ne = Nokogiri::HTML(pg.body).xpath(".//table[@border='0' and not(@width or @style)]/tr/td[font/span]/following-sibling::td/font/a")
      if ne.nil? or ne.empty?       
        break
      else
        begin
          params={"__EVENTTARGET"=>"ctl00$CPHLogin$CorpGrid","__EVENTARGUMENT"=>"Page$#{pgno}"}
          pg.form_with(:id=>'aspnetForm') do |f|
            params.each{|k,v| f[k]=v}
            pg = f.submit
          end
          scrape(pg.body.gsub(/id="__VIEWSTATE" value=(.*)>/,">"))
          pgno = pgno + 1
        rescue Exception => e
          puts "ERROR: While processing subsequent pages #{srch} :: #{e.inspect} :: #{e.backtrace}"      
        end
      end
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time|locked/i
  end
end

action("%")