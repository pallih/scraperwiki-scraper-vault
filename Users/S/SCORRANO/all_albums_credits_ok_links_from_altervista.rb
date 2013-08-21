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


url = "http://andreascorrano88.altervista.org/exits_2005_2010_albums_credits.html"

num=1

doc = Nokogiri.HTML(open(url))
#puts doc

rows=doc.search('p a')
#puts rows

rows.each do |row|

link=row[:href]

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
  
  credit[:id] = num
  
  #credit[:lfm_a_name] = artist_url.inner_text #prende il nome dell'artista autore dell'album
  
  credit[:am_url] = artist_url.search('a').map { |link| link[:href]} #prende il link dell'artista autore dell'album
  
  credit[:person_name] = link.inner_text #prende il nome del collab
  
  credit[:album_url] = url #prende il link della pagina da cui si scaricano i dati e a cui va tolto successivamente la stringa /credits
  
  credit[:person_url] = link[:href] #prende l'URL del collab
  
  credit[:credit] = row.search('.name-credit').inner_text.strip #prende il ruolo che il collab ha avuto nell'album analizzato
  

num=num+1

ScraperWiki::save_sqlite([:id], credit, table_name="ALL_credits_info", verbose=0)
#ScraperWiki.save([:id], credit)

end #ends the iteration on the rows

end #ends iteration over altervista links


