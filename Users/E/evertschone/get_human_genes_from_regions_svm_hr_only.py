import scraperwiki

# Blank Python
# import libraries
import scraperwiki           
import lxml.html
import xlrd
import csv           


# import list of genes with mutations in breastcancer, this files is exported from http://cancer.sanger.ac.uk/cosmic/browse/tissue, using samples from breast tissue only and all possible subtypes.

data = scraperwiki.scrape("http://www.estyles.nl/HR+_mutated_genes.csv")
reader = csv.reader(data.splitlines())

knowngenelist = dict()
reader.next()
for row in reader:
    knowngenelist[row[0]] = [float(row[1]),float(row[2])]   #store mutationratio in dictionary, (calculated as: samples with mutations devided by all tested samples)

print len(knowngenelist)

#import xls file with ensembl urls generate from the regions, eg. http://may2009.archive.ensembl.org/Homo_sapiens/Location/Synteny?r=17:35127745-35230638 (Synteny view gives easily scrapable results)

xlbin = scraperwiki.scrape("http://www.estyles.nl/biomarkers.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_name('weight by SVM (2)')
print sheet.name, sheet.nrows

for x in range(1,sheet.nrows):    #for each region scrape the ensemble url for genes
    region_id = str(sheet.cell(x,8))[7:].split('.')[0]

    url = str(sheet.cell(x,14))[7:-1]
    print region_id, url
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for tr in root.cssselect("table[class='ss autocenter'] tr"):    #for each gene in the region

        tds = tr.cssselect("td[class=' left-border'] a")
        if len(tds) > 0:
            genename = tds[0].text_content()
            print genename
            
            if genename in knowngenelist:    #check if the gene is a possible oncogene from the sanger list of somatic mutations in cancer (COSMIC)
                
                genehtml = scraperwiki.scrape("http://may2009.archive.ensembl.org/"+str(tds[0].attrib['href'])) #get more info on the gene from this URL
                root2 = lxml.html.fromstring(genehtml)
                p = root2.cssselect("div[class='content'] p")
                if len(p) > 0:
                    print p[0].text_content()
                    if len(p[0].cssselect("a")) > 0:
                        uniprotlink = p[0].cssselect("a")[-1].attrib['href'] #get uniprotlink
                    else:
                        uniprotlink = ''
                    print uniprotlink
                    
                    data = {     #format data
                        'region_id' : region_id,                    #id from excel file
                        'gene' : genename,                          #gene name
                        'desc' : p[0].text_content(),               #description from uniprot
                        'geneurl' : uniprotlink,                    #uniprot link
                        'mutated' : knowngenelist[genename][0],     #mutation ratio from the cosmic database
                        'samples' : knowngenelist[genename][1]
                    }
                    print data
                    scraperwiki.sqlite.save(unique_keys=['gene'], data=data)  #save data
                        import scraperwiki

# Blank Python
# import libraries
import scraperwiki           
import lxml.html
import xlrd
import csv           


# import list of genes with mutations in breastcancer, this files is exported from http://cancer.sanger.ac.uk/cosmic/browse/tissue, using samples from breast tissue only and all possible subtypes.

data = scraperwiki.scrape("http://www.estyles.nl/HR+_mutated_genes.csv")
reader = csv.reader(data.splitlines())

knowngenelist = dict()
reader.next()
for row in reader:
    knowngenelist[row[0]] = [float(row[1]),float(row[2])]   #store mutationratio in dictionary, (calculated as: samples with mutations devided by all tested samples)

print len(knowngenelist)

#import xls file with ensembl urls generate from the regions, eg. http://may2009.archive.ensembl.org/Homo_sapiens/Location/Synteny?r=17:35127745-35230638 (Synteny view gives easily scrapable results)

xlbin = scraperwiki.scrape("http://www.estyles.nl/biomarkers.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_name('weight by SVM (2)')
print sheet.name, sheet.nrows

for x in range(1,sheet.nrows):    #for each region scrape the ensemble url for genes
    region_id = str(sheet.cell(x,8))[7:].split('.')[0]

    url = str(sheet.cell(x,14))[7:-1]
    print region_id, url
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for tr in root.cssselect("table[class='ss autocenter'] tr"):    #for each gene in the region

        tds = tr.cssselect("td[class=' left-border'] a")
        if len(tds) > 0:
            genename = tds[0].text_content()
            print genename
            
            if genename in knowngenelist:    #check if the gene is a possible oncogene from the sanger list of somatic mutations in cancer (COSMIC)
                
                genehtml = scraperwiki.scrape("http://may2009.archive.ensembl.org/"+str(tds[0].attrib['href'])) #get more info on the gene from this URL
                root2 = lxml.html.fromstring(genehtml)
                p = root2.cssselect("div[class='content'] p")
                if len(p) > 0:
                    print p[0].text_content()
                    if len(p[0].cssselect("a")) > 0:
                        uniprotlink = p[0].cssselect("a")[-1].attrib['href'] #get uniprotlink
                    else:
                        uniprotlink = ''
                    print uniprotlink
                    
                    data = {     #format data
                        'region_id' : region_id,                    #id from excel file
                        'gene' : genename,                          #gene name
                        'desc' : p[0].text_content(),               #description from uniprot
                        'geneurl' : uniprotlink,                    #uniprot link
                        'mutated' : knowngenelist[genename][0],     #mutation ratio from the cosmic database
                        'samples' : knowngenelist[genename][1]
                    }
                    print data
                    scraperwiki.sqlite.save(unique_keys=['gene'], data=data)  #save data
                        