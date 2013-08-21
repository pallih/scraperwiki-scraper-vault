# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/cf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.companies.gov.nu/pls/web/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/^,|,$/,'').strip
  end
end

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"").strip
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
    records = []
    Nokogiri::HTML(data).xpath(".//table[@cellspacing='5']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records << {
        #"company_number" => text(td[0].xpath("./a/font/text()")),
        #"company_name" => text(td[1].xpath("./a/font/text()")),
        #"type" => text(td[2].xpath("./a/text()")),
        #"status" => text(td[3].xpath("./a/text()")),
        "tmp_url" => BASE_URL + attributes(td[0].xpath("./a"),"href"),
        #"doc" => Time.now
      }
    }
    return records
  elsif act == "details"
    r = {"doc"=>Time.now}
    doc = Nokogiri::HTML(data).xpath(".//td[@align='center' and @colspan='3']/table[@width='90%']")
    r["company_number"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Company Number']]/following-sibling::*[1][self::td]/font/text()"))
    r["company_name"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Company']]/following-sibling::*[1][self::td]/font/text()"))
    r["incorporated"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Incorporated']]/following-sibling::*[1][self::td]/font/text()"))
    r["status"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Current Status']]/following-sibling::*[1][self::td]/font/text()"))
    r["type"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Entity Type']]/following-sibling::*[1][self::td]/font/text()"))
    r["filing_month"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Annual Return Filing Month']]/following-sibling::*[1][self::td]/font/text()"))

    tmp = []
    doc.xpath(".//tr[td/font/b[normalize-space(text())='Previous Names']]/following-sibling::*[1][self::tr]/td[@colspan='4' and not(@valign)]/table[@width='100%']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      tmp << {
        "company_name" => s_text(td[0].xpath("./font/text()")),
        "changed_dt" => s_text(td[1].xpath("./font/text()")),
      }
    }
    r["previous_names"] = JSON.generate tmp unless tmp.empty? 
    r["address"] = a_text(doc.xpath(".//tr[td/font/b[normalize-space(text())='Registered Office']]/following-sibling::*[following-sibling::tr[td/font/b[normalize-space(text())='Directors']]]/td/font")).join(",").pretty
    tmp = []
    doc.xpath(".//tr[td/font/b[normalize-space(text())='Directors']]/following-sibling::*[3][self::tr]/td/table/tr[count(td)=2]").each{|tr|
      td = tr.xpath("td")
      tmp << {
        "name" => s_text(td[0].xpath("./font/text()")),
        "appointed_dt" => s_text(td[1].xpath("./font/text()")),
        "address" => s_text(tr.xpath("./following-sibling::*[1][self::tr]/td/font/text()"))
      }
    }
    r["directors"] = JSON.generate tmp unless tmp.empty? 
    tmp = []
    doc.xpath(".//tr[td/font/b[normalize-space(text())='Documents Registered']]/following-sibling::*[2][self::tr]/td/table/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      tmp << {
        "published_dt" => s_text(td[1].xpath("./a/font[1]/text()")),
        "published_time" => s_text(td[1].xpath("./a/font[2]/text()")),
        "barcode" => s_text(td[2].xpath("./a/font/text()")),
        "description" => s_text(td[3].xpath("./a/font/text()")),
        "file-size" => s_text(td[4].xpath("./a/font/text()")),
        "link" => BASE_URL + attributes(td[1].xpath("./a"),"href")
      }
    }
    r["documents"] = JSON.generate tmp unless tmp.empty? 
    r["coi_link"] = BASE_URL + attributes(doc.xpath(".//a[normalize-space(text())='View Certificate Of Incorporation']"),"href")

    return r
  end
end

def action(srch)
  begin
    @pg = @br.post("http://www.companies.gov.nu/pls/web/DBSSEARC.searchdb",
      "v_access_no=#{@access_no}&v_user_type=C&v_search_type=C&v_call_type=&v_body_list=&New_Search.x=24&New_Search.y=16",
      {"Content-Type"=>"application/x-www-form-urlencoded"}) if @pg.nil? 
    params = {"v_cname"=>srch,"Submit_Search.x"=>39,"Submit_Search.y"=>12}
    pg_tmp = nil
    raise "error" if @pg.body =~ /An error has occurred while processing your request/
    @pg.form_with(:action=>"DBSVALCO.validate_company") do |f|
      params.each{|k,v| f[k] = v}
      pg_tmp = f.submit
    end
    list = scrape(pg_tmp.body,"list",{})
    list.each{|rec|
      record = scrape(@br.get(rec['tmp_url']).body,"details",nil)
      ScraperWiki.save_sqlite(unique_keys=['company_number'],record)
    }
  end 
end

pg_main = @br.get("http://www.companies.gov.nu/pls/web/dbsportal.cms_application_call?p_option=CNAME")
@access_no = pg_main.body.scan(/accessno=(.*); path=/).flatten.first



#save_metadata("OFFSET",0)
range = ('A'..'Z').to_a + (0..9).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  next if index < offset
  action(srch) 
  save_metadata("OFFSET",index.next)
end


# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/cf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.companies.gov.nu/pls/web/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/^,|,$/,'').strip
  end
end

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"").strip
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
    records = []
    Nokogiri::HTML(data).xpath(".//table[@cellspacing='5']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records << {
        #"company_number" => text(td[0].xpath("./a/font/text()")),
        #"company_name" => text(td[1].xpath("./a/font/text()")),
        #"type" => text(td[2].xpath("./a/text()")),
        #"status" => text(td[3].xpath("./a/text()")),
        "tmp_url" => BASE_URL + attributes(td[0].xpath("./a"),"href"),
        #"doc" => Time.now
      }
    }
    return records
  elsif act == "details"
    r = {"doc"=>Time.now}
    doc = Nokogiri::HTML(data).xpath(".//td[@align='center' and @colspan='3']/table[@width='90%']")
    r["company_number"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Company Number']]/following-sibling::*[1][self::td]/font/text()"))
    r["company_name"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Company']]/following-sibling::*[1][self::td]/font/text()"))
    r["incorporated"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Incorporated']]/following-sibling::*[1][self::td]/font/text()"))
    r["status"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Current Status']]/following-sibling::*[1][self::td]/font/text()"))
    r["type"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Entity Type']]/following-sibling::*[1][self::td]/font/text()"))
    r["filing_month"] = s_text(doc.xpath(".//td[font/b[normalize-space(text())='Annual Return Filing Month']]/following-sibling::*[1][self::td]/font/text()"))

    tmp = []
    doc.xpath(".//tr[td/font/b[normalize-space(text())='Previous Names']]/following-sibling::*[1][self::tr]/td[@colspan='4' and not(@valign)]/table[@width='100%']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      tmp << {
        "company_name" => s_text(td[0].xpath("./font/text()")),
        "changed_dt" => s_text(td[1].xpath("./font/text()")),
      }
    }
    r["previous_names"] = JSON.generate tmp unless tmp.empty? 
    r["address"] = a_text(doc.xpath(".//tr[td/font/b[normalize-space(text())='Registered Office']]/following-sibling::*[following-sibling::tr[td/font/b[normalize-space(text())='Directors']]]/td/font")).join(",").pretty
    tmp = []
    doc.xpath(".//tr[td/font/b[normalize-space(text())='Directors']]/following-sibling::*[3][self::tr]/td/table/tr[count(td)=2]").each{|tr|
      td = tr.xpath("td")
      tmp << {
        "name" => s_text(td[0].xpath("./font/text()")),
        "appointed_dt" => s_text(td[1].xpath("./font/text()")),
        "address" => s_text(tr.xpath("./following-sibling::*[1][self::tr]/td/font/text()"))
      }
    }
    r["directors"] = JSON.generate tmp unless tmp.empty? 
    tmp = []
    doc.xpath(".//tr[td/font/b[normalize-space(text())='Documents Registered']]/following-sibling::*[2][self::tr]/td/table/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      tmp << {
        "published_dt" => s_text(td[1].xpath("./a/font[1]/text()")),
        "published_time" => s_text(td[1].xpath("./a/font[2]/text()")),
        "barcode" => s_text(td[2].xpath("./a/font/text()")),
        "description" => s_text(td[3].xpath("./a/font/text()")),
        "file-size" => s_text(td[4].xpath("./a/font/text()")),
        "link" => BASE_URL + attributes(td[1].xpath("./a"),"href")
      }
    }
    r["documents"] = JSON.generate tmp unless tmp.empty? 
    r["coi_link"] = BASE_URL + attributes(doc.xpath(".//a[normalize-space(text())='View Certificate Of Incorporation']"),"href")

    return r
  end
end

def action(srch)
  begin
    @pg = @br.post("http://www.companies.gov.nu/pls/web/DBSSEARC.searchdb",
      "v_access_no=#{@access_no}&v_user_type=C&v_search_type=C&v_call_type=&v_body_list=&New_Search.x=24&New_Search.y=16",
      {"Content-Type"=>"application/x-www-form-urlencoded"}) if @pg.nil? 
    params = {"v_cname"=>srch,"Submit_Search.x"=>39,"Submit_Search.y"=>12}
    pg_tmp = nil
    raise "error" if @pg.body =~ /An error has occurred while processing your request/
    @pg.form_with(:action=>"DBSVALCO.validate_company") do |f|
      params.each{|k,v| f[k] = v}
      pg_tmp = f.submit
    end
    list = scrape(pg_tmp.body,"list",{})
    list.each{|rec|
      record = scrape(@br.get(rec['tmp_url']).body,"details",nil)
      ScraperWiki.save_sqlite(unique_keys=['company_number'],record)
    }
  end 
end

pg_main = @br.get("http://www.companies.gov.nu/pls/web/dbsportal.cms_application_call?p_option=CNAME")
@access_no = pg_main.body.scan(/accessno=(.*); path=/).flatten.first



#save_metadata("OFFSET",0)
range = ('A'..'Z').to_a + (0..9).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  next if index < offset
  action(srch) 
  save_metadata("OFFSET",index.next)
end


