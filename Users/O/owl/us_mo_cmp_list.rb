# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.sos.mo.gov/BusinessEntity/soskb/"

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
  Nokogiri::HTML(data).xpath(".//table[@width='98%']/tr[position()>3]").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME"=>text(td[0].xpath("font/a")),
      "COMPANY_NUMBER"=>text(td[1].xpath("font/a")),
      "TYPE"=>text(td[2].xpath("center")),
      "STATUS"=>text(td[3].xpath("center")),
      "CREATION_DT"=>text(td[4].xpath("font")),
      "URL"=> BASE_URL+attributes(td[0].xpath("font/a"),"href"),
      "DOC"=>Time.now
    }
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL+"SearchResults.asp?FormName=CorpNameSearch&Words=Starting&SearchStr=#{srch}&SearchType=Search"
    pg = br.get(s_url)
    offset = get_metadata("OFFSET",0)
    scrape(pg.body)
    begin
      nex = pg.at("input[@value='Next 50 >>']")
      if nex.nil? 
        break
      else
        params = {"FormName"=>"CorpNameSearch","searchstr"=>srch,"TopRec"=>offset,"Pos"=>"Next 50 >>"}
        pg.form_with(:name=>"CorpNameSearch") do |f|
          params.each{|k,v| f[k]=v }
          pg = f.submit
        end
        scrape(pg.body)
        offset = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@name='TopRec']"),"value")
        save_metadata("OFFSET",offset)
      end
    rescue Exception=>e
      puts "ERROR: While looping #{srch} :: #{e.inspect} :: #{e.backtrace}"
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry
  end
  delete_metadata("OFFSET")
end

range = ['#','@','%','^','&','(','!',')','*'].to_a + (0..10).to_a + ('A'..'Z').to_a
strt = get_metadata("STRT",0)
strt = 0 if strt >= range.length
range.each_with_index{|srch,idx|
  next if idx<strt  
  action("A")
  save_metadata("STRT",idx.next)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.sos.mo.gov/BusinessEntity/soskb/"

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
  Nokogiri::HTML(data).xpath(".//table[@width='98%']/tr[position()>3]").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME"=>text(td[0].xpath("font/a")),
      "COMPANY_NUMBER"=>text(td[1].xpath("font/a")),
      "TYPE"=>text(td[2].xpath("center")),
      "STATUS"=>text(td[3].xpath("center")),
      "CREATION_DT"=>text(td[4].xpath("font")),
      "URL"=> BASE_URL+attributes(td[0].xpath("font/a"),"href"),
      "DOC"=>Time.now
    }
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL+"SearchResults.asp?FormName=CorpNameSearch&Words=Starting&SearchStr=#{srch}&SearchType=Search"
    pg = br.get(s_url)
    offset = get_metadata("OFFSET",0)
    scrape(pg.body)
    begin
      nex = pg.at("input[@value='Next 50 >>']")
      if nex.nil? 
        break
      else
        params = {"FormName"=>"CorpNameSearch","searchstr"=>srch,"TopRec"=>offset,"Pos"=>"Next 50 >>"}
        pg.form_with(:name=>"CorpNameSearch") do |f|
          params.each{|k,v| f[k]=v }
          pg = f.submit
        end
        scrape(pg.body)
        offset = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@name='TopRec']"),"value")
        save_metadata("OFFSET",offset)
      end
    rescue Exception=>e
      puts "ERROR: While looping #{srch} :: #{e.inspect} :: #{e.backtrace}"
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry
  end
  delete_metadata("OFFSET")
end

range = ['#','@','%','^','&','(','!',')','*'].to_a + (0..10).to_a + ('A'..'Z').to_a
strt = get_metadata("STRT",0)
strt = 0 if strt >= range.length
range.each_with_index{|srch,idx|
  next if idx<strt  
  action("A")
  save_metadata("STRT",idx.next)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.sos.mo.gov/BusinessEntity/soskb/"

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
  Nokogiri::HTML(data).xpath(".//table[@width='98%']/tr[position()>3]").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME"=>text(td[0].xpath("font/a")),
      "COMPANY_NUMBER"=>text(td[1].xpath("font/a")),
      "TYPE"=>text(td[2].xpath("center")),
      "STATUS"=>text(td[3].xpath("center")),
      "CREATION_DT"=>text(td[4].xpath("font")),
      "URL"=> BASE_URL+attributes(td[0].xpath("font/a"),"href"),
      "DOC"=>Time.now
    }
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL+"SearchResults.asp?FormName=CorpNameSearch&Words=Starting&SearchStr=#{srch}&SearchType=Search"
    pg = br.get(s_url)
    offset = get_metadata("OFFSET",0)
    scrape(pg.body)
    begin
      nex = pg.at("input[@value='Next 50 >>']")
      if nex.nil? 
        break
      else
        params = {"FormName"=>"CorpNameSearch","searchstr"=>srch,"TopRec"=>offset,"Pos"=>"Next 50 >>"}
        pg.form_with(:name=>"CorpNameSearch") do |f|
          params.each{|k,v| f[k]=v }
          pg = f.submit
        end
        scrape(pg.body)
        offset = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@name='TopRec']"),"value")
        save_metadata("OFFSET",offset)
      end
    rescue Exception=>e
      puts "ERROR: While looping #{srch} :: #{e.inspect} :: #{e.backtrace}"
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry
  end
  delete_metadata("OFFSET")
end

range = ['#','@','%','^','&','(','!',')','*'].to_a + (0..10).to_a + ('A'..'Z').to_a
strt = get_metadata("STRT",0)
strt = 0 if strt >= range.length
range.each_with_index{|srch,idx|
  next if idx<strt  
  action("A")
  save_metadata("STRT",idx.next)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.sos.mo.gov/BusinessEntity/soskb/"

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
  Nokogiri::HTML(data).xpath(".//table[@width='98%']/tr[position()>3]").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME"=>text(td[0].xpath("font/a")),
      "COMPANY_NUMBER"=>text(td[1].xpath("font/a")),
      "TYPE"=>text(td[2].xpath("center")),
      "STATUS"=>text(td[3].xpath("center")),
      "CREATION_DT"=>text(td[4].xpath("font")),
      "URL"=> BASE_URL+attributes(td[0].xpath("font/a"),"href"),
      "DOC"=>Time.now
    }
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL+"SearchResults.asp?FormName=CorpNameSearch&Words=Starting&SearchStr=#{srch}&SearchType=Search"
    pg = br.get(s_url)
    offset = get_metadata("OFFSET",0)
    scrape(pg.body)
    begin
      nex = pg.at("input[@value='Next 50 >>']")
      if nex.nil? 
        break
      else
        params = {"FormName"=>"CorpNameSearch","searchstr"=>srch,"TopRec"=>offset,"Pos"=>"Next 50 >>"}
        pg.form_with(:name=>"CorpNameSearch") do |f|
          params.each{|k,v| f[k]=v }
          pg = f.submit
        end
        scrape(pg.body)
        offset = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@name='TopRec']"),"value")
        save_metadata("OFFSET",offset)
      end
    rescue Exception=>e
      puts "ERROR: While looping #{srch} :: #{e.inspect} :: #{e.backtrace}"
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry
  end
  delete_metadata("OFFSET")
end

range = ['#','@','%','^','&','(','!',')','*'].to_a + (0..10).to_a + ('A'..'Z').to_a
strt = get_metadata("STRT",0)
strt = 0 if strt >= range.length
range.each_with_index{|srch,idx|
  next if idx<strt  
  action("A")
  save_metadata("STRT",idx.next)
}