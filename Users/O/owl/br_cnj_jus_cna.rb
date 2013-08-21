# Blank Ruby
require 'nokogiri'
require 'mechanize'
require 'pp'


Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://www.cnj.jus.br/'
@url = BASE_URL + 'cna/View/consultaPublicaView.php'
@br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}

def strip(str)
   return (str.nil?) ? "":str.gsub(/[\x80-\xff]|\302\240|^\s+|:|\s+$|\n|\t|\r/,"")
end

def getAttributes(opt,attr)
    return (opt.nil? or opt.first.nil? or opt.first.attributes.nil?) ? "" : opt.first.attributes[attr].value
end

def scrape_loc(data)
  loc = []
  Nokogiri::HTML(data).xpath('.//*[@id="ufLocalizacao"]/option[position() > 1]').each{|l|
      loc << l.inner_text
  }
  return loc
end

def scrape_com(data)
    loc = []
    Nokogiri::HTML(data).xpath('.//*[@id="comarca"]/option[position() > 1]').each{|l|
        loc << l.attributes['value'].text
    }
  return loc
end

def scrape_vara(data)
    loc = []
    Nokogiri::HTML(data).xpath('.//*[@id="vara"]/option[position() > 1]').each{|l|
        loc << l.attributes['value'].text
    }
    return loc
end

def scrape_details(data)
    details = {}
    Nokogiri::HTML(data).xpath('.//*[@id="procura_criancas"]/table/tr[position()>1 and position()<=8]').each{|td|
        details[strip(td.children[0].text)] = td.children[2].text
    }
    return details
end

def get_loc(url)
    pg = @br.get(url)
    scrape_loc(pg.body)
end

def get_com(url)
    pg = @br.get(url)
    scrape_com(pg.body)
end

def get_vara(url)
    pg = @br.get(url)
    scrape_vara(pg.body)
end

def get_details(url)
    pg=@br.get(url)
    scrape_details(pg.body)
end

begin
#loc = get_loc(BASE_URL+'cna/View/consultaPublicaView.php')
#loc.each{|l|
#    com = get_com(BASE_URL+"cna/Controle/ConsultaPublicaBuscaControle.php?transacao=COMARCAS&uf=#{l}")
#    com.each{|v|
#        vara = get_vara(BASE_URL+"cna/Controle/ConsultaPublicaBuscaControle.php?transacao=VARAS&comarca=#{v}")
#        vara.each{|va|
#            details =  get_details(BASE_URL+"cna/Controle/ConsultaPublicaBuscaControle.php?transacao=CONSULTA&ufLocalizacao=#{l}&comarca=#{v}&vara=#{va}")
#            ScraperWiki.save(unique_keys=['Endereo'],details)
#        }
#    }
#}
strt = ScraperWiki.get_var("STRT",1)
if strt == 3157
  strt = 1
end
range = (strt..3156).to_a
range.each{|va|
  details = get_details(BASE_URL+"cna/Controle/ConsultaPublicaBuscaControle.php?transacao=CONSULTA&vara=#{va}")
  puts details.inspect
  begin
    details["ID"] = va
    ScraperWiki.save(unique_keys=['ID'],details)
    ScraperWiki.save_var("STRT",va+1)
  end unless details.nil?  or details['Endereo'].empty? 
}
rescue Exception => e
  puts e.inspect
end
