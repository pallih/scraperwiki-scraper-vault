# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://business.sos.state.ms.us/"

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
      return tmp.join("\n").strip
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,scraped_number,url)
  return nil if data=~ /Error: problems with the information./
  doc = Nokogiri::HTML(data,nil,"ISO-8859-1")
  r = {'DOC'=>Time.now,'SCRAPED_NUMBER'=>scraped_number,'URL'=>url}
  r['COMPANY_NAME']=text(doc.xpath(".//table[@width='98%' and @border='0']/tr[3]/td[1]"))
  #r['NAME_TYPE']=text(doc.xpath(".//table[@width='98%' and @border='0']/tr[3]/td[2]"))
  r['TYPE']=text(doc.xpath(".//table[@width='98%' and @border='0']/tr[5]/td[1]/font"))
  doc.xpath(".//table[@width='98%' and @border='0']/tr[position()>5 and count(td)=2]").each{|tr|
    td = tr.xpath("td")
    tmp_key = text(td[0].xpath("font/b|b/font"))
    value = text(td[1].xpath("font"))
    case tmp_key
      when "Business ID:"
        key = "COMPANY_NUMBER"
      when "Status:"
        key = "STATUS"
      when "Creation Date:"
        key = "CREATION_DT"
      #when "State of Incorporation:"
      #  key = "INCORP_ST"
      #when "Principal Office Address:"
      #  key = "ADDR1"
      #when "Listing Address:"
      #  key = "ADDR2"
      else
        key = nil
    end
    r[key]=value unless key.nil? 
  }
  ScraperWiki.save_sqlite(unique_keys=['SCRAPED_NUMBER'],r,table_name='swdata',verbose=2) unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? or r['STATUS'] =~ /Reserved Name/
  return r['COMPANY_NUMBER']
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE      
    }
    s_url = BASE_URL+"corp/soskb/Corp.asp?#{num}"
    pg = br.get(s_url,[],"https://business.sos.state.ms.us/corp/soskb/CSearch.asp?dtm=590902777777778")
    return scrape(pg.body,num,s_url)
  end
end

#save_metadata("OFFSET",594890)
strt = get_metadata("OFFSET",562407).to_i
endd = strt+50
(strt..endd).each{|num|
  ret = action(num)
  save_metadata("OFFSET",num.next) unless ret.nil? or ret.empty? 
  sleep(10)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://business.sos.state.ms.us/"

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
      return tmp.join("\n").strip
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,scraped_number,url)
  return nil if data=~ /Error: problems with the information./
  doc = Nokogiri::HTML(data,nil,"ISO-8859-1")
  r = {'DOC'=>Time.now,'SCRAPED_NUMBER'=>scraped_number,'URL'=>url}
  r['COMPANY_NAME']=text(doc.xpath(".//table[@width='98%' and @border='0']/tr[3]/td[1]"))
  #r['NAME_TYPE']=text(doc.xpath(".//table[@width='98%' and @border='0']/tr[3]/td[2]"))
  r['TYPE']=text(doc.xpath(".//table[@width='98%' and @border='0']/tr[5]/td[1]/font"))
  doc.xpath(".//table[@width='98%' and @border='0']/tr[position()>5 and count(td)=2]").each{|tr|
    td = tr.xpath("td")
    tmp_key = text(td[0].xpath("font/b|b/font"))
    value = text(td[1].xpath("font"))
    case tmp_key
      when "Business ID:"
        key = "COMPANY_NUMBER"
      when "Status:"
        key = "STATUS"
      when "Creation Date:"
        key = "CREATION_DT"
      #when "State of Incorporation:"
      #  key = "INCORP_ST"
      #when "Principal Office Address:"
      #  key = "ADDR1"
      #when "Listing Address:"
      #  key = "ADDR2"
      else
        key = nil
    end
    r[key]=value unless key.nil? 
  }
  ScraperWiki.save_sqlite(unique_keys=['SCRAPED_NUMBER'],r,table_name='swdata',verbose=2) unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? or r['STATUS'] =~ /Reserved Name/
  return r['COMPANY_NUMBER']
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE      
    }
    s_url = BASE_URL+"corp/soskb/Corp.asp?#{num}"
    pg = br.get(s_url,[],"https://business.sos.state.ms.us/corp/soskb/CSearch.asp?dtm=590902777777778")
    return scrape(pg.body,num,s_url)
  end
end

#save_metadata("OFFSET",594890)
strt = get_metadata("OFFSET",562407).to_i
endd = strt+50
(strt..endd).each{|num|
  ret = action(num)
  save_metadata("OFFSET",num.next) unless ret.nil? or ret.empty? 
  sleep(10)
}