require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'
require 'pp'
require 'uri'
require 'net/http'
require 'scraperwiki/datastore'
require 'httpclient'
require 'scraperwiki/scraper_require'

def download_album_info(link)

url = link

doc = Nokogiri.HTML(open(url))

details = doc.search('.details') #punta alla barra laterale dove sono contenute tutte le info dell'album
a_url = doc.search('.album-artist a')[0] #punta alla cella 'a' dove si trova l'url dell'artista
#puts a_url

  album_info = {}

  album_info[:url] = url #url dell'album da cui prendere i dati

  album_info[:artist_url] = a_url[:href] #url dell'artista dell'album

  album_info[:release_date] = details.search('.release-date').inner_text.strip #release date dell'album

  album_info[:duration] = details.search('.duration').inner_text.strip #duration dell'album

  #album_info[:genres_url] = doc.xpath('//*[@id="sidebar"]/dl/dd[4]/ul/li/a').map { |link| link['href'] } #selettore xpath per i generi dell'album
  #album_info[:styles_url] = doc.xpath('//*[@id="sidebar"]/dl/dd[5]/ul/li/a').map { |link| link['href'] } #selettore xpath per gli stili dell'album

  album_info[:genres_url] = doc.search('dd.genres a').map { |link| link['href'] }
  album_info[:styles_url] = doc.search('dd.styles a').map { |link| link['href'] }


  moods = doc.xpath('//*[@id="sidebar"]/div[4]/ul/li/a').map { |link| link['href'] } #selettore xpath per i moods dell'album
  album_info[:moods_url] = moods
  #album[:moods_url] = row[:href]

  themes = doc.xpath('//*[@id="sidebar"]/div[5]/ul/li/a').map { |link| link['href'] } #selettore xpath per i themes dell'album
  album_info[:themes_url] = themes

ScraperWiki::save_sqlite([:url], album_info, table_name="ALL_albums_info", verbose=0)

end #ends method 'download_album_info' definition


ScraperWiki::attach("all_artists_albums_url_e_info_definitivo_step_1_1_", "step1")#prende le informazioni dallo scraper step 1 con solo i link degli
                                                                                  #album dell'artista(bisogna usare l'url dello scraper!!) e inoltre
                                                                                  #cambia il nome dello scraper in uno dato da me che in questo caso è
                                                                                  #'step1'


data = ScraperWiki::select(              #prende i dati dalla tabella 'data' dello scraper step 1
    "* from step1.ONLY_albums_URL
    order by album_url desc limit 150"    #il limite di righe che può prendere in questo caso è 50
)
data.each do |slot|                      #itera negli elementi dell'hash di dati provenienti dallo step1
  #puts slot
  
  slot.each do |x|                       #itera sugli url singoli dello step 1
    link_allmusic = x[1]
    #puts link_allmusic
    download_album_info(link_allmusic)
  end                                    #fine del primo ciclo di iterazione sugli slot
end                                      #fine del secondo ciclo di iterazione sui link