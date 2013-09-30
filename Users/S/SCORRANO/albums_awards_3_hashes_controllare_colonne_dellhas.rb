require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'



#START OF METHOD 'download_awards' DEFINITION

def download_awards(link, contatore_aggiornato)  #metodo che prende un link album allmusic e scarica le info sugli awards da esso vinti

url = link

doc = Nokogiri.HTML(open(url)) #apertura della pagina web da cui scaricare

rows = doc.search('#billboard-albums tbody tr') #variabile che incamera tutte le info di tutte le righe della tabella degli awards
#puts rows

rows.each do |row| #iterazione su ogni riga dei billboard_albums
  link = row.search('a')[0]
  #puts link
  awards = {} #creazione dell'hash awards
  
  awards[:id] = contatore_aggiornato #conteggio di tutti i file che vengono scaricati dallo scraper
  awards[:album] = url #prende il link dell'album vincitore e a cui bisognerà togliere la stringa '/awards'
  awards[:year] = row.search('.year').inner_text #prende l'anno dell'awards
  #puts bill_albums[:year]
  awards[:album_song] = row.search('.album-title').inner_text #prende il titolo dell'album vincitore
  #puts bill_albums[:title]
  awards[:chart] = row.search('.album-chart').inner_text #prende il nome della classifica dove l'album era presente
  #puts bill_albums[:chart]
  awards[:peak] = row.search('.peak').inner_text #prende la posizione di picco nella classifica dove l'album era presente
  #puts bill_albums[:peak]
  awards[:award_type] = "billboard_album" #tipo di award

  contatore_aggiornato = contatore_aggiornato +1 #aggiornamento del contatore globale dei file scaricati

  ScraperWiki::save_sqlite([:id], awards, table_name="ALL_albums_awards", verbose=0) #salvataggio dell'hash in ordine di id (sempre diverso per evitare sovrascrizioni)

  end #ends iteration on billboard_album rows

rows = doc.search('#billboard-singles tbody tr') #iterazione su ogni riga dei billboard_singles

rows.each do |row|
  link = row.search('a')[0]
  #puts link
  
  awards = {}
  awards[:id] = contatore_aggiornato #conteggio di tutti i file che vengono scaricati dallo scraper
  awards[:album] = url #prende il link dell'album vincitore e a cui bisognerà togliere la stringa '/awards'
  #bill_singles[:id] = num
  awards[:year] = row.search('.year').inner_text #prende l'anno dell'awards
  #puts bill_singles[:year]
  awards[:album_song] = row.search('.single strong a').inner_text#prende il titolo del singolo vincitore
  #puts bill_singles[:s_single]
  awards[:chart] = row.search('.single-chart').inner_text #prende il nome della classifica dove l'album era presente
  #puts bill_singles[:chart]
  awards[:peak] = row.search('.peak').inner_text #prende la posizione di picco nella classifica dove il singolo era presente
  #puts bill_singles[:peak]
  awards[:award_type] = "billboard_singles" #tipo di award
 
  contatore_aggiornato = contatore_aggiornato +1 #aggiornamento del contatore globale dei file scaricati
  
  ScraperWiki::save_sqlite([:id], awards, table_name="ALL_albums_awards", verbose=0) #salvataggio dell'hash in ordine di id (sempre diverso per evitare sovrascrizioni)

  end #ends iteration on billboard_singles rows

rows = doc.search('#grammy-awards')
  if rows == nil #controllare se questo funziona!!!!!!!
    
    return contatore_aggiornato

  else
    rows = doc.search('#grammy-awards tbody tr')
    #puts rows

    rows.each do |row| #iterazione su ogni riga dei grammy_awards
       link = row.search('a')[0]
       #puts link
  
       awards = {}
       awards[:id] = contatore_aggiornato #conteggio di tutti i file che vengono scaricati dallo scraper
       awards[:album] = url #prende il link dell'album vincitore e a cui bisognerà togliere la stringa '/awards'
       awards[:year] = row.search('.year').inner_text #prende l'anno dell'awards
       #puts grammy_awards[:g_year]
       awards[:album_song] = row.search('.grammy-title').inner_text #prende il titolo del singolo o album vincitore
       #puts grammy_awards[:album_track]
       awards[:chart] = row.search('td.grammy-award').inner_text.strip #prende il tipo di grammy award vinto
       #puts grammy_awards[:winner]
       awards[:peak] = row.search('.grammy-winner a').map { |link| link['href'] } #link dei vincitori del grammy
       #link[:href]
       #puts grammy_awards[:winner_URL]
       awards[:award_type] = "grammy_awards" #tipo di award
       #puts grammy_awards[:award_type] 

       contatore_aggiornato= contatore_aggiornato+ 1 #aggiornamento del contatore globale dei file scaricati
 
       ScraperWiki::save_sqlite([:id], awards, table_name="ALL_albums_awards", verbose=0) #salvataggio dell'hash in ordine di id (sempre diverso per evitare sovrascrizioni)

       end #ends iteration on the grammy rows

       return contatore_aggiornato

  end #ends if-else checking on grammy-awards



end #ends method 'download_awards' definition 

#END OF METHOD DEFINITION





#START OF THE PROGRAM DOWNLOAD ALBUMS' AWARDS

ScraperWiki::attach("all_artists_albums_url_e_info_definitivo_step_1_1_", "step1")#prende le informazioni dallo scraper step 1 con solo i link degli
                                                                                  #album dell'artista(bisogna usare l'url dello scraper!!) e inoltre
                                                                                  #cambia il nome dello scraper in uno dato da me che in questo caso è
                                                                                  #'step1'
cont=0
data = ScraperWiki::select(              #prende i dati dalla tabella 'data' dello scraper step 1
    "* from step1.ONLY_albums_URL
    order by album_url desc limit 150"    #il limite di righe che può prendere in questo caso è 50 (supponendo che gli album di un'artista siano meno di 50 in tutto ma si può modificare e ritoccare a rialzo)
)
data.each do |slot|                      #itera negli elementi dell'hash di dati provenienti dallo step1
  #puts slot
  
  slot.each do |x|                       #itera sugli url singoli dello step 1
    link_allmusic = x[1]+"/awards"
                                         #cambia l'url dell'album aggiungendo "/awards" per accedere alla pagina dei credits di ogni album
    #puts link
    if cont==0
      cont = download_awards(link_allmusic, cont)      #invocazione del metodo 'download_awards' con passaggio di volta in volta del link da cui scaricare gli awards
      
    else 
      cont = download_awards(link_allmusic, cont)      #invocazione del metodo 'download_awards' con passaggio di volta in volta del link da cui scaricare gli awards

    end                                  #fine dell'if-else 
  end                                    #fine del primo ciclo di iterazione sugli slot
end                                      #fine del secondo ciclo di iterazione sui link

#END OF THE PROGRAM DOWNLOAD ALBUMS' AWARDSrequire 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'



#START OF METHOD 'download_awards' DEFINITION

def download_awards(link, contatore_aggiornato)  #metodo che prende un link album allmusic e scarica le info sugli awards da esso vinti

url = link

doc = Nokogiri.HTML(open(url)) #apertura della pagina web da cui scaricare

rows = doc.search('#billboard-albums tbody tr') #variabile che incamera tutte le info di tutte le righe della tabella degli awards
#puts rows

rows.each do |row| #iterazione su ogni riga dei billboard_albums
  link = row.search('a')[0]
  #puts link
  awards = {} #creazione dell'hash awards
  
  awards[:id] = contatore_aggiornato #conteggio di tutti i file che vengono scaricati dallo scraper
  awards[:album] = url #prende il link dell'album vincitore e a cui bisognerà togliere la stringa '/awards'
  awards[:year] = row.search('.year').inner_text #prende l'anno dell'awards
  #puts bill_albums[:year]
  awards[:album_song] = row.search('.album-title').inner_text #prende il titolo dell'album vincitore
  #puts bill_albums[:title]
  awards[:chart] = row.search('.album-chart').inner_text #prende il nome della classifica dove l'album era presente
  #puts bill_albums[:chart]
  awards[:peak] = row.search('.peak').inner_text #prende la posizione di picco nella classifica dove l'album era presente
  #puts bill_albums[:peak]
  awards[:award_type] = "billboard_album" #tipo di award

  contatore_aggiornato = contatore_aggiornato +1 #aggiornamento del contatore globale dei file scaricati

  ScraperWiki::save_sqlite([:id], awards, table_name="ALL_albums_awards", verbose=0) #salvataggio dell'hash in ordine di id (sempre diverso per evitare sovrascrizioni)

  end #ends iteration on billboard_album rows

rows = doc.search('#billboard-singles tbody tr') #iterazione su ogni riga dei billboard_singles

rows.each do |row|
  link = row.search('a')[0]
  #puts link
  
  awards = {}
  awards[:id] = contatore_aggiornato #conteggio di tutti i file che vengono scaricati dallo scraper
  awards[:album] = url #prende il link dell'album vincitore e a cui bisognerà togliere la stringa '/awards'
  #bill_singles[:id] = num
  awards[:year] = row.search('.year').inner_text #prende l'anno dell'awards
  #puts bill_singles[:year]
  awards[:album_song] = row.search('.single strong a').inner_text#prende il titolo del singolo vincitore
  #puts bill_singles[:s_single]
  awards[:chart] = row.search('.single-chart').inner_text #prende il nome della classifica dove l'album era presente
  #puts bill_singles[:chart]
  awards[:peak] = row.search('.peak').inner_text #prende la posizione di picco nella classifica dove il singolo era presente
  #puts bill_singles[:peak]
  awards[:award_type] = "billboard_singles" #tipo di award
 
  contatore_aggiornato = contatore_aggiornato +1 #aggiornamento del contatore globale dei file scaricati
  
  ScraperWiki::save_sqlite([:id], awards, table_name="ALL_albums_awards", verbose=0) #salvataggio dell'hash in ordine di id (sempre diverso per evitare sovrascrizioni)

  end #ends iteration on billboard_singles rows

rows = doc.search('#grammy-awards')
  if rows == nil #controllare se questo funziona!!!!!!!
    
    return contatore_aggiornato

  else
    rows = doc.search('#grammy-awards tbody tr')
    #puts rows

    rows.each do |row| #iterazione su ogni riga dei grammy_awards
       link = row.search('a')[0]
       #puts link
  
       awards = {}
       awards[:id] = contatore_aggiornato #conteggio di tutti i file che vengono scaricati dallo scraper
       awards[:album] = url #prende il link dell'album vincitore e a cui bisognerà togliere la stringa '/awards'
       awards[:year] = row.search('.year').inner_text #prende l'anno dell'awards
       #puts grammy_awards[:g_year]
       awards[:album_song] = row.search('.grammy-title').inner_text #prende il titolo del singolo o album vincitore
       #puts grammy_awards[:album_track]
       awards[:chart] = row.search('td.grammy-award').inner_text.strip #prende il tipo di grammy award vinto
       #puts grammy_awards[:winner]
       awards[:peak] = row.search('.grammy-winner a').map { |link| link['href'] } #link dei vincitori del grammy
       #link[:href]
       #puts grammy_awards[:winner_URL]
       awards[:award_type] = "grammy_awards" #tipo di award
       #puts grammy_awards[:award_type] 

       contatore_aggiornato= contatore_aggiornato+ 1 #aggiornamento del contatore globale dei file scaricati
 
       ScraperWiki::save_sqlite([:id], awards, table_name="ALL_albums_awards", verbose=0) #salvataggio dell'hash in ordine di id (sempre diverso per evitare sovrascrizioni)

       end #ends iteration on the grammy rows

       return contatore_aggiornato

  end #ends if-else checking on grammy-awards



end #ends method 'download_awards' definition 

#END OF METHOD DEFINITION





#START OF THE PROGRAM DOWNLOAD ALBUMS' AWARDS

ScraperWiki::attach("all_artists_albums_url_e_info_definitivo_step_1_1_", "step1")#prende le informazioni dallo scraper step 1 con solo i link degli
                                                                                  #album dell'artista(bisogna usare l'url dello scraper!!) e inoltre
                                                                                  #cambia il nome dello scraper in uno dato da me che in questo caso è
                                                                                  #'step1'
cont=0
data = ScraperWiki::select(              #prende i dati dalla tabella 'data' dello scraper step 1
    "* from step1.ONLY_albums_URL
    order by album_url desc limit 150"    #il limite di righe che può prendere in questo caso è 50 (supponendo che gli album di un'artista siano meno di 50 in tutto ma si può modificare e ritoccare a rialzo)
)
data.each do |slot|                      #itera negli elementi dell'hash di dati provenienti dallo step1
  #puts slot
  
  slot.each do |x|                       #itera sugli url singoli dello step 1
    link_allmusic = x[1]+"/awards"
                                         #cambia l'url dell'album aggiungendo "/awards" per accedere alla pagina dei credits di ogni album
    #puts link
    if cont==0
      cont = download_awards(link_allmusic, cont)      #invocazione del metodo 'download_awards' con passaggio di volta in volta del link da cui scaricare gli awards
      
    else 
      cont = download_awards(link_allmusic, cont)      #invocazione del metodo 'download_awards' con passaggio di volta in volta del link da cui scaricare gli awards

    end                                  #fine dell'if-else 
  end                                    #fine del primo ciclo di iterazione sugli slot
end                                      #fine del secondo ciclo di iterazione sui link

#END OF THE PROGRAM DOWNLOAD ALBUMS' AWARDS