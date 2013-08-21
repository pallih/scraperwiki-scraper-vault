import scraperwiki,requests,zipfile, StringIO,xlrd,re 

# available on the page:
# http://www.ons.gov.uk/ons/rel/pop-estimate/population-estimates-for-uk--england-and-wales--scotland-and-northern-ireland/population-estimates-timeseries-1971-to-current-year/index.html

def processsheet(sheet, gender):
    print "processing %s sheet"%gender
    for rowno in range(sheet.nrows):
        row = sheet.row(rowno)
        buildup=[]
        data={}
        #print [cell.value for cell in row]
        if not re.match('[A-Z][0-9]*$', row[0].value): # doesn't handle Northern Ireland
            if not re.match('[0-9][0-9][A-Z]$', row[0].value): # doesn't handle Northern Ireland
                continue
        row= map(lambda x: x.value, row)
        data['areacode']=row[0]
        data['areaname']=row[1] # TODO: trim numbers at end? 
        #data['arealevel']=                   # TODO: count indentation levels?
        data['gender']=gender
        
        for i in range(-1,91): # CHECK RANGE!
            tdata=dict(data)
            col=i+3
            if i==-1:
                tdata['age']='all'
            else:
                tdata['age']=i
            tdata['pop']=row[col]
            buildup.append(tdata)

        scraperwiki.sqlite.save(table_name='pop', data=buildup, unique_keys=['areacode','gender','age'])


url='http://www.ons.gov.uk/ons/rel/pop-estimate/population-estimates-for-uk--england-and-wales--scotland-and-northern-ireland/mid-2010-population-estimates/rft---mid-2010-population-estimates.zip'

# should read this file in the zip file as it has the ages per year (not per 5 years)
#     mid-2010-unformatted-data-file.xls
# Then can we calculate the student bulge, as well as recreate the same image


# See this table; click: [Graph]
#    https://views.scraperwiki.com/run/general_graphs/?name=ons-popestimates&sqlcode=select%20age%2C%20pop%20from%20pop%20where%20areaname%3D'Cambridge'%20and%20age!%3D'all'%0A

# For the highest pop20/pop15 results, click [Table] here:
#    https://views.scraperwiki.com/run/general_graphs/?name=ons-popestimates&sqlcode=SELECT%20pop1.areaname%2C%20%0A%20%20%20%20pop2.pop%2Fpop1.pop%20AS%20pop20over15%2C%20%0A%20%20%20%20pop1.pop%20AS%20pop15%20%0AFROM%20pop%20AS%20pop1%20%0ALEFT%20JOIN%20pop%20AS%20pop2%20ON%20pop2.areacode%3Dpop1.areacode%0AWHERE%20pop1.age%3D15%20AND%20pop2.age%3D20%20%0AORDER%20BY%20pop20over15%20desc%0ALIMIT%2050%0A

# Seems to have lots of University towns, but the annual table (rather than 5-year one) may be better for picking up the sharp 
# increase in 20 year olds.


zip=requests.get(url).content
#print zip

#with ZipFile('spam.zip', 'w') as myzip:
#    myzip.write('eggs.txt')

fp = StringIO.StringIO(zip)
zfp = zipfile.ZipFile(fp, "r")
xls = zfp.open('mid-2010-unformatted-data-file.xls').read()
book = xlrd.open_workbook(file_contents=xls)
#for n, sheet in enumerate(book.sheets()):
    #print "Sheet %d has %d columns and %d rows" % (n, sheet.ncols, sheet.nrows)

sheets=(('all',1),('male',2),('female',3))
for sheet in sheets:
    processsheet(book.sheets()[sheet[1]],sheet[0])


        #print sorted(data.items())
    
    