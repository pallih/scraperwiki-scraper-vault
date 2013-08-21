require 'mechanize'

agent = Mechanize.new
page = agent.get('http://www2.camara.gov.br/deputados/pesquisa')

form = page.form('form1')
options=form.field_with(:name => 'deputado').options
start=ScraperWiki.get_var('last_page')
if start == nil || start < 1 || start >= options.length then start = 1 end

for i in start..options.length do
  if options[i] != nil then
    nm = /([A-Z ]*)\|([0-9]+)%/.match(options[i].value)
    count= ScraperWiki.select("count(id) as c from deputados where id=#{nm[2]}")
    if nm != nil && count[0]['c'] == 0 then
      options[i].select
      form.radiobuttons_with(:name => 'rbDeputado', :value=>'VP')[0].check
      
      page = agent.submit(form)
      deputado_name_block = page.search(".//div[@id='content']/h3/a")
      if deputado_name_block != nil then
        begin
          m = /(.*) - (.*)\/(.*)/.match(deputado_name_block.inner_text)
          m2 = /Dep_Detalhe.asp\?id=(.*)/.match(deputado_name_block.attr('href'))
          if m != nil && m2 != nil then
            deputy_data = {'name'=>m[1], 'party'=>m[2], 'state'=>m[3], 'id' =>m2[1]}
            puts "scraping #{m[1]}"
            deputy_id = m2[1]
            
            ScraperWiki.save_sqlite(unique_keys=['name', 'party', 'id'], data=deputy_data, table_name="deputados")
            
            rows = page.search(".//div[@id='content']/table[@class='tabela-1']/tr")
            date = nil
            session_id = nil
            for row in rows do
              cols = row.search(".//td")
              if row.attr('class') == 'even' then
                if nm = /SESS.O (ORDIN.RIA|EXTRAORDIN.RIA) N. ([0-9]+) - ([0-9]{2}\/[0-9]{2}\/[0-9]{4})/i.match(cols[1].inner_text) then
                  date = Date.strptime(nm[3],"%d/%m/%Y")
                  session_data = {'sessao_id'=>nm[2], 'date' => date, 'type' => nm[1]}
                  session_id = nm[2]
                  presence_data = {'deputado_id'=> deputy_id, 'date' => date, 'sessao_id'=>nm[2]}
                  if cols[2].inner_text =~ /presente/i then
                    presence_data['presente'] = true
                  elsif cols[2].inner_text =~ /justificada/i then
                    presence_data['presente'] = false
                    presence_data['justificativa'] = cols[4].inner_text.gsub(/\W/,' ').strip
                  else
                    presence_data['presente'] = false
                  end
                  ScraperWiki.save_sqlite(unique_keys=['deputado_id', 'date', 'sessao_id'], data=presence_data, table_name="presence")
                  ScraperWiki.save_sqlite(unique_keys=['sessao_id', 'date'], data=session_data, table_name="sessao")
                end
              elsif session_id != nil then
                vote_data = {'deputado_id'=>deputy_id, 'date'=>date, 'sessao_id'=>session_id}
                if vm = /(([A-Z]+)[^0-9]+([0-9]+)\/([0-9]+)|[^-]+) - (.*)/.match(cols[1].inner_text.strip) then
                  vote_data['full_ref'] = vm[1].gsub(/\W/,' ').strip
                  vote_data['type'] = vm[2]
                  vote_data['number'] = vm[3]
                  vote_data['year'] = vm[4]
                  vote_data['title'] = vm[5]
                  
                  v = cols[3].inner_text.gsub(/\W/,' ').strip
                  vote_data['vote'] = if v.length >0 then  v[0].chr else nil end
                  
                  ScraperWiki.save_sqlite(unique_keys=['deputado_id', 'sessao_id','full_ref', 'title'], data=vote_data, table_name="votacao")
                end    
              end
            end
            ScraperWiki.save_var('last_deputado', i)
          end
        rescue
        end
      end
    end
  end
end
ScraperWiki.save_var('last_full', Date.today) 