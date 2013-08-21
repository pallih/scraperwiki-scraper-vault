# Blank Ruby
require 'nokogiri'
require 'mechanize'
require 'pp'
Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://www.ed.ac.uk/'
br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}


def strip(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/[\x80-\xff]|^\s+|:|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def getAttributes(t,attr)
    return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def get_field_names(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/[\x80-\xff]|^\s+|:|\s+|\s+$/,"_").upcase
  rescue Exception => e
      return str.text.upcase unless str.nil? 
      puts e.backtrace
  end
end

def get_urls
  return ScraperWiki.sqliteexecute("select url from peoplelist where name is not null or name =''")['data']
end

  
pg = br.get(BASE_URL + 'schools-departments/informatics/people/telephone')
Nokogiri::HTML(pg.body).xpath("//div[@class='inf-table']/table/tbody/tr").each{|tr|
  td = tr.xpath('td')
  
  begin
    records  = {}
    records['NAME'] = strip(td[1])
    records['URL'] = getAttributes(td[1].xpath('a'),'href')
    records['EMAIL'] = strip(td[2])
    records['EXTN'] = strip(td[3])
    records['OFFICE'] = strip(td[4])
  end unless td.nil? 
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=['EMAIL'],records,table_name="PEOPLELIST")
}


get_urls.each{|url|
  begin
    pg = br.get(url[0])
    doc = Nokogiri::HTML(pg.body)
    records = {}
    attr_names = []
    init_attr = nil
    doc.xpath("//dl[1]/dt/b").each{|b|
      attr_names << get_field_names(b)
      init_attr = strip(b) if init_attr.nil? 
    }
    
    attr_names.each_with_index{|attr,idx|
      val = ""
      doc.xpath("//dd[preceding-sibling::dt[#{idx+1}]/b/text()='#{init_attr}']").each{|v| 
        val << strip(v) <<"|" 
      }
      records[attr] = val.chomp("|")
    }
    temp = nil
    records.each{|k,v|
      if k =~ /,/
        attr = k.split(",")
        val = v.split(",")
        temp = Hash[*attr.zip(val).flatten]
        records.delete(k)
      end
    }
    records["NAME"] = strip(doc.xpath("//font[@size='+1']/b"))
    records = records.merge(temp) unless temp.nil? 
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['EMAIL_ADDRESS'],records,table_name="PEOPLEINFO") 
  rescue Exception => e
    puts "Error: While processing :: #{e.inspect} :: #{e.backtrace}"
  end

}

# Blank Ruby
require 'nokogiri'
require 'mechanize'
require 'pp'
Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://www.ed.ac.uk/'
br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}


def strip(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/[\x80-\xff]|^\s+|:|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def getAttributes(t,attr)
    return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def get_field_names(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/[\x80-\xff]|^\s+|:|\s+|\s+$/,"_").upcase
  rescue Exception => e
      return str.text.upcase unless str.nil? 
      puts e.backtrace
  end
end

def get_urls
  return ScraperWiki.sqliteexecute("select url from peoplelist where name is not null or name =''")['data']
end

  
pg = br.get(BASE_URL + 'schools-departments/informatics/people/telephone')
Nokogiri::HTML(pg.body).xpath("//div[@class='inf-table']/table/tbody/tr").each{|tr|
  td = tr.xpath('td')
  
  begin
    records  = {}
    records['NAME'] = strip(td[1])
    records['URL'] = getAttributes(td[1].xpath('a'),'href')
    records['EMAIL'] = strip(td[2])
    records['EXTN'] = strip(td[3])
    records['OFFICE'] = strip(td[4])
  end unless td.nil? 
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=['EMAIL'],records,table_name="PEOPLELIST")
}


get_urls.each{|url|
  begin
    pg = br.get(url[0])
    doc = Nokogiri::HTML(pg.body)
    records = {}
    attr_names = []
    init_attr = nil
    doc.xpath("//dl[1]/dt/b").each{|b|
      attr_names << get_field_names(b)
      init_attr = strip(b) if init_attr.nil? 
    }
    
    attr_names.each_with_index{|attr,idx|
      val = ""
      doc.xpath("//dd[preceding-sibling::dt[#{idx+1}]/b/text()='#{init_attr}']").each{|v| 
        val << strip(v) <<"|" 
      }
      records[attr] = val.chomp("|")
    }
    temp = nil
    records.each{|k,v|
      if k =~ /,/
        attr = k.split(",")
        val = v.split(",")
        temp = Hash[*attr.zip(val).flatten]
        records.delete(k)
      end
    }
    records["NAME"] = strip(doc.xpath("//font[@size='+1']/b"))
    records = records.merge(temp) unless temp.nil? 
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['EMAIL_ADDRESS'],records,table_name="PEOPLEINFO") 
  rescue Exception => e
    puts "Error: While processing :: #{e.inspect} :: #{e.backtrace}"
  end

}

