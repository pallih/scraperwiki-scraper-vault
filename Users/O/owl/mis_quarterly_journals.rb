require 'nokogiri'
require 'mechanize'
require 'pp'
require 'cgi'


Mechanize.html_parser = Nokogiri::HTML
br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}

BASE_URL ="http://misq.org/"


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
    puts "ERROR: #{e.inspect} during save_metadata(#{key}) :: #{e.backtrace}"
    retry
  end
end

def text(str)
  begin
    return str.text.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ")
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end

def form_key(str)
  return str.text.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/,"_").upcase
end

def escape(str)
  return CGI.unescapeHTML(str).gsub(/"/,"&quot;")#.gsub(/"/,"\"")
end

def scrape(action,data,url)
  if action == "group"
    journals = []
    Nokogiri::HTML(data).xpath(".//*[@id='main']/table/tr").each{|tr|
      td = tr.xpath("td[not(normalize-space(.)='')]")

      td.xpath("a").each{|a|
        records = {}
        records["year"],records["volume"]=text(td[0].xpath("strong[@class='maroon' and not(normalize-space(.)='')]/text()")).split(",")
        records["month"]=text(a)
        records["link"] =attributes(a.xpath("."),"href")
        journals << records
      }
    }
    return journals
  elsif action == "list"
      links = []
    Nokogiri::HTML(data).xpath(".//*[@id='main']/p[@style='padding-left: 1em;' and not(normalize-space(.)='') ]").each{|para|
      links << attributes(para.xpath("a[not(normalize-space(.)='')]"),"href")
    }
    return links
  elsif action == "details"
    records = {'TITLE' => text(Nokogiri::HTML(data).xpath(".//*[@class='product-name']/text()")),"URL"=>url}
    Nokogiri::HTML(data).xpath(".//*[@class='product-collateral']").each{|div|
      records['ABSTRACT'] = text(div.xpath("div[@class='collateral-box']/div[@class='product-specs']/text()"))
      div.xpath("div[@class='collateral-box']/div[@class='collateral-box attribute-specs']/table[@id='product-attribute-specs-table']/tr").each{|tr|
        td = tr.xpath("td")
        records[form_key(td[0])] = text(td[1])
      }
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['TITLE','AUTHOR'],records)
  end
end

def action(yr,mnth)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    if @journals.nil? 
      pg = br.get(BASE_URL + "archive/")
      @journals = scrape("group",pg.body,"")
    end
    @journals.each{|journal|
      month=journal["month"]
      year=journal["year"]
      link=journal["link"]
      begin
        pg_t = br.get(BASE_URL+ link) 
        volumes = scrape("list",pg_t.body,"") 
        volumes.each{|volume|
          begin
            pg_u = br.get(volume)
            scrape("details",pg_u.body,volume)
          rescue Exception=>e
            puts "ERROR: While processing #{defined?(volume) ? volume : nil} :: #{e.inspect} :: #{e.backtrace}"
            if e.inspect =~ /Timeout/
              sleep(10)
              retry
            end
          end
        }
      rescue Exception=>e
        puts "ERROR: While processing #{defined?(journal) ? journal.inspect : nil} :: #{e.inspect} :: #{e.backtrace}"
        if e.inspect =~ /Timeout/
          sleep(10)
          retry
        end
      end if yr.to_s==year and mnth==month
    } 
    rescue Exception=> e
      puts "ERROR: While initializing sequence :: #{e.inspect} :: #{e.backtrace}"
      if e.inspect =~ /Timeout/
        sleep(10)
        retry
      end
    end
end

@journals=nil
(2011..2011).each{|yr|
  ["March","June","September","Special Issue"].each{|mnth|
    action(yr,mnth)
  }
}


@debug=false
begin
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
  }
  pg = br.get("http://misq.org/profiling-the-research-productivity-of-tenured-information-systems-faculty-at-u-s-institutions.html")
  scrape("details",pg.body)
end if@debug
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'cgi'


Mechanize.html_parser = Nokogiri::HTML
br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}

BASE_URL ="http://misq.org/"


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
    puts "ERROR: #{e.inspect} during save_metadata(#{key}) :: #{e.backtrace}"
    retry
  end
end

def text(str)
  begin
    return str.text.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ")
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end

def form_key(str)
  return str.text.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/,"_").upcase
end

def escape(str)
  return CGI.unescapeHTML(str).gsub(/"/,"&quot;")#.gsub(/"/,"\"")
end

def scrape(action,data,url)
  if action == "group"
    journals = []
    Nokogiri::HTML(data).xpath(".//*[@id='main']/table/tr").each{|tr|
      td = tr.xpath("td[not(normalize-space(.)='')]")

      td.xpath("a").each{|a|
        records = {}
        records["year"],records["volume"]=text(td[0].xpath("strong[@class='maroon' and not(normalize-space(.)='')]/text()")).split(",")
        records["month"]=text(a)
        records["link"] =attributes(a.xpath("."),"href")
        journals << records
      }
    }
    return journals
  elsif action == "list"
      links = []
    Nokogiri::HTML(data).xpath(".//*[@id='main']/p[@style='padding-left: 1em;' and not(normalize-space(.)='') ]").each{|para|
      links << attributes(para.xpath("a[not(normalize-space(.)='')]"),"href")
    }
    return links
  elsif action == "details"
    records = {'TITLE' => text(Nokogiri::HTML(data).xpath(".//*[@class='product-name']/text()")),"URL"=>url}
    Nokogiri::HTML(data).xpath(".//*[@class='product-collateral']").each{|div|
      records['ABSTRACT'] = text(div.xpath("div[@class='collateral-box']/div[@class='product-specs']/text()"))
      div.xpath("div[@class='collateral-box']/div[@class='collateral-box attribute-specs']/table[@id='product-attribute-specs-table']/tr").each{|tr|
        td = tr.xpath("td")
        records[form_key(td[0])] = text(td[1])
      }
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['TITLE','AUTHOR'],records)
  end
end

def action(yr,mnth)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    if @journals.nil? 
      pg = br.get(BASE_URL + "archive/")
      @journals = scrape("group",pg.body,"")
    end
    @journals.each{|journal|
      month=journal["month"]
      year=journal["year"]
      link=journal["link"]
      begin
        pg_t = br.get(BASE_URL+ link) 
        volumes = scrape("list",pg_t.body,"") 
        volumes.each{|volume|
          begin
            pg_u = br.get(volume)
            scrape("details",pg_u.body,volume)
          rescue Exception=>e
            puts "ERROR: While processing #{defined?(volume) ? volume : nil} :: #{e.inspect} :: #{e.backtrace}"
            if e.inspect =~ /Timeout/
              sleep(10)
              retry
            end
          end
        }
      rescue Exception=>e
        puts "ERROR: While processing #{defined?(journal) ? journal.inspect : nil} :: #{e.inspect} :: #{e.backtrace}"
        if e.inspect =~ /Timeout/
          sleep(10)
          retry
        end
      end if yr.to_s==year and mnth==month
    } 
    rescue Exception=> e
      puts "ERROR: While initializing sequence :: #{e.inspect} :: #{e.backtrace}"
      if e.inspect =~ /Timeout/
        sleep(10)
        retry
      end
    end
end

@journals=nil
(2011..2011).each{|yr|
  ["March","June","September","Special Issue"].each{|mnth|
    action(yr,mnth)
  }
}


@debug=false
begin
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
  }
  pg = br.get("http://misq.org/profiling-the-research-productivity-of-tenured-information-systems-faculty-at-u-s-institutions.html")
  scrape("details",pg.body)
end if@debug
