# Este pequeño programa extrae el precio de una subasta concreta de una página de la Oficina Regional de Subastas de Madrid.
# Las líneas que comienzan con un signo # son comentarios y no hacen nada. El resto de lineas se ejecutan de arriba a abajo:
# un programa que "entiende" Ruby - el lenguaje que vamos a utilizar - se encarga de leerlas una a una y ejecutarlas.
# Al programa que sigue las instrucciones escritas en Ruby se le llama "intérprete".

# Vamos a usar una librería (un programa desarrollado por otros y empaquetado para que lo utilicen otros) que se llama Mechanize
# y nos va a ayudar a escrapear. Tenemos que decirle al intérprete que queremos usar esta libreria.
require 'mechanize'

# Ahora creamos una especie de "navegador web en miniatura" gracias a Mechanize, y lo llamamos 'robot'
robot = Mechanize.new

# Esta es la dirección de la página web que nos interesa; la llamamos simplemente 'direccion'
direccion = "http://www.empresia.es/persona/castano-castro-concepcion/"

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
tabla_con_datos = tablas[0]

# Ahora tenemos la tabla, pero necesitamos extraer la lista de filas (etiqueta 'tr' en HTML):
filas = tabla_con_datos.search('tr')

# Ahora tenemos todas las filas, pero queremos partir las filas en columnas (etiqueta 'td' en HTML).
columnas_empresa = filas[1].search('td')
columnas_cargo = filas[2].search('td')
columnas_nombramiento = filas [3].search ('td')
columnas_ceseodimision = filas [4].search ('td')

# Nos interesa la segunda columna, que es la que tiene la información, porque la primera sólo dice "Empresa", "cargo"...
casilla_valor_empresa = columnas_empresa[0]
casilla_valor_cargo = columnas_cargo[1]
casilla_valor_nombramiento = columnas_nombramiento[2]
casilla_valor_ceseodimision = columnas_ceseodimision[3]

# Y ahora mostramos el resultado por pantalla
puts "Empresa: "+casilla_valor_empresa
puts "Cargo: "+casilla_valor_cargo
puts "Nombramiento: "+casilla_valor_nombramiento
puts "Cese o dimision: "+casilla_valor_ceseodimision# Este pequeño programa extrae el precio de una subasta concreta de una página de la Oficina Regional de Subastas de Madrid.
# Las líneas que comienzan con un signo # son comentarios y no hacen nada. El resto de lineas se ejecutan de arriba a abajo:
# un programa que "entiende" Ruby - el lenguaje que vamos a utilizar - se encarga de leerlas una a una y ejecutarlas.
# Al programa que sigue las instrucciones escritas en Ruby se le llama "intérprete".

# Vamos a usar una librería (un programa desarrollado por otros y empaquetado para que lo utilicen otros) que se llama Mechanize
# y nos va a ayudar a escrapear. Tenemos que decirle al intérprete que queremos usar esta libreria.
require 'mechanize'

# Ahora creamos una especie de "navegador web en miniatura" gracias a Mechanize, y lo llamamos 'robot'
robot = Mechanize.new

# Esta es la dirección de la página web que nos interesa; la llamamos simplemente 'direccion'
direccion = "http://www.empresia.es/persona/castano-castro-concepcion/"

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
tabla_con_datos = tablas[0]

# Ahora tenemos la tabla, pero necesitamos extraer la lista de filas (etiqueta 'tr' en HTML):
filas = tabla_con_datos.search('tr')

# Ahora tenemos todas las filas, pero queremos partir las filas en columnas (etiqueta 'td' en HTML).
columnas_empresa = filas[1].search('td')
columnas_cargo = filas[2].search('td')
columnas_nombramiento = filas [3].search ('td')
columnas_ceseodimision = filas [4].search ('td')

# Nos interesa la segunda columna, que es la que tiene la información, porque la primera sólo dice "Empresa", "cargo"...
casilla_valor_empresa = columnas_empresa[0]
casilla_valor_cargo = columnas_cargo[1]
casilla_valor_nombramiento = columnas_nombramiento[2]
casilla_valor_ceseodimision = columnas_ceseodimision[3]

# Y ahora mostramos el resultado por pantalla
puts "Empresa: "+casilla_valor_empresa
puts "Cargo: "+casilla_valor_cargo
puts "Nombramiento: "+casilla_valor_nombramiento
puts "Cese o dimision: "+casilla_valor_ceseodimision