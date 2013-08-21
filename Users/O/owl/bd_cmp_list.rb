# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.roc.gov.bd:7781"

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    retry
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

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'') }
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
  doc = Nokogiri::HTML(data).xpath(".//table[@width='650' and @cellpadding='2']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME" => text(td[1].xpath("font")),
      "TYPE"=>text(td[2].xpath("font")),
      "DOC" => Time.now
    }
    r['STATUS'],t2 = text(td[3].xpath("font")).split("[")
    r['COMPANY_NUMBER']=t2.scan(/Reg. No. (.*) \]/).flatten.first if t2 =~ /Reg/
    records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
    
  }
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length==0
  return doc.length
end

def action(srch)
  begin
    br = Mechanize.new {|b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 12000
      b.max_history = 0
      b.log = Logger.new(STDERR)
    }
    pg_no = get_metadata("PG_NO",1)
    params = {"entity_type"=>1,"search_text"=>srch,"CB"=>1,"result_type"=>0,"p_entry_mode"=>3,"page_no"=>pg_no}
    s_url = URI(BASE_URL + "/psp/nc_search")
    begin 
      pg = br.post(s_url,params)
      scrape(pg.body)
      nex = pg.at("input[@name='b_Next1']")
      break if nex.nil? 
      pg_no = pg_no +1 
      params['page_no']=pg_no
    end while(true)
  end
end

range = (0..9).to_a + ('A0'..'Z9').to_a + ('A'..'ZZZ').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch)
  save_metadata("OFFSET",idx.next)
}