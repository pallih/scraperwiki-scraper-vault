# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.cvr.dk"

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
      str.collect{|st| tmp << st.text.strip}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  doc = Nokogiri::HTML(data).xpath(".//table[@id='ctl00_BodyPlaceholder_RadGrid1_ctl00']/tbody/tr")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "CVMR"=>text(td[1].xpath(".")),
      "COMPANY_NAME"=>text(td[2].xpath(".")),
      "URL"=>BASE_URL+attributes(td[0].xpath("a"),"href"),
      "CREATION_DT"=>text(td[3].xpath(".")),
      "DOC"=>Time.now
    }
    records << r unless r["COMPANY_NAME"].nil? or r["COMPANY_NAME"].empty? 
  }

  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.length
end

def action(from,to)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
    s_url = BASE_URL+"/Site/Forms/PublicService/CompanyRegSearch.aspx"
    pg = br.get(s_url)
    return "BLOCKED" if pg.body =~ /www.cvr.dk er blokeret/i
 params = {'ctl00$BodyPlaceholder$SearchTypeDropDownList'=>'0','ctl00$BodyPlaceholder$fromDate$uiDateText'=>from,'ctl00$BodyPlaceholder$toDate$uiDateText'=>to,'ctl00$BodyPlaceholder$AreaDistrict1$uiArea'=>'-1','ctl00$BodyPlaceholder$AjaxCommune1$OldNewSel'=>'radiobuttonNewCommunes','ctl00$BodyPlaceholder$AjaxCommune1$dropdownCommuneID'=>'-1','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$0'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$1'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$2'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$3'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$4'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$5'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$6'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$7'=>'on','ctl00$BodyPlaceholder$RegTypeCheckBoxList$0'=>'on','ctl00$BodyPlaceholder$SearchButton'=>'Udførsøgning'}
   pg.form_with(:name=>'aspnetForm') do |f|
      params.each{|k,v| f[k]=v }
      pg = f.submit
    end
   
    ttl = scrape(pg.body)
    begin
      name,nex = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@class='rgPageNext']"),"name"),attributes(Nokogiri::HTML(pg.body).xpath(".//input[@class='rgPageNext']"),"onclick")
      break if not (nex.nil? or nex.empty?) or (name.nil? or name.empty?)
      params = {name=>'+'}
      pg.form_with(:name=>'aspnetForm') do |f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      ttl = ttl + scrape(pg.body)
    rescue Exception=>e
      puts "ERROR: While looping #{srch} :: #{e.inspect} :: #{e.backtrace}"
      retry
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
  return from,to,ttl
end

#save_metadata("STRT",'20.02.2005')
strt = Date.strptime(get_metadata("STRT",'01.02.2012'),'%d.%m.%Y')
endd = Date.today
(strt..endd).each{|dt|
  dt_s = dt.strftime('%d.%m.%Y')
  ret = action(dt_s,dt_s)
  if ret == "BLOCKED"
    puts "IP Blocked"
    break
  end
  save_metadata("STRT",dt.next.strftime('%d.%m.%Y')) unless dt.next == Date.today
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.cvr.dk"

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
      str.collect{|st| tmp << st.text.strip}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  doc = Nokogiri::HTML(data).xpath(".//table[@id='ctl00_BodyPlaceholder_RadGrid1_ctl00']/tbody/tr")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "CVMR"=>text(td[1].xpath(".")),
      "COMPANY_NAME"=>text(td[2].xpath(".")),
      "URL"=>BASE_URL+attributes(td[0].xpath("a"),"href"),
      "CREATION_DT"=>text(td[3].xpath(".")),
      "DOC"=>Time.now
    }
    records << r unless r["COMPANY_NAME"].nil? or r["COMPANY_NAME"].empty? 
  }

  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.length
end

def action(from,to)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
    s_url = BASE_URL+"/Site/Forms/PublicService/CompanyRegSearch.aspx"
    pg = br.get(s_url)
    return "BLOCKED" if pg.body =~ /www.cvr.dk er blokeret/i
 params = {'ctl00$BodyPlaceholder$SearchTypeDropDownList'=>'0','ctl00$BodyPlaceholder$fromDate$uiDateText'=>from,'ctl00$BodyPlaceholder$toDate$uiDateText'=>to,'ctl00$BodyPlaceholder$AreaDistrict1$uiArea'=>'-1','ctl00$BodyPlaceholder$AjaxCommune1$OldNewSel'=>'radiobuttonNewCommunes','ctl00$BodyPlaceholder$AjaxCommune1$dropdownCommuneID'=>'-1','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$0'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$1'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$2'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$3'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$4'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$5'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$6'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$7'=>'on','ctl00$BodyPlaceholder$RegTypeCheckBoxList$0'=>'on','ctl00$BodyPlaceholder$SearchButton'=>'Udførsøgning'}
   pg.form_with(:name=>'aspnetForm') do |f|
      params.each{|k,v| f[k]=v }
      pg = f.submit
    end
   
    ttl = scrape(pg.body)
    begin
      name,nex = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@class='rgPageNext']"),"name"),attributes(Nokogiri::HTML(pg.body).xpath(".//input[@class='rgPageNext']"),"onclick")
      break if not (nex.nil? or nex.empty?) or (name.nil? or name.empty?)
      params = {name=>'+'}
      pg.form_with(:name=>'aspnetForm') do |f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      ttl = ttl + scrape(pg.body)
    rescue Exception=>e
      puts "ERROR: While looping #{srch} :: #{e.inspect} :: #{e.backtrace}"
      retry
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
  return from,to,ttl
end

#save_metadata("STRT",'20.02.2005')
strt = Date.strptime(get_metadata("STRT",'01.02.2012'),'%d.%m.%Y')
endd = Date.today
(strt..endd).each{|dt|
  dt_s = dt.strftime('%d.%m.%Y')
  ret = action(dt_s,dt_s)
  if ret == "BLOCKED"
    puts "IP Blocked"
    break
  end
  save_metadata("STRT",dt.next.strftime('%d.%m.%Y')) unless dt.next == Date.today
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.cvr.dk"

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
      str.collect{|st| tmp << st.text.strip}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  doc = Nokogiri::HTML(data).xpath(".//table[@id='ctl00_BodyPlaceholder_RadGrid1_ctl00']/tbody/tr")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "CVMR"=>text(td[1].xpath(".")),
      "COMPANY_NAME"=>text(td[2].xpath(".")),
      "URL"=>BASE_URL+attributes(td[0].xpath("a"),"href"),
      "CREATION_DT"=>text(td[3].xpath(".")),
      "DOC"=>Time.now
    }
    records << r unless r["COMPANY_NAME"].nil? or r["COMPANY_NAME"].empty? 
  }

  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.length
end

def action(from,to)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
    s_url = BASE_URL+"/Site/Forms/PublicService/CompanyRegSearch.aspx"
    pg = br.get(s_url)
    return "BLOCKED" if pg.body =~ /www.cvr.dk er blokeret/i
 params = {'ctl00$BodyPlaceholder$SearchTypeDropDownList'=>'0','ctl00$BodyPlaceholder$fromDate$uiDateText'=>from,'ctl00$BodyPlaceholder$toDate$uiDateText'=>to,'ctl00$BodyPlaceholder$AreaDistrict1$uiArea'=>'-1','ctl00$BodyPlaceholder$AjaxCommune1$OldNewSel'=>'radiobuttonNewCommunes','ctl00$BodyPlaceholder$AjaxCommune1$dropdownCommuneID'=>'-1','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$0'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$1'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$2'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$3'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$4'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$5'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$6'=>'on','ctl00$BodyPlaceholder$CompanyTypeCheckBoxList$7'=>'on','ctl00$BodyPlaceholder$RegTypeCheckBoxList$0'=>'on','ctl00$BodyPlaceholder$SearchButton'=>'Udførsøgning'}
   pg.form_with(:name=>'aspnetForm') do |f|
      params.each{|k,v| f[k]=v }
      pg = f.submit
    end
   
    ttl = scrape(pg.body)
    begin
      name,nex = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@class='rgPageNext']"),"name"),attributes(Nokogiri::HTML(pg.body).xpath(".//input[@class='rgPageNext']"),"onclick")
      break if not (nex.nil? or nex.empty?) or (name.nil? or name.empty?)
      params = {name=>'+'}
      pg.form_with(:name=>'aspnetForm') do |f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      ttl = ttl + scrape(pg.body)
    rescue Exception=>e
      puts "ERROR: While looping #{srch} :: #{e.inspect} :: #{e.backtrace}"
      retry
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
  return from,to,ttl
end

#save_metadata("STRT",'20.02.2005')
strt = Date.strptime(get_metadata("STRT",'01.02.2012'),'%d.%m.%Y')
endd = Date.today
(strt..endd).each{|dt|
  dt_s = dt.strftime('%d.%m.%Y')
  ret = action(dt_s,dt_s)
  if ret == "BLOCKED"
    puts "IP Blocked"
    break
  end
  save_metadata("STRT",dt.next.strftime('%d.%m.%Y')) unless dt.next == Date.today
}
