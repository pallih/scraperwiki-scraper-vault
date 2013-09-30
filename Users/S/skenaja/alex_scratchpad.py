# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'logger'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://delecorp.delaware.gov"

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
  end
end

def delete_metadata(name)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{name}"
  end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil?
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    Nokogiri::HTML(data).xpath(".//table[@width='554']/tbody/tr[position()>1]").each do|tr|
      td = tr.xpath("td")
      records = {
         "COMPANY_NUMBER" => text(td[0].xpath("a/text()")),
         "COMPANY_NAME" => text(td[1].xpath("a/text()")),
         "Entity_Kind" => text(td[2].xpath("a/text()")),
         "State" => text(td[3].xpath("a/text()")),
         "DOC" => Time.now.to_s
      }
      puts records.inspect
      #ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=0) unless records['COMPANY_NUMBER'].nil?
      #sleep(1)
    end
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 12000
    }
    pg = br.get(BASE_URL+"/tin/GINameSearch.jsp")
    params = {'JSPName'=>'GINAMESEARCH', 'frmEntityName'=>srch, 'frmFileNumber'=>'', 'action'=>'Search'}
    pg = br.post(BASE_URL+"/tin/controller",params)
    scrape(pg.body,"list")
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    #sleep(30)
    #retry if e.inspect =~ /Timeout|HTTP|TIMED|/
  end
end




range = ('A'..'ZZZZ').to_a + (0..9999).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next if index < offset
  action("#{srch}")
end


# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'logger'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://delecorp.delaware.gov"

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
  end
end

def delete_metadata(name)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{name}"
  end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil?
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    Nokogiri::HTML(data).xpath(".//table[@width='554']/tbody/tr[position()>1]").each do|tr|
      td = tr.xpath("td")
      records = {
         "COMPANY_NUMBER" => text(td[0].xpath("a/text()")),
         "COMPANY_NAME" => text(td[1].xpath("a/text()")),
         "Entity_Kind" => text(td[2].xpath("a/text()")),
         "State" => text(td[3].xpath("a/text()")),
         "DOC" => Time.now.to_s
      }
      puts records.inspect
      #ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=0) unless records['COMPANY_NUMBER'].nil?
      #sleep(1)
    end
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 12000
    }
    pg = br.get(BASE_URL+"/tin/GINameSearch.jsp")
    params = {'JSPName'=>'GINAMESEARCH', 'frmEntityName'=>srch, 'frmFileNumber'=>'', 'action'=>'Search'}
    pg = br.post(BASE_URL+"/tin/controller",params)
    scrape(pg.body,"list")
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    #sleep(30)
    #retry if e.inspect =~ /Timeout|HTTP|TIMED|/
  end
end




range = ('A'..'ZZZZ').to_a + (0..9999).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next if index < offset
  action("#{srch}")
end


