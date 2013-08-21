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

url = "http://andreascorrano88.altervista.org/exit_2005-2010_albums.html"

num=1

doc = Nokogiri.HTML(open(url))
#puts doc

rows=doc.search('p a')
#puts rows

rows.each do |row|

link=row[:href]

url = link


doc = Nokogiri.HTML(open(url))

details = doc.search('.details') #punta alla barra laterale dove sono contenute tutte le info dell'album
a_url = doc.search('.album-artist a')[0] #punta alla cella 'a' dove si trova l'url dell'artista
#puts a_url

  album_info = {}

  album_info[:album_url] = url #url dell'album da cui prendere i dati

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

ScraperWiki::save_sqlite([:album_url], album_info, table_name="ALL_albums_info", verbose=0)

end #ends iteration on altervista links

