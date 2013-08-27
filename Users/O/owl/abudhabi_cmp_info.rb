# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://adbc.abudhabi.ae/"

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

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where key=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
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
    Nokogiri::HTML(data).xpath(".//table[@id='ctl00_PlaceHolderMain_dgvTradeName']/tr[position()>2 and position()<last()]").each{|tr|
      td = tr.xpath("td")
      records = {
        "COMPANY_NUMBER" => text(td[0].xpath("div/a/strong/span/text()")),
        "URL"=> BASE_URL+attributes(td[0].xpath("div/a"),"href").gsub("..",'CitizenAccess'),
        "ENG_NAME" => text(td[1].xpath("div/span/text()")),
        "ARABIC_NAME" => text(td[2].xpath("div/span/text()")),
        "EXP_DT" => text(td[3].xpath("div/span/text()")),
        "STATUS" => text(td[4].xpath("div/span/text()")),
        "DOC" => Time.now.to_s
      }
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=0) unless records["COMPANY_NUMBER"].nil? 
    }
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    params = {'ctl00$ScriptManager1'=>'ctl00$PlaceHolderMain$updatePanel|ctl00$PlaceHolderMain$btnNewSearch',
      '__EVENTTARGET'=>'ctl00$PlaceHolderMain$btnNewSearch',
      'ctl00$PlaceHolderMain$txtEnglishTradeName'=>'.',
      '__ASYNCPOST'=>'false'
    }
    s_url = BASE_URL + "/CitizenAccess/Cap/CapHome.aspx?module=Licenses&TabName=LICENSES&FilterName=TRADENAME"
    pg = br.get(s_url)
    begin
      pg.form_with(:name => "aspnetForm") do |f|
        params.each{|k,v|
          f[k] = v
        }
        pg =  f.submit
      end unless pg.nil? or pg.form_with(:name=>"aspnetForm").nil? 
      scrape(pg.body,"list")
      params = {
        'ctl00$ScriptManager1'=>'ctl00$PlaceHolderMain$updatePanel|ctl00$PlaceHolderMain$dgvTradeName$ctl13$ctl12',
        'ctl00$PlaceHolderMain$txtEnglishTradeName'=>'.',
        '__EVENTTARGET'=>'ctl00$PlaceHolderMain$dgvTradeName$ctl13$ctl12',
        '__ASYNCPOST'=>'false'
      }
      break if not pg.at("//td[@class='aca_pagination_td aca_pagination_PrevNext']/a[text()='Next >']")
    rescue Exception => e
      puts "ERROR: While processing #{srch} inner_page :: #{e.inspect} :: #{e.backtrace}"
    end while(true)
    pg = br.get(s_url)
    scrape(pg.body,"list")
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end
action(".")



# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://adbc.abudhabi.ae/"

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

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where key=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
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
    Nokogiri::HTML(data).xpath(".//table[@id='ctl00_PlaceHolderMain_dgvTradeName']/tr[position()>2 and position()<last()]").each{|tr|
      td = tr.xpath("td")
      records = {
        "COMPANY_NUMBER" => text(td[0].xpath("div/a/strong/span/text()")),
        "URL"=> BASE_URL+attributes(td[0].xpath("div/a"),"href").gsub("..",'CitizenAccess'),
        "ENG_NAME" => text(td[1].xpath("div/span/text()")),
        "ARABIC_NAME" => text(td[2].xpath("div/span/text()")),
        "EXP_DT" => text(td[3].xpath("div/span/text()")),
        "STATUS" => text(td[4].xpath("div/span/text()")),
        "DOC" => Time.now.to_s
      }
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=0) unless records["COMPANY_NUMBER"].nil? 
    }
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    params = {'ctl00$ScriptManager1'=>'ctl00$PlaceHolderMain$updatePanel|ctl00$PlaceHolderMain$btnNewSearch',
      '__EVENTTARGET'=>'ctl00$PlaceHolderMain$btnNewSearch',
      'ctl00$PlaceHolderMain$txtEnglishTradeName'=>'.',
      '__ASYNCPOST'=>'false'
    }
    s_url = BASE_URL + "/CitizenAccess/Cap/CapHome.aspx?module=Licenses&TabName=LICENSES&FilterName=TRADENAME"
    pg = br.get(s_url)
    begin
      pg.form_with(:name => "aspnetForm") do |f|
        params.each{|k,v|
          f[k] = v
        }
        pg =  f.submit
      end unless pg.nil? or pg.form_with(:name=>"aspnetForm").nil? 
      scrape(pg.body,"list")
      params = {
        'ctl00$ScriptManager1'=>'ctl00$PlaceHolderMain$updatePanel|ctl00$PlaceHolderMain$dgvTradeName$ctl13$ctl12',
        'ctl00$PlaceHolderMain$txtEnglishTradeName'=>'.',
        '__EVENTTARGET'=>'ctl00$PlaceHolderMain$dgvTradeName$ctl13$ctl12',
        '__ASYNCPOST'=>'false'
      }
      break if not pg.at("//td[@class='aca_pagination_td aca_pagination_PrevNext']/a[text()='Next >']")
    rescue Exception => e
      puts "ERROR: While processing #{srch} inner_page :: #{e.inspect} :: #{e.backtrace}"
    end while(true)
    pg = br.get(s_url)
    scrape(pg.body,"list")
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end
action(".")



# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://adbc.abudhabi.ae/"

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

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where key=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
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
    Nokogiri::HTML(data).xpath(".//table[@id='ctl00_PlaceHolderMain_dgvTradeName']/tr[position()>2 and position()<last()]").each{|tr|
      td = tr.xpath("td")
      records = {
        "COMPANY_NUMBER" => text(td[0].xpath("div/a/strong/span/text()")),
        "URL"=> BASE_URL+attributes(td[0].xpath("div/a"),"href").gsub("..",'CitizenAccess'),
        "ENG_NAME" => text(td[1].xpath("div/span/text()")),
        "ARABIC_NAME" => text(td[2].xpath("div/span/text()")),
        "EXP_DT" => text(td[3].xpath("div/span/text()")),
        "STATUS" => text(td[4].xpath("div/span/text()")),
        "DOC" => Time.now.to_s
      }
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=0) unless records["COMPANY_NUMBER"].nil? 
    }
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    params = {'ctl00$ScriptManager1'=>'ctl00$PlaceHolderMain$updatePanel|ctl00$PlaceHolderMain$btnNewSearch',
      '__EVENTTARGET'=>'ctl00$PlaceHolderMain$btnNewSearch',
      'ctl00$PlaceHolderMain$txtEnglishTradeName'=>'.',
      '__ASYNCPOST'=>'false'
    }
    s_url = BASE_URL + "/CitizenAccess/Cap/CapHome.aspx?module=Licenses&TabName=LICENSES&FilterName=TRADENAME"
    pg = br.get(s_url)
    begin
      pg.form_with(:name => "aspnetForm") do |f|
        params.each{|k,v|
          f[k] = v
        }
        pg =  f.submit
      end unless pg.nil? or pg.form_with(:name=>"aspnetForm").nil? 
      scrape(pg.body,"list")
      params = {
        'ctl00$ScriptManager1'=>'ctl00$PlaceHolderMain$updatePanel|ctl00$PlaceHolderMain$dgvTradeName$ctl13$ctl12',
        'ctl00$PlaceHolderMain$txtEnglishTradeName'=>'.',
        '__EVENTTARGET'=>'ctl00$PlaceHolderMain$dgvTradeName$ctl13$ctl12',
        '__ASYNCPOST'=>'false'
      }
      break if not pg.at("//td[@class='aca_pagination_td aca_pagination_PrevNext']/a[text()='Next >']")
    rescue Exception => e
      puts "ERROR: While processing #{srch} inner_page :: #{e.inspect} :: #{e.backtrace}"
    end while(true)
    pg = br.get(s_url)
    scrape(pg.body,"list")
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end
action(".")



