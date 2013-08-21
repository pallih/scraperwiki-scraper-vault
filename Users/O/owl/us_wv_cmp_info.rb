# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://apps.sos.wv.gov/"

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

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,num,url)
  records = {"DOC"=>Time.now,"COMPANY_NUMBER"=>num,"URL"=>url}
  doc = Nokogiri::HTML(data)
  records['COMPANY_NAME']=text(doc.xpath(".//span[@id='lblOrg']/text()"))
  begin
    doc.xpath(".//table[@id='tableResults'][1]/tr[position()>2]").each{|tr|
      td = tr.xpath("td")
      records['TYPE']=text(td[0].xpath("strong/text()"))
      records['EFFECTIVE_DT']=text(td[1].xpath("text()"))
      records['FILING_DT']=text(td[2].xpath("text()"))
      records['CHARTER']=text(td[3].xpath("text()"))
      records['CLASS']=text(td[4].xpath("text()"))
      records['SECTYPE']=text(td[5].xpath("text()"))
      records['TERMINATION_DT']=text(td[6].xpath("text()"))
      records['TERMINATION_REASON']=text(td[7].xpath("text()"))

    }
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2)
    return 0
  end unless records['COMPANY_NAME'].nil? or records['COMPANY_NAME'].empty? 
  return nil
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    pg = br.get(BASE_URL+"business/corporations/organization.aspx?org=#{num}") rescue nil
    return if pg.nil? 
    re = scrape(pg.body,num,pg.uri.to_s)
    save_metadata("OFFSET",num.next) unless re.nil? 
  end
end

#save_metadata("OFFSET",302800)
strt = get_metadata("OFFSET",302600)
endd = strt+50
(strt..endd).each{|num|
  action(num)
  sleep(2)
}
