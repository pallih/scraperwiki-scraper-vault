# Este pequeño programa extrae la lista de subvenciones de una página del DOGC
# Las líneas que comienzan con un signo # son comentarios y no hacen nada. 
# El resto de lineas se ejecutan de arriba a abajo: ScraperWiki se encarga de leerlas una a una y ejecutarlas.

# Vamos a usar una librería (un programa desarrollado por otros y empaquetado para que lo utilicen otros) 
# que se llama Mechanize y nos va a ayudar a escrapear. Tenemos que decirle a ScraperWiki que queremos usar esta libreria.
require 'mechanize'
require 'scraperwiki'

# Ahora creamos una especie de "navegador web en miniatura" gracias a Mechanize, y lo llamamos 'robot'
robot = Mechanize.new

# Esta es la dirección de la página web que nos interesa
url = "http://www20.gencat.cat/portal/site/portaldogc/menuitem.c973d2fc58aa0083e4492d92b0c0e1a0/?vgnextoid=485946a6e5dfe210VgnVCM1000000b0c1e0aRCRD&appInstanceName=default&action=fitxa&documentId=546107&language=es_ES"

# Le decimos al robot que se baje la página que nos interesa, y llamamos al resultado 'page'
page = robot.get(url)

# Ahora extraemos de la página el contenido que queremos usando el método 'at'. 
# Estamos buscando la parte de la página que tiene el estilo CSS 'article-document'; 
# esto es algo que hemos averiguado mirando el código HTML de la página
content = page.at('.article-document').content

# Creamos una subvención en blanco
current_grant = {}

# Y recorremos el contenido línea a línea buscando las partes que nos interesan
content.each_line do |line|
  line.strip! # Quitamos el carácter de salto de línea

  # Si la línea empieza con "Entitat: " es el beneficiario, usamos una expresión regular 
  # sencilla para sacar la parte interesa
  if line =~ /^Entitat: (.*)$/
    current_grant['beneficiario'] = $1
    puts "He encontrado el beneficiario #{$1}"
  end

  # E igual con el resto...
  if line =~ /^Finalitat: (.*)$/
    current_grant['finalidad'] = $1
    puts "He encontrado la finalidad #{$1}"
  end
  if line =~ /^Import: (.*)$/
    current_grant['cantidad'] = $1
    puts "He encontrado la cantidad #{$1}"
  end
  if line =~ /^Aplicaci. pressupost.ria: (.*)$/
    current_grant['partida'] = $1
    puts "He encontrado la partida #{$1}"

    # Añadimos información aplicable a todas las subvenciones
    current_grant['url'] = url
    current_grant['fecha'] = page.search(".list-dades span")[1].text

    # Mirando la página vemos que la partida presupuestaria marca el final de la subvención, 
    # así que guardamos lo que hemos encontrado en la base de datos de ScraperWiki
    ScraperWiki::save_sqlite(['beneficiario', 'finalidad', 'cantidad', 'partida'], data=current_grant)

    # Y ponemos los datos de la "subvención actual" a cero, por si acaso, para que ningún
    # dato de la que acabamos de grabar se use por error en la siguiente
    current_grant = {}
  end
end


