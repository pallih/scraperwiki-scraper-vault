# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://rocsupport.mfsa.com.mt"

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
    end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip}
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
    doc = Nokogiri::HTML(data).xpath(".//table[@id='ctl00_cphMain_RadGrid1_ctl00']/tbody/tr")
    #puts [doc.inner_html,doc.xpath("td").length].inspect
    doc.each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NAME" => text(td[0].xpath(".")),
        "COMPANY_NUMBER" => text(td[1].xpath(".")),
        "ADDR" => text(td[2].xpath(".")),
        "LOCALITY" => text(td[3].xpath(".")),
        "STATUS" => text(td[4].xpath(".")),
        "DOC" => Time.now
      }
      #puts r.inspect
      records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
    } if doc.xpath("td").length >= 4
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length == 0
    return doc.length
end


def action(srch,index)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }

    pg = br.get(BASE_URL+"/pages/SearchCompanyInformation.aspx")
    params = {
      "__EVENTTARGET"=>"ctl00$cphMain$RadComboBoxFirstLetter",
      "__EVENTARGUMENT"=>'{"Command":"Select","Index": index}',
      "ctl00$cphMain$RadComboBoxFirstLetter"=>srch,
      "ctl00$cphMain$RadGrid1$ctl00$ctl03$ctl01$PageSizeComboBox"=>1000,
      "ctl00_cphMain_RadGrid1_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState"=>'{"logEntries":[],"value":"1000","text":"1000","enabled":true}',
      "ctl00_RadScriptManager1_TSM"=>attributes(Nokogiri::HTML(pg.body).xpath(".//script[contains(@src,'Telerik.Web.UI')]"),"src").split("&")[2].split("=").last,
      "ctl00_cphMain_RadComboBoxFirstLetter_ClientState"=>"{'logEntries':[],'value':\"#{srch}\",'text':\"#{srch}\",'enabled':true}",
    }
    begin
      pg.form_with(:name=>"aspnetForm") do |f|
        params.each{|k,v| f[k]=v }
        pg = f.submit
      end
      scrape(pg.body)
      nex = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@class='rgPageNext' and not(contains(@onclick,'return'))]"),"name")
      break if nex.nil? or nex.empty? 
      params["__EVENTTARGET"]=nex
      params["__ASYNCPOST"]="false"
      params["__EVENTARGUMENT"]=""
    end while(true)
  end  
end

range = ['"','\'','.'].to_a + (0..10).to_a + ('A'..'Z').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset>=range.length

range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch,idx+1)
  save_metadata("OFFSET",idx.next)
  sleep(10)
}# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://rocsupport.mfsa.com.mt"

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
    end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip}
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
    doc = Nokogiri::HTML(data).xpath(".//table[@id='ctl00_cphMain_RadGrid1_ctl00']/tbody/tr")
    #puts [doc.inner_html,doc.xpath("td").length].inspect
    doc.each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NAME" => text(td[0].xpath(".")),
        "COMPANY_NUMBER" => text(td[1].xpath(".")),
        "ADDR" => text(td[2].xpath(".")),
        "LOCALITY" => text(td[3].xpath(".")),
        "STATUS" => text(td[4].xpath(".")),
        "DOC" => Time.now
      }
      #puts r.inspect
      records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
    } if doc.xpath("td").length >= 4
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length == 0
    return doc.length
end


def action(srch,index)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }

    pg = br.get(BASE_URL+"/pages/SearchCompanyInformation.aspx")
    params = {
      "__EVENTTARGET"=>"ctl00$cphMain$RadComboBoxFirstLetter",
      "__EVENTARGUMENT"=>'{"Command":"Select","Index": index}',
      "ctl00$cphMain$RadComboBoxFirstLetter"=>srch,
      "ctl00$cphMain$RadGrid1$ctl00$ctl03$ctl01$PageSizeComboBox"=>1000,
      "ctl00_cphMain_RadGrid1_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState"=>'{"logEntries":[],"value":"1000","text":"1000","enabled":true}',
      "ctl00_RadScriptManager1_TSM"=>attributes(Nokogiri::HTML(pg.body).xpath(".//script[contains(@src,'Telerik.Web.UI')]"),"src").split("&")[2].split("=").last,
      "ctl00_cphMain_RadComboBoxFirstLetter_ClientState"=>"{'logEntries':[],'value':\"#{srch}\",'text':\"#{srch}\",'enabled':true}",
    }
    begin
      pg.form_with(:name=>"aspnetForm") do |f|
        params.each{|k,v| f[k]=v }
        pg = f.submit
      end
      scrape(pg.body)
      nex = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@class='rgPageNext' and not(contains(@onclick,'return'))]"),"name")
      break if nex.nil? or nex.empty? 
      params["__EVENTTARGET"]=nex
      params["__ASYNCPOST"]="false"
      params["__EVENTARGUMENT"]=""
    end while(true)
  end  
end

range = ['"','\'','.'].to_a + (0..10).to_a + ('A'..'Z').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset>=range.length

range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch,idx+1)
  save_metadata("OFFSET",idx.next)
  sleep(10)
}# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://rocsupport.mfsa.com.mt"

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
    end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip}
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
    doc = Nokogiri::HTML(data).xpath(".//table[@id='ctl00_cphMain_RadGrid1_ctl00']/tbody/tr")
    #puts [doc.inner_html,doc.xpath("td").length].inspect
    doc.each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NAME" => text(td[0].xpath(".")),
        "COMPANY_NUMBER" => text(td[1].xpath(".")),
        "ADDR" => text(td[2].xpath(".")),
        "LOCALITY" => text(td[3].xpath(".")),
        "STATUS" => text(td[4].xpath(".")),
        "DOC" => Time.now
      }
      #puts r.inspect
      records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
    } if doc.xpath("td").length >= 4
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length == 0
    return doc.length
end


def action(srch,index)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }

    pg = br.get(BASE_URL+"/pages/SearchCompanyInformation.aspx")
    params = {
      "__EVENTTARGET"=>"ctl00$cphMain$RadComboBoxFirstLetter",
      "__EVENTARGUMENT"=>'{"Command":"Select","Index": index}',
      "ctl00$cphMain$RadComboBoxFirstLetter"=>srch,
      "ctl00$cphMain$RadGrid1$ctl00$ctl03$ctl01$PageSizeComboBox"=>1000,
      "ctl00_cphMain_RadGrid1_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState"=>'{"logEntries":[],"value":"1000","text":"1000","enabled":true}',
      "ctl00_RadScriptManager1_TSM"=>attributes(Nokogiri::HTML(pg.body).xpath(".//script[contains(@src,'Telerik.Web.UI')]"),"src").split("&")[2].split("=").last,
      "ctl00_cphMain_RadComboBoxFirstLetter_ClientState"=>"{'logEntries':[],'value':\"#{srch}\",'text':\"#{srch}\",'enabled':true}",
    }
    begin
      pg.form_with(:name=>"aspnetForm") do |f|
        params.each{|k,v| f[k]=v }
        pg = f.submit
      end
      scrape(pg.body)
      nex = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@class='rgPageNext' and not(contains(@onclick,'return'))]"),"name")
      break if nex.nil? or nex.empty? 
      params["__EVENTTARGET"]=nex
      params["__ASYNCPOST"]="false"
      params["__EVENTARGUMENT"]=""
    end while(true)
  end  
end

range = ['"','\'','.'].to_a + (0..10).to_a + ('A'..'Z').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset>=range.length

range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch,idx+1)
  save_metadata("OFFSET",idx.next)
  sleep(10)
}# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://rocsupport.mfsa.com.mt"

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
    end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip}
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
    doc = Nokogiri::HTML(data).xpath(".//table[@id='ctl00_cphMain_RadGrid1_ctl00']/tbody/tr")
    #puts [doc.inner_html,doc.xpath("td").length].inspect
    doc.each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NAME" => text(td[0].xpath(".")),
        "COMPANY_NUMBER" => text(td[1].xpath(".")),
        "ADDR" => text(td[2].xpath(".")),
        "LOCALITY" => text(td[3].xpath(".")),
        "STATUS" => text(td[4].xpath(".")),
        "DOC" => Time.now
      }
      #puts r.inspect
      records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
    } if doc.xpath("td").length >= 4
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length == 0
    return doc.length
end


def action(srch,index)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }

    pg = br.get(BASE_URL+"/pages/SearchCompanyInformation.aspx")
    params = {
      "__EVENTTARGET"=>"ctl00$cphMain$RadComboBoxFirstLetter",
      "__EVENTARGUMENT"=>'{"Command":"Select","Index": index}',
      "ctl00$cphMain$RadComboBoxFirstLetter"=>srch,
      "ctl00$cphMain$RadGrid1$ctl00$ctl03$ctl01$PageSizeComboBox"=>1000,
      "ctl00_cphMain_RadGrid1_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState"=>'{"logEntries":[],"value":"1000","text":"1000","enabled":true}',
      "ctl00_RadScriptManager1_TSM"=>attributes(Nokogiri::HTML(pg.body).xpath(".//script[contains(@src,'Telerik.Web.UI')]"),"src").split("&")[2].split("=").last,
      "ctl00_cphMain_RadComboBoxFirstLetter_ClientState"=>"{'logEntries':[],'value':\"#{srch}\",'text':\"#{srch}\",'enabled':true}",
    }
    begin
      pg.form_with(:name=>"aspnetForm") do |f|
        params.each{|k,v| f[k]=v }
        pg = f.submit
      end
      scrape(pg.body)
      nex = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@class='rgPageNext' and not(contains(@onclick,'return'))]"),"name")
      break if nex.nil? or nex.empty? 
      params["__EVENTTARGET"]=nex
      params["__ASYNCPOST"]="false"
      params["__EVENTARGUMENT"]=""
    end while(true)
  end  
end

range = ['"','\'','.'].to_a + (0..10).to_a + ('A'..'Z').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset>=range.length

range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch,idx+1)
  save_metadata("OFFSET",idx.next)
  sleep(10)
}