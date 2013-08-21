# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.companies.gov.nu/pls/web/"

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


def scrape(data,act,s_url)
  if act == "list"
    lst = []
    Nokogiri::HTML(data).xpath(".//table[@cellspacing='5' and @cellpadding='0' and @border='0']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      lst << attributes(td[0].xpath("a"),"href")
    }
    return lst
  elsif act == "details"
    records = {'DOC'=>Time.now.to_s,"URL"=>s_url}
    Nokogiri::HTML(data).xpath(".//td/table[@width='100%' and @cellspacing='0'][1]/tr").each{|tr|
      td = tr.xpath("td")
      tmp_key = text(td[0].xpath("font/b/text()"))
      key = nil
      case tmp_key
        when /Company Number/
          key = "COMPANY_NUMBER"
        when /Company/
          key = "COMPANY_NAME"
        when /Incorporated/
          key = "CREATION_DT"
        when /Current Status/
          key = "STATUS"
        when /Entity Type/
          key = "TYPE"
        when /Annual Return Filing Month/
          key = "FILING_MONTH"
        else
          key = nil
      end
      records[key] = text(td[1].xpath("font/text()")) unless key.nil? 
    }
    records["STATUS"] = text(Nokogiri::HTML(data).xpath(".//td/table[3]/tr[2]/td[2]/font/text()")) if data =~ /Status Details/
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER','TYPE'],records,table_name='SWDATA',verbose=0) unless records['COMPANY_NUMBER'].nil? 
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    params = {'v_access_no'=>'DD276C9D3A1A7C1BF533958EA3CE2104', 'v_user_type'=>'C', 'v_search_type'=>'C', 'v_call_type'=>'', 'v_body_list'=>'', 'p_registry_country_code'=>'NU', 'v_compno'=>'', 'v_cname'=>srch, 'v_soundex'=>'CW', 'v_keyword'=>'', 'v_keyword2'=>'', 'Submit_Search.x'=>'0', 'Submit_Search.y'=>'0'}
    s_url = BASE_URL + "DBSVALCO.validate_company"
    pg = br.post(s_url,params,{'Cookie'=>'cmsdir="/cms"; LOOK2006-IS-ACTIVE="TRUE"; accessno=DD276C9D3A1A7C1BF533958EA3CE2104','Referer'=>BASE_URL+'pls/web/DBSVALCO.validate_company'})
    lst = scrape(pg.body,"list",nil)
    lst.each{|l_u|
      pg_l = br.get(BASE_URL+l_u,[],s_url,{'Cookie'=>'cmsdir="/cms"; LOOK2006-IS-ACTIVE="TRUE"; accessno=DD276C9D3A1A7C1BF533958EA3CE2104'})
      scrape(pg_l.body,"details",BASE_URL+l_u)
    }
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /Timeout|TIME|HTTP/
  end 
end


#save_metadata("OFFSET",0)
range = ('A'..'Z').to_a + (0..9).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  next if index < offset
  action(srch) 
  save_metadata("OFFSET",index.next)
end


