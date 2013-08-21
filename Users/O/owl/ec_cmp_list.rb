# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://declaraciones.sri.gob.ec"

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end
class Array
  def pretty
    self.collect{|a|a.strip}
  end
end


def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='reporte']/tr[position()>1]").each{|tr|
      records << {
        "company_number" => s_text(tr.xpath("./td[1]/a/text()")),
        "company_name" => s_text(tr.xpath("./td[2]/text()")),
        "trade_name" => s_text(tr.xpath("./td[3]/text()")),
        "doc" => Time.now
      }.merge(rec) unless s_text(tr.xpath("./td[1]/a/text()")).empty? 
    }
    return records
  end
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  params,ttl = {"pagina"=>"resultado","opcion"=>"2","texto"=>srch},0
  pg_no = 1
  begin
    url = (pg_no == 1)? BASE_URL+"/facturacion-internet/consultas/publico/ruc-datos1.jspa" : BASE_URL + "/facturacion-internet/consultas/publico/ruc-datos1-paginador.jspa"
    pg = br.post(url,params) rescue nil
    break if pg.nil? 
    return srch,0 if pg.body =~ /No se han encontrado resultados para esta/
    return srch,50 if pg.body =~ /demasiados resultados para el valor que se ingres|Ha ocurrido un error inesperado en el sistema/
    list = scrape(pg.body,"list",{})
    ScraperWiki.save_sqlite(['company_number'],list)
    ttl = ttl + list.length
    break if list.length < 10
    pg_no = pg_no + 1
    params = {"accion"=>"ir-a-pagina","numeroPagina"=>pg_no}
  end while(true)
  return srch,ttl
end

save_metadata("wa",true)

begin
  trail = get_metadata("trail","A").split(">>")
  srch = trail.last
  MAX_T = 20
  begin
    prev,ret = action(srch)
    if ret >= MAX_T
      srch = srch + "A"
      trail << srch
    else
      tmp = ''
      begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
      if tmp.nil? 
        trail == ["A"]
      else
        srch = (tmp == 'Z')? "A" : tmp.next
        trail << srch
      end
    end
    puts [ret,prev,srch,trail.join(">>")].inspect
    save_metadata("trail",trail.join(">>"))
    sleep(5)
  end while(true)
end
delete_metadata("trail")



