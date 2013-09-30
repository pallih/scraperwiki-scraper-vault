import scraperwiki           
import xlrd

#earlier years don't have complete lists
yearlist = ['1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011']

genderlist = ['boys','girls']

for year in yearlist:

    for gender in genderlist:

    #last three years have used three different formats...
        if year == '2011':
            url = "http://www.ons.gov.uk/ons/rel/vsob1/baby-names--england-and-wales/%s/rtd-baby-names--%s--%s.xls" %(year,gender,year)
        elif year == '2009':
            url = "http://www.ons.gov.uk/ons/rel/vsob1/baby-names--england-and-wales/%s/%s-names---%s.xls" %(year,gender,year)
        elif year == '2010':
            url = "http://www.ons.gov.uk/ons/rel/vsob1/baby-names--england-and-wales/%s/%s-%s-names.xls" %(year,year,gender)
        else:
            url = "http://www.ons.gov.uk/ons/rel/vsob1/baby-names--england-and-wales/%s/%s-baby-names-statistics-%s.xls" %(year,year,gender)

    #96 slightly diff format
        if year == '1996':
            sheet = "Table 3 - %s names - E&W" %(gender.title())
        else:
            sheet = "Table 6 - %s names - E&W" %(gender.title())

        xlbin = scraperwiki.scrape(url)
        book = xlrd.open_workbook(file_contents=xlbin)

        #Get sheet by name (check if consistent)
        sheet = book.sheet_by_name(sheet)


        data = []        
        for row in range(5,sheet.nrows): # for each row

            #name column
            namecell = sheet.cell(row,2)
            namecellValue = namecell.value

            #count of name column
            countcell = sheet.cell(row,3)
            countcellValue = countcell.value

            #build data for one sheet before writing to sql
            if namecellValue !="" and "--" not in namecellValue:
                data.append({
                    'Name' : namecellValue,
                    'Count' : countcellValue,
                    'Year' : year,
                    'Gender' : gender
                })
            else:
                print "empty name:", namecellValue 

        #some names unisex so need gender as part of key
        scraperwiki.sqlite.save(['Year','Gender','Name'], data)
        scraperwiki.sqlite.save_var('last_url', url)import scraperwiki           
import xlrd

#earlier years don't have complete lists
yearlist = ['1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011']

genderlist = ['boys','girls']

for year in yearlist:

    for gender in genderlist:

    #last three years have used three different formats...
        if year == '2011':
            url = "http://www.ons.gov.uk/ons/rel/vsob1/baby-names--england-and-wales/%s/rtd-baby-names--%s--%s.xls" %(year,gender,year)
        elif year == '2009':
            url = "http://www.ons.gov.uk/ons/rel/vsob1/baby-names--england-and-wales/%s/%s-names---%s.xls" %(year,gender,year)
        elif year == '2010':
            url = "http://www.ons.gov.uk/ons/rel/vsob1/baby-names--england-and-wales/%s/%s-%s-names.xls" %(year,year,gender)
        else:
            url = "http://www.ons.gov.uk/ons/rel/vsob1/baby-names--england-and-wales/%s/%s-baby-names-statistics-%s.xls" %(year,year,gender)

    #96 slightly diff format
        if year == '1996':
            sheet = "Table 3 - %s names - E&W" %(gender.title())
        else:
            sheet = "Table 6 - %s names - E&W" %(gender.title())

        xlbin = scraperwiki.scrape(url)
        book = xlrd.open_workbook(file_contents=xlbin)

        #Get sheet by name (check if consistent)
        sheet = book.sheet_by_name(sheet)


        data = []        
        for row in range(5,sheet.nrows): # for each row

            #name column
            namecell = sheet.cell(row,2)
            namecellValue = namecell.value

            #count of name column
            countcell = sheet.cell(row,3)
            countcellValue = countcell.value

            #build data for one sheet before writing to sql
            if namecellValue !="" and "--" not in namecellValue:
                data.append({
                    'Name' : namecellValue,
                    'Count' : countcellValue,
                    'Year' : year,
                    'Gender' : gender
                })
            else:
                print "empty name:", namecellValue 

        #some names unisex so need gender as part of key
        scraperwiki.sqlite.save(['Year','Gender','Name'], data)
        scraperwiki.sqlite.save_var('last_url', url)