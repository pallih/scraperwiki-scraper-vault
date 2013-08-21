# Programa en Ruby para obtener información de senadores españoles

html = ScraperWiki.scrape("http://www.senado.es/legis8/senadores/alfabet.html") #esta es la página con la información, sacamos la información en la variable html
puts html #la sacamos por pantalla

senadores={}#declaramos arrays para ir guardando información
electo={}
url={}
Senadorpor={}
Grupo ={}
Nacido={}
EstadoCivil={}
Formacion={}
Partido={}
Otros={}



i=0#contador para ir moviendonos por el array


# Ahora cargamos la libreria nokogiri para poder procesar el html
require 'nokogiri'
doc = Nokogiri::HTML(html)
doc.search('ul> li').each do |senadoryelecto| #buscamos en el html y los nombres de los senadores estan tras las etiquetas <ul><li>, con lo que vamos iterando y sacando una a una
  temp= senadoryelecto.inner_html
  temp=temp.gsub(/<\/?[^>]*>/,"") #con  la  función gsub hacemos un remplazo utilizando expresiones regulares,  see  http://en.wikipedia.org/wiki/Regular_expression, y quitamos todo  el  html
  senadoresyelecto=temp.split(".")
  senadores[i]=senadoresyelecto[0]
  electo[i]=senadoresyelecto[1]
  puts senadores[i]
  puts electo[i]
  i=i+1
end

i=0
doc2 = Nokogiri::HTML(html)
doc2.search('ul> li> a').each do |urls| #buscamos  en el html y los nombres de los senadores estan tras las etiquetas  <ul><li>, con lo que vamos iterando y sacando una a una
  temp=urls['href']
  url[i]=temp.slice(44..46)
  url[i]="http://www.senado.es/legis9/senadores/ficha/"+ url[i] +".html"
  puts url[i]
  i=i+1
end  

#ahora iteramos en el array de urls y en cada una de las páginas sacamos la informacion que nos interesa
for j in 0..i-1
  html = ScraperWiki.scrape(url[j]) #esta es la página con la información, sacamos la información en la variable html
  puts html
  counter=1
  
  doc = Nokogiri::HTML(html)
  doc.search('ul>li').each do |info| #aquí es donde esta la información
    
    temp=info.inner_html
    puts temp
    
    #dependiendo del tipo de información la guardamos en un array u otro
    
    if temp.include?  "Senador por" or temp.include?  "Senadora por"
        Senadorpor[j]=info.inner_html
        Senadorpor[j]=Senadorpor[j].gsub(/<\/?[^>]*>/,"")
        puts "Senadorpor[j] "+ Senadorpor[j]
    end
    if temp.include? "GRUPO PARLAMENTARIO"
        Grupo[j]=info.inner_html
        Grupo[j]=Grupo[j].gsub(/<\/?[^>]*>/,"")
        puts "Grupo[j] "+ Grupo[j]
    end
    if temp.include? "Nacido en" or temp.include? "Nacida en"
        Nacido[j]=info.inner_html
        Nacido[j]=Nacido[j].gsub(/<\/?[^>]*>/,"")
        puts "Nacido[j] "+ Nacido[j]
    end
    if temp.include? "Casad" or temp.include? "Divorciad" or temp.include? "Solter"
        EstadoCivil[j]=info.inner_html
        puts "EstadoCivil[j] "+ EstadoCivil[j]
    end
    if temp.include? "Partido Pol"
         Partido[j]=info.inner_html
         Partido[j]=Partido[j].gsub(/<\/?[^>]*>/,"")
         puts "Partido[j] "+ Partido[j]
     end
    if temp.include? "Formaci"
        Formacion[j]=info.inner_html
        Formacion[j]=Formacion[j].gsub(/<\/?[^>]*>/,"")
        puts "Formacion[j] "+ Formacion[j]
    end
    if temp.include? "MIEMBRO" or temp.include? "REPRESENTANTE" or temp.include? "SECRETARIA" or temp.include? "PRESIDENTE" or temp.include? "VICEPRESIDENTE"
         if counter==1
            Otros[j]=info.inner_html
            Otros[j]=Otros[j].gsub(/<\/?[^>]*>/,"")
         else
            Otros[j]=Otros[j] +"; "+info.inner_html
            Otros[j]=Otros[j].gsub(/<\/?[^>]*>/,"")           
         end
         puts "Otros[j] "+ Otros[j]
         puts "counter "+ counter.to_s()
         counter=counter + 1
     end

  end
  #con la siguiente linea metemos los datos en una tabla donde el nombre del senador es su id único y vamos incoorporando el resto de arrays

  ScraperWiki.save_sqlite(unique_keys=["Senadores"], data={"Senadores"=> senadores[j], "electo"=> electo[j], "url"=> url[j], "Senadorpor"=> Senadorpor[j],"Grupo"=> Grupo[j],"Nacido"=> Nacido[j],"EstadoCivil"=> EstadoCivil[j], "Formacion"=> Formacion[j], "Partido"=> Partido[j], "Otros"=> Otros[j]})

end 




