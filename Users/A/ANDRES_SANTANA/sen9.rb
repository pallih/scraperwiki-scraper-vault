#=======================================================================================================================================
# Muy buenas ladrondebicicletas, como puedes ver he estado tocando algunas cosillas. Lee los comentarios y me vas contando que te parece
# - Programa en Ruby para obtener información de senadores españoles de la 9a legislatura
#=======================================================================================================================================

# STEP 0 - DECLARACION DE VARIABLES
# Declaramos arrays para ir guardando información
#_______________________________________________________________________________________________________________________________________

senadores={},electo={},url={},electo9={},Senadorpor={},ProvyFecha={},Prov={},Fecha={},Grupo ={},Nacido={},EstadoCivil={},Hijos={},Num_Hijos={},Formacion={},Partido={},Otros={},Miembr={},Repres={},Secret={},Presid={},Vicepr={}

# STEP 1 - INFORMACION DE LISTADO DE SENADORES
#_______________________________________________________________________________________________________________________________________
html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html") #esta es la página con la información, sacamos la información en la variable html
puts html #la sacamos por pantalla

i=0#contador para ir moviendonos por el array
# Ahora cargamos la libreria nokogiri para poder procesar el html
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'UTF-8')
doc.search('ul> li').each do |temp| #buscamos en el html y los nombres de los senadores estan tras las etiquetas <ul><li>, con lo que vamos iterando y sacando una a una
  ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
  temp = ic.iconv(temp.inner_html)   
  puts temp 
  temp=temp.gsub(/<\/?[^>]*>/,"") #con  la  función gsub hacemos un remplazo utilizando expresiones regulares,  see  http://en.wikipedia.org/wiki/Regular_expression, y quitamos todo  el  html
  senadoresyelecto=temp.split(".")
  senadores[i]=senadoresyelecto[0]
  electo[i]=senadoresyelecto[1]
  #provinciaydia=senadores[i].split("desde el") No me funciona separar esta informacion---Pero aqui senadores no tiene informacion sobre provincia y dia, eso esta abajo en senadorpor 
  #province[i]=provinciaydia[0]  entra[i]=provinciaydia[1]
  
  electo9[i]=electo[i].slice(0..10) #esta variable sera 1=Designado/a, 2=Electo/a
  electo9[i]=electo9[i].gsub(/Electo por/, "2")
  electo9[i]=electo9[i].gsub(/Electa por/, "2") 
  electo9[i]=electo9[i].gsub(/Designado/, "1") 
  electo9[i]=electo9[i].gsub(/Designada/, "1")

  # esto de arriba tambien lo puedes hacer de forma mas elegante
  #if electo[i].include? "Elect" 
  #   electo[i]=2
  #else 
  #   electo[i]=1
  #end
  
  puts senadores[i]
  puts electo[i] 
  puts electo9[i]
  i=i+1

end

# STEP 2 - OBTENEMOS URLS DE LAS PAGINAS DE LOS SENADORES
#_______________________________________________________________________________________________________________________________________
i=0
doc2 = Nokogiri::HTML(html, nil, 'UTF-8')
doc2.search('ul> li> a').each do |urls| #buscamos  en el html y los nombres de los senadores estan tras las etiquetas  <ul><li>, con lo que vamos iterando y sacando una a una
  temp=urls['href']
  url[i]=temp.slice(44..46)
  url[i]="http://www.senado.es/legis9/senadores/ficha/"+ url[i] +".html"
  puts url[i]
  i=i+1
end  


# STEP 3 - SACAMOS INFORMACION DE CADA UNA DE LAS PAGINAS DE SENADORES
# Ahora iteramos en el array de urls y en cada una de las páginas sacamos la informacion que nos interesa
#_______________________________________________________________________________________________________________________________________

for j in 0..i-1
  html = ScraperWiki.scrape(url[j]) #esta es la página con la información, sacamos la información en la variable html
  puts html
  counter=1 #   contador general que incluye a cualquiera de los 5 que siguen, tomados como un conjunto único
  countermi=1 # contador de 'Miembro'
  counterre=1 # contador de 'Representante'
  counterse=1 # contador de 'Secretaria'
  counterpr=1 # contador de 'Presidente'
  countervi=1 # contador de 'Vicepresidente'
  counterhi=1 # contador de 'Hijos'


  doc = Nokogiri::HTML(html, nil, 'UTF-8')
  doc.search('ul>li').each do |info| #aquí es donde esta la información
    
    temp=info.inner_html
    #puts temp
    
    #dependiendo del tipo de información la guardamos en un array u otro
    
    if temp.include?  "Senador por" or temp.include?  "Senadora por"
        Senadorpor[j]=info.inner_html
        Senadorpor[j]=Senadorpor[j].gsub(/<\/?[^>]*>/,"")
        ProvyFecha=Senadorpor[j].split("desde el")
        Prov[j]=ProvyFecha[0].gsub(/Senador?. por /,"") # elegantemente utilizando una expresion regular quitamos senador o senadora por
        Fecha[j]=ProvyFecha[1].gsub(/d&iacute;a /,"")#nos deshacemos de "dia"
        puts "Senadorpor[j] "+ Senadorpor[j]
        puts "Prov[j]"+ Prov[j]
        puts "Fecha[j]"+ Fecha[j] 
    end
  
    if temp.include? "GRUPO PARLAMENTARIO"
        Grupo[j]=info.inner_html
        Grupo[j]=Grupo[j].gsub(/<\/?[^>]*>/,"")
        #puts "Grupo[j] "+ Grupo[j]
    end
    if temp.include? "Nacido en" or temp.include? "Nacida en"
        Nacido[j]=info.inner_html
        Nacido[j]=Nacido[j].gsub(/<\/?[^>]*>/,"")
        #puts "Nacido[j] "+ Nacido[j]
    end 
    # Ahora intentare separar la info del estado civil y la de los hijos. 
    if temp.include? "Casad" or temp.include? "Divorciad" or temp.include? "Solter" or temp.include? "Viud"
        EstadoCivil[j]=info.inner_html        
        EstadoCivil[j]=EstadoCivil[j].gsub(/Casado/,"C")  
        EstadoCivil[j]=EstadoCivil[j].gsub(/Casada/,"c")
        EstadoCivil[j]=EstadoCivil[j].gsub(/Divorciado/,"D")  
        EstadoCivil[j]=EstadoCivil[j].gsub(/Divorciada/,"d")
        EstadoCivil[j]=EstadoCivil[j].gsub(/Soltero/,"S")     
        EstadoCivil[j]=EstadoCivil[j].gsub(/Soltera/,"s")
        EstadoCivil[j]=EstadoCivil[j].gsub(/Viudo/,"V")     
        EstadoCivil[j]=EstadoCivil[j].gsub(/Viuda/,"v")    
        Hijos[j]=EstadoCivil[j]
        #EstadoCivil[j]=EstadoCivil[j].gsub(/!/,"99") Intentaba convertir los blancos en 99, pero no funciona
        EstadoCivil[j]=EstadoCivil[j].slice(0..1) 
        Hijos[j]=Hijos[j].slice(1..50)
        #Hijos[j]=Hijos[j].gsub(/./, "") tampoco me puedo quitar el punto porque me deja sin datos
        puts "EstadoCivil[j] "+ EstadoCivil[j]   
        
        # aquí de forma un poco chusquera sacamos el numero de hijos
        puts "Hijos[j] "+ Hijos[j]
        hijos=0
        if Hijos[j].include? "un" or Hijos[j].include? "Un"
            hijos=hijos+1
            #puts hijos        
        end
        if Hijos[j].include? "un" and Hijos[j].include? "Un"
            hijos=hijos+1
            #puts hijos        
        end
        if Hijos[j].include? "dos" or Hijos[j].include? "Dos"
            hijos=hijos+2
            #puts hijos
        end
        if Hijos[j].include? "dos" and Hijos[j].include? "Dos"
            hijos=hijos+2
            #puts hijos
        end
        if Hijos[j].include? "tres" or Hijos[j].include? "Tres"
            hijos=hijos+3
            #puts hijos
        end
        Num_Hijos[j]=hijos
    end 
    if temp.include? "Partido Pol"
         Partido[j]=info.inner_html
         Partido[j]=Partido[j].gsub(/<\/?[^>]*>/,"")
         Partido[j]=Partido[j].slice(25..100) 
         # puts "Partido[j] "+ Partido[j]
     end
    if temp.include? "Formaci"
        Formacion[j]=info.inner_html
        Formacion[j]=Formacion[j].gsub(/<\/?[^>]*>/,"")
        Formacion[j]=Formacion[j].slice(75..200)
        # puts "Formacion[j] "+ Formacion[j]
    end
    if temp.include? "MIEMBRO" or temp.include? "REPRESENTANTE" or temp.include? "SECRETARIA" or temp.include? "PRESIDENTE" or temp.include? "VICEPRESIDENTE" 
         if counter==1
            Otros[j]=info.inner_html
            Otros[j]=Otros[j].gsub(/<\/?[^>]*>/,"")
         else
            Otros[j]=Otros[j] +"; "+info.inner_html
            Otros[j]=Otros[j].gsub(/<\/?[^>]*>/,"")           
         end
         #puts "Otros[j] "+ Otros[j]
         #puts "counter "+ counter.to_s()
         counter=counter + 1
     end
     if temp.include? "MIEMBRO"
         if countermi==1
            Miembr[j]=info.inner_html
            Miembr[j]=Miembr[j].gsub(/<\/?[^>]*>/,"")
         else
            Miembr[j]=Miembr[j] +"; "+info.inner_html
            Miembr[j]=Miembr[j].gsub(/<\/?[^>]*>/,"")           
         end
         #puts "Miembr[j] "+ Miembr[j]
         #puts "countermiembro "+ countermi.to_s()
         countermi=countermi + 1
     end 
     if temp.include? "REPRESENTANTE"
         if counterre==1
            Repres[j]=info.inner_html
            Repres[j]=Repres[j].gsub(/<\/?[^>]*>/,"")
         else
            Repres[j]=Repres[j] +"; "+info.inner_html
            Repres[j]=Repres[j].gsub(/<\/?[^>]*>/,"")           
         end
         #puts "Repres[j] "+ Repres[j]
         #puts "counterrepresentante "+ counterre.to_s()
         counterre=counterre + 1
     end  
     if temp.include? "SECRETARIA"
         if counterse==1
            Secret[j]=info.inner_html
            Secret[j]=Secret[j].gsub(/<\/?[^>]*>/,"")
         else
            Secret[j]=Secret[j] +"; "+info.inner_html
            Secret[j]=Secret[j].gsub(/<\/?[^>]*>/,"")           
         end
         #puts "Secret[j] "+ Secret[j]
         #puts "countersecretaria "+ counterse.to_s()
         counterse=counterse + 1
     end  
     if temp.include? "PRESIDENTE" and not temp.include? "VICEPRESIDENTE"
         if counterpr==1
            Presid[j]=info.inner_html
            Presid[j]=Presid[j].gsub(/<\/?[^>]*>/,"")
         else
            Presid[j]=Presid[j] +"; "+info.inner_html
            Presid[j]=Presid[j].gsub(/<\/?[^>]*>/,"")           
         end
         #puts "Presid[j] "+ Presid[j]
         #puts "counterpresidente "+ counterpr.to_s()
         counterpr=counterpr + 1
     end   
     if temp.include? "VICEPRESIDENTE"          
         if countervi==1
            Vicepr[j]=info.inner_html
            Vicepr[j]=Vicepr[j].gsub(/<\/?[^>]*>/,"")
         else
            Vicepr[j]=Vicepr[j] +"; "+info.inner_html
            Vicepr[j]=Vicepr[j].gsub(/<\/?[^>]*>/,"")           
         end
         #puts "Vicepr[j] "+ Vicepr[j]
         #puts "countervicepresidente "+ countervi.to_s()
         countervi=countervi + 1
     end  
  end

# STEP 4 - METEMOS LOS DATOS EN LA BASE DE DATOS
# Con la siguiente linea metemos los datos en una tabla donde el nombre del senador es su id único y vamos incoorporando el resto de arrays 
#__________________________________________________________________________________________________________________________________________

  ScraperWiki.save_sqlite(unique_keys=["Senadores"], data={"Senadores"=> senadores[j], "electo"=> electo[j], "electo9"=> electo9[j], "Senadorpor"=> Senadorpor[j], "Provincia"=> Prov[j] , "Fecha"=> Fecha[j], "Grupo"=> Grupo[j],"Nacido"=> Nacido[j],"EstadoCivil"=> EstadoCivil[j], "Hijos"=> Hijos[j], "Num_Hijos"=> Num_Hijos[j], "Formacion"=> Formacion[j], "Partido"=> Partido[j], "Otros"=> Otros[j], "Miembr"=> Miembr[j], "Repres"=> Repres[j], "Secret"=> Secret[j], "Presid"=> Presid[j], "Vicepr"=> Vicepr[j], "url"=> url[j]}) 


end





