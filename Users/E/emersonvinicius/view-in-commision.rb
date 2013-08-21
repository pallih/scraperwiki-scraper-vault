sourcescraper = 'in-commision'

limit = 20
offset = 0
project = []

URL_SENADO="http://www.senado.gov.br/atividade/materia/detalhes.asp?p_cod_mate="
data = ScraperWiki.getData(sourcescraper)

id = ENV['URLQUERY']; 

if id.empty? 
  id = '96674';
end 

data.any? do |p| 
  if p['id'] == id
    project = p
  end
end

section_style = 'style="background: #EEE; width: 241px;"'
h1_style = 'style="margin: 0; padding:7px; background: #DDD; font: normal 18px/20px Georgia, serif;"'
a_style = 'style="color: #000;text-decoration:none;"'
p_style = 'style="margin: 0px; padding: 7px; font: normal normal normal 23px/25px Verdana, sans-serif;"'
time_style = 'style="color: #123763; display: block; font-size: 40px; line-height: 44px;"'
span_style = 'style="margin: 5px 0 0; color: #123763; display: block; font-size: 13px; line-height: 14px;"'


puts "<section id=\"project\" #{section_style}>"
puts "<h1 #{h1_style}><a #{a_style} href=\"#{URL_SENADO + project['id']}\">#{project['project_name']}</a></h1>"
puts ""
puts "<p #{p_style}>Parado há <time #{time_style}>#{project['last_stopped']} dias</time>
na comissão <span #{span_style}>#{project['last_commission']}</span></p> "
puts '</section>'
