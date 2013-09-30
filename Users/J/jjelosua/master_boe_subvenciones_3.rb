# encoding: utf-8
# El objetivo de este scraper es obtener los datos de las subvenciones
# a partidos políticos por gastos ordinarios y de seguridad
# Este es el tercer paso de un scraper combinado (origen: boe_subvpartidospoliticos1 y 2)
# En este scraper trataremos aquellas disposiciones que no has sido correctamente parseadas
require 'open-uri'
require 'mechanize'

def log(id,url,msg) 
  data_log = {
    id: id,
    url: url,
    msg: msg
  }
  ScraperWiki::save_sqlite(unique_keys=['id'], data_log, table_name="sw_log")
end

agent = Mechanize.new

ScraperWiki::attach("master_boe_subvenciones_2")
disposiciones = ScraperWiki::select("* from master_boe_subvenciones_2.sw_log")
disposiciones.each do |disp|
  # To easen up webpage overload
  sleep(1)
  id = disp['id']
  begin
    page = agent.get(disp['url'])
  rescue Mechanize::ResponseCodeError => the_error
    puts the_error.response_code
  end
  if (page)
    #Access nokogiri parser
    doc = page.parser
    # We extract the title of the resolution
    # We will need to determine the period and concept of the subsidies
    title = doc.css("h3.documento-tit").text.strip
    # Ignore documents that are not resolutions
    next if not (title =~ /^Resolución/)
    title =~ /^Resolución de (\d{1,2}\s*de\s*[a-z]+\s*de\s*\d{4}),?.*gastos de (funcionamiento ordinario|seguridad),?/
    if $2.nil? 
      log(disp['id'],disp['url'],"Could not get the concept of the subsidy")
      next
    end
    res_date, desc_concept = $1, $2
    concept = "seguridad".eql?(desc_concept) ?  2 : 1  
    left_over = $~.post_match
    left_over =~ /.*durante\s+el\s+([a-z]+)\s+trimestre\s+del\s+ejercicio\s+(?:de\s+)?(\d{4})/
    desc_period, year = $1, $2
    if $2.nil? 
      log(disp['id'],disp['url'],"Could not get the year of the subsidy")
      next
    end
    period = 0
    case desc_period
      when "primer"
        period = 1
      when "segundo"
        period = 2
      when "tercer"
        period = 3
      when "cuarto"
        period = 4
    end
    # We extract the rows of the data table
    disp_text = doc.css("div#textoxslt").text.gsub(/\n/,"").gsub(/\t/, ' ').squeeze(" ").strip
    disp_text =~ /entidades\s+beneficiarias:(.*)Lo\s+que\s+se\s+hace/
    if $1.nil? 
      log(disp['id'],disp['url'],"Could not parse data on the document")
      next
    end
    disp_data = $1
    disp_data.gsub!(/([0-9])\.([^0-9])/,'\1|\2').gsub!(/\|\s*$/,"")
    subsidies = disp_data.split("|")
    #subsidies = disp_data.split(/[0-9]\.[^0-9]/)
    if (subsidies.length == 0)
      log(disp['id'],disp['url'],"Could not split data on the document")
      next
    end
    subsidies.each do |subsidy|
      parts = subsidy.split(/\s*[:\.]\s+/)
      if (parts.length != 2)
        puts subsidy.length
        puts "Could not split party and amount on the document #{subsidy} #{disp['url']}"
        next
      end
      data = {
        id: disp['id'],
        url: disp['url'],
        res_date: res_date,
        year: year,
        period: period,
        concept: concept,
        party: parts[0].strip,
        amount: parts[1].strip.gsub(/\./,"").gsub(/,/,".")
      }
      ScraperWiki::save_sqlite(unique_keys=['id','year','period','concept','party'],data,table_name="swdata")
    end
  end
end



# encoding: utf-8
# El objetivo de este scraper es obtener los datos de las subvenciones
# a partidos políticos por gastos ordinarios y de seguridad
# Este es el tercer paso de un scraper combinado (origen: boe_subvpartidospoliticos1 y 2)
# En este scraper trataremos aquellas disposiciones que no has sido correctamente parseadas
require 'open-uri'
require 'mechanize'

def log(id,url,msg) 
  data_log = {
    id: id,
    url: url,
    msg: msg
  }
  ScraperWiki::save_sqlite(unique_keys=['id'], data_log, table_name="sw_log")
end

agent = Mechanize.new

ScraperWiki::attach("master_boe_subvenciones_2")
disposiciones = ScraperWiki::select("* from master_boe_subvenciones_2.sw_log")
disposiciones.each do |disp|
  # To easen up webpage overload
  sleep(1)
  id = disp['id']
  begin
    page = agent.get(disp['url'])
  rescue Mechanize::ResponseCodeError => the_error
    puts the_error.response_code
  end
  if (page)
    #Access nokogiri parser
    doc = page.parser
    # We extract the title of the resolution
    # We will need to determine the period and concept of the subsidies
    title = doc.css("h3.documento-tit").text.strip
    # Ignore documents that are not resolutions
    next if not (title =~ /^Resolución/)
    title =~ /^Resolución de (\d{1,2}\s*de\s*[a-z]+\s*de\s*\d{4}),?.*gastos de (funcionamiento ordinario|seguridad),?/
    if $2.nil? 
      log(disp['id'],disp['url'],"Could not get the concept of the subsidy")
      next
    end
    res_date, desc_concept = $1, $2
    concept = "seguridad".eql?(desc_concept) ?  2 : 1  
    left_over = $~.post_match
    left_over =~ /.*durante\s+el\s+([a-z]+)\s+trimestre\s+del\s+ejercicio\s+(?:de\s+)?(\d{4})/
    desc_period, year = $1, $2
    if $2.nil? 
      log(disp['id'],disp['url'],"Could not get the year of the subsidy")
      next
    end
    period = 0
    case desc_period
      when "primer"
        period = 1
      when "segundo"
        period = 2
      when "tercer"
        period = 3
      when "cuarto"
        period = 4
    end
    # We extract the rows of the data table
    disp_text = doc.css("div#textoxslt").text.gsub(/\n/,"").gsub(/\t/, ' ').squeeze(" ").strip
    disp_text =~ /entidades\s+beneficiarias:(.*)Lo\s+que\s+se\s+hace/
    if $1.nil? 
      log(disp['id'],disp['url'],"Could not parse data on the document")
      next
    end
    disp_data = $1
    disp_data.gsub!(/([0-9])\.([^0-9])/,'\1|\2').gsub!(/\|\s*$/,"")
    subsidies = disp_data.split("|")
    #subsidies = disp_data.split(/[0-9]\.[^0-9]/)
    if (subsidies.length == 0)
      log(disp['id'],disp['url'],"Could not split data on the document")
      next
    end
    subsidies.each do |subsidy|
      parts = subsidy.split(/\s*[:\.]\s+/)
      if (parts.length != 2)
        puts subsidy.length
        puts "Could not split party and amount on the document #{subsidy} #{disp['url']}"
        next
      end
      data = {
        id: disp['id'],
        url: disp['url'],
        res_date: res_date,
        year: year,
        period: period,
        concept: concept,
        party: parts[0].strip,
        amount: parts[1].strip.gsub(/\./,"").gsub(/,/,".")
      }
      ScraperWiki::save_sqlite(unique_keys=['id','year','period','concept','party'],data,table_name="swdata")
    end
  end
end



