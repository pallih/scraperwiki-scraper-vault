import scraperwiki           
import xlrd

# -*- coding: utf-8 -*-



# перед парсингом подготовить файлы на соответствия столбцов
#для skfo 6-97 без 24, 30, 37, 44, 52, 53, 68, 75, 88. значит записываем вычитая единицу, т.к. индекс идет с нуля
#для ufo 6-96 без 24, 30, 37, 51, 52, 67, 74, 87. значит записываем вычитая единицу, т.к. индекс идет с нуля


years = ['2012', '2011', '2010','2009', '2008', '2007', '2006', '2005', '2004']
skfo_years = ['2012','2011','2010']
ufo_years = ['2009', '2008']
years_2007_choose = ['2007']
years_2005_choose = ['2006', '2005']
years_2004_choose = ['2004']

minus_rows_skfo = [23, 29, 36, 43, 51, 52, 67, 74, 87]
years_2004 = [23, 29, 36, 50, 51, 67, 74, 91]
years_2005 = [23, 29, 36, 50, 51, 66, 73, 90]
years_2006 = [23, 29, 36, 50, 51, 66, 73, 90]
years_2007 = [23, 29, 36, 50, 51, 66, 73, 88, 98, 99, 100, 101, 102]
minus_rows_ufo = [23, 29, 36, 50, 51, 66, 73, 86, 96, 97, 98, 99, 100, 101, 102]


for elem in years:
    xlbin = scraperwiki.scrape("http://www.gibdd.ru/stat/files/otchet/1/" + elem + ".xls")
    book = xlrd.open_workbook(file_contents=xlbin)

    for n, s in enumerate(book.sheets()):
        print "Sheet %d is called %s and has %d columns and %d rows" % (n, s.name, s.ncols, s.nrows)
        if s.name.encode("utf-8") == "Таблица 2":
            average = s.name
        
    if elem in skfo_years:
        minus_rows=minus_rows_skfo
    elif elem in ufo_years:
        minus_rows=minus_rows_ufo
    elif elem in years_2007_choose:
        minus_rows=years_2007
    elif elem in years_2005_choose:
        minus_rows=years_2005
    elif elem in years_2004_choose:
        minus_rows=years_2004


    i = 5
    while i<97: 
        if not i in minus_rows:
            sheet = book.sheet_by_name(average)
            region = sheet.cell(i, 0).value.replace('*','').strip()
            if sheet.cell(i,3).value!='': 
                amount_cars = "%d" % (sheet.cell(i,3).value)
            else: 
                amount_cars = 0
            if sheet.cell(i,4).value!='': 
                amount_citizens = "%.3f" % (sheet.cell(i,4).value)
            else: 
                amount_citizens = 0
            
            print sheet.cell(i,4).value    

            data = {
                'region': region,
                'amount_cars': amount_cars,
                'amount_citizens': amount_citizens,
                }
            scraperwiki.sqlite.save(unique_keys=['region'], data=data, table_name="gibdd-amount"+elem)
        i += 1
    
    print 'Готов парсинг за ' + elem + ' год. Имя таблицы "gibdd'+elem+'".'