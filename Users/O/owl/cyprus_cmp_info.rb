# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'cgi'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.cyprus-data.com"

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
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip }
      return tmp.join(" ")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(sn,data,act,cname,url)
  records = []
  doc = Nokogiri::HTML(data,nil,"ISO-8859-7").xpath(".//table[@width='900px' and @border=0]/tr[td[@width='100px'] and not(td/p/font/font)]")
  doc.each{|tr|
    td=tr.xpath("td")
    next unless cname == text(td[0].xpath("p/font"))
    r={"SCRAPED_NUMBER"=>sn,"URL"=>url,"DOC"=>Time.now}
    r["COMPANY_NAME"],r["COMPANY_NUMBER"],n_status,r['STATUS']= text(td[0].xpath("p/font")),text(td[1].xpath("p/font")).gsub(/\n|&nbsp/,''),text(td[2].xpath("p/font")),text(td[3].xpath("p/font"))
    records << r unless (r["COMPANY_NAME"].nil? or r['COMPANY_NAME'].empty?) if n_status =="Current Name"
  }

  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length == 0 ? nil : 1
end


def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL + "/product/#{num}/company-name.html"
    pg = br.get(s_url)
    cname = pg.at("h1[@class='title-right fn']/text()").to_s
    return if cname.nil?  or cname.empty? 
    pg = br.get("http://www.drcor.mcit.gov.cy/portal/page/portal/Eforos/dttSearch_en")
    raise "retry" if pg.body =~ /An error occurred while processing the request/i
    pg.form_with(:name=>'dttSearch') do|f|
      f['cn']=cname
      pg = f.submit
    end 
    url = pg.uri.to_s
    pg = br.get("http://www.drcor.mcit.gov.cy/portal/page/portal/Eforos/dttDisplayResults_en")
    resp=scrape(num,pg.body,"details",cname,url) unless pg.body =~ /Your search criteria is not returning any names/
    save_metadata("STRT",num.next) unless resp.nil? 
  rescue Exception => e
    puts [num,e.inspect,e.backtrace].inspect
  end
end

strt = get_metadata("STRT",375645)
endd = strt + 100
(strt..endd).each{|num|
  action(num)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'cgi'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.cyprus-data.com"

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
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip }
      return tmp.join(" ")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(sn,data,act,cname,url)
  records = []
  doc = Nokogiri::HTML(data,nil,"ISO-8859-7").xpath(".//table[@width='900px' and @border=0]/tr[td[@width='100px'] and not(td/p/font/font)]")
  doc.each{|tr|
    td=tr.xpath("td")
    next unless cname == text(td[0].xpath("p/font"))
    r={"SCRAPED_NUMBER"=>sn,"URL"=>url,"DOC"=>Time.now}
    r["COMPANY_NAME"],r["COMPANY_NUMBER"],n_status,r['STATUS']= text(td[0].xpath("p/font")),text(td[1].xpath("p/font")).gsub(/\n|&nbsp/,''),text(td[2].xpath("p/font")),text(td[3].xpath("p/font"))
    records << r unless (r["COMPANY_NAME"].nil? or r['COMPANY_NAME'].empty?) if n_status =="Current Name"
  }

  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length == 0 ? nil : 1
end


def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL + "/product/#{num}/company-name.html"
    pg = br.get(s_url)
    cname = pg.at("h1[@class='title-right fn']/text()").to_s
    return if cname.nil?  or cname.empty? 
    pg = br.get("http://www.drcor.mcit.gov.cy/portal/page/portal/Eforos/dttSearch_en")
    raise "retry" if pg.body =~ /An error occurred while processing the request/i
    pg.form_with(:name=>'dttSearch') do|f|
      f['cn']=cname
      pg = f.submit
    end 
    url = pg.uri.to_s
    pg = br.get("http://www.drcor.mcit.gov.cy/portal/page/portal/Eforos/dttDisplayResults_en")
    resp=scrape(num,pg.body,"details",cname,url) unless pg.body =~ /Your search criteria is not returning any names/
    save_metadata("STRT",num.next) unless resp.nil? 
  rescue Exception => e
    puts [num,e.inspect,e.backtrace].inspect
  end
end

strt = get_metadata("STRT",375645)
endd = strt + 100
(strt..endd).each{|num|
  action(num)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'cgi'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.cyprus-data.com"

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
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip }
      return tmp.join(" ")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(sn,data,act,cname,url)
  records = []
  doc = Nokogiri::HTML(data,nil,"ISO-8859-7").xpath(".//table[@width='900px' and @border=0]/tr[td[@width='100px'] and not(td/p/font/font)]")
  doc.each{|tr|
    td=tr.xpath("td")
    next unless cname == text(td[0].xpath("p/font"))
    r={"SCRAPED_NUMBER"=>sn,"URL"=>url,"DOC"=>Time.now}
    r["COMPANY_NAME"],r["COMPANY_NUMBER"],n_status,r['STATUS']= text(td[0].xpath("p/font")),text(td[1].xpath("p/font")).gsub(/\n|&nbsp/,''),text(td[2].xpath("p/font")),text(td[3].xpath("p/font"))
    records << r unless (r["COMPANY_NAME"].nil? or r['COMPANY_NAME'].empty?) if n_status =="Current Name"
  }

  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length == 0 ? nil : 1
end


def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL + "/product/#{num}/company-name.html"
    pg = br.get(s_url)
    cname = pg.at("h1[@class='title-right fn']/text()").to_s
    return if cname.nil?  or cname.empty? 
    pg = br.get("http://www.drcor.mcit.gov.cy/portal/page/portal/Eforos/dttSearch_en")
    raise "retry" if pg.body =~ /An error occurred while processing the request/i
    pg.form_with(:name=>'dttSearch') do|f|
      f['cn']=cname
      pg = f.submit
    end 
    url = pg.uri.to_s
    pg = br.get("http://www.drcor.mcit.gov.cy/portal/page/portal/Eforos/dttDisplayResults_en")
    resp=scrape(num,pg.body,"details",cname,url) unless pg.body =~ /Your search criteria is not returning any names/
    save_metadata("STRT",num.next) unless resp.nil? 
  rescue Exception => e
    puts [num,e.inspect,e.backtrace].inspect
  end
end

strt = get_metadata("STRT",375645)
endd = strt + 100
(strt..endd).each{|num|
  action(num)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'cgi'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.cyprus-data.com"

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
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip }
      return tmp.join(" ")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(sn,data,act,cname,url)
  records = []
  doc = Nokogiri::HTML(data,nil,"ISO-8859-7").xpath(".//table[@width='900px' and @border=0]/tr[td[@width='100px'] and not(td/p/font/font)]")
  doc.each{|tr|
    td=tr.xpath("td")
    next unless cname == text(td[0].xpath("p/font"))
    r={"SCRAPED_NUMBER"=>sn,"URL"=>url,"DOC"=>Time.now}
    r["COMPANY_NAME"],r["COMPANY_NUMBER"],n_status,r['STATUS']= text(td[0].xpath("p/font")),text(td[1].xpath("p/font")).gsub(/\n|&nbsp/,''),text(td[2].xpath("p/font")),text(td[3].xpath("p/font"))
    records << r unless (r["COMPANY_NAME"].nil? or r['COMPANY_NAME'].empty?) if n_status =="Current Name"
  }

  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length == 0 ? nil : 1
end


def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL + "/product/#{num}/company-name.html"
    pg = br.get(s_url)
    cname = pg.at("h1[@class='title-right fn']/text()").to_s
    return if cname.nil?  or cname.empty? 
    pg = br.get("http://www.drcor.mcit.gov.cy/portal/page/portal/Eforos/dttSearch_en")
    raise "retry" if pg.body =~ /An error occurred while processing the request/i
    pg.form_with(:name=>'dttSearch') do|f|
      f['cn']=cname
      pg = f.submit
    end 
    url = pg.uri.to_s
    pg = br.get("http://www.drcor.mcit.gov.cy/portal/page/portal/Eforos/dttDisplayResults_en")
    resp=scrape(num,pg.body,"details",cname,url) unless pg.body =~ /Your search criteria is not returning any names/
    save_metadata("STRT",num.next) unless resp.nil? 
  rescue Exception => e
    puts [num,e.inspect,e.backtrace].inspect
  end
end

strt = get_metadata("STRT",375645)
endd = strt + 100
(strt..endd).each{|num|
  action(num)
}
