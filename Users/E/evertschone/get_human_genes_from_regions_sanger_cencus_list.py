import scraperwiki

# Blank Python
# import libraries
import scraperwiki           
import lxml.html
import xlrd
import csv           


# import list of genes with mutations in breastcancer, this files is exported from http://cancer.sanger.ac.uk/cosmic/browse/tissue, using samples from breast tissue only and all possible subtypes.
'''
data = scraperwiki.scrape("http://www.estyles.nl/cosmic_genes.csv")
reader = csv.reader(data.splitlines())

knowngenelist = dict()
reader.next()
for row in reader:
    knowngenelist[row[0]] = float(row[1])/float(row[2])    #store mutationratio in dictionary, (calculated as: samples with mutations devided by all tested samples)

print len(knowngenelist)
'''

# import list of census genes
'''
xlbin = scraperwiki.scrape("http://www.estyles.nl/cancer_gene_census.xls")
book1 = xlrd.open_workbook(file_contents=xlbin)
sheet1 = book1.sheet_by_name('List')
print sheet1.name, sheet1.nrows
censusgenelist = dict()

for x in range(1,sheet1.nrows):    #for each region scrape the ensemble url for genes
    censusgenelist[str(sheet1.cell(x,0))[7:-1]]= [str(sheet1.cell(x,1))[7:-1], str(sheet1.cell(x,7))[7:-1]]

print censusgenelist.keys()
'''

data2 = scraperwiki.scrape("http://www.estyles.nl/symbol.csv")
reader2 = csv.reader(data2.splitlines())

knowngenelist2 = dict()
reader2.next()
for row in reader2:
    knowngenelist2[row[0]] = [row[0],row[1],row[3]]
    for syn in row[5].split(';'):
        knowngenelist2[syn] = [row[0],row[1],row[3]]   #store mutationratio in dictionary, (calculated as: samples with mutations devided by all tested samples)

print len(knowngenelist2)


#import xls file with ensembl urls generate from the regions, eg. http://may2009.archive.ensembl.org/Homo_sapiens/Location/Synteny?r=17:35127745-35230638 (Synteny view gives easily scrapable results)

xlbin = scraperwiki.scrape("http://www.estyles.nl/biomarkers.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_name('weight by SVM (2)')
print sheet.name, sheet.nrows

for x in range(1,sheet.nrows):    #for each region scrape the ensemble url for genes
    region_id = str(sheet.cell(x,8))[7:].split('.')[0]

    url = str(sheet.cell(x,14))[7:-1]
    print region_id,'-',url
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)


    for tr in root.cssselect("table[class='ss autocenter'] tr"):    #for each gene in the region

        tds = tr.cssselect("td[class=' left-border'] a")
        if len(tds) > 0:
            genename = tds[0].text_content()
            print genename
            
            if genename in knowngenelist2:    #check if the gene is a possible oncogene from the sanger list of somatic mutations in cancer (COSMIC)
                print genename, 'is a known cancer gene', knowngenelist2[genename][0]
                print knowngenelist2[genename]
                data = {     #format data
                    'region_id' : region_id,                    #id from excel file
                    'gene' : genename,                          #gene name
                    'desc' : knowngenelist2[genename][0]+' - '+knowngenelist2[genename][1],               #description from uniprot
                    'tissue' : knowngenelist2[genename][2]  #mutation ratio from the cosmic database
                }
                print data
                scraperwiki.sqlite.save(unique_keys=['gene'], data=data)  #save data