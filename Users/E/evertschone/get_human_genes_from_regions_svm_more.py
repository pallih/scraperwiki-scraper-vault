import scraperwiki

# Blank Python
# import libraries
import scraperwiki           
import lxml.html
import xlrd
import csv           
import re

# import list of genes with mutations in breastcancer, this files is exported from http://cancer.sanger.ac.uk/cosmic/browse/tissue, using samples from breast tissue only and all possible subtypes.

data = scraperwiki.scrape("http://www.estyles.nl/biomart_export_breast.csv")
reader = csv.reader(data.splitlines())

knowngenelist = dict()
reader.next()
for row in reader:
    knowngenelist[row[2]] = [row[6],row[7],row[11]]    #store mutationratio in dictionary, (calculated as: samples with mutations devided by all tested samples)

print len(knowngenelist)

#import xls file with ensembl urls generate from the regions, eg. http://may2009.archive.ensembl.org/Homo_sapiens/Location/Synteny?r=17:35127745-35230638 (Synteny view gives easily scrapable results)

xlbin = scraperwiki.scrape("http://www.estyles.nl/biomarkers.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_name('weight by SVM (2)')
print sheet.name, sheet.nrows

for x in range(1,sheet.nrows):    #for each region scrape the ensemble url for genes
    region_id = str(sheet.cell(x,8))[7:].split('.')[0]

    url = str(sheet.cell(x,14))[7:-1]
    print url, region_id
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)


    for tr in root.cssselect("table[class='ss autocenter'] tr"):    #for each gene in the region

        tds = tr.cssselect("td[class=' left-border'] a")
        if len(tds) > 0:
            genename = tds[0].text_content()
            print genename

            if genename not in knowngenelist:
                myRe = re.compile(genename+'.*') #regex for possible suffixes in cosmic genelist
                for key in knowngenelist:
                    match = myRe.match(key)
                    if match:
                        genename = match.group(0)
                        print match.group(0)
                        break
                    
            if genename in knowngenelist:    #check if the gene is a possible oncogene from the sanger list of somatic mutations in cancer (COSMIC)
                '''
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
                '''
                data = {     #format data
                    'region_id' : region_id,                    #id from excel file
                    'breastcancergene' : 'yes',
                    'gene' : genename,                          #gene name
                    'censusgene' : knowngenelist[genename][0],  
                    'acc' : knowngenelist[genename][1],           
                    'subtype' : knowngenelist[genename][2] 
                }
                print data
                scraperwiki.sqlite.save(unique_keys=['gene'], data=data)  #save data
            else:
                data = {     #format data
                    'region_id' : region_id,                    #id from excel file
                    'breastcancergene' : 'no',
                    'gene' : genename,                          #gene name
                    'censusgene' : '',  
                    'acc' : '',           
                    'subtype' : '' 
                }
                scraperwiki.sqlite.save(unique_keys=['gene'], data=data)  #save data