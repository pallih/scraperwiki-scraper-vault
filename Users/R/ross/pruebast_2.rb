#=======================================================================================================================================
# - Programa en Ruby para obtener información de senadores españoles de la 9a legislatura
#=======================================================================================================================================

# STEP 0 - DECLARACION DE VARIABLES
#_______________________________________________________________________________________________________________________________________
# Declaramos arrays para ir guardando información

temp2={},apellidos={},nombre={},grupo={},electo={},lugar={},senador={},sexo={},leg9={},url={},senadores={},electo={},url={},electo9={},Senadorpor={},ProvyFecha={},Prov={},Fecha={},Grupo ={},Nacido={},EstadoCivil={},Hijos={},Num_Hijos={},Formacion={},Partido={},Otros={},Miembr={},Repres={},Secret={},Presid={},Vicepr={}


# STEP 1 - INFORMACION DE LISTADO DE SENADORES
#_______________________________________________________________________________________________________________________________________
# extraemos la info de la pagina relevante en la variable html
html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
# puts html
 
# Creamos loop no controlado y cargamos la libreria con su ajuste por acentos
i=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'iso-8859-1')

# Buscamos en el html tras las etiquetas donte esta la info que queremos (iteramos para cada una), lo guardamos en temp, que sustituimos sobre si misma solo por la parte que esta tras las etiquetas
doc.search('ul> li').each do |temp|
  temp = temp.inner_html  
  #puts temp
  
  # Iteramos la función gsub para remplazar, primero quitamos todo el html, y luego mas cosas. Ver  http://en.wikipedia.org/wiki/Regular_expression, y quitamos todo  el  html
  temp=temp.gsub(/<\/?[^>]*>/,"")
  temp=temp.gsub(/por la Comunidad Aut?.noma de?. /,".")  
  temp=temp.gsub(/por la Comunidad de/,".")
  temp=temp.gsub(/por /,".")
  temp=temp.gsub("(G",".G") # Añado la 'G' para que se restrinja a los grupos y no a las provincias y, así, evitar generar mas puntos y, por ende, más splits de los deseados
  temp=temp.gsub(/, /,".")  

  # Genero un array ('temp2') a partir de 'temp', con un split que usa '.' para dividir. Como hay cuatro puntos para cada senador, hay cinco piezas de info para cada uno en el array. Genero tb sendas variables para recoger cada pieza de info del array
  temp2=temp.split(".")
  apellidos[i]=temp2[0]
  nombre[i]=temp2[1]
  grupo[i]=temp2[2]
  electo[i]=temp2[3]
  lugar[i]=temp2[4]   
  #puts "APELLIDOS: "+apellidos[i]  
  #puts "NOMBRE: "+nombre[i]
  #puts "GRUPO: "+grupo[i]
  #puts "ELECTO: "+electo[i]
  #puts "LUGAR:" +lugar[i]

  # Genero una variable que encadene apellidos y nombre, por compatibilidad con otras de nuestras bases de datos
  senador[i]=apellidos[i] + ", " + nombre[i]
  puts "SENADOR: "+senador[i]  

  # Refino 'grupo' quitándole los paréntesis finales; lo hago aquí y no al refinar temp para no quitar los paréntesis de las provincias, cuando los hay
  grupo[i]=grupo[i].gsub(")","")
  #puts "GRUPO: "+grupo[i]


  # Genero una variable nueva, sexo, y la reemplazo con el valor 2 para las mujeres y 1 para los hombres  
  sexo[i]="999"
  if electo[i].include? "Electa" or  electo[i].include? "Designada"
     sexo[i]="2"
  else
     sexo[i]="1"
  end
  #puts "SEXO: "+sexo[i]

  # Usamos la expresión .slice para quedarnos solo con los 11 primeros caracteres y, así, esta variable será 1=Designado/a, 2=Electo/a
  # electo[i]= electo[i].slice(0..10) Con el split más refinado, esto ya no es necesario
  # Usamos la expresión if.include? para dar valor 2 a los electos/as y 1 a los designados/as.
  #puts "ELECTO: "+electo[i]   
  if electo[i].include? "Elect"
     electo[i]="2"
  else
     electo[i]="1"
  end   
  #puts "ELECTO: "+electo[i]  

 
  # Genero un parámetro igual para todos los senadores que indique que todos son senadores (=1) en la legislatura 9
  leg9[i]="1"

  # Sacamos por pantalla la información
  #puts "LEGISLATURA9: "+leg9[i]

   i=i+1

end




# STEP 2 - OBTENEMOS URLS DE LAS PAGINAS DE LOS SENADORES
#_______________________________________________________________________________________________________________________________________
i=0
doc2 = Nokogiri::HTML(html, nil, 'iso-8859-1')
doc2.search('ul> li> a').each do |urls|
  temp=urls['href']
  url[i]=temp.slice(44..46)
  url[i]="http://www.senado.es/legis9/senadores/ficha/"+ url[i] +".html"
  #puts url[i]
  i=i+1
end   

 
# STEP 3 - SACAMOS INFORMACION DE CADA UNA DE LAS PAGINAS DE SENADORES
# Ahora iteramos en el array de urls y en cada una de las páginas sacamos la informacion que nos interesa
#_______________________________________________________________________________________________________________________________________

for j in 0..i-1
  html = ScraperWiki.scrape(url[j])   
  #puts html
  counter=1 #   contador general que incluye a cualquiera de los 5 que siguen, tomados como un conjunto único
  countermi=1 # contador de 'Miembro'
  counterre=1 # contador de 'Representante'
  counterse=1 # contador de 'Secretaria'
  counterpr=1 # contador de 'Presidente'
  countervi=1 # contador de 'Vicepresidente'
  counterhi=1 # contador de 'Hijos'

  doc = Nokogiri::HTML(html, nil, 'iso-8859-1')
  doc.search('ul>li').each do |info|
    temp = info.inner_html
    temp=temp.gsub(/<\/?[^>]*>/,"")
    puts temp  

    #dependiendo del tipo de información la guardamos en un array u otro

=begin
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
  
=end

    if temp.include? "GRUPO PARLAMENTARIO"
        Grupo[j]=info.inner_html
        Grupo[j]=Grupo[j].gsub(/<\/?[^>]*>/,"")
        puts "Grupo[j] "+ Grupo[j]
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







#=======================================================================================================================================
# - Programa en Ruby para obtener información de senadores españoles de la 9a legislatura
#=======================================================================================================================================

# STEP 0 - DECLARACION DE VARIABLES
#_______________________________________________________________________________________________________________________________________
# Declaramos arrays para ir guardando información

temp2={},apellidos={},nombre={},grupo={},electo={},lugar={},senador={},sexo={},leg9={},url={},senadores={},electo={},url={},electo9={},Senadorpor={},ProvyFecha={},Prov={},Fecha={},Grupo ={},Nacido={},EstadoCivil={},Hijos={},Num_Hijos={},Formacion={},Partido={},Otros={},Miembr={},Repres={},Secret={},Presid={},Vicepr={}


# STEP 1 - INFORMACION DE LISTADO DE SENADORES
#_______________________________________________________________________________________________________________________________________
# extraemos la info de la pagina relevante en la variable html
html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
# puts html
 
# Creamos loop no controlado y cargamos la libreria con su ajuste por acentos
i=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'iso-8859-1')

# Buscamos en el html tras las etiquetas donte esta la info que queremos (iteramos para cada una), lo guardamos en temp, que sustituimos sobre si misma solo por la parte que esta tras las etiquetas
doc.search('ul> li').each do |temp|
  temp = temp.inner_html  
  #puts temp
  
  # Iteramos la función gsub para remplazar, primero quitamos todo el html, y luego mas cosas. Ver  http://en.wikipedia.org/wiki/Regular_expression, y quitamos todo  el  html
  temp=temp.gsub(/<\/?[^>]*>/,"")
  temp=temp.gsub(/por la Comunidad Aut?.noma de?. /,".")  
  temp=temp.gsub(/por la Comunidad de/,".")
  temp=temp.gsub(/por /,".")
  temp=temp.gsub("(G",".G") # Añado la 'G' para que se restrinja a los grupos y no a las provincias y, así, evitar generar mas puntos y, por ende, más splits de los deseados
  temp=temp.gsub(/, /,".")  

  # Genero un array ('temp2') a partir de 'temp', con un split que usa '.' para dividir. Como hay cuatro puntos para cada senador, hay cinco piezas de info para cada uno en el array. Genero tb sendas variables para recoger cada pieza de info del array
  temp2=temp.split(".")
  apellidos[i]=temp2[0]
  nombre[i]=temp2[1]
  grupo[i]=temp2[2]
  electo[i]=temp2[3]
  lugar[i]=temp2[4]   
  #puts "APELLIDOS: "+apellidos[i]  
  #puts "NOMBRE: "+nombre[i]
  #puts "GRUPO: "+grupo[i]
  #puts "ELECTO: "+electo[i]
  #puts "LUGAR:" +lugar[i]

  # Genero una variable que encadene apellidos y nombre, por compatibilidad con otras de nuestras bases de datos
  senador[i]=apellidos[i] + ", " + nombre[i]
  puts "SENADOR: "+senador[i]  

  # Refino 'grupo' quitándole los paréntesis finales; lo hago aquí y no al refinar temp para no quitar los paréntesis de las provincias, cuando los hay
  grupo[i]=grupo[i].gsub(")","")
  #puts "GRUPO: "+grupo[i]


  # Genero una variable nueva, sexo, y la reemplazo con el valor 2 para las mujeres y 1 para los hombres  
  sexo[i]="999"
  if electo[i].include? "Electa" or  electo[i].include? "Designada"
     sexo[i]="2"
  else
     sexo[i]="1"
  end
  #puts "SEXO: "+sexo[i]

  # Usamos la expresión .slice para quedarnos solo con los 11 primeros caracteres y, así, esta variable será 1=Designado/a, 2=Electo/a
  # electo[i]= electo[i].slice(0..10) Con el split más refinado, esto ya no es necesario
  # Usamos la expresión if.include? para dar valor 2 a los electos/as y 1 a los designados/as.
  #puts "ELECTO: "+electo[i]   
  if electo[i].include? "Elect"
     electo[i]="2"
  else
     electo[i]="1"
  end   
  #puts "ELECTO: "+electo[i]  

 
  # Genero un parámetro igual para todos los senadores que indique que todos son senadores (=1) en la legislatura 9
  leg9[i]="1"

  # Sacamos por pantalla la información
  #puts "LEGISLATURA9: "+leg9[i]

   i=i+1

end




# STEP 2 - OBTENEMOS URLS DE LAS PAGINAS DE LOS SENADORES
#_______________________________________________________________________________________________________________________________________
i=0
doc2 = Nokogiri::HTML(html, nil, 'iso-8859-1')
doc2.search('ul> li> a').each do |urls|
  temp=urls['href']
  url[i]=temp.slice(44..46)
  url[i]="http://www.senado.es/legis9/senadores/ficha/"+ url[i] +".html"
  #puts url[i]
  i=i+1
end   

 
# STEP 3 - SACAMOS INFORMACION DE CADA UNA DE LAS PAGINAS DE SENADORES
# Ahora iteramos en el array de urls y en cada una de las páginas sacamos la informacion que nos interesa
#_______________________________________________________________________________________________________________________________________

for j in 0..i-1
  html = ScraperWiki.scrape(url[j])   
  #puts html
  counter=1 #   contador general que incluye a cualquiera de los 5 que siguen, tomados como un conjunto único
  countermi=1 # contador de 'Miembro'
  counterre=1 # contador de 'Representante'
  counterse=1 # contador de 'Secretaria'
  counterpr=1 # contador de 'Presidente'
  countervi=1 # contador de 'Vicepresidente'
  counterhi=1 # contador de 'Hijos'

  doc = Nokogiri::HTML(html, nil, 'iso-8859-1')
  doc.search('ul>li').each do |info|
    temp = info.inner_html
    temp=temp.gsub(/<\/?[^>]*>/,"")
    puts temp  

    #dependiendo del tipo de información la guardamos en un array u otro

=begin
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
  
=end

    if temp.include? "GRUPO PARLAMENTARIO"
        Grupo[j]=info.inner_html
        Grupo[j]=Grupo[j].gsub(/<\/?[^>]*>/,"")
        puts "Grupo[j] "+ Grupo[j]
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







#=======================================================================================================================================
# - Programa en Ruby para obtener información de senadores españoles de la 9a legislatura
#=======================================================================================================================================

# STEP 0 - DECLARACION DE VARIABLES
#_______________________________________________________________________________________________________________________________________
# Declaramos arrays para ir guardando información

temp2={},apellidos={},nombre={},grupo={},electo={},lugar={},senador={},sexo={},leg9={},url={},senadores={},electo={},url={},electo9={},Senadorpor={},ProvyFecha={},Prov={},Fecha={},Grupo ={},Nacido={},EstadoCivil={},Hijos={},Num_Hijos={},Formacion={},Partido={},Otros={},Miembr={},Repres={},Secret={},Presid={},Vicepr={}


# STEP 1 - INFORMACION DE LISTADO DE SENADORES
#_______________________________________________________________________________________________________________________________________
# extraemos la info de la pagina relevante en la variable html
html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
# puts html
 
# Creamos loop no controlado y cargamos la libreria con su ajuste por acentos
i=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'iso-8859-1')

# Buscamos en el html tras las etiquetas donte esta la info que queremos (iteramos para cada una), lo guardamos en temp, que sustituimos sobre si misma solo por la parte que esta tras las etiquetas
doc.search('ul> li').each do |temp|
  temp = temp.inner_html  
  #puts temp
  
  # Iteramos la función gsub para remplazar, primero quitamos todo el html, y luego mas cosas. Ver  http://en.wikipedia.org/wiki/Regular_expression, y quitamos todo  el  html
  temp=temp.gsub(/<\/?[^>]*>/,"")
  temp=temp.gsub(/por la Comunidad Aut?.noma de?. /,".")  
  temp=temp.gsub(/por la Comunidad de/,".")
  temp=temp.gsub(/por /,".")
  temp=temp.gsub("(G",".G") # Añado la 'G' para que se restrinja a los grupos y no a las provincias y, así, evitar generar mas puntos y, por ende, más splits de los deseados
  temp=temp.gsub(/, /,".")  

  # Genero un array ('temp2') a partir de 'temp', con un split que usa '.' para dividir. Como hay cuatro puntos para cada senador, hay cinco piezas de info para cada uno en el array. Genero tb sendas variables para recoger cada pieza de info del array
  temp2=temp.split(".")
  apellidos[i]=temp2[0]
  nombre[i]=temp2[1]
  grupo[i]=temp2[2]
  electo[i]=temp2[3]
  lugar[i]=temp2[4]   
  #puts "APELLIDOS: "+apellidos[i]  
  #puts "NOMBRE: "+nombre[i]
  #puts "GRUPO: "+grupo[i]
  #puts "ELECTO: "+electo[i]
  #puts "LUGAR:" +lugar[i]

  # Genero una variable que encadene apellidos y nombre, por compatibilidad con otras de nuestras bases de datos
  senador[i]=apellidos[i] + ", " + nombre[i]
  puts "SENADOR: "+senador[i]  

  # Refino 'grupo' quitándole los paréntesis finales; lo hago aquí y no al refinar temp para no quitar los paréntesis de las provincias, cuando los hay
  grupo[i]=grupo[i].gsub(")","")
  #puts "GRUPO: "+grupo[i]


  # Genero una variable nueva, sexo, y la reemplazo con el valor 2 para las mujeres y 1 para los hombres  
  sexo[i]="999"
  if electo[i].include? "Electa" or  electo[i].include? "Designada"
     sexo[i]="2"
  else
     sexo[i]="1"
  end
  #puts "SEXO: "+sexo[i]

  # Usamos la expresión .slice para quedarnos solo con los 11 primeros caracteres y, así, esta variable será 1=Designado/a, 2=Electo/a
  # electo[i]= electo[i].slice(0..10) Con el split más refinado, esto ya no es necesario
  # Usamos la expresión if.include? para dar valor 2 a los electos/as y 1 a los designados/as.
  #puts "ELECTO: "+electo[i]   
  if electo[i].include? "Elect"
     electo[i]="2"
  else
     electo[i]="1"
  end   
  #puts "ELECTO: "+electo[i]  

 
  # Genero un parámetro igual para todos los senadores que indique que todos son senadores (=1) en la legislatura 9
  leg9[i]="1"

  # Sacamos por pantalla la información
  #puts "LEGISLATURA9: "+leg9[i]

   i=i+1

end




# STEP 2 - OBTENEMOS URLS DE LAS PAGINAS DE LOS SENADORES
#_______________________________________________________________________________________________________________________________________
i=0
doc2 = Nokogiri::HTML(html, nil, 'iso-8859-1')
doc2.search('ul> li> a').each do |urls|
  temp=urls['href']
  url[i]=temp.slice(44..46)
  url[i]="http://www.senado.es/legis9/senadores/ficha/"+ url[i] +".html"
  #puts url[i]
  i=i+1
end   

 
# STEP 3 - SACAMOS INFORMACION DE CADA UNA DE LAS PAGINAS DE SENADORES
# Ahora iteramos en el array de urls y en cada una de las páginas sacamos la informacion que nos interesa
#_______________________________________________________________________________________________________________________________________

for j in 0..i-1
  html = ScraperWiki.scrape(url[j])   
  #puts html
  counter=1 #   contador general que incluye a cualquiera de los 5 que siguen, tomados como un conjunto único
  countermi=1 # contador de 'Miembro'
  counterre=1 # contador de 'Representante'
  counterse=1 # contador de 'Secretaria'
  counterpr=1 # contador de 'Presidente'
  countervi=1 # contador de 'Vicepresidente'
  counterhi=1 # contador de 'Hijos'

  doc = Nokogiri::HTML(html, nil, 'iso-8859-1')
  doc.search('ul>li').each do |info|
    temp = info.inner_html
    temp=temp.gsub(/<\/?[^>]*>/,"")
    puts temp  

    #dependiendo del tipo de información la guardamos en un array u otro

=begin
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
  
=end

    if temp.include? "GRUPO PARLAMENTARIO"
        Grupo[j]=info.inner_html
        Grupo[j]=Grupo[j].gsub(/<\/?[^>]*>/,"")
        puts "Grupo[j] "+ Grupo[j]
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







#=======================================================================================================================================
# - Programa en Ruby para obtener información de senadores españoles de la 9a legislatura
#=======================================================================================================================================

# STEP 0 - DECLARACION DE VARIABLES
#_______________________________________________________________________________________________________________________________________
# Declaramos arrays para ir guardando información

temp2={},apellidos={},nombre={},grupo={},electo={},lugar={},senador={},sexo={},leg9={},url={},senadores={},electo={},url={},electo9={},Senadorpor={},ProvyFecha={},Prov={},Fecha={},Grupo ={},Nacido={},EstadoCivil={},Hijos={},Num_Hijos={},Formacion={},Partido={},Otros={},Miembr={},Repres={},Secret={},Presid={},Vicepr={}


# STEP 1 - INFORMACION DE LISTADO DE SENADORES
#_______________________________________________________________________________________________________________________________________
# extraemos la info de la pagina relevante en la variable html
html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
# puts html
 
# Creamos loop no controlado y cargamos la libreria con su ajuste por acentos
i=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'iso-8859-1')

# Buscamos en el html tras las etiquetas donte esta la info que queremos (iteramos para cada una), lo guardamos en temp, que sustituimos sobre si misma solo por la parte que esta tras las etiquetas
doc.search('ul> li').each do |temp|
  temp = temp.inner_html  
  #puts temp
  
  # Iteramos la función gsub para remplazar, primero quitamos todo el html, y luego mas cosas. Ver  http://en.wikipedia.org/wiki/Regular_expression, y quitamos todo  el  html
  temp=temp.gsub(/<\/?[^>]*>/,"")
  temp=temp.gsub(/por la Comunidad Aut?.noma de?. /,".")  
  temp=temp.gsub(/por la Comunidad de/,".")
  temp=temp.gsub(/por /,".")
  temp=temp.gsub("(G",".G") # Añado la 'G' para que se restrinja a los grupos y no a las provincias y, así, evitar generar mas puntos y, por ende, más splits de los deseados
  temp=temp.gsub(/, /,".")  

  # Genero un array ('temp2') a partir de 'temp', con un split que usa '.' para dividir. Como hay cuatro puntos para cada senador, hay cinco piezas de info para cada uno en el array. Genero tb sendas variables para recoger cada pieza de info del array
  temp2=temp.split(".")
  apellidos[i]=temp2[0]
  nombre[i]=temp2[1]
  grupo[i]=temp2[2]
  electo[i]=temp2[3]
  lugar[i]=temp2[4]   
  #puts "APELLIDOS: "+apellidos[i]  
  #puts "NOMBRE: "+nombre[i]
  #puts "GRUPO: "+grupo[i]
  #puts "ELECTO: "+electo[i]
  #puts "LUGAR:" +lugar[i]

  # Genero una variable que encadene apellidos y nombre, por compatibilidad con otras de nuestras bases de datos
  senador[i]=apellidos[i] + ", " + nombre[i]
  puts "SENADOR: "+senador[i]  

  # Refino 'grupo' quitándole los paréntesis finales; lo hago aquí y no al refinar temp para no quitar los paréntesis de las provincias, cuando los hay
  grupo[i]=grupo[i].gsub(")","")
  #puts "GRUPO: "+grupo[i]


  # Genero una variable nueva, sexo, y la reemplazo con el valor 2 para las mujeres y 1 para los hombres  
  sexo[i]="999"
  if electo[i].include? "Electa" or  electo[i].include? "Designada"
     sexo[i]="2"
  else
     sexo[i]="1"
  end
  #puts "SEXO: "+sexo[i]

  # Usamos la expresión .slice para quedarnos solo con los 11 primeros caracteres y, así, esta variable será 1=Designado/a, 2=Electo/a
  # electo[i]= electo[i].slice(0..10) Con el split más refinado, esto ya no es necesario
  # Usamos la expresión if.include? para dar valor 2 a los electos/as y 1 a los designados/as.
  #puts "ELECTO: "+electo[i]   
  if electo[i].include? "Elect"
     electo[i]="2"
  else
     electo[i]="1"
  end   
  #puts "ELECTO: "+electo[i]  

 
  # Genero un parámetro igual para todos los senadores que indique que todos son senadores (=1) en la legislatura 9
  leg9[i]="1"

  # Sacamos por pantalla la información
  #puts "LEGISLATURA9: "+leg9[i]

   i=i+1

end




# STEP 2 - OBTENEMOS URLS DE LAS PAGINAS DE LOS SENADORES
#_______________________________________________________________________________________________________________________________________
i=0
doc2 = Nokogiri::HTML(html, nil, 'iso-8859-1')
doc2.search('ul> li> a').each do |urls|
  temp=urls['href']
  url[i]=temp.slice(44..46)
  url[i]="http://www.senado.es/legis9/senadores/ficha/"+ url[i] +".html"
  #puts url[i]
  i=i+1
end   

 
# STEP 3 - SACAMOS INFORMACION DE CADA UNA DE LAS PAGINAS DE SENADORES
# Ahora iteramos en el array de urls y en cada una de las páginas sacamos la informacion que nos interesa
#_______________________________________________________________________________________________________________________________________

for j in 0..i-1
  html = ScraperWiki.scrape(url[j])   
  #puts html
  counter=1 #   contador general que incluye a cualquiera de los 5 que siguen, tomados como un conjunto único
  countermi=1 # contador de 'Miembro'
  counterre=1 # contador de 'Representante'
  counterse=1 # contador de 'Secretaria'
  counterpr=1 # contador de 'Presidente'
  countervi=1 # contador de 'Vicepresidente'
  counterhi=1 # contador de 'Hijos'

  doc = Nokogiri::HTML(html, nil, 'iso-8859-1')
  doc.search('ul>li').each do |info|
    temp = info.inner_html
    temp=temp.gsub(/<\/?[^>]*>/,"")
    puts temp  

    #dependiendo del tipo de información la guardamos en un array u otro

=begin
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
  
=end

    if temp.include? "GRUPO PARLAMENTARIO"
        Grupo[j]=info.inner_html
        Grupo[j]=Grupo[j].gsub(/<\/?[^>]*>/,"")
        puts "Grupo[j] "+ Grupo[j]
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







