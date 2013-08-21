import scraperwiki
import scrapemark

# Filialliste nach URL durchsuchen (Warum kommt nur eine raus, nicht alle?)
data = scrapemark.scrape("""
        {*
                <ul class="storelist"><a href="{{ [links].url }}" /></section>
                             
        *}
        """,
        url='http://www.lidl.de/de/Filialsuche')

print data
scraperwiki.sqlite.save(unique_keys=["url"], data=data["links"], table_name="Websites", verbose=2)


#Beispiel für durchsuchen einer Filial-URL
data = scrapemark.scrape("""
        {*
                <tr class><span>{{ [filiale].adresse }}<br/>
                {{ [filiale].plz }}</span>
                <td>{{ [filiale].offen }}</td>
                             
        *}
        """,
        url='http://www.lidl.de/filialen/aalen/')

print data
scraperwiki.sqlite.save(unique_keys=["adresse"], data=data["filiale"], table_name="Filialnetz", verbose=2)





