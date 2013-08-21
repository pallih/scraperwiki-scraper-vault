# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.cro.gov.np"

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
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip }
      return tmp.join("\n")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    #Nokogiri::HTML(data).xpath(".//table[@class='dataTable' and @cellpadding='5']/tr[position()>1]").each{|tr|
    #puts     Nokogiri::HTML(data).inspect
    Nokogiri::HTML(data).xpath(".//tr[@class='row']").each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NUMBER" => text(td[0].xpath(".")),
        "ENG_NAME" => text(td[1].xpath(".")),
        "NEP_NAME" => text(td[2].xpath(".")),
        "CREATION_DT" => text(td[3].xpath(".")),
        "ADDR" => text(td[4].xpath(".")),
        "DOC" => Time.now
      }
      records << r unless r["COMPANY_NUMBER"].nil? 
    }
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER","ENG_NAME"],records,table_name="SWDATA",verbose=2) unless records.length == 0
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.open_timeout = 1200
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL + "/search.php"
    pg = br.post(s_url,{'formSubmit'=>'1','registerNum'=>'','companyName'=>srch,'submit'=>'Search'})
    scrape(pg.body.scan(/class="dataTable">(.*?)<\/table>/m).flatten[1],"list")
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time/
  end
end

range = ('AAA'..'ZZZ').to_a+(0..9).to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset>=range.length


range.each_with_index{|srch,index|
  next if index<offset
  resp = action(srch)
  save_metadata("OFFSET",index.next)
}


# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.cro.gov.np"

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
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip }
      return tmp.join("\n")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    #Nokogiri::HTML(data).xpath(".//table[@class='dataTable' and @cellpadding='5']/tr[position()>1]").each{|tr|
    #puts     Nokogiri::HTML(data).inspect
    Nokogiri::HTML(data).xpath(".//tr[@class='row']").each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NUMBER" => text(td[0].xpath(".")),
        "ENG_NAME" => text(td[1].xpath(".")),
        "NEP_NAME" => text(td[2].xpath(".")),
        "CREATION_DT" => text(td[3].xpath(".")),
        "ADDR" => text(td[4].xpath(".")),
        "DOC" => Time.now
      }
      records << r unless r["COMPANY_NUMBER"].nil? 
    }
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER","ENG_NAME"],records,table_name="SWDATA",verbose=2) unless records.length == 0
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.open_timeout = 1200
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL + "/search.php"
    pg = br.post(s_url,{'formSubmit'=>'1','registerNum'=>'','companyName'=>srch,'submit'=>'Search'})
    scrape(pg.body.scan(/class="dataTable">(.*?)<\/table>/m).flatten[1],"list")
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time/
  end
end

range = ('AAA'..'ZZZ').to_a+(0..9).to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset>=range.length


range.each_with_index{|srch,index|
  next if index<offset
  resp = action(srch)
  save_metadata("OFFSET",index.next)
}


