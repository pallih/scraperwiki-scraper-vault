# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.mtq.gouv.qc.ca/pls/apex/"

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
   retry
  end
end

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
   retry
  end
end

def text(str)
  begin
    return (str.nil? or str.text.nil?) ? "" : str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "list"
    lst = []
    Nokogiri::HTML(data).xpath(".//table[@id='R10432126941777590']//table[@class='t3standard' and @summary='Report']/tr[position()>1 and position()<last()]").each{|tr|
      td = tr.xpath("td")
      lst << attributes(td[0].xpath("a"),"href")
    }
    return lst
  elsif act == "details"
    records={"DOC"=>Time.now.to_s,"URL"=>s_url}
    hdr = "-1"
    Nokogiri::HTML(data).xpath(".//*[@id='R3886317546232168' or @id='R3885321914232164' or @id='R3885717878232165' or @id='R3885913021232166' or @id='R40849519870562027' or @id='R12060520927302613']//table[@class='t3standard' and @summary='Report']/tr").each{|tr|
      tmp_hdr = text(tr.xpath("th[@colspan]/text()")) 
      if not (tmp_hdr.nil? or tmp_hdr.empty? )
        hdr = tmp_hdr
        #puts hdr.inspect
        next
      end
      td = tr.xpath("td[@class='t3data']")
      tmp_key = text(tr.xpath("th[@align]/text()|th[@align]/table/tr/th/text()"))
      key = nil
      value = text(td.xpath("text()"))
      case hdr
        when "Identification"
          case tmp_key
            when "Numéro du pont","Numéro du mur","Numéro du ponceau","Numéro du tunnel"
              key = "PROJECT_ID"
            when "Nom"
              key = "NAME"
            when "Type de structure"
              key = "TYPE"
            else
              key = nil
          end
        when "Route"
          case tmp_key
            when "Nom"
              key = "ROUTE"
            when "Classe route"
              key = "C_ROUTE"
          end
        when "Municipalité"
          case tmp_key
            when "Municipalité"
              key = "MUNICIPALITY"
            when "MRC"
              key = "MRC"
            when "CEP"
              key = "CEP"
          end
        when "Obstacle"
          case tmp_key
            when "Nom"
              key = "OBSTACLE"
            when "Type de voie"
              key = "O_TYPE"
            when "Classe route"
              key = "O_ROUTE"
          end
        when "Localisation"
          td_tmp = tr.xpath("td")
          begin
            records['LAT']=text(td_tmp[0].xpath("text()"))
          records['LONG']=text(td_tmp[1].xpath("text()"))
          end if td_tmp.length==2 unless td_tmp.nil? 
          case tmp_key
            when "Latitude"
              key = "LAT"
            when "Longitude"
              key = "LONG"
            when "Carte"
              key = "CART"
              value = attributes(td.xpath("a/img"),"alt")
          end
        when "Dimension"
          case tmp_key
            when /Longueur total/
              key = "TOTAL_LENGTH"
            when /Largeur totale/
              key = "TOTAL_WIDTH"
            when /Longueur tablier/
              key = "LENGTH_TABLIER"
            when /Largeur hors tout/
              key = "OVERALL_WIDTH"
            when /Largeur carrossable/
              key = "CARRIAGE_WIDTH"
            when /Superficie tablier/
              key = "SURFACE_AREA"
            when /Hauteur moyenne/
              key = "AVERAGE_HEIGHT"
            when "Superficie"
              key = "SURFACE"
            when /Ouverture totale/
              key = "TOTAL_OUVERTURE"
            when /Longueur/
              key = "LENGTH"
            when /Superficie totale/
              key = "TOTAL_AREA"
            when /Épaisseur du remblai/
              key = "FILL_THICKNESS"
          end
        when "Année"
          case tmp_key
            when "Construction"
              key = "YR_CONSTRUCT"
          end
        when "Indicateur"
          case tmp_key
            when "Indice decondition générale"
              key = "G_COND"
            when /Indice d'accessibilité/
              key = "A_IDX"
              value = attributes(td.xpath("img"),"alt")
          end
        when "Inspections générales"
          case tmp_key
            when "Dernière inspection générale"
              key = "LG_INSP"
              value = text(td.xpath("nobr/text()"))
            when "Prochaine inspection générale"
              key = "NG_INSP"
            when /Rapport/
              key = "LIMITATION"
              value = "http://www.mtq.gouv.qc.ca"+attributes(td.xpath("a"),"href")
          end
        when "Circulation"
          td_tmp = tr.xpath("td")
          begin
            records['DJMA']=text(td_tmp[0].xpath("text()"))
            records['CAMION']=text(td_tmp[1].xpath("text()"))
          end if td_tmp.length==2 unless td_tmp.nil? 
          #case tmp_key
            #when "DJMA"
            #  key = "DJMA"
            #when "% camion"
            #  key = "CAMION"
          #end
        when "Chaussée"
          case tmp_key
            when "Nombre de voies"
              key = "NO_CHANNELS"
          end
      end
      limitation = attributes(Nokogiri::HTML(data).xpath(".//*[@id='R12060520927302613']//table/tr/td/a"),"href")

      records["LIMITATION"] = "http://www.mtq.gouv.qc.ca"+limitation unless limitation.nil? or limitation.empty? 
      #puts limitation
      #puts [hdr,tmp_key,key,value].inspect
      records[key]= value unless key.nil? 
    }
    ScraperWiki.save_sqlite(unique_keys=['PROJECT_ID'],records,table_name='swdata',verbose=2) unless records['PROJECT_ID'].nil? or records['PROJECT_ID'].empty? 
    puts records.inspect if records['PROJECT_ID'].nil? or records['PROJECT_ID'].empty? 
  end
end

def action(offset)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    begin
      pg = br.get(BASE_URL+"f?p=102:56:4154096641622118:pg_R_10432126941777590:NO&pg_min_row=#{offset}&pg_max_rows=15&pg_rows_fetched=15")
      resp = scrape(pg.body,"list",nil)
      resp.each{|s_url|
        begin
          pg_tmp = br.get(BASE_URL+s_url)
          scrape(pg_tmp.body,"details",BASE_URL+s_url)
        rescue Exception => e
          puts "ERROR: While processing #{s_url} :: #{e.inspect} :: #{e.backtrace}"
          #retry
        end
      }
      lnk = pg.link_with(:text => 'Suivant')
      #puts [lnk.inspect,pg.uri].inspect
      if lnk #pg.at("a[text()='Suivant']")
        offset = offset + 15
        save_metadata("OFFSET",offset)# unless resp.nil? or resp.length ==0 
        pg = br.click(lnk)
      else
        break
      end
    rescue Exception => e
      puts "ERROR: While processing #{offset} :: #{e.inspect} :: #{e.backtrace}"
      #retry
    end while(true)
  end
  delete_metadata("OFFSET")
end
def trial(s_url)
  pg = Mechanize.new().get(s_url)
  scrape(pg.body,"details",s_url)
end
action(get_metadata("OFFSET",1))
#trial(BASE_URL+"f?p=102:53:4154096641622118::NO:53:P53_IDE_STRCT_0001:202267")
#trial(BASE_URL+"f?p=102:53:1229407459053091::NO:53:P53_IDE_STRCT_0001:204312")
