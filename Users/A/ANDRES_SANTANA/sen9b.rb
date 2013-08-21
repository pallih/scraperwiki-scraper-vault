#=======================================================================================================================================
# - Programa en Ruby para obtener información de senadores españoles de la 9a legislatura
#=======================================================================================================================================

# STEP 0 - DECLARACION DE VARIABLES
#_______________________________________________________________________________________________________________________________________

# Declaramos arrays para ir guardando información
apellidos={},nombre={},grupo={},electo={},lugar={},senador={},sexo={},leg9={},url={},Senadorpor={},ProvyFecha={},Prov={},Fecha={},Grupo ={},Nacido={},EstadoCivil={},Hijos={},Num_Hijos={},Formacion={},Partido={},Otros={},Miembr={},Repres={},Secret={},Presid={},Vicepr={}


# STEP 1 - INFORMACION DE LISTADO DE SENADORES
#_______________________________________________________________________________________________________________________________________

# Sacamos la info de la página con la información en la variable html
html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html") 
# La sacamos por pantalla
puts html 

# Generamos un contador para ir moviendonos por el array. Es un loop no controlado, toma todos los 'ul> li' que encuentra
i=0
# Cargamos la libreria nokogiri para poder procesar el html; lo hacemos con el ajuste para el tema de los acentos: , nil, 'UTF-8'
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'UTF-8')

# Buscamos en el html, buscamos las etiquetas <ul><li> e iteramos, porque es tras ellas que están los nombres de los senadores; sacamos la info en 'temp'
doc.search('ul> li').each do |temp|
  # Sustituimos temp solo por la parte que está dentro de la etiqueta, definida por los signos de apertura <...> y cierre </a>, con el ajuste para acentos definido por ic...
  ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
  temp = ic.iconv(temp.inner_html)
  # Lo sacamos por pantalla    
  puts temp     
  =begin
  # Usamos la función gsub para substituir lo que está entre // por lo que está entre "". Así, quitamos todo el html. Ver: http://en.wikipedia.org/wiki/Regular_expression
  temp=temp.gsub(/<\/?[^>]*>/,"")     
  # Volvemos a utilizar varias veces gsub para afinar al máximo. En la primera línea, con '?.' cubro también el caso "del País Vasco"
  temp=temp.gsub(/por la Comunidad Autónoma de?./,".")  
  temp=temp.gsub(/por la Comunidad de/,".") 
  temp=temp.gsub(/por /,".") 
  temp=temp.gsub(/(G/,".G") # Añado la 'G' para que se restrinja a los grupos y no a las provincias y, así, evitar generar mas puntos y, por ende, más splits de los deseados
  temp=temp.gsub(/, /,".")    
  
  # Genero un array ('temp2') a partir de 'temp', con un split que usa '.' para dividir. Como hay cuatro puntos para cada senador, hay cinco piezas de info para cada uno en el array
  temp2=temp.split(".")
  # Generamos sendas variables que recojan cada pieza de info del array
  apellidos[i]=temp2[0]
  nombre[i]=temp2[1] 
  grupo[i]=temp2[2]
  electo[i]=temp2[3]
  lugar[i]=temp2[4]  

  # Genero una variable que encadene apellidos y nombre, por compatibilidad con otras de nuestras bases de datos
  senador[i]=apellidos[i] + ", " + nombre[i]
  # Refino 'grupo' quitándole los paréntesis finales; lo hago aquí y no al refinar temp para no quitar los paréntesis de las provincias, cuando los hay
  grupo[i]=grupo[i].gsub(/)/,".") 
  # Usamos la expresión .slice para quedarnos solo con los 11 primeros caracteres y, así, esta variable será 1=Designado/a, 2=Electo/a 
  # electo[i]= electo[i].slice(0..10) Con el split más refinado, esto ya no es necesario
  # Usamos la expresión if.include? para dar valor 2 a los electos/as y 1 a los designados/as.
  if electo[i].include? "Elect" 
  electo[i]=2
  else 
  electo[i]=1
  end  
  # Generamos una variable nueva, 'sexo'. Uso if.include? para reemplazar 'sexo' con el valor 2 para las mujeres y 1 para los hombres.  
  sexo[i]=999
  if electo[i].include? "Electa" or   electo[i].include? "Designada"
  sexo[i]=2
  else 
  sexo[i]=1
  end

  # Genero un parámetro igual para todos los senadores que indique que todos son senadores (=1) en la legislatura 9
  leg9[i]=1

  # Sacamos por pantalla la información
  puts senador[i]
  puts apellidos[i]  
  puts nombre[i]
  puts grupo[i]
  puts electo[i] 
  puts sexo[i]
  puts lugar[i]
  puts leg9[i]

  i=i+1
=end
end

# STEP 2 - OBTENEMOS URLS DE LAS PAGINAS DE LOS SENADORES
#_______________________________________________________________________________________________________________________________________
# Generamos un contador, nuevamente, un loop no controlado; cargamos la libreria nokogiri para poder procesar el html e iteramos la busqueda y extracción tras las etiquetas <ul><li>
i=0
doc2 = Nokogiri::HTML(html, nil, 'UTF-8')
doc2.search('ul> li> a').each do |urls| 
  # Sustituimos temp solo por la parte que está dentro de 'href' (es otro tipo de etiqueta)
  temp=urls['href']
  url[i]=temp.slice(44..46)
  url[i]="http://www.senado.es/legis9/senadores/ficha/"+ url[i] +".html"
  puts url[i]
  i=i+1
end  


# STEP 3 - SACAMOS INFORMACION DE CADA UNA DE LAS PAGINAS DE SENADORES
# Ahora iteramos en el array de urls y en cada una de las páginas sacamos la informacion que nos interesa
#_______________________________________________________________________________________________________________________________________

# Genero un contador con 'for... in...', con lo que ahora es un loop controlado, pues especifico dónde empieza y donde termina. 
for j in 0..i-1
  # Especifico la página con la información, saco la info en la variable 'html', y saco por pantalla los datos extraidos
  html = ScraperWiki.scrape(url[j])    
  puts html
  counter=1   # contador general que incluye a cualquiera de los 6 que siguen, tomados como un conjunto único
  countermi=1 # contador de 'Miembro'
  counterre=1 # contador de 'Representante'
  counterse=1 # contador de 'Secretaria'
  counterpr=1 # contador de 'Presidente'
  countervi=1 # contador de 'Vicepresidente'
  counterhi=1 # contador de 'Hijos'

  # Cargo Nokogiri con el ajuste, especifico la página donde esta ínformación, la extraigo a la variable 'info', y la restringo a lo que está dentro de las etiquetas, teniendo en cuenta el ajuste por los acentos.
  doc = Nokogiri::HTML(html, nil, 'UTF-8')
  doc.search('ul>li').each do |info|
  ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
  temp = ic.iconv(info.inner_html)
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





















