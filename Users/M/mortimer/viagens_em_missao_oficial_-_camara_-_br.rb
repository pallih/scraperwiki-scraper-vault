require 'mechanize'

agent = Mechanize.new
agent.user_agent_alias = 'Mac Safari'

page = agent.get('http://www2.camara.gov.br/transparencia/viagens-em-missao-oficial')

form = page.form_with(:action => "http://www2.camara.gov.br/transparencia/viagens-em-missao-oficial/missao_oficial_index")
options=form.field_with(:name => 'nome-deputado').options
form.radiobuttons_with(:name => 'deputado', :value=>'1')[0].check
#TODO use scraping dates here (from last_scrap to today)
form['dati'] = "12/11/2003"
form['datf'] = "30/12/2011"

start=ScraperWiki.get_var('last_page')
if start == nil || start < 1 || start >= options.length then start = 1 end

for i in start..options.length do
  if options[i] != nil then
    count= ScraperWiki.select("count(travel_id) as c from participants where name='#{options[i].value.gsub('\\','\\\\').gsub('\'','\\\'')}'") #TODO check date too
    if true then #nm != nil && count[0]['c'] == 0 then
      options[i].select
      puts "processing #{options[i].value}"
      begin
        trav_page = agent.submit(form)

        rows = trav_page.search(".//table[@class='tabela-2']/tbody[@class='coresAlternadas']/tr")
        ro_cnt = 0;
        for travel in rows do
          cols = travel.search('.//td')
          relatorio = cols[5].search('.//li')
          
          t_id = -1
          if relatorio.length >0 then
            links = relatorio[0].search('.//a')
            if links.length > 0 && idm = /missao_oficial_relatorio\?codViagem=([^&]*)&ponto=/.match(links[0].attr('href')) then
              t_id = idm[1]
            end
          end # if relatorio.length >0 then
          inicio = Date.strptime(cols[0].inner_text.strip,"%d/%m/%Y")
          termino= Date.strptime(cols[1].inner_text.strip,"%d/%m/%Y")
          travel_data= {'inicio_date'=>inicio, 
                        'termino_date'=>termino,
                         'assunto' => cols[2].inner_text.strip, 'destino' => cols[3].inner_text.strip, 'id'=>t_id}
          ScraperWiki.save_sqlite(unique_keys=['inicio_date', 'termino_date', 'destino', 'id'], data=travel_data, table_name="travels")
  
          participants = cols[4].search('.//li/span')
          mech_links=trav_page.links_with(:href=>/missao_oficial_relatorio/)
          cnt = 0;
          for pa in participants do
                part_data = {'name' => pa.inner_html,'travel_id'=>t_id, 'inicio_date'=>inicio, 'termino_date'=>termino, 'destino' => cols[3].inner_text.strip}
              if t_id != '-1' then
                mech_link = mech_links[cnt+ro_cnt]
                begin
                  r_page = mech_link.click
                  details = r_page.search(".//div[@id='content']/div[@class='sessionBox']//div[contains(@class,'gradient')]")
                  diarias = details[1].search('.//li')
                  part_data['quantity'] = nil
                  if qm = /Quantidade:([ 0-9.]+)/.match(diarias[0].inner_html) then
                     part_data['quantity'] = qm[1].strip.to_f
                  end     
                  part_data['value'] = nil       
                  if qm = /Valor Unit.rio:([^0-9]+)([ 0-9.]+)/.match(diarias[1].inner_html) then
                     part_data['value'] = qm[2].strip.to_f
                     part_data['currency'] = qm[1].strip
                  end
                  pass = details[2].search('.//li')
                  part_data['passagens_pagas_por'] = nil
                  if qm = /Passagens pagas por:(.+)/.match(pass[0].inner_html) then
                     part_data['passagens_pagas_por'] = qm[1].strip
                  end     
                  part_data['tipo_passagem'] = nil       
                  if qm = /Tipo de Passagem:(.+)/.match(pass[1].inner_html) then
                     part_data['tipo_passagem'] = qm[1].strip
                  end
                  cnt=cnt+1
                rescue
                  if mech_link != nil then
                    puts "Error trying to fetch travel details:"+mech_link.href
                  else
                    puts "Error trying to fetch travel details: no mech link!"
                  end
                end #begin-rescue
              end #if t_id != '-1' do
           ScraperWiki.save_sqlite(unique_keys=['inicio_date', 'termino_date', 'destino', 'travel_id', 'name'],
                                   data=part_data, table_name="participants")
  
          end #for pa in participants do
          ro_cnt=ro_cnt+1
        end #for travel in rows do
        ScraperWiki.save_var('last_page', i) 
      rescue
        puts "fail"
      end
    end #if true then #nm != nil && count[0]['c'] == 0 then
  end #if options[i] != nil then
end #for i in start..options.length do
ScraperWiki.save_var('last_full', Date.today) require 'mechanize'

agent = Mechanize.new
agent.user_agent_alias = 'Mac Safari'

page = agent.get('http://www2.camara.gov.br/transparencia/viagens-em-missao-oficial')

form = page.form_with(:action => "http://www2.camara.gov.br/transparencia/viagens-em-missao-oficial/missao_oficial_index")
options=form.field_with(:name => 'nome-deputado').options
form.radiobuttons_with(:name => 'deputado', :value=>'1')[0].check
#TODO use scraping dates here (from last_scrap to today)
form['dati'] = "12/11/2003"
form['datf'] = "30/12/2011"

start=ScraperWiki.get_var('last_page')
if start == nil || start < 1 || start >= options.length then start = 1 end

for i in start..options.length do
  if options[i] != nil then
    count= ScraperWiki.select("count(travel_id) as c from participants where name='#{options[i].value.gsub('\\','\\\\').gsub('\'','\\\'')}'") #TODO check date too
    if true then #nm != nil && count[0]['c'] == 0 then
      options[i].select
      puts "processing #{options[i].value}"
      begin
        trav_page = agent.submit(form)

        rows = trav_page.search(".//table[@class='tabela-2']/tbody[@class='coresAlternadas']/tr")
        ro_cnt = 0;
        for travel in rows do
          cols = travel.search('.//td')
          relatorio = cols[5].search('.//li')
          
          t_id = -1
          if relatorio.length >0 then
            links = relatorio[0].search('.//a')
            if links.length > 0 && idm = /missao_oficial_relatorio\?codViagem=([^&]*)&ponto=/.match(links[0].attr('href')) then
              t_id = idm[1]
            end
          end # if relatorio.length >0 then
          inicio = Date.strptime(cols[0].inner_text.strip,"%d/%m/%Y")
          termino= Date.strptime(cols[1].inner_text.strip,"%d/%m/%Y")
          travel_data= {'inicio_date'=>inicio, 
                        'termino_date'=>termino,
                         'assunto' => cols[2].inner_text.strip, 'destino' => cols[3].inner_text.strip, 'id'=>t_id}
          ScraperWiki.save_sqlite(unique_keys=['inicio_date', 'termino_date', 'destino', 'id'], data=travel_data, table_name="travels")
  
          participants = cols[4].search('.//li/span')
          mech_links=trav_page.links_with(:href=>/missao_oficial_relatorio/)
          cnt = 0;
          for pa in participants do
                part_data = {'name' => pa.inner_html,'travel_id'=>t_id, 'inicio_date'=>inicio, 'termino_date'=>termino, 'destino' => cols[3].inner_text.strip}
              if t_id != '-1' then
                mech_link = mech_links[cnt+ro_cnt]
                begin
                  r_page = mech_link.click
                  details = r_page.search(".//div[@id='content']/div[@class='sessionBox']//div[contains(@class,'gradient')]")
                  diarias = details[1].search('.//li')
                  part_data['quantity'] = nil
                  if qm = /Quantidade:([ 0-9.]+)/.match(diarias[0].inner_html) then
                     part_data['quantity'] = qm[1].strip.to_f
                  end     
                  part_data['value'] = nil       
                  if qm = /Valor Unit.rio:([^0-9]+)([ 0-9.]+)/.match(diarias[1].inner_html) then
                     part_data['value'] = qm[2].strip.to_f
                     part_data['currency'] = qm[1].strip
                  end
                  pass = details[2].search('.//li')
                  part_data['passagens_pagas_por'] = nil
                  if qm = /Passagens pagas por:(.+)/.match(pass[0].inner_html) then
                     part_data['passagens_pagas_por'] = qm[1].strip
                  end     
                  part_data['tipo_passagem'] = nil       
                  if qm = /Tipo de Passagem:(.+)/.match(pass[1].inner_html) then
                     part_data['tipo_passagem'] = qm[1].strip
                  end
                  cnt=cnt+1
                rescue
                  if mech_link != nil then
                    puts "Error trying to fetch travel details:"+mech_link.href
                  else
                    puts "Error trying to fetch travel details: no mech link!"
                  end
                end #begin-rescue
              end #if t_id != '-1' do
           ScraperWiki.save_sqlite(unique_keys=['inicio_date', 'termino_date', 'destino', 'travel_id', 'name'],
                                   data=part_data, table_name="participants")
  
          end #for pa in participants do
          ro_cnt=ro_cnt+1
        end #for travel in rows do
        ScraperWiki.save_var('last_page', i) 
      rescue
        puts "fail"
      end
    end #if true then #nm != nil && count[0]['c'] == 0 then
  end #if options[i] != nil then
end #for i in start..options.length do
ScraperWiki.save_var('last_full', Date.today) 