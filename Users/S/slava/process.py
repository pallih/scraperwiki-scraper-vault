import scraperwiki
import re

data = """678190, Республика Саха (Якутия), п.Айхал, ул.Промышленная 24 
163061, г. Архангельск, ул. Поморская, д. 36 Телефон (8182) 65-32-26 Факс (8182) 65-32-26 e-mail makbank@atnet.ru 
664023, г. Иркутск, ул. Пискунова, д.122 
665826, г. Ангарск, 14 мкр., д. 1, 
350001, Краснодарский край, г. Краснодар, Карасунский округ, ул. им. Шевченко, д. 134/1 
678144, г. Ленск, Республика Саха (Якутия), ул. Победы, д.6 
678170, г. Мирный, Республика Саха (Якутия), ул. Тихонова, д. 3 
119180, г.Москва, ул.Большая Полянка, дом 10/9, строение 1 
630009, г.Новосибирск, ул.Большевистская, дом 103 
302001, г.Орел, ул.Комсомольская, дом 44
678188, Республика Саха (Якутия), Мирнинский район, г.Удачный, Центральная площадь, дом 2 
677999, РС (Я), г. Якутск, пр. Ленина, д. 24"""

data = data.split("\n")
pc = re.compile('^(\d+)?,', re.U | re.I)
region = re.compile('(,|^)(.+)?\s(обл\.|область|рег|край|Республика|округ)', re.U | re.I)
raion = re.compile(', (.+)?\s(район|р-н)', re.U | re.I)
city = re.compile('(с\.|г\.|г\.\ |город\ |город|п\.|п|пос\.|пгт\.)(.+?),(.+)', re.U | re.I)
sch = ' \t\n\r.,'
#district = re.compile('(микрорайон|мкр-н)(.+?),', re.U | re.I)
#street = re.compile('(ул\.|улица|пр\.|пр-т|проспект|просп\.|пер\.|переулок)(.+)', re.U | re.I)

#scraperwiki.sqlite.attach('slava_test1')
#data = scraperwiki.sqlite.select("* from swdata")
i=0
for row in data:
    i+=1
    out = {'id':i, 'original':row, 'postal_code': '', 'raion':'', 'region':'','city':'', 'district':'', 'street':''}
    #addr = row['address'].encode('utf-8')
    addr = row
    #addr = addr.replace("Российская Федерация, ", "")
    #addr = addr.replace("Россия, ", "")

    #print addr
    m = pc.findall(addr)
    if len(m)>0:
        out['postal_code'] = m[0]
        addr = addr.replace(out['postal_code']+",","")

    m = region.findall(addr)
    if len(m)>0:
        out['region'] = (m[0][1] + " " + m[0][2]).strip(sch)
        addr = addr.replace(out['region']+",","")

    m = raion.findall(addr)
    if len(m)>0:
        out['raion'] = (m[0][0] + " " + m[0][1]).strip(sch )
        addr = addr.replace(out['raion']+",","")

    m = city.findall(addr)
    if len(m)>0:
        out['city'] = (str(m[0][0]) + str(m[0][1])).strip(sch)
        addr = addr.replace(out['city'],"")
        out['street'] = str(m[0][2]).strip(sch)

    #m = district.findall(addr)
    #if len(m)>0:
    #    out['district'] = str(m[0][0]) + str(m[0][1])

    #m = street.findall(addr)
    #if len(m)>0:
    #    out['street'] = m[0][0] + " " + str(m[0][1])
        

    scraperwiki.sqlite.save(unique_keys=['id'], data=out, table_name="swdata_process")


import scraperwiki
import re

data = """678190, Республика Саха (Якутия), п.Айхал, ул.Промышленная 24 
163061, г. Архангельск, ул. Поморская, д. 36 Телефон (8182) 65-32-26 Факс (8182) 65-32-26 e-mail makbank@atnet.ru 
664023, г. Иркутск, ул. Пискунова, д.122 
665826, г. Ангарск, 14 мкр., д. 1, 
350001, Краснодарский край, г. Краснодар, Карасунский округ, ул. им. Шевченко, д. 134/1 
678144, г. Ленск, Республика Саха (Якутия), ул. Победы, д.6 
678170, г. Мирный, Республика Саха (Якутия), ул. Тихонова, д. 3 
119180, г.Москва, ул.Большая Полянка, дом 10/9, строение 1 
630009, г.Новосибирск, ул.Большевистская, дом 103 
302001, г.Орел, ул.Комсомольская, дом 44
678188, Республика Саха (Якутия), Мирнинский район, г.Удачный, Центральная площадь, дом 2 
677999, РС (Я), г. Якутск, пр. Ленина, д. 24"""

data = data.split("\n")
pc = re.compile('^(\d+)?,', re.U | re.I)
region = re.compile('(,|^)(.+)?\s(обл\.|область|рег|край|Республика|округ)', re.U | re.I)
raion = re.compile(', (.+)?\s(район|р-н)', re.U | re.I)
city = re.compile('(с\.|г\.|г\.\ |город\ |город|п\.|п|пос\.|пгт\.)(.+?),(.+)', re.U | re.I)
sch = ' \t\n\r.,'
#district = re.compile('(микрорайон|мкр-н)(.+?),', re.U | re.I)
#street = re.compile('(ул\.|улица|пр\.|пр-т|проспект|просп\.|пер\.|переулок)(.+)', re.U | re.I)

#scraperwiki.sqlite.attach('slava_test1')
#data = scraperwiki.sqlite.select("* from swdata")
i=0
for row in data:
    i+=1
    out = {'id':i, 'original':row, 'postal_code': '', 'raion':'', 'region':'','city':'', 'district':'', 'street':''}
    #addr = row['address'].encode('utf-8')
    addr = row
    #addr = addr.replace("Российская Федерация, ", "")
    #addr = addr.replace("Россия, ", "")

    #print addr
    m = pc.findall(addr)
    if len(m)>0:
        out['postal_code'] = m[0]
        addr = addr.replace(out['postal_code']+",","")

    m = region.findall(addr)
    if len(m)>0:
        out['region'] = (m[0][1] + " " + m[0][2]).strip(sch)
        addr = addr.replace(out['region']+",","")

    m = raion.findall(addr)
    if len(m)>0:
        out['raion'] = (m[0][0] + " " + m[0][1]).strip(sch )
        addr = addr.replace(out['raion']+",","")

    m = city.findall(addr)
    if len(m)>0:
        out['city'] = (str(m[0][0]) + str(m[0][1])).strip(sch)
        addr = addr.replace(out['city'],"")
        out['street'] = str(m[0][2]).strip(sch)

    #m = district.findall(addr)
    #if len(m)>0:
    #    out['district'] = str(m[0][0]) + str(m[0][1])

    #m = street.findall(addr)
    #if len(m)>0:
    #    out['street'] = m[0][0] + " " + str(m[0][1])
        

    scraperwiki.sqlite.save(unique_keys=['id'], data=out, table_name="swdata_process")


