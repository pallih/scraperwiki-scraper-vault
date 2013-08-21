# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end
class Array
  def pretty
    self.collect{|a|a.strip}
  end
  def strip_dquote
    self.collect{|a| a.gsub('"',"").strip }
  end
end


def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    data = Iconv.iconv('UTF-8//IGNORE', 'euc-kr', data).first
    records = []
    Nokogiri::HTML(data,nil,'UTF-8').xpath(".//div[@class='list_table']/table/tr[position()>1]").each{|tr|
      r = {}
      r['registry'] = s_text(tr.xpath("./td[2]/text()"))
      r['type'] = s_text(tr.xpath("./td[3]/text()"))
      r['registration_no'] = s_text(tr.xpath("./td[4]/text()"))
      r['company_name'] = s_text(tr.xpath("./td[5]/a/text()"))
      r['entry_type'] = s_text(tr.xpath("./td[6]/text()"))
      r['address'] = s_text(tr.xpath("./td[7]/text()"))
      r['status'] = s_text(tr.xpath("./td[8]/text()"))
      tmp = attributes(tr.xpath("./td[5]/a"),"onclick").split("(")[1].split(')')[0].split(",").strip_dquote
      r['flag'], r['term'], r['regt_no'], r['regt_ver'], r['bubin_code'], r['bubin_ver'], r['jumal'] , r['sangho'], r['rosangho'], r['dg_no'] = tmp

      records << r.merge(rec)
    }
    return records
  end
end

def action()
  @br.get("http://www.iros.go.kr/PMainJ.jsp")
  pg = @br.get("http://www.iros.go.kr/ifrontservlet?cmd=INSEInputNseC&FINDGB=1")
  list = JSON.parse(Mechanize.new().get("http://gist.github.com/shyamperi/7f92eb8233f57152a049/raw/b3e3d64ecfeace5d8e7fdf3be1c2e772713da099/kr_chars_ord").body)
  lstart = get_metadata("list",0)
  list[lstart..-1].each{|r|
    pg_no = get_metadata("page_no",1)
    begin
      pg_tmp = @br.post("http://www.iros.go.kr/ifrontservlet?cmd=INSERetrieveBySanghoC",{"FINDGB"=>"1", "FINDSTRTEG"=>"#{r['ord']};", "REGTNO"=>"0", "CLOSEGB"=>"", "JUMALGB"=>"", "SAMEGB"=>"0", "RetFlag"=>"", "STARTSTR"=>"", "NextGb"=>"3", "SEARCHMODE"=>"2", "BEFOREQUERY"=>"", "TOTALQUERY"=>"", "REPEATFLAG"=>"", "IDXSANGHO_SEARCH"=>r['search'], "REALSEARCHSANGHOSTR"=>r['search'], "currentPage"=>pg_no})
      records = scrape(pg_tmp,"list",{"doc"=>Time.now})
      ScraperWiki.save_sqlite(['registry','registration_no'],records)
      break if records.length < 20
      pg_no = pg_no + 1
      save_metadata("page_no",pg_no)
    end while(true)
    delete_metadata("page_no")
    lstart = lstart + 1
    save_metadata("list",lstart)
  }
  delete_metadata("list")
end

action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end
class Array
  def pretty
    self.collect{|a|a.strip}
  end
  def strip_dquote
    self.collect{|a| a.gsub('"',"").strip }
  end
end


def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    data = Iconv.iconv('UTF-8//IGNORE', 'euc-kr', data).first
    records = []
    Nokogiri::HTML(data,nil,'UTF-8').xpath(".//div[@class='list_table']/table/tr[position()>1]").each{|tr|
      r = {}
      r['registry'] = s_text(tr.xpath("./td[2]/text()"))
      r['type'] = s_text(tr.xpath("./td[3]/text()"))
      r['registration_no'] = s_text(tr.xpath("./td[4]/text()"))
      r['company_name'] = s_text(tr.xpath("./td[5]/a/text()"))
      r['entry_type'] = s_text(tr.xpath("./td[6]/text()"))
      r['address'] = s_text(tr.xpath("./td[7]/text()"))
      r['status'] = s_text(tr.xpath("./td[8]/text()"))
      tmp = attributes(tr.xpath("./td[5]/a"),"onclick").split("(")[1].split(')')[0].split(",").strip_dquote
      r['flag'], r['term'], r['regt_no'], r['regt_ver'], r['bubin_code'], r['bubin_ver'], r['jumal'] , r['sangho'], r['rosangho'], r['dg_no'] = tmp

      records << r.merge(rec)
    }
    return records
  end
end

def action()
  @br.get("http://www.iros.go.kr/PMainJ.jsp")
  pg = @br.get("http://www.iros.go.kr/ifrontservlet?cmd=INSEInputNseC&FINDGB=1")
  list = JSON.parse(Mechanize.new().get("http://gist.github.com/shyamperi/7f92eb8233f57152a049/raw/b3e3d64ecfeace5d8e7fdf3be1c2e772713da099/kr_chars_ord").body)
  lstart = get_metadata("list",0)
  list[lstart..-1].each{|r|
    pg_no = get_metadata("page_no",1)
    begin
      pg_tmp = @br.post("http://www.iros.go.kr/ifrontservlet?cmd=INSERetrieveBySanghoC",{"FINDGB"=>"1", "FINDSTRTEG"=>"#{r['ord']};", "REGTNO"=>"0", "CLOSEGB"=>"", "JUMALGB"=>"", "SAMEGB"=>"0", "RetFlag"=>"", "STARTSTR"=>"", "NextGb"=>"3", "SEARCHMODE"=>"2", "BEFOREQUERY"=>"", "TOTALQUERY"=>"", "REPEATFLAG"=>"", "IDXSANGHO_SEARCH"=>r['search'], "REALSEARCHSANGHOSTR"=>r['search'], "currentPage"=>pg_no})
      records = scrape(pg_tmp,"list",{"doc"=>Time.now})
      ScraperWiki.save_sqlite(['registry','registration_no'],records)
      break if records.length < 20
      pg_no = pg_no + 1
      save_metadata("page_no",pg_no)
    end while(true)
    delete_metadata("page_no")
    lstart = lstart + 1
    save_metadata("list",lstart)
  }
  delete_metadata("list")
end

action()
