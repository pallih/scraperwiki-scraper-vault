# Este pequeño programa extrae el precio de una subasta concreta de una página de la Oficina Regional de Subastas de Madrid.
# Las líneas que comienzan con un signo # son comentarios y no hacen nada. El resto de lineas se ejecutan de arriba a abajo:
# un programa que "entiende" Ruby - el lenguaje que vamos a utilizar - se encarga de leerlas una a una y ejecutarlas.
# Al programa que sigue las instrucciones escritas en Ruby se le llama "intérprete".

# Vamos a usar una librería (un programa desarrollado por otros y empaquetado para que lo utilicen otros) que se llama Mechanize
# y nos va a ayudar a escrapear. Tenemos que decirle al intérprete que queremos usar esta libreria.
require 'mechanize'
require 'scraperwiki'


38230.upto(38240) do |identificador_subasta|

puts "Voy a descargar la subasta numero "+identificador_subasta.to_s

# Ahora creamos una especie de "navegador web en miniatura" gracias a Mechanize, y lo llamamos 'robot'
robot = Mechanize.new

# Esta es la dirección de la página web que nos interesa; la llamamos simplemente 'direccion'
direccion = "http://gestiona.madrid.org/suju/servlet/Servidor?opcion=SUJUFichaSeleccionada&COD="+identificador_subasta.to_s+"&MONEDAACTIVA=EUROS"

# Le decimos al robot que se baje la página que nos interesa, y llamamos al resultado 'página'
pagina = robot.get(direccion)

# Ahora extraemos de la página las tablas (etiqueta 'table' en HTML), usando el método 'search'
tablas = pagina.search('table')

# El metodo 'puts' imprime un mensaje por pantalla. En este caso queremos ver cuantas tablas hemos encontrado:
puts "He encontrado #{tablas.length} tablas."

# Mediante prueba y error o mirando el código de la página web descubrimos que la tabla que realmente nos interesa,
# la que tiene todos los datos, es la segunda. Usamos la sintaxis tablas[n] para acceder al elemento en la posición 'n'
# de una lista. Pero hay que tener en cuenta que la mayoría de los lenguajes de programación empiezan a contar en 0,
# así que hacemos:
tabla_con_datos = tablas[1]

# Ahora tenemos la tabla, pero necesitamos extraer la lista de filas (etiqueta 'tr' en HTML):
filas = tabla_con_datos.search('tr')

# Ahora tenemos todas las filas, pero queremos partir las filas en columnas (etiqueta 'td' en HTML).
# Como esto es un ejercicio básico vamos a hacerlo sólo con una fila en concreto, la sexta, que tiene el precio:
# (de nuevo, recordad que empezamos a contar en cero)
columnas_precio = filas[5].search('td')

# Nos interesa la segunda columna, que es la que tiene la información, porque la primera sólo dice "Precio"
casilla_valor_precio = columnas_precio[1]

# Y ahora guardamos el resultado
ScraperWiki::save_sqlite(["precio"], data={"precio"=>casilla_valor_precio.text})

end
# Este pequeño programa extrae el precio de una subasta concreta de una página de la Oficina Regional de Subastas de Madrid.
# Las líneas que comienzan con un signo # son comentarios y no hacen nada. El resto de lineas se ejecutan de arriba a abajo:
# un programa que "entiende" Ruby - el lenguaje que vamos a utilizar - se encarga de leerlas una a una y ejecutarlas.
# Al programa que sigue las instrucciones escritas en Ruby se le llama "intérprete".

# Vamos a usar una librería (un programa desarrollado por otros y empaquetado para que lo utilicen otros) que se llama Mechanize
# y nos va a ayudar a escrapear. Tenemos que decirle al intérprete que queremos usar esta libreria.
require 'mechanize'
require 'scraperwiki'


38230.upto(38240) do |identificador_subasta|

puts "Voy a descargar la subasta numero "+identificador_subasta.to_s

# Ahora creamos una especie de "navegador web en miniatura" gracias a Mechanize, y lo llamamos 'robot'
robot = Mechanize.new

# Esta es la dirección de la página web que nos interesa; la llamamos simplemente 'direccion'
direccion = "http://gestiona.madrid.org/suju/servlet/Servidor?opcion=SUJUFichaSeleccionada&COD="+identificador_subasta.to_s+"&MONEDAACTIVA=EUROS"

# Le decimos al robot que se baje la página que nos interesa, y llamamos al resultado 'página'
pagina = robot.get(direccion)

# Ahora extraemos de la página las tablas (etiqueta 'table' en HTML), usando el método 'search'
tablas = pagina.search('table')

# El metodo 'puts' imprime un mensaje por pantalla. En este caso queremos ver cuantas tablas hemos encontrado:
puts "He encontrado #{tablas.length} tablas."

# Mediante prueba y error o mirando el código de la página web descubrimos que la tabla que realmente nos interesa,
# la que tiene todos los datos, es la segunda. Usamos la sintaxis tablas[n] para acceder al elemento en la posición 'n'
# de una lista. Pero hay que tener en cuenta que la mayoría de los lenguajes de programación empiezan a contar en 0,
# así que hacemos:
tabla_con_datos = tablas[1]

# Ahora tenemos la tabla, pero necesitamos extraer la lista de filas (etiqueta 'tr' en HTML):
filas = tabla_con_datos.search('tr')

# Ahora tenemos todas las filas, pero queremos partir las filas en columnas (etiqueta 'td' en HTML).
# Como esto es un ejercicio básico vamos a hacerlo sólo con una fila en concreto, la sexta, que tiene el precio:
# (de nuevo, recordad que empezamos a contar en cero)
columnas_precio = filas[5].search('td')

# Nos interesa la segunda columna, que es la que tiene la información, porque la primera sólo dice "Precio"
casilla_valor_precio = columnas_precio[1]

# Y ahora guardamos el resultado
ScraperWiki::save_sqlite(["precio"], data={"precio"=>casilla_valor_precio.text})

end
