# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.sos.state.co.us"

@br = Mechanize.new {|b|
  b.user_agent_alias = 'Linux Firefox'
  b.max_history=0
  b.read_timeout = 1200
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.strip.gsub(/(\s)+/,' ').strip
  end  
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(data,act,rec)
  if act == "length"
    return Nokogiri::HTML(data).xpath(".//div[@id='box']/table/tr[position()>1]").length
  elsif act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//div[@id='box']/table/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      next if td.length < 8
      records << {
        "company_number" => s_text(td[1].xpath("./a/text()")),
        "document_number" => s_text(td[2].xpath("./text()")),
        "company_name" => s_text(td[3].xpath("./text()")),
        "event" => s_text(td[4].xpath("./text()")),
        "status" => s_text(td[5].xpath("./text()")),
        "type" => s_text(td[6].xpath("./text()")),
        "incorporation_dt" => s_text(td[7].xpath("./text()")),
        "link" => "http://www.sos.state.co.us/biz/" + attributes(td[1].xpath("./a"),"href"),
        "doc" => Time.now
      }
    }
    return records,Nokogiri::HTML(data).xpath(".//div[@id='box']/table/tr[position()>1]").length
  end
end

def action(dt)
  begin

    list = ('A'..'Z').to_a
    lstart = get_metadata("list",0)
    list[lstart..-1].each.each{|srch|
      pg = @br.get(BASE_URL + "/biz/AdvancedSearchCriteria.do")
      params = {"dateFrom"=>dt.strftime("%m/%d/%Y"),"dateTo"=>dt.strftime("%m/%d/%Y"),"includeEntity"=>"true","searchName"=>srch,"cmd"=>"Search"}
      begin
        pg.form_with(:name=>"AdvancedSearchCriteriaForm") do |f| 
          params.each{|k,v| f[k] = v}
          pg = f.submit()
        end
        begin
          record,len = scrape(pg.body,"list",{})
          ScraperWiki.save_sqlite(unique_keys=['company_number','event'],record)
          tmp = attributes(Nokogiri::HTML(pg.body).xpath(".//dd[@class='linkNext']/a"),"href")
          break if tmp.nil? or tmp.empty? or len < 20
          pg = @br.get(BASE_URL + tmp)
        end while(true) unless pg.nil? 
      end
      lstart = lstart + 1
      save_metadata("list",lstart)
    }
    delete_metadata("list")
  end
end

dt_str = get_metadata("date","2012-08-01")

(Date.parse(dt_str)..Date.parse(dt_str)+30).each{|dt|
  action(dt)
  save_metadata("date",dt.to_s)
  sleep(10)
}


# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.sos.state.co.us"

@br = Mechanize.new {|b|
  b.user_agent_alias = 'Linux Firefox'
  b.max_history=0
  b.read_timeout = 1200
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.strip.gsub(/(\s)+/,' ').strip
  end  
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(data,act,rec)
  if act == "length"
    return Nokogiri::HTML(data).xpath(".//div[@id='box']/table/tr[position()>1]").length
  elsif act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//div[@id='box']/table/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      next if td.length < 8
      records << {
        "company_number" => s_text(td[1].xpath("./a/text()")),
        "document_number" => s_text(td[2].xpath("./text()")),
        "company_name" => s_text(td[3].xpath("./text()")),
        "event" => s_text(td[4].xpath("./text()")),
        "status" => s_text(td[5].xpath("./text()")),
        "type" => s_text(td[6].xpath("./text()")),
        "incorporation_dt" => s_text(td[7].xpath("./text()")),
        "link" => "http://www.sos.state.co.us/biz/" + attributes(td[1].xpath("./a"),"href"),
        "doc" => Time.now
      }
    }
    return records,Nokogiri::HTML(data).xpath(".//div[@id='box']/table/tr[position()>1]").length
  end
end

def action(dt)
  begin

    list = ('A'..'Z').to_a
    lstart = get_metadata("list",0)
    list[lstart..-1].each.each{|srch|
      pg = @br.get(BASE_URL + "/biz/AdvancedSearchCriteria.do")
      params = {"dateFrom"=>dt.strftime("%m/%d/%Y"),"dateTo"=>dt.strftime("%m/%d/%Y"),"includeEntity"=>"true","searchName"=>srch,"cmd"=>"Search"}
      begin
        pg.form_with(:name=>"AdvancedSearchCriteriaForm") do |f| 
          params.each{|k,v| f[k] = v}
          pg = f.submit()
        end
        begin
          record,len = scrape(pg.body,"list",{})
          ScraperWiki.save_sqlite(unique_keys=['company_number','event'],record)
          tmp = attributes(Nokogiri::HTML(pg.body).xpath(".//dd[@class='linkNext']/a"),"href")
          break if tmp.nil? or tmp.empty? or len < 20
          pg = @br.get(BASE_URL + tmp)
        end while(true) unless pg.nil? 
      end
      lstart = lstart + 1
      save_metadata("list",lstart)
    }
    delete_metadata("list")
  end
end

dt_str = get_metadata("date","2012-08-01")

(Date.parse(dt_str)..Date.parse(dt_str)+30).each{|dt|
  action(dt)
  save_metadata("date",dt.to_s)
  sleep(10)
}


