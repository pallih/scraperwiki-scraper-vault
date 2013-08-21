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


url = "http://andreascorrano88.altervista.org/1-1000.html"

num=1

doc = Nokogiri.HTML(open(url))
#puts doc

rows=doc.search('p a')
#puts rows

rows.each do |row|

link=row[:href]

url = link

doc = Nokogiri.HTML(open(url))

rows = doc.search('tbody tr') #nella pagina profilo del credist va a prendere le info di ogni riga della tabella delle sue collaborazioni e le assegna alla variabile rows
#puts rows

rows.each do |row| #start of the iteration on the rows
  link = row.search('a')[0]
  #puts link
  
  credit_albums = {}
  
  credit_albums[:id] = num
  
  credit_albums[:person_url] = url #prende l'URL del collab
  
  credit_albums[:credit] = row.search('td.credit').inner_text.strip #prende il ruolo del collab nell'album analizzato
  #puts credit_album[:name]
  
  credit_albums[:album_artist_url] = row.search('a').map { |link| link['href'] }  #prende direttamente gli URL incompleti (manca http://www.allmusic.com/ da aggiungere poi) di album e artista dell'album separati da una virgola e facilmente completabili una volta importati in excel
  #puts credit_album[:url]
  
  credit_albums[:year] = row.search('td.year').inner_text.strip #prende l'anno della collaborazione all'album analizzato
  #puts credit_album[:year]

  num=num+1

  ScraperWiki::save_sqlite(unique_keys=[:id], data=credit_albums, table_name="collaborators_albums_with_credits_page", verbose=0)

 
end #ends the iteration on the rows

end #ends iteration on altervista links
