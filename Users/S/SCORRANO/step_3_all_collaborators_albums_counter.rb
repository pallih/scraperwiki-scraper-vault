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

url = "http://andreascorrano88.altervista.org/andreascorrano88_0002.html"

doc = Nokogiri.HTML(open(url))
#puts doc

rows=doc.search('p a')
#puts rows

rows.each do |row|  #starts the iteration on the links

link=row[:href] 

url = link

doc = Nokogiri.HTML(open(url))

rows = doc.search('tbody tr') #nella pagina profilo del credist va a prendere le info di ogni riga della tabella delle sue collaborazioni e le assegna alla variabile rows
#puts rows

count= -1   #counter of all the albums where the collaborator has partecipated

rows.each do |row| #start of the iteration on the rows
  #link = row.search('a')[0]
  #puts link
  
  count=count+1
 
end #ends the iteration on the rows

credit_albums = {}

credit_albums[:person_url] = url #prende l'URL del collab

credit_albums[:num_of_albums] = count

ScraperWiki::save_sqlite(unique_keys=[:person_url], data=credit_albums, table_name="collaborators_albums", verbose=0)


end #ends the iteration on the links




=begin
#START OF DOWNLOADING PROGRAM

ScraperWiki::attach("only_all_albums_credits_deduplicate_step_2---step3", "step2")  #prende le informazioni dallo scraper step 2 con solo i link univoci dei collaboratori dell'artista(bisogna usare l'url dello scraper!!) e inoltre cambia il nome dello scraper in uno dato da me che in questo caso è 'step2'

#pp ScraperWiki::table_info("step2.swdata")
cont=0

data = ScraperWiki::select(              #prende i dati dalla tabella 'data' dello scraper step 2
    "* from step2.only_credits_URL
    order by url desc limit 1000"        #il limite di righe che può prendere in questo caso è 1000
)
data.each do |slot|                      #itera negli elementi dell'hash di dati provenienti dallo step2
  #puts slot

  slot.each do |x|                       #itera sugli url singoli dello step 2
    #puts x[1]

    link_credits = x[1] << "/credits"
                                         #cambia l'url dell'album aggiungendo "/credits" per accedere alla pagina dei credits di ogni album
    #puts link
    if cont==0 #check iniziale per capire se siamo all'inizio della raccolta degli album (cioè al primo credit)
     cont = download_collab_album(link_credits, cont)      #invocazione del metodo 'download_credits' con passaggio di volta in volta del link da cui scaricare i #credits
      
    else #si verifica quando abbiamo scaricato il primo link e dunque andiamo a scaricare il secondo e via via tutti gli altri
      cont = download_collab_album(link_credits, cont)

    end                                  #fine dell'if-else 
  end                                    #fine del primo ciclo di iterazione sugli slot
end                                      #fine del secondo ciclo di iterazione sui link

#END OF DOWNLOADING PROGRAM
=endrequire 'nokogiri'
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

url = "http://andreascorrano88.altervista.org/andreascorrano88_0002.html"

doc = Nokogiri.HTML(open(url))
#puts doc

rows=doc.search('p a')
#puts rows

rows.each do |row|  #starts the iteration on the links

link=row[:href] 

url = link

doc = Nokogiri.HTML(open(url))

rows = doc.search('tbody tr') #nella pagina profilo del credist va a prendere le info di ogni riga della tabella delle sue collaborazioni e le assegna alla variabile rows
#puts rows

count= -1   #counter of all the albums where the collaborator has partecipated

rows.each do |row| #start of the iteration on the rows
  #link = row.search('a')[0]
  #puts link
  
  count=count+1
 
end #ends the iteration on the rows

credit_albums = {}

credit_albums[:person_url] = url #prende l'URL del collab

credit_albums[:num_of_albums] = count

ScraperWiki::save_sqlite(unique_keys=[:person_url], data=credit_albums, table_name="collaborators_albums", verbose=0)


end #ends the iteration on the links




=begin
#START OF DOWNLOADING PROGRAM

ScraperWiki::attach("only_all_albums_credits_deduplicate_step_2---step3", "step2")  #prende le informazioni dallo scraper step 2 con solo i link univoci dei collaboratori dell'artista(bisogna usare l'url dello scraper!!) e inoltre cambia il nome dello scraper in uno dato da me che in questo caso è 'step2'

#pp ScraperWiki::table_info("step2.swdata")
cont=0

data = ScraperWiki::select(              #prende i dati dalla tabella 'data' dello scraper step 2
    "* from step2.only_credits_URL
    order by url desc limit 1000"        #il limite di righe che può prendere in questo caso è 1000
)
data.each do |slot|                      #itera negli elementi dell'hash di dati provenienti dallo step2
  #puts slot

  slot.each do |x|                       #itera sugli url singoli dello step 2
    #puts x[1]

    link_credits = x[1] << "/credits"
                                         #cambia l'url dell'album aggiungendo "/credits" per accedere alla pagina dei credits di ogni album
    #puts link
    if cont==0 #check iniziale per capire se siamo all'inizio della raccolta degli album (cioè al primo credit)
     cont = download_collab_album(link_credits, cont)      #invocazione del metodo 'download_credits' con passaggio di volta in volta del link da cui scaricare i #credits
      
    else #si verifica quando abbiamo scaricato il primo link e dunque andiamo a scaricare il secondo e via via tutti gli altri
      cont = download_collab_album(link_credits, cont)

    end                                  #fine dell'if-else 
  end                                    #fine del primo ciclo di iterazione sugli slot
end                                      #fine del secondo ciclo di iterazione sui link

#END OF DOWNLOADING PROGRAM
=end