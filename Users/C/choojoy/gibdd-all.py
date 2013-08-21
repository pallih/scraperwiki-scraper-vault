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
#        print "Sheet %d is called %s and has %d columns and %d rows" % (n, s.name, s.ncols, s.nrows)
        if s.name.encode("utf-8") == "Таблица 1":
            all = s.name
        elif s.name.encode("utf-8") == "Водит":
            driver = s.name
        elif s.name.encode("utf-8") == "Таблица 2":
            average = s.name
        elif s.name.encode("utf-8") == "Нетрез":
            drunk = s.name        
        elif s.name.encode("utf-8") == "Пешеход":
            pedestrian = s.name
        elif s.name.encode("utf-8") == "Дети":
            child = s.name
        elif s.name.encode("utf-8") == "ТехН":
            car = s.name
        elif s.name.encode("utf-8") == "НДУ":
            road = s.name
        elif s.name.encode("utf-8") == "Скрыв":
            elope = s.name

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
            sheet = book.sheet_by_name(all)
            region = sheet.cell(i, 0).value.replace('*','').strip()
            if sheet.cell(i,1).value!='': 
                all_accident = "%d" % (sheet.cell(i,1).value)
            else: 
                all_accident = 0
            if sheet.cell(i,3).value!='': 
                all_death = "%d" % (sheet.cell(i,3).value)
            else: 
                all_death = 0      
            if sheet.cell(i,5).value!='': 
                all_wound = "%d" % (sheet.cell(i,5).value)
            else: 
                all_wound = 0    
    
    
            sheet = book.sheet_by_name(driver)
            if sheet.cell(i,1).value!='': 
                driver_accident = "%d" % (sheet.cell(i,1).value)
            else: 
                driver_accident = 0
            if sheet.cell(i,4).value!='': 
                driver_death = "%d" % (sheet.cell(i,4).value)
            else: 
                driver_death = 0
            if sheet.cell(i,6).value!='': 
                driver_wound = "%d" % (sheet.cell(i,6).value)
            else: 
                driver_wound = 0
    
        
    #        sheet = book.sheet_by_index(2)
    #        average_accidents = sheet.cell(i,1).value
    #        average_injured = sheet.cell(i,3).value
    
    
            sheet = book.sheet_by_name(drunk)
            if sheet.cell(i,1).value!='': 
                drunk_accident = "%d" % (sheet.cell(i,1).value)
            else: 
                drunk_accident = 0
            if sheet.cell(i,4).value!='': 
                drunk_death = "%d" % (sheet.cell(i,4).value)
            else: 
                drunk_death = 0
            if sheet.cell(i,6).value!='': 
                drunk_wound = "%d" % (sheet.cell(i,6).value)
            else: 
                drunk_wound = 0
    
    
            sheet = book.sheet_by_name(pedestrian)
            if sheet.cell(i,1).value!='': 
                pedestrian_accident = "%d" % (sheet.cell(i,1).value)
            else: 
                pedestrian_accident = 0
            if sheet.cell(i,4).value!='': 
                pedestrian_death = "%d" % (sheet.cell(i,4).value)
            else: 
                pedestrian_death = 0
            if sheet.cell(i,6).value!='': 
                pedestrian_wound = "%d" % (sheet.cell(i,6).value)
            else: 
                pedestrian_wound = 0
    
    
    
            sheet = book.sheet_by_name(child)
            if sheet.cell(i,1).value!='': 
                child_accident = "%d" % (sheet.cell(i,1).value)
            else: 
                child_accident = 0
            if sheet.cell(i,4).value!='': 
                child_death = "%d" % (sheet.cell(i,4).value)
            else: 
                child_death = 0
            if sheet.cell(i,6).value!='': 
                child_wound = "%d" % (sheet.cell(i,6).value)
            else: 
                child_wound = 0
    
    
    
            sheet = book.sheet_by_name(car)
            if sheet.cell(i,1).value!='': 
                car_accident = "%d" % (sheet.cell(i,1).value)
            else: 
                car_accident = 0
            if sheet.cell(i,4).value!='': 
                car_death = "%d" % (sheet.cell(i,4).value)
            else: 
                car_death = 0
            if sheet.cell(i,6).value!='': 
                car_wound = "%d" % (sheet.cell(i,6).value)
            else: 
                car_wound = 0
    
    
            sheet = book.sheet_by_name(road)
            if sheet.cell(i,1).value!='': 
                road_accident = "%d" % (sheet.cell(i,1).value)
            else: 
                road_accident = 0
            if sheet.cell(i,4).value!='': 
                road_death = "%d" % (sheet.cell(i,4).value)
            else: 
                road_death = 0
            if sheet.cell(i,6).value!='': 
                road_wound = "%d" % (sheet.cell(i,6).value)
            else: 
                road_wound = 0
    
    
            sheet = book.sheet_by_name(elope)
            if sheet.cell(i,1).value!='': 
                elope_accident = "%d" % (sheet.cell(i,1).value)
            else: 
                elope_accident = 0
            if sheet.cell(i,4).value!='': 
                elope_death = "%d" % (sheet.cell(i,4).value)
            else: 
                elope_death = 0
            if sheet.cell(i,6).value!='': 
                elope_wound = "%d" % (sheet.cell(i,6).value)
            else: 
                elope_wound = 0
    
    
            data = {
                'region': region,
                'all_accident': all_accident,
                'all_death': all_death,
                'all_wound': all_wound,
                'driver_accident': driver_accident,
                'driver_death': driver_death,
                'driver_wound': driver_wound,  
     #           'average_accidents': average_accidents,           
     #           'average_injured': average_injured,
                'drunk_accident': drunk_accident,
                'drunk_death': drunk_death,
                'drunk_wound': drunk_wound,
                'pedestrian_accident': pedestrian_accident,
                'pedestrian_death': pedestrian_death,
                'pedestrian_wound': pedestrian_wound,            
                'child_accident': child_accident,
                'child_death': child_death,
                'child_wound': child_wound,
                'car_accident': car_accident,
                'car_death': car_death,
                'car_wound': car_wound,
                'road_accident': road_accident,
                'road_death': road_death,
                'road_wound': road_wound,
                'elope_accident': elope_accident,
                'elope_death': elope_death,
                'elope_wound': elope_wound,
                }
            scraperwiki.sqlite.save(unique_keys=['region'], data=data, table_name="gibdd"+elem)
        i += 1
    
    print 'Готов парсинг за ' + elem + ' год. Имя таблицы "gibdd'+elem+'".'