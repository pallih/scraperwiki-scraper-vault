# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.nebraska.gov/sos/corp/"

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
  Nokogiri::HTML(data).xpath(".//table[@class='bordered']/tr[position()<last()]").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME"=>text(td[0].xpath(".")),
      "COMPANY_NUMBER"=>text(td[1].xpath(".")),
      "TYPE"=>text(td[2].xpath(".")),
      "STATUS"=>text(td[3].xpath(".")),
      "URL"=> BASE_URL + attributes(td[4].xpath("a"),"href"),
      "DOC"=>Time.now
    }
    #puts r.inspect
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? or r["TYPE"]=~ /name/i
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
    s_url = BASE_URL+"corpsearch.cgi?search_type=keyword_search&status=&corpname=#{srch}&keyword_type=any&acct-num=&search=1"
    pg = br.get(s_url)
    scrape(pg.body)
    begin
      nex = pg.link_with(:text=>'Next Page')
      if nex.nil? 
        break
      else
        pg = br.click(nex)
        scrape(pg.body)
      end
    rescue Exception=>e
      puts "ERROR: While looping #{srch} :: #{e.inspect} :: #{e.backtrace}"
      break
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end

#save_metadata("STRT",0)
range = ('AAA'..'ZZZ').to_a + ('000'..'1000').to_a
strt = get_metadata("STRT",0)
strt = 0 if strt >= range.length
range.each_with_index{|srch,idx|
  next if idx < strt
  action(srch)
  save_metadata("STRT",idx.next)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.nebraska.gov/sos/corp/"

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
  Nokogiri::HTML(data).xpath(".//table[@class='bordered']/tr[position()<last()]").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME"=>text(td[0].xpath(".")),
      "COMPANY_NUMBER"=>text(td[1].xpath(".")),
      "TYPE"=>text(td[2].xpath(".")),
      "STATUS"=>text(td[3].xpath(".")),
      "URL"=> BASE_URL + attributes(td[4].xpath("a"),"href"),
      "DOC"=>Time.now
    }
    #puts r.inspect
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? or r["TYPE"]=~ /name/i
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
    s_url = BASE_URL+"corpsearch.cgi?search_type=keyword_search&status=&corpname=#{srch}&keyword_type=any&acct-num=&search=1"
    pg = br.get(s_url)
    scrape(pg.body)
    begin
      nex = pg.link_with(:text=>'Next Page')
      if nex.nil? 
        break
      else
        pg = br.click(nex)
        scrape(pg.body)
      end
    rescue Exception=>e
      puts "ERROR: While looping #{srch} :: #{e.inspect} :: #{e.backtrace}"
      break
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end

#save_metadata("STRT",0)
range = ('AAA'..'ZZZ').to_a + ('000'..'1000').to_a
strt = get_metadata("STRT",0)
strt = 0 if strt >= range.length
range.each_with_index{|srch,idx|
  next if idx < strt
  action(srch)
  save_metadata("STRT",idx.next)
}