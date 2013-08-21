# encoding: utf-8
# El objetivo de este scraper es obtener los datos de las subvenciones
# a partidos políticos por gastos ordinarios y de seguridad
# Este es el segundo paso de un scraper combinado (origen: boe_subvpartidospoliticos1)
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

ScraperWiki::attach("master_boe_subvenciones_1")
disposiciones = ScraperWiki::select("* from master_boe_subvenciones_1.swdata")
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
    puts res_date
    puts desc_concept
    concept = "seguridad".eql?(desc_concept) ?  2 : 1  
    puts concept
    left_over = $~.post_match
    puts left_over
    left_over =~ /.*durante\s+el\s+([a-z]+)\s+trimestre\s+del\s+ejercicio\s+(?:de\s+)?(\d{4})/
    desc_period, year = $1, $2
    if $2.nil? 
      log(disp['id'],disp['url'],"Could not get the year of the subsidy")
      next
    end
    puts desc_period
    puts year
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
    puts period
    # We extract the rows of the data table
    rows = doc.css("table.tabla tr")
    puts rows.length
    if rows.length == 0
      log(disp['id'],disp['url'],"Could not get the table data")
      next
    end
    rows.each do |row|
      cells = row.css("td")
      #Ignore header row
      next if cells.length < 2
      data = {
        id: disp['id'],
        url: disp['url'],
        res_date: res_date,
        year: year,
        period: period,
        concept: concept,
        party: cells[0].text.strip,
        amount: cells[1].text.strip.gsub(/\./,"").gsub(/,/,".")
      }
      ScraperWiki::save_sqlite(unique_keys=['id','year','period','concept','party'],data,table_name="swdata",verbose=0)
    end
  end
end

