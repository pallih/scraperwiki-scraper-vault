# Blank Python

import scraperwiki
import lxml.html

for i in range(2082, 3000):

    print "Pelicula: %d" % (i)
    url = "http://www.cinechile.cl//pelicula.php?pelicula_id=%d" % (i)
    eg = lxml.html.parse(url).getroot()

    #Extract Director and ScriptWriter

    c = 0 #Counter to filter only 1st appearance of style
    for el in eg.cssselect("div.funcion a"):
        c = c + 1
        if c==1:
            Director = el.text;
            #print (Director)
        if c==2:
            Guionista = el.text;
            #print (Guionista)

    #Extract Title

    for el in eg.cssselect("span.titulomayuscula"):
        title = el.text
        #print (title)

    #Extract Year
    for el in eg.cssselect("span.ano"):
        year = el.text
        #print (year)

    #Extract Genre
    c = 0 #Counter to filter only 1st appearance of style
    for el in eg.cssselect("span.caract1"):
        c = c + 1
        #print (c)
        if c == 1:
            genero = el.text
            #print (genero)

    #Extract País and Rodaje

    c = 0 #Counter to filter only 1st appearance of style
    for el in eg.cssselect("span.fichita strong"):
        c = c + 1
        #print(el.tail)
        if c==1:
            Pais = el.tail;
            #print (Pais)
        if c==2:
            Rodaje = el.tail;
            #print (Rodaje)


    #save to database
    scraperwiki.sqlite.save(unique_keys=["a"], data={"a":"%.4d" % (i), "Title":(title), "Year":(year), "Genero":(genero), "Director":(Director), "Guionista":(Guionista), "Pais":(Pais), "Rodaje":(Rodaje)})
