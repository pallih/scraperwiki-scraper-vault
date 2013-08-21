require 'mechanize'
require 'nokogiri'

ScraperWiki.attach("votacao_deputado_br")
proposicoes= ScraperWiki.select("distinct year, number, type from votacao_deputado_br.votacao where year not null")

#for some strange reason, the webservice return FORBIDEN when trying to access it directly, so we trick it to think that we are coming
# from the test form
agent = Mechanize.new
page = agent.get('http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx?op=ObterProposicao')

form = page.forms.first

for prop in proposicoes do
  if prop['type'] != 'REQ' && prop['type'] != 'REC' then #the webservice doesn't like the REQ or REC types (??)
    #check that we haven't processed this one already
      count= ScraperWiki.select("count(id) as c from proposicoes where tipo='#{prop['type']}' and numero='#{prop['number']}' and ano='#{prop['year']}'")
    if count[0]['c'] == 0 then
      form['tipo'] = prop['type']
      form["numero"] = prop['number']
      form["ano"] = prop['year']
      puts "scraping tipo=#{prop['type']} and numero=#{prop['number']} and ano=#{prop['year']}"
      page = agent.submit(form)
      @doc = Nokogiri::XML(page.body)
      prop_data = {'tipo' => prop['type'], 'numero'=>prop['number'], 'ano' => prop['year']}
      prop_data['id'] =  @doc.xpath('.//idProposicao').inner_text
      prop_data['ementa'] = @doc.xpath('.//Ementa').inner_text
      prop_data['explicacao_ementa'] = @doc.xpath('.//ExplicacaoEmenta').inner_text
      prop_data['autor'] = @doc.xpath('.//Autor').inner_text
      prop_data['data'] = Date.strptime(@doc.xpath('.//DataApresentacao').inner_text,"%d/%m/%Y")
      prop_data['regime_tramitacao'] = @doc.xpath('.//RegimeTramitacao').inner_text
      prop_data['apreciacao'] = @doc.xpath('.//Apreciacao').inner_text
      prop_data['situacao'] = @doc.xpath('.//Situacao').inner_text
      prop_data['links_inteiro_teor'] = @doc.xpath('.//LinkInteiroTeor').inner_text
    
      #get the indexacao keywords and put that in a better format in a table.
      keywords = @doc.xpath('.//Indexacao').inner_text.split(/[,.\n_]/)
      for key in keywords do
        key.strip!
      if key.length > 0 then
        ScraperWiki.save_sqlite(unique_keys=['tipo', 'ano','numero', 'proposicao_id', 'keyword'], 
                                data={'tipo' => prop['type'], 'numero'=>prop['number'], 'ano' => prop['year'],
                                      'proposicao_id'=>prop_data['id'], 'keyword' => key.downcase},
                                table_name="indexacao")
        end
      end
  
      ScraperWiki.save_sqlite(unique_keys=['tipo', 'ano','numero', 'id'], data=prop_data, table_name="proposicoes") 
    end
  end
end
