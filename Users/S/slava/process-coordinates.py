import scraperwiki
import re

data = """        myMap.panTo([55.786764,49.122853]);
        myMap.controls.add('zoomControl');
        // Создаем метку и задаем изображение для ее иконки
        var myPlacemark = new ymaps.Placemark([55.792002554167,49.108604804893], {
            balloonContent: 'ул. Чернышевского, 18/23'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.769255591712,49.220836993799], {
            balloonContent: 'ул. Проспект Победы д.100'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.841452999994,49.099599279762], {
            balloonContent: 'ул. Короленко д. 93а'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.743136999994,49.142134813492], {
            balloonContent: 'ул. Кулагина д.4'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.816688923208,49.063569186508], {
            balloonContent: 'ул. Краснококшайская д.125'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.840434122317,49.080292706372], {
            balloonContent: 'ул. Декабристов д.205'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.837394225078,49.198338288361], {
            balloonContent: 'ул. Сибирский тракт д.48'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.858594863181,49.085531101852], {
            balloonContent: 'ул. Копылова д.18'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.872049935783,49.223631186508], {
            balloonContent: 'ул. Липатова д.5'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.748406621601,49.141887707024], {
            balloonContent: 'ул. Модельная, 19'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([], {
            balloonContent: 'ул. Карбышева, д.36/2'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.83718894915,49.198252457672], {
            balloonContent: 'ул. Сибирский тракт д.48 (Автосалон КАН АВТО)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.837382150054,49.198263186508], {
            balloonContent: 'ул. Сибирский тракт д.48(сервисная зона Автосалон КАН АВТО)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.792038821674,49.108712093254], {
            balloonContent: 'ул. Чернышевского д.18/23 (центральный офис)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.86976487015,49.21978082209], {
            balloonContent: 'ул. Липатова д.37 корпус 46 (ОАО &quot;КОМЗ&quot;)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.836868821094,49.196291493393], {
            balloonContent: 'ул. Сибирский тракт д.51(Автосалон КАН АВТО)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.841483151652,49.100676400139], {
            balloonContent: 'ул. Короленко д.58 (ОАО &quot;Завода Элекон&quot;)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.772502097817,49.220910469559], {
            balloonContent: 'ул. Минская д.1(Автосалон «АЗИНО АВТО»)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.79965991544,49.065658789024], {
            balloonContent: 'ул.Кл. Цеткин д.8/27 (РГУП «Бюро технической инвентаризации» МСАЖКХ РТ)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.788652151295,49.173612652779], {
            balloonContent: 'ул.Волочаевская д.6 (РГУП «Бюро технической инвентаризации» МСАЖКХ РТ)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.841718311123,49.086235311402], {
            balloonContent: 'ул.Ибрагимова д.2 (РГУП «Бюро технической инвентаризации» МСАЖКХ РТ)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.716290233836,52.399723009772], {
            balloonContent: 'ул.Ахметшина д.120 (Комплекс 60/06)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([], {
            balloonContent: 'ул. Привокзальная д.4 (Завод &quot;Серго&quot;)'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.847357921195,48.52337624884], {
            balloonContent: 'ул. Ленина д.25в'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
        var myPlacemark = new ymaps.Placemark([55.364435691744,50.641529987773], {
            balloonContent: 'ул. Тукая 54б'
        }, {
            iconImageHref: '/images/map_ico.png', // картинка иконки
            iconImageSize: [38, 51], // размеры картинки
            iconImageOffset: [-3, -42] // смещение картинки
        });
    // Добавление метки на карту
    myMap.geoObjects.add(myPlacemark);
    });
});"""

pc = re.compile('^(\d+)?,', re.U | re.I)
region = re.compile(', (.+)?(обл\.|область|рег|край)', re.U | re.I)
city = re.compile('(г\.|г\.\ |город\ |город)(.+?),(.+)', re.U | re.I)

address = re.compile("new ymaps.Placemark\(\[([\d\.]+?),([\d\.]+?)\]\,\ \{.*?balloonContent: '(.+?)'", re.U | re.I | re.S);

#scraperwiki.sqlite.attach('slava_test1')
#data = scraperwiki.sqlite.select("* from swdata")
i=0
if data!= "":

    for a in address.findall(data):
        i+=1
        scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'lat':a[0], 'lon':a[1], 'address':a[2] }, table_name="coordonate_adrese")
    exit()
    out = {'postal_code': '', 'region':'','city':'', 'street':''}
    #addr = row['address'].encode('utf-8')
    addr = row
    #addr = addr.replace("Российская Федерация, ", "")
    #addr = addr.replace("Россия, ", "")

    #print addr
    m = pc.findall(addr)
    if len(m)>0:
        out['postal_code'] = m[0]

    m = region.findall(addr)
    if len(m)>0:
        out['region'] = m[0][0] + m[0][1]

    addr = addr.replace(out['region'],"")
    m = city.findall(addr)
    #print m
    if len(m)>0:
        #print m[0]
        out['city'] = "г. " + str(m[0][1])
        out['street'] = m[0][2]
        


