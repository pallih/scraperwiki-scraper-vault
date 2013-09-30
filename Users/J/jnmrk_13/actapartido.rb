# Environmental Investment Organisation Global 800 Carbon Ranking
require 'nokogiri'

EIO_GLOBAL_800_URL = "http://www.acb.com/fichas/LACB57059.php"


eio_global_800_html = ScraperWiki::scrape(EIO_GLOBAL_800_URL)
eio_global_800_doc = Nokogiri::HTML eio_global_800_html

# tr class="estverde

eio_global_800_doc.search("table#estadisticasnew tr").each do |fila|

  cells = fila.search("td")
  if company_cells.count == 11
    company_data = {

      dorsal: cells[0].inner_html,
      nombre: cells[1].search("a").inner_html,
      min: cells[2].inner_html
    }

    ScraperWiki::save_sqlite(['ID: '], dorsal)
  end
end
# Environmental Investment Organisation Global 800 Carbon Ranking
require 'nokogiri'

EIO_GLOBAL_800_URL = "http://www.acb.com/fichas/LACB57059.php"


eio_global_800_html = ScraperWiki::scrape(EIO_GLOBAL_800_URL)
eio_global_800_doc = Nokogiri::HTML eio_global_800_html

# tr class="estverde

eio_global_800_doc.search("table#estadisticasnew tr").each do |fila|

  cells = fila.search("td")
  if company_cells.count == 11
    company_data = {

      dorsal: cells[0].inner_html,
      nombre: cells[1].search("a").inner_html,
      min: cells[2].inner_html
    }

    ScraperWiki::save_sqlite(['ID: '], dorsal)
  end
end
