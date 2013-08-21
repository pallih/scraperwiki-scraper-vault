def print_series(series_name,base_url,year_range):
    print "<table>"
    print "<tr><th>",series_name,"</th></tr>" 
    for year in year_range:
        url = base_url + str(year)
        print "<tr>"
        print "<td> <a href=\"", url, "\">", url,"</a></td>"
        print "</tr>"
    print "</table>"

        

print "<html><head>"
print "<title>Elenco URL Archivio Gazzette Ufficiali Formato Testuale 1946 - 2006</title>"
print "</head>"
print "<body>"
print "<h1> Elenco URL Archivio Gazzette Ufficiali Formato Testuale 1946 - 2006</h1>"


print_series("Serie Generale","http://www.gazzettaufficiale.it/ricercaArchivioCompleto/serie_generale/",range(1946,2007))
print_series("Corte Costituzionale","http://www.gazzettaufficiale.it/ricercaArchivioCompleto/corte_costituzionale/",range(1946,2007))
print_series("Unione Europea","http://www.gazzettaufficiale.it/ricercaArchivioCompleto/unione_europea/",range(1946,2007))
#probably this is not useful
print_series("Regioni","http://www.gazzettaufficiale.it/ricercaArchivioCompleto/regioni/",range(1946,2007)) 
print_series("Concorsi","http://www.gazzettaufficiale.it/ricercaArchivioCompleto/concorsi/",range(1946,2007))
print_series("Contratti","http://www.gazzettaufficiale.it/ricercaArchivioCompleto/contratti/",range(1946,2007)) 
print_series("Parte Seconda","http://www.gazzettaufficiale.it/ricercaArchivioCompleto/parte_seconda/",range(1946,2007)) 


print "</body></html>"

