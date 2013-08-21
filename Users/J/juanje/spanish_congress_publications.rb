# Spanish Congress' Publications
require 'mechanize'

url = "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Publicaciones/IndPub"
series = ["Serie A: Proyectos de Ley",
          "Serie B: Proposiciones de ley",
          "Serie C: Tratados y Convenios Internacionales",
          "Serie D: General"]

agent = Mechanize.new
agent.get(url) do |page|

  series.each do |serie|

    serie_page = agent.click(page.link_with(:text => /#{serie}/))

    serie_page.parser.xpath('//p[@class = "titulo_iniciativa"]/a').each do |a|
      data = {
        'serie' => serie,
        'publication' => a.text,
        'url' => a.attribute('href').value
        }
      ScraperWiki.save(unique_keys=['publication'], data=data)
    end
  end
end