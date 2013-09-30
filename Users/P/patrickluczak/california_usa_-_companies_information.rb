require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "https://businessfilings.sos.ca.gov/frmDetail.asp"

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
        puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{default})"
    end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\302\240|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action,num,url)
  if action == "details"
    doc = Nokogiri::HTML(data)
    records = {"SCRAPED_NUMBER"=>num,"URL"=>url,"DOC"=>Time.now.to_s}
    td = doc.xpath("//table[@width='75%']/tr[position()>1 and position()<last()-3]/td")
    begin
      records['COMPANY_NAME'] = text(td[0])
      records['COMPANY_NUMBER'] = text(td[1]).split(":")[1]
      records['CREATION_DT'] = text(td[2]).split(":")[1]
      records['STATUS'] = text(td[3]).split(":")[1]
      records['PLACE'] = text(td[4]).split(":")[1]
      records['TYPE'] = text(td[5]).split(":")[1]
      records['ADDR'] = text(td[7])+text(td[8])
    end unless td.nil? 
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name='CMPINFO') unless records['COMPANY_NUMBER'].nil? 
    return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0
  end
  return nil
end

def is_available(num)
  return ScraperWiki.sqliteexecute("select count(*) from cmpinfo where scraped_number=?",[num])['data'][0][0]
end

def get_list()
  return ScraperWiki.sqliteexecute("select scraped_number from cmpinfo")['data']
end
def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
      b.retry_change_requests = true
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
    s_url = BASE_URL+"?CorpID="+"%08d" % num
    pg = br.get(s_url)
    re = scrape(pg.body,"details",num,s_url)
    save_metadata("INDEX",num.next) unless re.nil? 
  end if is_available(num) == 0
    
end

#puts get_list.inspect
#save_metadata("INDEX",3414607)
strt = get_metadata("INDEX",1).to_i
endd = strt + 2000
(strt..endd).each{|num|
  action(num)
}
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "https://businessfilings.sos.ca.gov/frmDetail.asp"

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
        puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{default})"
    end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\302\240|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action,num,url)
  if action == "details"
    doc = Nokogiri::HTML(data)
    records = {"SCRAPED_NUMBER"=>num,"URL"=>url,"DOC"=>Time.now.to_s}
    td = doc.xpath("//table[@width='75%']/tr[position()>1 and position()<last()-3]/td")
    begin
      records['COMPANY_NAME'] = text(td[0])
      records['COMPANY_NUMBER'] = text(td[1]).split(":")[1]
      records['CREATION_DT'] = text(td[2]).split(":")[1]
      records['STATUS'] = text(td[3]).split(":")[1]
      records['PLACE'] = text(td[4]).split(":")[1]
      records['TYPE'] = text(td[5]).split(":")[1]
      records['ADDR'] = text(td[7])+text(td[8])
    end unless td.nil? 
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name='CMPINFO') unless records['COMPANY_NUMBER'].nil? 
    return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0
  end
  return nil
end

def is_available(num)
  return ScraperWiki.sqliteexecute("select count(*) from cmpinfo where scraped_number=?",[num])['data'][0][0]
end

def get_list()
  return ScraperWiki.sqliteexecute("select scraped_number from cmpinfo")['data']
end
def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
      b.retry_change_requests = true
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
    s_url = BASE_URL+"?CorpID="+"%08d" % num
    pg = br.get(s_url)
    re = scrape(pg.body,"details",num,s_url)
    save_metadata("INDEX",num.next) unless re.nil? 
  end if is_available(num) == 0
    
end

#puts get_list.inspect
#save_metadata("INDEX",3414607)
strt = get_metadata("INDEX",1).to_i
endd = strt + 2000
(strt..endd).each{|num|
  action(num)
}
