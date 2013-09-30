# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'
DATE = Time.new.tv_sec

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.ithala.co.za"

class String
  def join(str)
    return self+str
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
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def key(str)
  return str.gsub(/ /,'_').upcase
end

def scrape(data)
  records = []
  list = Nokogiri::HTML(data).xpath(".//table[@border='0' and @width='100%' and not(@id or @summary or @cellspacing)]")
 
  list.each{|ele|
    tbl = ele.xpath("tr")
    r = {}
    tbl.each{|tr|
      r[key(text(tr.xpath("td[@class='ms-stylelabel']")))] = text(tr.xpath("td[@class='ms-stylebody']"))
    }
    #puts r.inspect
    r['TOWN'], r['POSTAL-CODE'] = r['PHYSICAL_ADDRESS'].scan(/,([^,]+),[^,]*([0-9]{4})/)[-1]
    r['DATE-SCRAPED'] = DATE
    records << r unless r["BRANCH_NAME"].nil? or r["BRANCH_NAME"].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['BRANCH_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length
end

def action()
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  begin
    urls = ["/Ithala_Limited/LocateBranch/_layouts/inplview.aspx?List={C7398F88-2516-43D7-B2D0-0233D75CF315}&View={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}&ViewCount=306&ListViewPageUrl=http://www.ithala.co.za/Ithala_Limited/LocateBranch/Pages/default.aspx&IsXslView=TRUE&GroupString=%3B%23Central%3B%23&IsGroupRender=TRUE&WebPartID={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}","/Ithala_Limited/LocateBranch/_layouts/inplview.aspx?List={C7398F88-2516-43D7-B2D0-0233D75CF315}&View={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}&ViewCount=306&ListViewPageUrl=http://www.ithala.co.za/Ithala_Limited/LocateBranch/Pages/default.aspx&IsXslView=TRUE&GroupString=%3B%23East%3B%23&IsGroupRender=TRUE&WebPartID={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}","/Ithala_Limited/LocateBranch/_layouts/inplview.aspx?List={C7398F88-2516-43D7-B2D0-0233D75CF315}&View={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}&ViewCount=306&ListViewPageUrl=http://www.ithala.co.za/Ithala_Limited/LocateBranch/Pages/default.aspx&IsXslView=TRUE&GroupString=%3B%23Midlands%3B%23&IsGroupRender=TRUE&WebPartID={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}","/Ithala_Limited/LocateBranch/_layouts/inplview.aspx?List={C7398F88-2516-43D7-B2D0-0233D75CF315}&View={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}&ViewCount=306&ListViewPageUrl=http://www.ithala.co.za/Ithala_Limited/LocateBranch/Pages/default.aspx&IsXslView=TRUE&GroupString=%3B%23North%3B%23&IsGroupRender=TRUE&WebPartID={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}","/Ithala_Limited/LocateBranch/_layouts/inplview.aspx?List={C7398F88-2516-43D7-B2D0-0233D75CF315}&View={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}&ViewCount=306&ListViewPageUrl=http://www.ithala.co.za/Ithala_Limited/LocateBranch/Pages/default.aspx&IsXslView=TRUE&GroupString=%3B%23South%3B%23&IsGroupRender=TRUE&WebPartID={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}"]
  urls.each{|url|
    pg = br.get(BASE_URL+url)
    scrape(pg.body)
  }
  rescue Exception => e
   raise e
  end
end
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'
DATE = Time.new.tv_sec

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.ithala.co.za"

class String
  def join(str)
    return self+str
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
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def key(str)
  return str.gsub(/ /,'_').upcase
end

def scrape(data)
  records = []
  list = Nokogiri::HTML(data).xpath(".//table[@border='0' and @width='100%' and not(@id or @summary or @cellspacing)]")
 
  list.each{|ele|
    tbl = ele.xpath("tr")
    r = {}
    tbl.each{|tr|
      r[key(text(tr.xpath("td[@class='ms-stylelabel']")))] = text(tr.xpath("td[@class='ms-stylebody']"))
    }
    #puts r.inspect
    r['TOWN'], r['POSTAL-CODE'] = r['PHYSICAL_ADDRESS'].scan(/,([^,]+),[^,]*([0-9]{4})/)[-1]
    r['DATE-SCRAPED'] = DATE
    records << r unless r["BRANCH_NAME"].nil? or r["BRANCH_NAME"].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['BRANCH_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length
end

def action()
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  begin
    urls = ["/Ithala_Limited/LocateBranch/_layouts/inplview.aspx?List={C7398F88-2516-43D7-B2D0-0233D75CF315}&View={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}&ViewCount=306&ListViewPageUrl=http://www.ithala.co.za/Ithala_Limited/LocateBranch/Pages/default.aspx&IsXslView=TRUE&GroupString=%3B%23Central%3B%23&IsGroupRender=TRUE&WebPartID={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}","/Ithala_Limited/LocateBranch/_layouts/inplview.aspx?List={C7398F88-2516-43D7-B2D0-0233D75CF315}&View={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}&ViewCount=306&ListViewPageUrl=http://www.ithala.co.za/Ithala_Limited/LocateBranch/Pages/default.aspx&IsXslView=TRUE&GroupString=%3B%23East%3B%23&IsGroupRender=TRUE&WebPartID={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}","/Ithala_Limited/LocateBranch/_layouts/inplview.aspx?List={C7398F88-2516-43D7-B2D0-0233D75CF315}&View={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}&ViewCount=306&ListViewPageUrl=http://www.ithala.co.za/Ithala_Limited/LocateBranch/Pages/default.aspx&IsXslView=TRUE&GroupString=%3B%23Midlands%3B%23&IsGroupRender=TRUE&WebPartID={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}","/Ithala_Limited/LocateBranch/_layouts/inplview.aspx?List={C7398F88-2516-43D7-B2D0-0233D75CF315}&View={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}&ViewCount=306&ListViewPageUrl=http://www.ithala.co.za/Ithala_Limited/LocateBranch/Pages/default.aspx&IsXslView=TRUE&GroupString=%3B%23North%3B%23&IsGroupRender=TRUE&WebPartID={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}","/Ithala_Limited/LocateBranch/_layouts/inplview.aspx?List={C7398F88-2516-43D7-B2D0-0233D75CF315}&View={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}&ViewCount=306&ListViewPageUrl=http://www.ithala.co.za/Ithala_Limited/LocateBranch/Pages/default.aspx&IsXslView=TRUE&GroupString=%3B%23South%3B%23&IsGroupRender=TRUE&WebPartID={B7394C10-D9DE-4BEA-890D-C04F60A6DDEE}"]
  urls.each{|url|
    pg = br.get(BASE_URL+url)
    scrape(pg.body)
  }
  rescue Exception => e
   raise e
  end
end
action()