# -*- coding: utf-8 -*-


import scraperwiki
import dateutil.parser

months = {u'Januar':'01', u'Februar':'02', u'März':'03', u'April':'04', u'Mai':'05', u'Juni':'06', u'Juli':'07', u'August':'08', u'September':'09', u'Oktober':'10', u'November':'11', u'Dezember':'12'}


scraperwiki.sqlite.attach("wetterbericht_bremen") 

data = scraperwiki.sqlite.select("* from wetter_bremen_kurz")

new_data = []

for d in data: 

    date = d['datum']
    day = date.split('.')[0]
    if len(day) == 1:   
        day = '0' + day

    rest = date.split('.')[1]
    
    month = rest.split()[0]
    year = rest.split()[1]
    month_digit = months[month]
    new_date = year + '-' + month_digit + '-' + day
    d['datum'] = new_date

    time = d['Uhrzeit'].split(':')[0]
    if len(time) == 1:
        time = '0' + time 

    new_date = dateutil.parser.parse(new_date + ' ' + time)

    description = d['wetter_kurz'].split(',')[0]
    degree = d['wetter_kurz'].split(',')[1:]
    degree = ('.'.join(degree)).replace(u'° C', '')

    new_data_row = {'date':new_date, 'degree in Celsius':degree, 'description':description}
    new_data.append(new_data_row)


scraperwiki.sqlite.save(unique_keys=['date'], data=new_data, table_name="sanitized_weather_data")



# -*- coding: utf-8 -*-


import scraperwiki
import dateutil.parser

months = {u'Januar':'01', u'Februar':'02', u'März':'03', u'April':'04', u'Mai':'05', u'Juni':'06', u'Juli':'07', u'August':'08', u'September':'09', u'Oktober':'10', u'November':'11', u'Dezember':'12'}


scraperwiki.sqlite.attach("wetterbericht_bremen") 

data = scraperwiki.sqlite.select("* from wetter_bremen_kurz")

new_data = []

for d in data: 

    date = d['datum']
    day = date.split('.')[0]
    if len(day) == 1:   
        day = '0' + day

    rest = date.split('.')[1]
    
    month = rest.split()[0]
    year = rest.split()[1]
    month_digit = months[month]
    new_date = year + '-' + month_digit + '-' + day
    d['datum'] = new_date

    time = d['Uhrzeit'].split(':')[0]
    if len(time) == 1:
        time = '0' + time 

    new_date = dateutil.parser.parse(new_date + ' ' + time)

    description = d['wetter_kurz'].split(',')[0]
    degree = d['wetter_kurz'].split(',')[1:]
    degree = ('.'.join(degree)).replace(u'° C', '')

    new_data_row = {'date':new_date, 'degree in Celsius':degree, 'description':description}
    new_data.append(new_data_row)


scraperwiki.sqlite.save(unique_keys=['date'], data=new_data, table_name="sanitized_weather_data")



