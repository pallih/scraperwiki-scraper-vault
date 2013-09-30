# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.sos.ok.gov"

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
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//table[@summary='']/tbody/tr").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=>text(td[0].xpath("a")),
      "COMPANY_NAME"=>text(td[1].xpath("span")),
      "TYPE"=>text(td[2].xpath("span")),
      "NAME_TYPE"=>text(td[4].xpath("span"))[0],
      "STATUS"=>text(td[4].xpath("span"))[1],
      "DOC"=>Time.now
    }
    #puts r.inspect
    records << r unless r['NAME_TYPE']=='Tradename' or r['TYPE']=="Name Reservation" or r['TYPE']=="LLC Name Reservation" or r['STATUS']=='Former' or r['NAME_TYPE']=='Fictitious'
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length==0
  return records.length
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
  pg = br.get(BASE_URL+"/corp/corpInquiryFind.aspx")
  params = {
    "ctl00$ScriptManager1"=>"ctl00$ScriptManager1|ctl00$DefaultContent$CorpNameSearch1$SearchButton",
    "ctl00$DefaultContent$CorpNameSearch1$_singlename"=>srch,"ctl00$DefaultContent$CorpNameSearch1$SearchButton"=>"Search"
  }
  pg.form_with(:id => "aspnetForm") do |f|
    params.each{|k,v| f[k]=v}
    pg = f.submit
  end
  scrape(pg.body)
  pgno=2
  begin
    ne = Nokogiri::HTML(pg.body).xpath(".//div[@class='AspNet-GridView-Pagination AspNet-GridView-Bottom']/span/following-sibling::a")
    if ne.nil? or ne.empty?       
      break
    else
      params={
        "ctl00$ScriptManager1"=>"ctl00$DefaultContent$CorpNameSearch1$ResultsUpdatePanel|ctl00$DefaultContent$CorpNameSearch1$EntityGridView",
        "ctl00$DefaultContent$CorpNameSearch1$_singlename"=>srch,"__EVENTTARGET"=>"ctl00$DefaultContent$CorpNameSearch1$EntityGridView","__EVENTARGUMENT"=>"Page$#{pgno}"
      }
      pg.form_with(:id=>'aspnetForm') do |f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      scrape(pg.body)
      pgno = pgno + 1
    end
  end while(true)
  end
end

range = ('A'..'ZZZ').to_a.sort + (0..100).to_a
rstart = get_metadata("start",0)
range[rstart..-1].each_with_index{|srch,idx|
  action(srch)
  rstart = rstart + 1
  save_metadata("start",rstart)
}
delete_metadata("start")
#action("LOCKH")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.sos.ok.gov"

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
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//table[@summary='']/tbody/tr").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=>text(td[0].xpath("a")),
      "COMPANY_NAME"=>text(td[1].xpath("span")),
      "TYPE"=>text(td[2].xpath("span")),
      "NAME_TYPE"=>text(td[4].xpath("span"))[0],
      "STATUS"=>text(td[4].xpath("span"))[1],
      "DOC"=>Time.now
    }
    #puts r.inspect
    records << r unless r['NAME_TYPE']=='Tradename' or r['TYPE']=="Name Reservation" or r['TYPE']=="LLC Name Reservation" or r['STATUS']=='Former' or r['NAME_TYPE']=='Fictitious'
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length==0
  return records.length
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
  pg = br.get(BASE_URL+"/corp/corpInquiryFind.aspx")
  params = {
    "ctl00$ScriptManager1"=>"ctl00$ScriptManager1|ctl00$DefaultContent$CorpNameSearch1$SearchButton",
    "ctl00$DefaultContent$CorpNameSearch1$_singlename"=>srch,"ctl00$DefaultContent$CorpNameSearch1$SearchButton"=>"Search"
  }
  pg.form_with(:id => "aspnetForm") do |f|
    params.each{|k,v| f[k]=v}
    pg = f.submit
  end
  scrape(pg.body)
  pgno=2
  begin
    ne = Nokogiri::HTML(pg.body).xpath(".//div[@class='AspNet-GridView-Pagination AspNet-GridView-Bottom']/span/following-sibling::a")
    if ne.nil? or ne.empty?       
      break
    else
      params={
        "ctl00$ScriptManager1"=>"ctl00$DefaultContent$CorpNameSearch1$ResultsUpdatePanel|ctl00$DefaultContent$CorpNameSearch1$EntityGridView",
        "ctl00$DefaultContent$CorpNameSearch1$_singlename"=>srch,"__EVENTTARGET"=>"ctl00$DefaultContent$CorpNameSearch1$EntityGridView","__EVENTARGUMENT"=>"Page$#{pgno}"
      }
      pg.form_with(:id=>'aspnetForm') do |f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      scrape(pg.body)
      pgno = pgno + 1
    end
  end while(true)
  end
end

range = ('A'..'ZZZ').to_a.sort + (0..100).to_a
rstart = get_metadata("start",0)
range[rstart..-1].each_with_index{|srch,idx|
  action(srch)
  rstart = rstart + 1
  save_metadata("start",rstart)
}
delete_metadata("start")
#action("LOCKH")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.sos.ok.gov"

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
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//table[@summary='']/tbody/tr").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=>text(td[0].xpath("a")),
      "COMPANY_NAME"=>text(td[1].xpath("span")),
      "TYPE"=>text(td[2].xpath("span")),
      "NAME_TYPE"=>text(td[4].xpath("span"))[0],
      "STATUS"=>text(td[4].xpath("span"))[1],
      "DOC"=>Time.now
    }
    #puts r.inspect
    records << r unless r['NAME_TYPE']=='Tradename' or r['TYPE']=="Name Reservation" or r['TYPE']=="LLC Name Reservation" or r['STATUS']=='Former' or r['NAME_TYPE']=='Fictitious'
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length==0
  return records.length
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
  pg = br.get(BASE_URL+"/corp/corpInquiryFind.aspx")
  params = {
    "ctl00$ScriptManager1"=>"ctl00$ScriptManager1|ctl00$DefaultContent$CorpNameSearch1$SearchButton",
    "ctl00$DefaultContent$CorpNameSearch1$_singlename"=>srch,"ctl00$DefaultContent$CorpNameSearch1$SearchButton"=>"Search"
  }
  pg.form_with(:id => "aspnetForm") do |f|
    params.each{|k,v| f[k]=v}
    pg = f.submit
  end
  scrape(pg.body)
  pgno=2
  begin
    ne = Nokogiri::HTML(pg.body).xpath(".//div[@class='AspNet-GridView-Pagination AspNet-GridView-Bottom']/span/following-sibling::a")
    if ne.nil? or ne.empty?       
      break
    else
      params={
        "ctl00$ScriptManager1"=>"ctl00$DefaultContent$CorpNameSearch1$ResultsUpdatePanel|ctl00$DefaultContent$CorpNameSearch1$EntityGridView",
        "ctl00$DefaultContent$CorpNameSearch1$_singlename"=>srch,"__EVENTTARGET"=>"ctl00$DefaultContent$CorpNameSearch1$EntityGridView","__EVENTARGUMENT"=>"Page$#{pgno}"
      }
      pg.form_with(:id=>'aspnetForm') do |f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      scrape(pg.body)
      pgno = pgno + 1
    end
  end while(true)
  end
end

range = ('A'..'ZZZ').to_a.sort + (0..100).to_a
rstart = get_metadata("start",0)
range[rstart..-1].each_with_index{|srch,idx|
  action(srch)
  rstart = rstart + 1
  save_metadata("start",rstart)
}
delete_metadata("start")
#action("LOCKH")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.sos.ok.gov"

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
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//table[@summary='']/tbody/tr").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=>text(td[0].xpath("a")),
      "COMPANY_NAME"=>text(td[1].xpath("span")),
      "TYPE"=>text(td[2].xpath("span")),
      "NAME_TYPE"=>text(td[4].xpath("span"))[0],
      "STATUS"=>text(td[4].xpath("span"))[1],
      "DOC"=>Time.now
    }
    #puts r.inspect
    records << r unless r['NAME_TYPE']=='Tradename' or r['TYPE']=="Name Reservation" or r['TYPE']=="LLC Name Reservation" or r['STATUS']=='Former' or r['NAME_TYPE']=='Fictitious'
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length==0
  return records.length
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
  pg = br.get(BASE_URL+"/corp/corpInquiryFind.aspx")
  params = {
    "ctl00$ScriptManager1"=>"ctl00$ScriptManager1|ctl00$DefaultContent$CorpNameSearch1$SearchButton",
    "ctl00$DefaultContent$CorpNameSearch1$_singlename"=>srch,"ctl00$DefaultContent$CorpNameSearch1$SearchButton"=>"Search"
  }
  pg.form_with(:id => "aspnetForm") do |f|
    params.each{|k,v| f[k]=v}
    pg = f.submit
  end
  scrape(pg.body)
  pgno=2
  begin
    ne = Nokogiri::HTML(pg.body).xpath(".//div[@class='AspNet-GridView-Pagination AspNet-GridView-Bottom']/span/following-sibling::a")
    if ne.nil? or ne.empty?       
      break
    else
      params={
        "ctl00$ScriptManager1"=>"ctl00$DefaultContent$CorpNameSearch1$ResultsUpdatePanel|ctl00$DefaultContent$CorpNameSearch1$EntityGridView",
        "ctl00$DefaultContent$CorpNameSearch1$_singlename"=>srch,"__EVENTTARGET"=>"ctl00$DefaultContent$CorpNameSearch1$EntityGridView","__EVENTARGUMENT"=>"Page$#{pgno}"
      }
      pg.form_with(:id=>'aspnetForm') do |f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      scrape(pg.body)
      pgno = pgno + 1
    end
  end while(true)
  end
end

range = ('A'..'ZZZ').to_a.sort + (0..100).to_a
rstart = get_metadata("start",0)
range[rstart..-1].each_with_index{|srch,idx|
  action(srch)
  rstart = rstart + 1
  save_metadata("start",rstart)
}
delete_metadata("start")
#action("LOCKH")
