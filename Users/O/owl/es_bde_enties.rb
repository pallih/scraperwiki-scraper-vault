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
    records = []
    doc = Nokogiri::XML(data)
    doc.remove_namespaces!
    doc.xpath(".//data/row").each{|row|
      r = {}
      r['NOMTIPO'] = attributes(row.xpath("."),"NOMTIPO")
      r['COD_TIPO'] = attributes(row.xpath("."),"COD_TIPO")
      r['COD_BE'] = attributes(row.xpath("."),"COD_BE")
      r['NOMBRE105'] = attributes(row.xpath("."),"NOMBRE105")
      r['OBSERVACIONES'] = attributes(row.xpath("."),"OBSERVACIONES")
      r['NOMCOMERCIAL'] = attributes(row.xpath("."),"NOMCOMERCIAL")
      r['INDICATIVONC'] = attributes(row.xpath("."),"INDICATIVONC")
      r['CODIGOCIF'] = attributes(row.xpath("."),"CODIGOCIF")
      r['ROW_NUM'] = attributes(row.xpath("."),"ROW_NUM")

      records << r.merge(rec)
    }
    return records
  elsif act == "details"
    doc = Nokogiri::XML(data)
    doc.remove_namespaces!
    r = {}
    d = doc.xpath(".//xml[@id='REN_ENTIDADES']/data[@isnull='false']/row") 
    begin
      d.xpath(".").first.attributes.each{|k,v|
        r[v.name] = v.value
      }
    end unless d.nil? or d.empty? 

    return r.merge(rec)
  end
end

def action()
  pg_no = get_metadata("page_no",1)
  begin
    list = scrape(@br.get("http://app.bde.es/ren/app/Search?CFG=ConsultaEntidadesCon.xml&TipoFormato=XML&Paginate=MOVE&NOMBRE=%25&DONDE=11&ORDEN=2&RADIO=0&Page=#{pg_no}"),"list",{})
    lstart = get_metadata("list",0)
    list[lstart..-1].each{|rec|
      records = scrape(@br.get("http://app.bde.es/ren/app/Search?CFG=ConsultaDetalleEntidadCon.xml&TipoFormato=XML&Paginate=OPEN&CODBE=#{rec['COD_BE']}&DONDE=11&RADIO=0&VDETALLE=S"),"details",{})
      ScraperWiki.save_sqlite(['COD_BE'],records,'current_entity_data')
    }
    break if list.length < 10
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
  end while(true)
  delete_metadata("page_no")
end

action()
#puts scrape(@br.get("http://app.bde.es/ren/app/Search?CFG=ConsultaDetalleEntidadCon.xml&TipoFormato=XML&Paginate=OPEN&CODBE=6851&DONDE=11&RADIO=0&VDETALLE=S"),"details",{})
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
    records = []
    doc = Nokogiri::XML(data)
    doc.remove_namespaces!
    doc.xpath(".//data/row").each{|row|
      r = {}
      r['NOMTIPO'] = attributes(row.xpath("."),"NOMTIPO")
      r['COD_TIPO'] = attributes(row.xpath("."),"COD_TIPO")
      r['COD_BE'] = attributes(row.xpath("."),"COD_BE")
      r['NOMBRE105'] = attributes(row.xpath("."),"NOMBRE105")
      r['OBSERVACIONES'] = attributes(row.xpath("."),"OBSERVACIONES")
      r['NOMCOMERCIAL'] = attributes(row.xpath("."),"NOMCOMERCIAL")
      r['INDICATIVONC'] = attributes(row.xpath("."),"INDICATIVONC")
      r['CODIGOCIF'] = attributes(row.xpath("."),"CODIGOCIF")
      r['ROW_NUM'] = attributes(row.xpath("."),"ROW_NUM")

      records << r.merge(rec)
    }
    return records
  elsif act == "details"
    doc = Nokogiri::XML(data)
    doc.remove_namespaces!
    r = {}
    d = doc.xpath(".//xml[@id='REN_ENTIDADES']/data[@isnull='false']/row") 
    begin
      d.xpath(".").first.attributes.each{|k,v|
        r[v.name] = v.value
      }
    end unless d.nil? or d.empty? 

    return r.merge(rec)
  end
end

def action()
  pg_no = get_metadata("page_no",1)
  begin
    list = scrape(@br.get("http://app.bde.es/ren/app/Search?CFG=ConsultaEntidadesCon.xml&TipoFormato=XML&Paginate=MOVE&NOMBRE=%25&DONDE=11&ORDEN=2&RADIO=0&Page=#{pg_no}"),"list",{})
    lstart = get_metadata("list",0)
    list[lstart..-1].each{|rec|
      records = scrape(@br.get("http://app.bde.es/ren/app/Search?CFG=ConsultaDetalleEntidadCon.xml&TipoFormato=XML&Paginate=OPEN&CODBE=#{rec['COD_BE']}&DONDE=11&RADIO=0&VDETALLE=S"),"details",{})
      ScraperWiki.save_sqlite(['COD_BE'],records,'current_entity_data')
    }
    break if list.length < 10
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
  end while(true)
  delete_metadata("page_no")
end

action()
#puts scrape(@br.get("http://app.bde.es/ren/app/Search?CFG=ConsultaDetalleEntidadCon.xml&TipoFormato=XML&Paginate=OPEN&CODBE=6851&DONDE=11&RADIO=0&VDETALLE=S"),"details",{})
