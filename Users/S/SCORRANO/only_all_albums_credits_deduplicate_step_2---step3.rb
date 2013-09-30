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

def download_credits(link)

url = link

doc = Nokogiri.HTML(open(url))
#puts doc

rows = doc.search('tr') #dò a rows il contenuto di ogni riga della tabella dei credits dell'album che sto analizzando
#puts rows
artist_url = doc.search('#wrapper .album-artist')[0] #prende la riga in alto a sinistra dove c'è il nome e il link dell'artista
#puts artist_url

rows.each do |row| #start of the iteration on the rows  
  link = row.search('a')[0]
  #puts link

  credit = {}
  #credit[:artist_name] = artist_url.inner_text #prende il nome dell'artista autore dell'album
  #credit[:artist_url] = artist_url.search('a').map { |link| link[:href]} #prende il link dell'artista autore dell'album
  #puts credit[:artist_url] 
  #credit[:name] = link.inner_text #prende il nome del collab
  #puts credit[:name]
  #credit[:album_name] = url #prende il link della pagina da cui si scaricano i dati e a cui va tolto successivamente la stringa /credits
  credit[:url] = link[:href] #prende l'URL del collab
  #puts credit[:url]
  #credit[:role] = row.search('.name-credit').inner_text.strip #prende il ruolo che il collab ha avuto nell'album analizzato
  #puts credit[:role]

#ScraperWiki.save([:url], credit)
ScraperWiki::save_sqlite([:url], credit, table_name="only_credits_URL", verbose=0)

end #ends the iteration on the rows
end #ends method def


ScraperWiki::attach("all_artists_albums_url_e_info_definitivo_step_1_1_", "step1") #prende le informazioni dallo scraper step 1 con solo i link degli album dell'artista(bisogna usare l'url dello scraper!!) e inoltre cambia il nome dello scraper in uno dato da me che in questo caso è 'step1'
#pp ScraperWiki::table_info("step1.swdata")
data = ScraperWiki::select(              #prende i dati dalla tabella 'data' dello scraper step 1
    "* from step1.ONLY_albums_URL 
    order by album_url desc limit 50"    #il limite di righe che può prendere in questo caso è 50
)
data.each do |slot|                      #itera negli elementi dell'hash di dati provenienti dallo step1
  #puts slot
  slot.each do |x|                       #itera sugli url singoli dello step 1
    link_allmusic = x[1]+"/credits"      #cambia l'url dell'album aggiungendo "/credits" per accedere alla pagina dei credits di ogni album
    #puts link
    download_credits(link_allmusic)      #invocazione del metodo 'download_credits' con passaggio di volta in volta del link da cui scaricare i credits
end                                      #fine del primo ciclo di iterazione sugli slot
end                                      #fine del secondo ciclo di iterazione sui linkrequire 'nokogiri'
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

def download_credits(link)

url = link

doc = Nokogiri.HTML(open(url))
#puts doc

rows = doc.search('tr') #dò a rows il contenuto di ogni riga della tabella dei credits dell'album che sto analizzando
#puts rows
artist_url = doc.search('#wrapper .album-artist')[0] #prende la riga in alto a sinistra dove c'è il nome e il link dell'artista
#puts artist_url

rows.each do |row| #start of the iteration on the rows  
  link = row.search('a')[0]
  #puts link

  credit = {}
  #credit[:artist_name] = artist_url.inner_text #prende il nome dell'artista autore dell'album
  #credit[:artist_url] = artist_url.search('a').map { |link| link[:href]} #prende il link dell'artista autore dell'album
  #puts credit[:artist_url] 
  #credit[:name] = link.inner_text #prende il nome del collab
  #puts credit[:name]
  #credit[:album_name] = url #prende il link della pagina da cui si scaricano i dati e a cui va tolto successivamente la stringa /credits
  credit[:url] = link[:href] #prende l'URL del collab
  #puts credit[:url]
  #credit[:role] = row.search('.name-credit').inner_text.strip #prende il ruolo che il collab ha avuto nell'album analizzato
  #puts credit[:role]

#ScraperWiki.save([:url], credit)
ScraperWiki::save_sqlite([:url], credit, table_name="only_credits_URL", verbose=0)

end #ends the iteration on the rows
end #ends method def


ScraperWiki::attach("all_artists_albums_url_e_info_definitivo_step_1_1_", "step1") #prende le informazioni dallo scraper step 1 con solo i link degli album dell'artista(bisogna usare l'url dello scraper!!) e inoltre cambia il nome dello scraper in uno dato da me che in questo caso è 'step1'
#pp ScraperWiki::table_info("step1.swdata")
data = ScraperWiki::select(              #prende i dati dalla tabella 'data' dello scraper step 1
    "* from step1.ONLY_albums_URL 
    order by album_url desc limit 50"    #il limite di righe che può prendere in questo caso è 50
)
data.each do |slot|                      #itera negli elementi dell'hash di dati provenienti dallo step1
  #puts slot
  slot.each do |x|                       #itera sugli url singoli dello step 1
    link_allmusic = x[1]+"/credits"      #cambia l'url dell'album aggiungendo "/credits" per accedere alla pagina dei credits di ogni album
    #puts link
    download_credits(link_allmusic)      #invocazione del metodo 'download_credits' con passaggio di volta in volta del link da cui scaricare i credits
end                                      #fine del primo ciclo di iterazione sugli slot
end                                      #fine del secondo ciclo di iterazione sui link