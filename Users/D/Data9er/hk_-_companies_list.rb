# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.icris.cr.gov.hk/"

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


def scrape(scraped_number,data)
  records = {'SCRAPED_NUMBER'=>scraped_number}
  return if data.nil? or data.empty? 
  Nokogiri::HTML(data).xpath(".//table[@width='99%' and not(@class)]/tr").each{|tr|
      td = tr.xpath("td")
      tmp_key = text(td[0].xpath("."))
      value = text(td[1].xpath("."))
      key = nil
      case tmp_key
        when "CR No.:"
          key = "COMPANY_NUMBER"
          value = text(td[1].xpath("font"))
        when "Company Name:"
          key = ["COMPANY_NAME","COMPANY_NAME_RL"]
          #value = value.join("|") if value.kind_of?(Array)
          value = value.split(/\r/)
        when "Company Type:"
          key = "TYPE"
        #when "Date of Incorporation:"
        #  key = "INC_DT"
        #when "Company Status:"
        #  key = "LISTING_STATUS"
        when "Active Status:"
          key = "STATUS"
        #when "Remarks:"
        #  key = "REMARKS"
        #when "Winding Up Mode:"
        #  key = "W_MODE"
        #when "Date of Dissolution:"
        #  key = "DIS_DT"
        #when "Important Note:"
        #  key = "NOTE"
        else
          key = nil
      end
      if key.kind_of?(Array)
        key.zip(value) {|k,v| records[k]=v}
      else
        records[key]=value unless key.nil? 
      end
  }
  return ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
end

def action(srch)
  begin
    params = {'nextAction'=>'cps_criteria', 'searchPage'=>'True', 'DPDSInd'=>'true', 'searchMode'=>'BYCRNO', 'radioButton'=>'BYCRNO', 'CRNo'=>srch, 'mode'=>'EXACT+NAME', 'showMedium'=>'true', 'language'=>'en', 'companyName'=>'', 'page'=>'1'}
    headers = {"Cookie"=>"JSESSIONID=PBcyvh2LQX4GL3zJ7hD2bMnGXzgQzpXbhdvchLNvhm8LhTR2yjg2!-476690198"}
    pg = @br.post(BASE_URL+"csci/cps_criteria.do",params)
    cmpname=text(pg.at(".//span[@class='coyname']"))
    if pg.body =~ /temporarily suspended|NO MATCHING RECORD FOUND FOR THE SEARCH INFORMATION INPUT/
      puts "Looks like the service provider went offline"
      exit
    elsif cmpname.nil? or cmpname.empty? or pg.body =~ /normal.html/i
      sleep(2)
      raise("retry:: #{cmpname}")
    else
      sleep(1)
    end
    return scrape(srch,pg.body)
  end
end


@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 2400
  b.max_history = 0
}
@br.get(BASE_URL+"csci/clearsession.jsp?user_type=iguest")
@br.get(BASE_URL+"csci/login_i.do?loginType=iguest&username=iguest")


strt = get_metadata("STRT",1695943)
endd = strt + 200

(strt..endd).each{|srch|
  resp = action(srch)
  save_metadata("STRT",srch.next) if resp['nrecords'] >= 1 unless resp.nil? or resp['nrecords'].nil? 
}

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.icris.cr.gov.hk/"

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


def scrape(scraped_number,data)
  records = {'SCRAPED_NUMBER'=>scraped_number}
  return if data.nil? or data.empty? 
  Nokogiri::HTML(data).xpath(".//table[@width='99%' and not(@class)]/tr").each{|tr|
      td = tr.xpath("td")
      tmp_key = text(td[0].xpath("."))
      value = text(td[1].xpath("."))
      key = nil
      case tmp_key
        when "CR No.:"
          key = "COMPANY_NUMBER"
          value = text(td[1].xpath("font"))
        when "Company Name:"
          key = ["COMPANY_NAME","COMPANY_NAME_RL"]
          #value = value.join("|") if value.kind_of?(Array)
          value = value.split(/\r/)
        when "Company Type:"
          key = "TYPE"
        #when "Date of Incorporation:"
        #  key = "INC_DT"
        #when "Company Status:"
        #  key = "LISTING_STATUS"
        when "Active Status:"
          key = "STATUS"
        #when "Remarks:"
        #  key = "REMARKS"
        #when "Winding Up Mode:"
        #  key = "W_MODE"
        #when "Date of Dissolution:"
        #  key = "DIS_DT"
        #when "Important Note:"
        #  key = "NOTE"
        else
          key = nil
      end
      if key.kind_of?(Array)
        key.zip(value) {|k,v| records[k]=v}
      else
        records[key]=value unless key.nil? 
      end
  }
  return ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
end

def action(srch)
  begin
    params = {'nextAction'=>'cps_criteria', 'searchPage'=>'True', 'DPDSInd'=>'true', 'searchMode'=>'BYCRNO', 'radioButton'=>'BYCRNO', 'CRNo'=>srch, 'mode'=>'EXACT+NAME', 'showMedium'=>'true', 'language'=>'en', 'companyName'=>'', 'page'=>'1'}
    headers = {"Cookie"=>"JSESSIONID=PBcyvh2LQX4GL3zJ7hD2bMnGXzgQzpXbhdvchLNvhm8LhTR2yjg2!-476690198"}
    pg = @br.post(BASE_URL+"csci/cps_criteria.do",params)
    cmpname=text(pg.at(".//span[@class='coyname']"))
    if pg.body =~ /temporarily suspended|NO MATCHING RECORD FOUND FOR THE SEARCH INFORMATION INPUT/
      puts "Looks like the service provider went offline"
      exit
    elsif cmpname.nil? or cmpname.empty? or pg.body =~ /normal.html/i
      sleep(2)
      raise("retry:: #{cmpname}")
    else
      sleep(1)
    end
    return scrape(srch,pg.body)
  end
end


@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 2400
  b.max_history = 0
}
@br.get(BASE_URL+"csci/clearsession.jsp?user_type=iguest")
@br.get(BASE_URL+"csci/login_i.do?loginType=iguest&username=iguest")


strt = get_metadata("STRT",1695943)
endd = strt + 200

(strt..endd).each{|srch|
  resp = action(srch)
  save_metadata("STRT",srch.next) if resp['nrecords'] >= 1 unless resp.nil? or resp['nrecords'].nil? 
}

