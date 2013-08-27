require 'nokogiri'
require 'mechanize'
require 'pp'
require 'cgi'


Mechanize.html_parser = Nokogiri::HTML
br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}

BASE_URL ="http://president.ie/"


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
    ret = ""
    
    str.each{|s|
      if str.inner_html.nil? or str.inner_html.empty? 
        ret = ret + s.text.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ") + ((s.text.strip.nil? or s.text.strip.empty?)? "" : "|")
      else
        ret = ret + s.inner_html.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ").gsub("<br>","|") + ((s.inner_html.strip.nil? or s.inner_html.strip.empty?)? "" : "|")
      end
    } unless str.nil? 
    return ret.chop
    #return ret.empty? ? ((str.nil? or str.text.nil?) ? nil : str.text.strip.gsub(/\n|\t|^\s+|\s+$/,"")) : ret.chmop
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.attributes.nil? or t.attributes[attr].nil?) ? nil : t.attributes[attr].value
end

def escape(str)
  return CGI.unescapeHTML(str).gsub(/"/,"&quot;")#.gsub(/"/,"\"")
end

def scrape(action,data)
  if action == "group"
    links = []
    Nokogiri::HTML(data).xpath(".//*[@id='content']/div[3]/a").each{|a|
      links << attributes(a,"href")
    }
  elsif action == "list"
      links = []
    Nokogiri::HTML(data).xpath(".//div[@class='text']/ul/li/a").each{|a|
      #pp a.attributes['href']
      links << attributes(a,"href")
    }
    return links
  elsif action == "details"

    records={}
    Nokogiri::HTML(data).xpath(".//*[@id='content']/div[3]/dl").each_with_index{|date_doc,date_idx|
      records['DATE'] = text(date_doc.xpath("dt/strong"))
      str = "\302\240"
      date_doc.xpath("dd").each{|dd_doc|
        details_path="following-sibling::node()[not(normalize-space(.)='' or normalize-space(.)='#{str}')][1]"
        dd_doc.xpath("../dd/strong[not(normalize-space(.)='') and following-sibling::*[1]/self::strong]").each{|span_doc|
          time_place = text(span_doc.xpath("text()[1]|span[@class='bodytextBold']/text()[1]"))
          temp = span_doc.xpath("following-sibling::*[1]/self::strong") 
          time_place = time_place +" "+text(temp) unless temp.nil? or temp.empty? 
          records['TIME_PLACE']=time_place
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath(details_path)) : text(temp.xpath(details_path))
          puts "#{records.inspect} :: #1" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }


        dd_doc.xpath("span[@class='bodytextBold' and strong[not(normalize-space(.)='')]]").each{|span_doc|
          time_place = span_doc.xpath("strong/text()")
          records['TIME_PLACE']=text(time_place)
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #2" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
        dd_doc.xpath("p/strong[not(normalize-space(.)='') and not(following-sibling::*[1]/self::strong or preceding::*[1]/self::strong)]").each{|span_doc|
          time_place = text(span_doc.xpath("text()[1]|span[not(normalize-space(.)='')]/text()[1]"))
          temp = span_doc.xpath("following-sibling::*[1]/self::strong") 
          time_place = time_place +" "+text(temp) unless temp.nil? or temp.empty? 
          records['TIME_PLACE']=time_place
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath(details_path)) : text(temp.xpath(details_path))
          
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath("parent::p[1]/"+details_path)) : text(temp.xpath("parent::p[1]/"+details_path)) if records['DETAILS'].nil? or records['DETAILS'].empty? 
          puts "#{records.inspect} :: #3" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
        dd_doc.xpath("../dd/span[@style='font-weight: bold;']").each{|span_doc|
          time_place = span_doc.xpath("text()")
          records['TIME_PLACE']=text(time_place)
          path = "[preceding::span[1][text()=\"#{escape(time_place.text)}\"]]"
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #4 :: #{path} :: #{time_place.text} :: #{records['TIME_PLACE']}" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}        
        }
        dd_doc.xpath("../dd/p/span[@style='font-weight: bold;']").each{|span_doc|
          time_place = span_doc.xpath("text()")
          records['TIME_PLACE']=text(time_place)
          path = "[preceding::span[1][text()=\"#{escape(time_place.text)}\"]]"
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #5" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}        
        }
        dd_doc.xpath("span[@class='bodytextBold']/span[@class='bodytextBold' or strong[not(normalize-space(.)='')]]").each{|span_doc|
          time_place = span_doc.xpath("strong/text()")
          records['TIME_PLACE']=text(time_place)
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #6" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
        dd_doc.xpath("p/strong[not(normalize-space(.)='') and (following-sibling::*[1]/self::strong and preceding::*[1]/self::p)]").each{|span_doc|
          time_place = text(span_doc.xpath("text()[1]|span[not(normalize-space(.)='')]/text()[1]"))
          temp = span_doc.xpath("following-sibling::*[1]/self::strong") 
          time_place = time_place +" "+text(temp) unless temp.nil? or temp.empty? 
          records['TIME_PLACE']=time_place
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath(details_path)) : text(temp.xpath(details_path))
          
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath("parent::p[1]/"+details_path)) : text(temp.xpath("parent::p[1]/"+details_path)) if records['DETAILS'].nil? or records['DETAILS'].empty? 
          puts "#{records.inspect} :: #7" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
      }
    }         
  end
end

def action(year)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    pg = br.get(BASE_URL + "index.php?year=#{year}&section=6&lang=eng")
    links = scrape("list",pg.body)
    links.each{|lnk|
      begin
        pg_t = br.get(BASE_URL+ lnk)
        scrape("details",pg_t.body)
      rescue Exception=>e
        puts "ERROR: While processing #{lnk} :: #{e.inspect} :: #{e.backtrace}"
        if e.inspect =~ /Timeout|ETIMEDOUT/
          sleep(10)
          retry
        end
      end
    }
  rescue Exception=> e
    puts "ERROR: While processing #{year} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect =~ /Timeout|ETIMEDOUT/
      sleep(10)
      retry
    end
  end
end
@debug = false
begin
  #ScraperWiki.sqliteexecute("delete from swdata where date like '%1997%'")
  #action(1997) if not @debug
  #exit
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
  }
  pg = br.get(BASE_URL + "index.php?section=6&engagement=201128&lang=eng")
  #puts pg.body
  scrape("details",pg.body)
end if@debug
(2011..2011).each do|yr|
  action(yr)
end unless@debug
#puts ScraperWiki.sqliteexecute("select * from swdata where details=''").inspect if @debug
#puts ScraperWiki.sqliteexecute("select * from swdata limit 1")['data'].inspect

require 'nokogiri'
require 'mechanize'
require 'pp'
require 'cgi'


Mechanize.html_parser = Nokogiri::HTML
br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}

BASE_URL ="http://president.ie/"


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
    ret = ""
    
    str.each{|s|
      if str.inner_html.nil? or str.inner_html.empty? 
        ret = ret + s.text.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ") + ((s.text.strip.nil? or s.text.strip.empty?)? "" : "|")
      else
        ret = ret + s.inner_html.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ").gsub("<br>","|") + ((s.inner_html.strip.nil? or s.inner_html.strip.empty?)? "" : "|")
      end
    } unless str.nil? 
    return ret.chop
    #return ret.empty? ? ((str.nil? or str.text.nil?) ? nil : str.text.strip.gsub(/\n|\t|^\s+|\s+$/,"")) : ret.chmop
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.attributes.nil? or t.attributes[attr].nil?) ? nil : t.attributes[attr].value
end

def escape(str)
  return CGI.unescapeHTML(str).gsub(/"/,"&quot;")#.gsub(/"/,"\"")
end

def scrape(action,data)
  if action == "group"
    links = []
    Nokogiri::HTML(data).xpath(".//*[@id='content']/div[3]/a").each{|a|
      links << attributes(a,"href")
    }
  elsif action == "list"
      links = []
    Nokogiri::HTML(data).xpath(".//div[@class='text']/ul/li/a").each{|a|
      #pp a.attributes['href']
      links << attributes(a,"href")
    }
    return links
  elsif action == "details"

    records={}
    Nokogiri::HTML(data).xpath(".//*[@id='content']/div[3]/dl").each_with_index{|date_doc,date_idx|
      records['DATE'] = text(date_doc.xpath("dt/strong"))
      str = "\302\240"
      date_doc.xpath("dd").each{|dd_doc|
        details_path="following-sibling::node()[not(normalize-space(.)='' or normalize-space(.)='#{str}')][1]"
        dd_doc.xpath("../dd/strong[not(normalize-space(.)='') and following-sibling::*[1]/self::strong]").each{|span_doc|
          time_place = text(span_doc.xpath("text()[1]|span[@class='bodytextBold']/text()[1]"))
          temp = span_doc.xpath("following-sibling::*[1]/self::strong") 
          time_place = time_place +" "+text(temp) unless temp.nil? or temp.empty? 
          records['TIME_PLACE']=time_place
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath(details_path)) : text(temp.xpath(details_path))
          puts "#{records.inspect} :: #1" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }


        dd_doc.xpath("span[@class='bodytextBold' and strong[not(normalize-space(.)='')]]").each{|span_doc|
          time_place = span_doc.xpath("strong/text()")
          records['TIME_PLACE']=text(time_place)
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #2" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
        dd_doc.xpath("p/strong[not(normalize-space(.)='') and not(following-sibling::*[1]/self::strong or preceding::*[1]/self::strong)]").each{|span_doc|
          time_place = text(span_doc.xpath("text()[1]|span[not(normalize-space(.)='')]/text()[1]"))
          temp = span_doc.xpath("following-sibling::*[1]/self::strong") 
          time_place = time_place +" "+text(temp) unless temp.nil? or temp.empty? 
          records['TIME_PLACE']=time_place
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath(details_path)) : text(temp.xpath(details_path))
          
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath("parent::p[1]/"+details_path)) : text(temp.xpath("parent::p[1]/"+details_path)) if records['DETAILS'].nil? or records['DETAILS'].empty? 
          puts "#{records.inspect} :: #3" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
        dd_doc.xpath("../dd/span[@style='font-weight: bold;']").each{|span_doc|
          time_place = span_doc.xpath("text()")
          records['TIME_PLACE']=text(time_place)
          path = "[preceding::span[1][text()=\"#{escape(time_place.text)}\"]]"
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #4 :: #{path} :: #{time_place.text} :: #{records['TIME_PLACE']}" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}        
        }
        dd_doc.xpath("../dd/p/span[@style='font-weight: bold;']").each{|span_doc|
          time_place = span_doc.xpath("text()")
          records['TIME_PLACE']=text(time_place)
          path = "[preceding::span[1][text()=\"#{escape(time_place.text)}\"]]"
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #5" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}        
        }
        dd_doc.xpath("span[@class='bodytextBold']/span[@class='bodytextBold' or strong[not(normalize-space(.)='')]]").each{|span_doc|
          time_place = span_doc.xpath("strong/text()")
          records['TIME_PLACE']=text(time_place)
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #6" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
        dd_doc.xpath("p/strong[not(normalize-space(.)='') and (following-sibling::*[1]/self::strong and preceding::*[1]/self::p)]").each{|span_doc|
          time_place = text(span_doc.xpath("text()[1]|span[not(normalize-space(.)='')]/text()[1]"))
          temp = span_doc.xpath("following-sibling::*[1]/self::strong") 
          time_place = time_place +" "+text(temp) unless temp.nil? or temp.empty? 
          records['TIME_PLACE']=time_place
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath(details_path)) : text(temp.xpath(details_path))
          
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath("parent::p[1]/"+details_path)) : text(temp.xpath("parent::p[1]/"+details_path)) if records['DETAILS'].nil? or records['DETAILS'].empty? 
          puts "#{records.inspect} :: #7" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
      }
    }         
  end
end

def action(year)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    pg = br.get(BASE_URL + "index.php?year=#{year}&section=6&lang=eng")
    links = scrape("list",pg.body)
    links.each{|lnk|
      begin
        pg_t = br.get(BASE_URL+ lnk)
        scrape("details",pg_t.body)
      rescue Exception=>e
        puts "ERROR: While processing #{lnk} :: #{e.inspect} :: #{e.backtrace}"
        if e.inspect =~ /Timeout|ETIMEDOUT/
          sleep(10)
          retry
        end
      end
    }
  rescue Exception=> e
    puts "ERROR: While processing #{year} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect =~ /Timeout|ETIMEDOUT/
      sleep(10)
      retry
    end
  end
end
@debug = false
begin
  #ScraperWiki.sqliteexecute("delete from swdata where date like '%1997%'")
  #action(1997) if not @debug
  #exit
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
  }
  pg = br.get(BASE_URL + "index.php?section=6&engagement=201128&lang=eng")
  #puts pg.body
  scrape("details",pg.body)
end if@debug
(2011..2011).each do|yr|
  action(yr)
end unless@debug
#puts ScraperWiki.sqliteexecute("select * from swdata where details=''").inspect if @debug
#puts ScraperWiki.sqliteexecute("select * from swdata limit 1")['data'].inspect

require 'nokogiri'
require 'mechanize'
require 'pp'
require 'cgi'


Mechanize.html_parser = Nokogiri::HTML
br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}

BASE_URL ="http://president.ie/"


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
    ret = ""
    
    str.each{|s|
      if str.inner_html.nil? or str.inner_html.empty? 
        ret = ret + s.text.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ") + ((s.text.strip.nil? or s.text.strip.empty?)? "" : "|")
      else
        ret = ret + s.inner_html.strip.gsub(/\r\n|\n|\t|^\s+|\s+$/," ").gsub("<br>","|") + ((s.inner_html.strip.nil? or s.inner_html.strip.empty?)? "" : "|")
      end
    } unless str.nil? 
    return ret.chop
    #return ret.empty? ? ((str.nil? or str.text.nil?) ? nil : str.text.strip.gsub(/\n|\t|^\s+|\s+$/,"")) : ret.chmop
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.attributes.nil? or t.attributes[attr].nil?) ? nil : t.attributes[attr].value
end

def escape(str)
  return CGI.unescapeHTML(str).gsub(/"/,"&quot;")#.gsub(/"/,"\"")
end

def scrape(action,data)
  if action == "group"
    links = []
    Nokogiri::HTML(data).xpath(".//*[@id='content']/div[3]/a").each{|a|
      links << attributes(a,"href")
    }
  elsif action == "list"
      links = []
    Nokogiri::HTML(data).xpath(".//div[@class='text']/ul/li/a").each{|a|
      #pp a.attributes['href']
      links << attributes(a,"href")
    }
    return links
  elsif action == "details"

    records={}
    Nokogiri::HTML(data).xpath(".//*[@id='content']/div[3]/dl").each_with_index{|date_doc,date_idx|
      records['DATE'] = text(date_doc.xpath("dt/strong"))
      str = "\302\240"
      date_doc.xpath("dd").each{|dd_doc|
        details_path="following-sibling::node()[not(normalize-space(.)='' or normalize-space(.)='#{str}')][1]"
        dd_doc.xpath("../dd/strong[not(normalize-space(.)='') and following-sibling::*[1]/self::strong]").each{|span_doc|
          time_place = text(span_doc.xpath("text()[1]|span[@class='bodytextBold']/text()[1]"))
          temp = span_doc.xpath("following-sibling::*[1]/self::strong") 
          time_place = time_place +" "+text(temp) unless temp.nil? or temp.empty? 
          records['TIME_PLACE']=time_place
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath(details_path)) : text(temp.xpath(details_path))
          puts "#{records.inspect} :: #1" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }


        dd_doc.xpath("span[@class='bodytextBold' and strong[not(normalize-space(.)='')]]").each{|span_doc|
          time_place = span_doc.xpath("strong/text()")
          records['TIME_PLACE']=text(time_place)
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #2" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
        dd_doc.xpath("p/strong[not(normalize-space(.)='') and not(following-sibling::*[1]/self::strong or preceding::*[1]/self::strong)]").each{|span_doc|
          time_place = text(span_doc.xpath("text()[1]|span[not(normalize-space(.)='')]/text()[1]"))
          temp = span_doc.xpath("following-sibling::*[1]/self::strong") 
          time_place = time_place +" "+text(temp) unless temp.nil? or temp.empty? 
          records['TIME_PLACE']=time_place
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath(details_path)) : text(temp.xpath(details_path))
          
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath("parent::p[1]/"+details_path)) : text(temp.xpath("parent::p[1]/"+details_path)) if records['DETAILS'].nil? or records['DETAILS'].empty? 
          puts "#{records.inspect} :: #3" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
        dd_doc.xpath("../dd/span[@style='font-weight: bold;']").each{|span_doc|
          time_place = span_doc.xpath("text()")
          records['TIME_PLACE']=text(time_place)
          path = "[preceding::span[1][text()=\"#{escape(time_place.text)}\"]]"
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #4 :: #{path} :: #{time_place.text} :: #{records['TIME_PLACE']}" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}        
        }
        dd_doc.xpath("../dd/p/span[@style='font-weight: bold;']").each{|span_doc|
          time_place = span_doc.xpath("text()")
          records['TIME_PLACE']=text(time_place)
          path = "[preceding::span[1][text()=\"#{escape(time_place.text)}\"]]"
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #5" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}        
        }
        dd_doc.xpath("span[@class='bodytextBold']/span[@class='bodytextBold' or strong[not(normalize-space(.)='')]]").each{|span_doc|
          time_place = span_doc.xpath("strong/text()")
          records['TIME_PLACE']=text(time_place)
          records['DETAILS'] = text(span_doc.xpath(details_path))
          puts "#{records.inspect} :: #6" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
        dd_doc.xpath("p/strong[not(normalize-space(.)='') and (following-sibling::*[1]/self::strong and preceding::*[1]/self::p)]").each{|span_doc|
          time_place = text(span_doc.xpath("text()[1]|span[not(normalize-space(.)='')]/text()[1]"))
          temp = span_doc.xpath("following-sibling::*[1]/self::strong") 
          time_place = time_place +" "+text(temp) unless temp.nil? or temp.empty? 
          records['TIME_PLACE']=time_place
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath(details_path)) : text(temp.xpath(details_path))
          
          records['DETAILS'] = (temp.nil? or temp.empty?) ? text(span_doc.xpath("parent::p[1]/"+details_path)) : text(temp.xpath("parent::p[1]/"+details_path)) if records['DETAILS'].nil? or records['DETAILS'].empty? 
          puts "#{records.inspect} :: #7" if @debug
          ScraperWiki.save_sqlite(unique_keys=['DATE','TIME_PLACE'],records)
          records={'DATE'=>records['DATE']}
        }
      }
    }         
  end
end

def action(year)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    pg = br.get(BASE_URL + "index.php?year=#{year}&section=6&lang=eng")
    links = scrape("list",pg.body)
    links.each{|lnk|
      begin
        pg_t = br.get(BASE_URL+ lnk)
        scrape("details",pg_t.body)
      rescue Exception=>e
        puts "ERROR: While processing #{lnk} :: #{e.inspect} :: #{e.backtrace}"
        if e.inspect =~ /Timeout|ETIMEDOUT/
          sleep(10)
          retry
        end
      end
    }
  rescue Exception=> e
    puts "ERROR: While processing #{year} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect =~ /Timeout|ETIMEDOUT/
      sleep(10)
      retry
    end
  end
end
@debug = false
begin
  #ScraperWiki.sqliteexecute("delete from swdata where date like '%1997%'")
  #action(1997) if not @debug
  #exit
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
  }
  pg = br.get(BASE_URL + "index.php?section=6&engagement=201128&lang=eng")
  #puts pg.body
  scrape("details",pg.body)
end if@debug
(2011..2011).each do|yr|
  action(yr)
end unless@debug
#puts ScraperWiki.sqliteexecute("select * from swdata where details=''").inspect if @debug
#puts ScraperWiki.sqliteexecute("select * from swdata limit 1")['data'].inspect

