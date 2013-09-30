import scraperwiki
import lxml.html 
import time

for i in range(100):# 100 is used as an absolut maximum of 100x100 hits, there is a break 
    #change the search criteria to make other searches
    html = scraperwiki.scrape("http://us-east.omim.org/search?index=clinicalSynopsis&start="+str(i)+"&limit=100&search=myopia&sort=score+desc")
    i=0;
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("span[class='definition']"):
        i+=1
        prefix = tr.cssselect("span[class='prefix']")
        if(len(prefix)==0):
            id=tr.text_content().strip()[:-1]
        else:
            id=tr.text_content().strip()[2:-1]
        time.sleep(1);
        phenoHtml=scraperwiki.scrape("http://us-east.omim.org/entry/"+id.strip())
        rootPheno=lxml.html.fromstring(phenoHtml)
        for tr1 in rootPheno.cssselect("table[class='gene-map-table border'] tr"):
            tds = tr1.cssselect("td")
            if(len(tds) ==5 ):
                data = {
                    'location':tds[0].text_content().strip(),
                    'phenotype':tds[1].text_content().strip(),
                    'mim_phenotype':tds[2].text_content().strip(),
                    'gene_locus':tds[3].text_content().strip(),
                    'mim_gene_locus':tds[4].text_content().strip(),
                    'genomic_location':""
                }
                if(data["phenotype"]!="Phenotype"):
                    scraperwiki.sqlite.save(unique_keys=['phenotype','gene_locus'], data=data)
            if(len(tds) ==3 ):
                location=""
                for sp in rootPheno.cssselect("span[class='genomic-coordinates text-font']"):
                    location=sp.text_content().split(")")[1][2:].replace(",","").replace(" ","")
                data = {
                    'location':tds[0].text_content().strip(),
                    'phenotype':tds[1].text_content().strip(),
                    'mim_phenotype':tds[2].text_content().strip(),
                    'gene_locus':"",
                    'mim_gene_locus':"",
                    'genomic_location': location
                }
                if(data["phenotype"]!="Phenotype"):
                    scraperwiki.sqlite.save(unique_keys=['phenotype','gene_locus'], data=data)
    if(i<100):
        break

import scraperwiki
import lxml.html 
import time

for i in range(100):# 100 is used as an absolut maximum of 100x100 hits, there is a break 
    #change the search criteria to make other searches
    html = scraperwiki.scrape("http://us-east.omim.org/search?index=clinicalSynopsis&start="+str(i)+"&limit=100&search=myopia&sort=score+desc")
    i=0;
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("span[class='definition']"):
        i+=1
        prefix = tr.cssselect("span[class='prefix']")
        if(len(prefix)==0):
            id=tr.text_content().strip()[:-1]
        else:
            id=tr.text_content().strip()[2:-1]
        time.sleep(1);
        phenoHtml=scraperwiki.scrape("http://us-east.omim.org/entry/"+id.strip())
        rootPheno=lxml.html.fromstring(phenoHtml)
        for tr1 in rootPheno.cssselect("table[class='gene-map-table border'] tr"):
            tds = tr1.cssselect("td")
            if(len(tds) ==5 ):
                data = {
                    'location':tds[0].text_content().strip(),
                    'phenotype':tds[1].text_content().strip(),
                    'mim_phenotype':tds[2].text_content().strip(),
                    'gene_locus':tds[3].text_content().strip(),
                    'mim_gene_locus':tds[4].text_content().strip(),
                    'genomic_location':""
                }
                if(data["phenotype"]!="Phenotype"):
                    scraperwiki.sqlite.save(unique_keys=['phenotype','gene_locus'], data=data)
            if(len(tds) ==3 ):
                location=""
                for sp in rootPheno.cssselect("span[class='genomic-coordinates text-font']"):
                    location=sp.text_content().split(")")[1][2:].replace(",","").replace(" ","")
                data = {
                    'location':tds[0].text_content().strip(),
                    'phenotype':tds[1].text_content().strip(),
                    'mim_phenotype':tds[2].text_content().strip(),
                    'gene_locus':"",
                    'mim_gene_locus':"",
                    'genomic_location': location
                }
                if(data["phenotype"]!="Phenotype"):
                    scraperwiki.sqlite.save(unique_keys=['phenotype','gene_locus'], data=data)
    if(i<100):
        break

