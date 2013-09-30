# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
# Blank Python

#
#urls = """http://www.alfabank.ru/russia/moscow/"""
url = "http://www.nskbl.ru/offices_terminals/offices/filter_jx.php"
html ="""<h2>Новосибирск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/945/">Головной офис</a></strong></big></p>
                    <p><big><strong>Россия, 630054 г. Новосибирск, ул. Плахотного, 25/1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:root@nskbl.ru">root@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/959/">Дополнительный офис «Дзержинский»</a></strong></big></p>
                    <p><big><strong>630015, г. Новосибирск, ул. Королева, 21/1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:rem@nskbl.ru">rem@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/958/">Дополнительный офис «Заельцовский»</a></strong></big></p>
                    <p><big><strong>630082, г. Новосибирск, Дуси Ковальчук, 252</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:pirv@nsknl.ru">pirv@nsknl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/954/">Дополнительный офис «К. Маркса, 23»</a></strong></big></p>
                    <p><big><strong>630064, г. Новосибирск, пр. Карла Маркса, 23</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:maa@nskbl.ru">maa@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/957/">Дополнительный офис «Кировский»</a></strong></big></p>
                    <p><big><strong>630088, г.Новосибирск, ул. Громова, 17</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:pap@nskbl.ru">pap@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/960/">Дополнительный офис «Октябрьский»</a></strong></big></p>
                    <p><big><strong>630009, г. Новосибирск, ул. Кирова, 108</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:lta@nskbl.ru">lta@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/961/">Дополнительный офис «Площадь Труда»</a></strong></big></p>
                    <p><big><strong>630108, г. Новосибирск, площадь Труда, 1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:shvv@nskbl.ru">shvv@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/955/">Дополнительный офис «Центральный»</a></strong></big></p>
                    <p><big><strong>630099, г. Новосибирск, Орджоникидзе, 33</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:sas@nskbl.ru">sas@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/952/">Кредитно-кассовый офис «Академический»</a></strong></big></p>
                    <p><big><strong>630090, г. Новосибирск, ул. Ильича, 6</strong></big></p>
                    <p>
                        (383) 330-40-29, 330-32-20<br />

                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/946/">Кредитно-кассовый офис «Студенческий»</a></strong></big></p>
                    <p><big><strong>630092, г. Новосибирск, пр. К. Маркса, 20 (НГТУ, корпус 2, 1 этаж)</strong></big></p>
                    <p>
                        (383) 346-06-90<br />
   <a href="mailto:deskngtu@kbl.nsk.su ">deskngtu@kbl.nsk.su </a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/7600/">Дополнительный офис &quot;Калининский&quot;</a></strong></big></p>
                    <p><big><strong>630110, Новосибирск, ул. Богдана Хмельницкого, 41</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:mevl@nskbl.ru">mevl@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/8377/">Дополнительный офис «Коммунистическая,48а»</a></strong></big></p>
                    <p><big><strong>630007, г. Новосибирск, ул. Коммунистическая,48а</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:ktj@nskbl.ru">ktj@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/23955/">Дополнительный офис «Первомайский»</a></strong></big></p>
                    <p><big><strong>630037, г. Новосибирск, ул. Маяковского, 5</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:zatv@nskbl.ru">zatv@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/25821/">Кредитно-кассовый офис &quot;На Восходе&quot;</a></strong></big></p>
                    <p><big><strong>630102, г. Новосибирск, ул. Зыряновская, 53</strong></big></p>
                    <p>
                        (383) 3-600-900<br />

                    </p>
                </div>
            </div>

            <div class="spacer"></div>

            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/26084/">Центр кредитования малого бизнеса</a></strong></big></p>
                    <p><big><strong>630007, г. Новосибирск, ул. Коммунистическая,48а</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:zed@nskbl.ru">zed@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/26087/">Китайский офис</a></strong></big></p>
                    <p><big><strong>630009, г. Новосибирск, ул. Кирова, 108</strong></big></p>
                    <p>
   <a href="mailto:ten@nskbl.ru">ten@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/30298/">Дополнительный офис «Советский»</a></strong></big></p>
                    <p><big><strong>630090 г. Новосибирск, Морской проспект, 24</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:cvs@nskbl.ru">cvs@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/42727/">Дополнительный офис «Голден Парк» </a></strong></big></p>
                    <p><big><strong>630129, г. Новосибирск, ул. Курчатова, 1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:ksb@nskbl.ru">ksb@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/47969/">Кредитно-кассовый офис «На Гусинобродском шоссе»</a></strong></big></p>
                    <p><big><strong>630124, г. Новосибирск, Гусинобродское шоссе, 33/1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />

                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/50158/">Дополнительный офис «Западный»</a></strong></big></p>
                    <p><big><strong>630071, г. Новосибирск, ул. Забалуева, 51/1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:mlb@nskbl.ru">mlb@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/66985/">Кредитно-кассовый офис «Хилокский»</a></strong></big></p>
                    <p><big><strong>630052, г. Новосибирск, ул. Хилокская, 30</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:deskhlk@nskbl.ru">deskhlk@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Кемерово</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/962/">Операционный офис «Кемеровский»</a></strong></big></p>
                    <p><big><strong>650070 Кемеровская область, г. Кемерово, проспект Молодежный, 3а</strong></big></p>
                    <p>
                        (3842) 31-45-91 начальник ОО<br />
(3842) 31-74-66<br />
   <a href="mailto:kmkev@nskbl.ru ">kmkev@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Юридические лица: понедельник — пятница с 9.00 до 17.00 (без перерыва)
Физические лица: понедельник — пятница с 9.00 до 20.00 (без перерыва), суббота с 9.00 до 17.00 (без перерыва), выходной: воскресенье
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/20955/">Операционный офис &quot;Кемеровский-2&quot;</a></strong></big></p>
                    <p><big><strong>650000 Кемеровская область, г. Кемерово, ул. Ноградская, 16</strong></big></p>
                    <p>
                        (3842) 36-49-00, 36-48-27<br />
   <a href="mailto:kmeeg@nskbl.ru ">kmeeg@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Юридические лица: понедельник — пятница с 9.00 до 17.00 (без перерыва)
Физические лица: понедельник — пятница с 9.00 до 20.00 (без перерыва), суббота с 9.00 до 17.00 (без перерыва), выходной: воскресенье                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/48020/">Операционный офис «Кемеровский-3» </a></strong></big></p>
                    <p><big><strong>650066 г. Кемерово, проспект Октябрьский, 3г</strong></big></p>
                    <p>
                        (3842) 72-17-82<br />
   <a href="mailto:kmvsn@nskbl.ru">kmvsn@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Юридические лица: понедельник — пятница с 10.00 до 17.00 (без перерыва)
Физические лица: Понедельник с 08.30 до 18.00, вторник    с 08.30 до 20.00, среда    с 08.30 до 18.00, четверг с 08.30 до 20.00, пятница с 08.30 до 18.00, суббота с 08.30 до 18.00. Выходной: воскресенье                </div>
            </div>


            <div class="spacer"></div>
            <h2>Новокузнецк</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/963/">Операционный офис «Новокузнецкий»</a></strong></big></p>
                    <p><big><strong>654080, Кемеровская область, г. Новокузнецк, ул. Кирова, 103</strong></big></p>
                    <p>
                        (3843) 76-52-40 начальник ОО<br />
(3843) 76-17-09 Отдел расчетного обслуживания (частных лиц)<br />
(3843) 76-43-80 Отдел расчетного обслуживания (юридических лиц)<br />
   <a href="mailto:nksnp@nskbl.ru">nksnp@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Юридические лица: понедельник — пятница с 9.00 до 17.00 (без перерыва), выходной: суббота и воскресенье 
Физические лица: понедельник — пятница с 9.00 до 20.00 (без перерыва), суббота с 9.00 до 17.00 (без перерыва), выходной: воскресенье                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/55192/">Кредитно-кассовый офис «Новокузнецкий–2»</a></strong></big></p>
                    <p><big><strong>654041, г. Новокузнецк, пр. Бардина, 2</strong></big></p>
                    <p>
                        (3843) 76-17-09<br />

                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Физические лица: понедельник — воскресенье с 10.00 до 20.00, перерыв с 13.00 до 14.00                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Барнаул</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/12758/">Операционный офис &quot;Барнаульский&quot;</a></strong></big></p>
                    <p><big><strong>656056 г. Барнаул, пр. Ленина, 29</strong></big></p>
                    <p>
                        (3852) 22-90-70, 22-90-71, 22-90-72<br />
   <a href="mailto:brpuv@nskbl.ru">brpuv@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 9.00 до 20.00 (без перерыва), в субботу с 9.00 до 17.00 (без перерыва)
Для юридических лиц: понедельник-пятница с 9.00 до 17.00 (без перерыва)                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/35605/">Кредитно–кассовый офис «Барнаульский-2» </a></strong></big></p>
                    <p><big><strong>656023, г. Барнаул, пр. Космонавтов, 59</strong></big></p>
                    <p>
                        (3852) 337-309<br />

                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 9.00 до 17.00 часов, выходные дни – суббота, воскресенье.                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Красноярск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/15286/">Операционный офис &quot;Красноярский&quot;</a></strong></big></p>
                    <p><big><strong>660049 г. Красноярск, Урицкого ул., 52</strong></big></p>
                    <p>
                        (391) 265-35-35, 265-35-25, 265-35-05<br />
   <a href="mailto:krshoa@nskbl.ru">krshoa@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Юридические лица: понедельник — пятница с 9.00 до 17.00 (без перерыва), выходной: суббота и воскресенье 
Физические лица: понедельник — пятница с 9.00 до 20.00 (без перерыва), суббота с 9.00 до 17.00 (без перерыва), выходной: воскресенье                </div>
            </div>


            <div class="spacer"></div>
            <h2>Томск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/32393/">Операционный офис &quot;Томский&quot;</a></strong></big></p>
                    <p><big><strong>634009 г. Томск, Совпартшкольный переулок, 13</strong></big></p>
                    <p>
                        (3822) 900-410, 512-845, 512-865<br />
   <a href="mailto:tmnta@nskbl.ru">tmnta@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    обслуживание юридических лиц: понедельник-пятница с 9.00 до 17.00, выходные дни – суббота, воскресенье;
обслуживание физических лиц: понедельник-пятница с 9.00 до 20.00, суббота с 9.00 до 17.00, выходной день – воскресенье.                </div>
            </div>


            <div class="spacer"></div>
            <h2>Обь</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/956/">Дополнительный офис в г. Обь</a></strong></big></p>
                    <p><big><strong>633103, НСО, г. Обь, ул. ЖКО Аэропорта, 24</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:kmvl@nskbl.ru">kmvl@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/948/">Кредитно-кассовый офис «Толмачево»</a></strong></big></p>
                    <p><big><strong>633103, НСО, г. Обь, ул. Аэропорта, 1</strong></big></p>
                    <p>
                        (383) 216-99-32<br />
   <a href="mailto:desktlm@nskbl.ru">desktlm@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Бердск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/949/">Дополнительный офис «Бердский»</a></strong></big></p>
                    <p><big><strong>Россия, 633009 Новосибирская область, г. Бердск ул. Рогачева, 1</strong></big></p>
                    <p>
                        (383) 258-19-57 <br />
(383) 258-19-55 Отдел расчетного обслуживания юридических лиц<br />
(383-41) 48-284 Отдел расчетного обслуживания физических лиц<br />
(383) 204-91-53  Кредитный отдел<br />
   <a href="mailto:basv@nskbl.ru">basv@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/951/">Дополнительный офис «Бердский-2» </a></strong></big></p>
                    <p><big><strong>633010, НСО, г. Бердск, ул. Максима Горького, 3</strong></big></p>
                    <p>
                        (383-41) 22-585 Начальник дополнительного офиса <br />
(383) 335-69-12<br />
   <a href="mailto:bmvv@nskbl.ru">bmvv@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/950/">Дополнительный офис «Бердский-3»</a></strong></big></p>
                    <p><big><strong>633010, НСО, г. Бердск, ул. Ленина, 69</strong></big></p>
                    <p>
                        (383-41) 29-630 Начальник дополнительного офиса<br />
(383-41) 29-640<br />
(383-41) 29-664<br />
   <a href="mailto:bslv@nskbl.ru">bslv@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Баган</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/965/">Дополнительный офис «Баганский»</a></strong></big></p>
                    <p><big><strong>632770, НСО, с. Баган, ул. М. Горького, 25а</strong></big></p>
                    <p>
                        (383-53) 22-444 начальник дополнительного офиса<br />
(383-53) 21-104<br />
(383-53) 22-451<br />
   <a href="mailto:901boss@nskbl.ru">901boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Барабинск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/1290/">Дополнительный офис «Барабинский»</a></strong></big></p>
                    <p><big><strong>632336, НСО, г. Барабинск, ул. Ульяновская, 60</strong></big></p>
                    <p>
                        (383-61) 23-167 начальник дополнительного офиса,<br />
(383-61) 25-778,<br />
(383-61) 25-526<br />
   <a href="mailto:902boss@nskbl.ru">902boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресение
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Болотное</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/966/">Дополнительный офис «Болотнинский»</a></strong></big></p>
                    <p><big><strong>633340, НСО, г. Болотное, ул. М. Горького, 33</strong></big></p>
                    <p>
                        (383-49) 25-100 начальник дополнительного офиса<br />
(383-49) 24-452<br />
(383-49) 24-453<br />
   <a href="mailto:903boss@nskbl.ru">903boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Венгерово</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/967/">Дополнительный офис «Венгеровский»</a></strong></big></p>
                    <p><big><strong>632240, НСО, с. Венгерово, ул. Ленина, 63</strong></big></p>
                    <p>
                        (383-69) 22-602 начальник дополнительного офиса<br />
(383-69) 22-603<br />
   <a href="mailto:904boss@nskbl.ru">904boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Довольное</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/968/">Дополнительный офис «Доволенский»</a></strong></big></p>
                    <p><big><strong>632450, НСО, с. Довольное, ул. Мичурина, 14а</strong></big></p>
                    <p>
                        (383-54) 20-360 начальник дополнительного офиса<br />
(383-54) 20-361<br />
(383-54) 20-362<br />
   <a href="mailto:905boss@nskbl.ru ">905boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Здвинск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/969/">Дополнительный офис «Здвинский»</a></strong></big></p>
                    <p><big><strong>632951, НСО, с. Здвинск, ул. Калинина, 41</strong></big></p>
                    <p>
                        (383-63) 22-569<br />
(383-63) 22-560<br />
(383-63) 22-509<br />
   <a href="mailto:906boss@nskbl.ru ">906boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Искитим</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/964/">Дополнительный офис «Искитимский»</a></strong></big></p>
                    <p><big><strong>633210, НСО, г. Искитим, ул. Пушкина, 91</strong></big></p>
                    <p>
                        (383-43) 22-024<br />
(383-43) 22-009<br />
(383-43) 22-212<br />
   <a href="mailto:907boss@nskbl.ru ">907boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    для физических лиц:понедельник - пятница  с 8.30 до 19.00 (без перерыва); суббота с 9.00 до 17.00 (перерыв с 13.00 до 13.30); выходной: воскресенье.
для юридических лиц: понедельник - пятница  с 8.30 до 17-00; выходной: суббота, воскресенье.                </div>
            </div>

            <div class="spacer"></div>

            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/953/">Кредитно-кассовый офис «Искитимский»</a></strong></big></p>
                    <p><big><strong>630090, НСО, г. Искитим, ул. Пушкина, 28Б</strong></big></p>
                    <p>
                        (38343) 4-25-72<br />

                    </p>
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Карасук</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/970/">Дополнительный офис «Карасукский»</a></strong></big></p>
                    <p><big><strong>632865, НСО, г. Карасук, ул. Ленина, 37</strong></big></p>
                    <p>
                        (383-55) 33-050 начальник дополнительного офиса<br />
(383-55) 33-892<br />
(383-55) 33-465<br />
   <a href="mailto:908boss@nskbl.ru ">908boss@nskbl.ru </a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/15284/">Удаленное рабочее место по выдаче потребительских кредитов</a></strong></big></p>
                    <p><big><strong>г. Карасук, Пархоменко ул. , 7</strong></big></p>
                    <p>

                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    в понедельник, четверг и пятницу с 9.00 до 18.00, в субботу и воскресение с 9.00 до 16.00, выходной: вторник и среда                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Каргат</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/971/">Дополнительный офис «Каргатский»</a></strong></big></p>
                    <p><big><strong>632402, НСО, г. Каргат, ул. Советская, 158</strong></big></p>
                    <p>
                        (383-65) 21-683 начальник дополнительного офиса<br />
(383-65) 21-064<br />
   <a href="mailto:909boss@nskbl.ru ">909boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Колывань</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/972/">Дополнительный офис «Колыванский»</a></strong></big></p>
                    <p><big><strong>633160, НСО, р.п. Колывань, ул. Советская, 56/1</strong></big></p>
                    <p>
                        (383-52) 51-846 начальник дополнительного офиса<br />
(383-52) 51-628<br />
   <a href="mailto:910boss@nskbl.ru ">910boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Коченево</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/973/">Дополнительный офис «Коченевский»</a></strong></big></p>
                    <p><big><strong>632640, НСО, р. п. Коченево, ул. Саратовская, 57</strong></big></p>
                    <p>
                        (383-51) 27-177 начальник дополнительного офиса<br />
(383-51) 27-208<br />
(383-51) 24-630<br />
   <a href="mailto:911boss@nskbl.ru ">911boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Кочки</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/974/">Дополнительный офис «Кочковский»</a></strong></big></p>
                    <p><big><strong>632490, НСО, с. Кочки, ул. Советская, 24</strong></big></p>
                    <p>
                        (383-56) 22-403 начальник дополнительного офиса<br />
(383-56) 22-146<br />
   <a href="mailto:912boss@nskbl.ru ">912boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Краснозёрское</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/975/">Дополнительный офис «Краснозерский»</a></strong></big></p>
                    <p><big><strong>632902, НСО, р. п. Краснозёрское, ул. Чкалова, 8</strong></big></p>
                    <p>
                        (383-57) 41-019 начальник дополнительного офиса<br />
(383-57) 41-093<br />
   <a href="mailto:913boss@nskbl.ru">913boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/13269/">Удаленное рабочее место</a></strong></big></p>
                    <p><big><strong>р.п. Краснозерское, ул. Чкалова, 1</strong></big></p>
                    <p>

                    </p>
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Куйбышев</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/976/">Дополнительный офис «Куйбышевский»</a></strong></big></p>
                    <p><big><strong>632383, НСО, г. Куйбышев, Квартал 11, д. 20</strong></big></p>
                    <p>
                        (383-62) 23-575 начальник дополнительного офиса<br />
(383-62) 22-531<br />
(383-62) 22-738<br />
   <a href="mailto:914boss@nskbl.ru">914boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Купино</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/977/">Дополнительный офис «Купинский»</a></strong></big></p>
                    <p><big><strong>632735, НСО, г. Купино, ул. Советов, 97а</strong></big></p>
                    <p>
                        (383-58) 20-410 начальник дополнительного офиса<br />
(383-58) 20-238<br />
   <a href="mailto:915boss@nskbl.ru">915boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Кыштовка</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/978/">Дополнительный офис «Кыштовский»</a></strong></big></p>
                    <p><big><strong>632270, НСО, с. Кыштовка, ул. Садовая, 1</strong></big></p>
                    <p>
                        (383-71) 21-156 начальник дополнительного офиса<br />
(383-71) 21-587<br />
   <a href="mailto:916boss@nskbl.ru ">916boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/about/opinions/53280/">Коваленок Ирина Игоревна</a></strong></big></p>
                    <p><big><strong></strong></big></p>
                    <p>

                    </p>
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Линево</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/13982/">Удаленное рабочее место по выдаче кредитов малому бизнесу</a></strong></big></p>
                    <p><big><strong>пос. Линёво, пр. Коммунистический, 2</strong></big></p>
                    <p>

                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    понедельник-пятница с 9.00 до 18.00                </div>
            </div>


            <div class="spacer"></div>
            <h2>Маслянино</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/979/">Дополнительный офис «Маслянинский»</a></strong></big></p>
                    <p><big><strong>633564, НСО, р. п. Маслянино, ул. Партизанская, 9</strong></big></p>
                    <p>
                        (383-47) 21-265<br />
(383-47) 21-707<br />
   <a href="mailto:917boss@nskbl.ru    ">917boss@nskbl.ru    </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Мошково</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/980/">Дополнительный офис «Мошковский»</a></strong></big></p>
                    <p><big><strong>633131, НСО, р. п. Мошково, ул. Советская, 4</strong></big></p>
                    <p>
                        (383-48) 23-251 начальник дополнительного офиса<br />
(383-48) 23-252<br />
   <a href="mailto:918boss@nskbl.ru ">918boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Ордынское</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/981/">Дополнительный офис «Ордынский»</a></strong></big></p>
                    <p><big><strong>633261, НСО, р. п. Ордынское, ул. Ленина, 17</strong></big></p>
                    <p>
                        (383-59) 23-661 Начальник дополнительного офиса<br />
(383-59) 23-669<br />
   <a href="mailto:920boss@nskbl.ru ">920boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Сузун</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/933/">Дополнительный офис «Сузунский»</a></strong></big></p>
                    <p><big><strong>633623, НСО, р. п. Сузун, ул. Ленина, 58</strong></big></p>
                    <p>
                        (383-46) 22-256 начальник дополнительного офиса<br />
(383-46) 21-471<br />
(383-46) 21-352<br />
   <a href="mailto:922boss@nskbl.ru ">922boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Татарск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/982/">Дополнительный офис «Татарский»</a></strong></big></p>
                    <p><big><strong>632122, НСО, г. Татарск, ул. Ленина, 61a</strong></big></p>
                    <p>
                        (383-64) 20-729 начальник дополнительного офиса<br />
(383-64) 20-729<br />
(383-64) 23-743<br />
(383-64) 21-737 (факс)<br />
   <a href="mailto:923boss@nskbl.ru">923boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Тогучин</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/983/">Дополнительный офис «Тогучинский»</a></strong></big></p>
                    <p><big><strong>633456, НСО, г. Тогучин, ул. Лапина, 21</strong></big></p>
                    <p>
                        (383-40) 28-561 начальник дополнительного офиса<br />
(383-40) 63-027<br />
(383-40) 21-671 (факс)<br />
   <a href="mailto:924boss@nskbl.ru ">924boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Убинское</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/984/">Дополнительный офис «Убинский»</a></strong></big></p>
                    <p><big><strong>632520, НСО, с. Убинское, ул. Ленина, 21а</strong></big></p>
                    <p>
                        (383-66) 21-796 начальник дополнительного офиса<br />
(383-66) 21-857<br />
   <a href="mailto:925boss@nskbl.ru">925boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Усть-Тарка</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/985/">Дополнительный офис «Усть-Таркский»</a></strong></big></p>
                    <p><big><strong>632160, НСО, с. Усть-Тарка, ул. Дзержинского, 10</strong></big></p>
                    <p>
                        (383-72) 22-892 начальник дополнительного офиса<br />
(383-72) 22-874<br />
   <a href="mailto:926boss@nskbl.ru  ">926boss@nskbl.ru  </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Чаны</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/986/">Дополнительный офис «Чановский»</a></strong></big></p>
                    <p><big><strong>63221, НСО, р.п. Чаны, ул. Советская, 189</strong></big></p>
                    <p>
                        (383-67) 22-728 начальник дополнительного офиса<br />
(383-67) 22-729<br />
   <a href="mailto:927boss@nskbl.ru     ">927boss@nskbl.ru     </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Черепаново</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/987/">Дополнительный офис «Черепановский»</a></strong></big></p>
                    <p><big><strong>633525, НСО, г. Черепаново, ул. Партизанская, 23</strong></big></p>
                    <p>
                        (383-45) 21-206 начальник дополнительного офиса<br />
(383-45) 21-003<br />
   <a href="mailto:928boss@nskbl.ru ">928boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Чистоозёрное</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/988/">Дополнительный офис «Чистоозерный»</a></strong></big></p>
                    <p><big><strong>632721, НСО, р.п. Чистоозёрное, ул. Дзержинского, 26/1</strong></big></p>
                    <p>
                        (383-68) 97-040  начальник дополнительного офиса<br />
(383-68) 97-041<br />
   <a href="mailto:929boss@nskbl.ru ">929boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Чулым</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/989/">Дополнительный офис «Чулымский»</a></strong></big></p>
                    <p><big><strong>632551, НСО, г. Чулым, ул. Чулымская, 20</strong></big></p>
                    <p>
                        (383-50) 22-730 начальник дополнительного офиса<br />
(383-50) 21-054<br />
(383-50) 22-749 операционист по работе с физическими лицами<br />
   <a href="mailto:930boss@nskbl.ru ">930boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>"""
branches_re = re.compile("""pointsList = {(.+?)\};""", re.I | re.U | re.S)


def fix_json(text):
    text = text.replace("\n","").replace("\t","").replace("  "," ")
    text = re.sub("'(\d+)': {", r' "\1":{', text, 0,  re.I | re.U | re.S)
    text = re.sub("\s*(\w+)\s*:", r"'\1':", text, 0,  re.I | re.U | re.S)
    #text = re.sub(":\s*'(.+?)'\s*(,|})\s*", r': "\1"\2', text,0,  re.I | re.U | re.S)
    return text

def get_field(regexp, text):
    r = re.findall(regexp,text)
    if len(r)>0:
        r = r[0]
    else:
        r = ''
    return r

def get_branch_data(html=''):
    branch_name = get_field(r'class="colBox">.*?<h1>(.+?)</h1',html)
    address = get_field(r'photoArchive-inner">.*?<p>.*?<strong>(.+?)</strong',html)
    latlon = get_field(r"ll=(.+?)&",html)

    if latlon != "": 
        lat = latlon.split(",")[0]
        lon = latlon.split(",")[1]
    else:
        lat = ''
        lon = ''

    return {'lat':lat,'lon':lon, 'branch_name':branch_name , 'address': address }


# get HTML code of the page
branches = re.findall(r'class="officeBox">(.+?)</div', html, re.I|re.U|re.S)


i=0
for branch in branches:

    data = {'url': '', 'id':-1, 'lat':'','lon':'', 'city':'', 'branch_url': '', 'branch_name':'' , 'address':'', 'address2': '' }
    
    branch_data = re.findall(r'<p>.*?<big>.*?<strong>(.+?)</strong', branch)
    if len(branch_data) < 2: continue

    branch_name = get_field(r'<a.+?>(.+?)</a', branch_data[0])
    branch_url = get_field(r'<a href="(.+?)"', branch_data[0])
    address = branch_data[1]

    data = get_branch_data(scraperwiki.scrape("http://www.nskbl.ru" + branch_url ))
    i+=1
    data = {'id':i, 'lat':data['lat'], 'lon':data['lon'],  \
            'branch_url': branch_url, 'branch_name': branch_name , 'address2':data['address'], 'address':address }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")


# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
# Blank Python

#
#urls = """http://www.alfabank.ru/russia/moscow/"""
url = "http://www.nskbl.ru/offices_terminals/offices/filter_jx.php"
html ="""<h2>Новосибирск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/945/">Головной офис</a></strong></big></p>
                    <p><big><strong>Россия, 630054 г. Новосибирск, ул. Плахотного, 25/1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:root@nskbl.ru">root@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/959/">Дополнительный офис «Дзержинский»</a></strong></big></p>
                    <p><big><strong>630015, г. Новосибирск, ул. Королева, 21/1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:rem@nskbl.ru">rem@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/958/">Дополнительный офис «Заельцовский»</a></strong></big></p>
                    <p><big><strong>630082, г. Новосибирск, Дуси Ковальчук, 252</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:pirv@nsknl.ru">pirv@nsknl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/954/">Дополнительный офис «К. Маркса, 23»</a></strong></big></p>
                    <p><big><strong>630064, г. Новосибирск, пр. Карла Маркса, 23</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:maa@nskbl.ru">maa@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/957/">Дополнительный офис «Кировский»</a></strong></big></p>
                    <p><big><strong>630088, г.Новосибирск, ул. Громова, 17</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:pap@nskbl.ru">pap@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/960/">Дополнительный офис «Октябрьский»</a></strong></big></p>
                    <p><big><strong>630009, г. Новосибирск, ул. Кирова, 108</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:lta@nskbl.ru">lta@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/961/">Дополнительный офис «Площадь Труда»</a></strong></big></p>
                    <p><big><strong>630108, г. Новосибирск, площадь Труда, 1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:shvv@nskbl.ru">shvv@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/955/">Дополнительный офис «Центральный»</a></strong></big></p>
                    <p><big><strong>630099, г. Новосибирск, Орджоникидзе, 33</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:sas@nskbl.ru">sas@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/952/">Кредитно-кассовый офис «Академический»</a></strong></big></p>
                    <p><big><strong>630090, г. Новосибирск, ул. Ильича, 6</strong></big></p>
                    <p>
                        (383) 330-40-29, 330-32-20<br />

                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/946/">Кредитно-кассовый офис «Студенческий»</a></strong></big></p>
                    <p><big><strong>630092, г. Новосибирск, пр. К. Маркса, 20 (НГТУ, корпус 2, 1 этаж)</strong></big></p>
                    <p>
                        (383) 346-06-90<br />
   <a href="mailto:deskngtu@kbl.nsk.su ">deskngtu@kbl.nsk.su </a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/7600/">Дополнительный офис &quot;Калининский&quot;</a></strong></big></p>
                    <p><big><strong>630110, Новосибирск, ул. Богдана Хмельницкого, 41</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:mevl@nskbl.ru">mevl@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/8377/">Дополнительный офис «Коммунистическая,48а»</a></strong></big></p>
                    <p><big><strong>630007, г. Новосибирск, ул. Коммунистическая,48а</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:ktj@nskbl.ru">ktj@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/23955/">Дополнительный офис «Первомайский»</a></strong></big></p>
                    <p><big><strong>630037, г. Новосибирск, ул. Маяковского, 5</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:zatv@nskbl.ru">zatv@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/25821/">Кредитно-кассовый офис &quot;На Восходе&quot;</a></strong></big></p>
                    <p><big><strong>630102, г. Новосибирск, ул. Зыряновская, 53</strong></big></p>
                    <p>
                        (383) 3-600-900<br />

                    </p>
                </div>
            </div>

            <div class="spacer"></div>

            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/26084/">Центр кредитования малого бизнеса</a></strong></big></p>
                    <p><big><strong>630007, г. Новосибирск, ул. Коммунистическая,48а</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:zed@nskbl.ru">zed@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/26087/">Китайский офис</a></strong></big></p>
                    <p><big><strong>630009, г. Новосибирск, ул. Кирова, 108</strong></big></p>
                    <p>
   <a href="mailto:ten@nskbl.ru">ten@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/30298/">Дополнительный офис «Советский»</a></strong></big></p>
                    <p><big><strong>630090 г. Новосибирск, Морской проспект, 24</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:cvs@nskbl.ru">cvs@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/42727/">Дополнительный офис «Голден Парк» </a></strong></big></p>
                    <p><big><strong>630129, г. Новосибирск, ул. Курчатова, 1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:ksb@nskbl.ru">ksb@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/47969/">Кредитно-кассовый офис «На Гусинобродском шоссе»</a></strong></big></p>
                    <p><big><strong>630124, г. Новосибирск, Гусинобродское шоссе, 33/1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />

                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/50158/">Дополнительный офис «Западный»</a></strong></big></p>
                    <p><big><strong>630071, г. Новосибирск, ул. Забалуева, 51/1</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:mlb@nskbl.ru">mlb@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/66985/">Кредитно-кассовый офис «Хилокский»</a></strong></big></p>
                    <p><big><strong>630052, г. Новосибирск, ул. Хилокская, 30</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:deskhlk@nskbl.ru">deskhlk@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Кемерово</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/962/">Операционный офис «Кемеровский»</a></strong></big></p>
                    <p><big><strong>650070 Кемеровская область, г. Кемерово, проспект Молодежный, 3а</strong></big></p>
                    <p>
                        (3842) 31-45-91 начальник ОО<br />
(3842) 31-74-66<br />
   <a href="mailto:kmkev@nskbl.ru ">kmkev@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Юридические лица: понедельник — пятница с 9.00 до 17.00 (без перерыва)
Физические лица: понедельник — пятница с 9.00 до 20.00 (без перерыва), суббота с 9.00 до 17.00 (без перерыва), выходной: воскресенье
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/20955/">Операционный офис &quot;Кемеровский-2&quot;</a></strong></big></p>
                    <p><big><strong>650000 Кемеровская область, г. Кемерово, ул. Ноградская, 16</strong></big></p>
                    <p>
                        (3842) 36-49-00, 36-48-27<br />
   <a href="mailto:kmeeg@nskbl.ru ">kmeeg@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Юридические лица: понедельник — пятница с 9.00 до 17.00 (без перерыва)
Физические лица: понедельник — пятница с 9.00 до 20.00 (без перерыва), суббота с 9.00 до 17.00 (без перерыва), выходной: воскресенье                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/48020/">Операционный офис «Кемеровский-3» </a></strong></big></p>
                    <p><big><strong>650066 г. Кемерово, проспект Октябрьский, 3г</strong></big></p>
                    <p>
                        (3842) 72-17-82<br />
   <a href="mailto:kmvsn@nskbl.ru">kmvsn@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Юридические лица: понедельник — пятница с 10.00 до 17.00 (без перерыва)
Физические лица: Понедельник с 08.30 до 18.00, вторник    с 08.30 до 20.00, среда    с 08.30 до 18.00, четверг с 08.30 до 20.00, пятница с 08.30 до 18.00, суббота с 08.30 до 18.00. Выходной: воскресенье                </div>
            </div>


            <div class="spacer"></div>
            <h2>Новокузнецк</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/963/">Операционный офис «Новокузнецкий»</a></strong></big></p>
                    <p><big><strong>654080, Кемеровская область, г. Новокузнецк, ул. Кирова, 103</strong></big></p>
                    <p>
                        (3843) 76-52-40 начальник ОО<br />
(3843) 76-17-09 Отдел расчетного обслуживания (частных лиц)<br />
(3843) 76-43-80 Отдел расчетного обслуживания (юридических лиц)<br />
   <a href="mailto:nksnp@nskbl.ru">nksnp@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Юридические лица: понедельник — пятница с 9.00 до 17.00 (без перерыва), выходной: суббота и воскресенье 
Физические лица: понедельник — пятница с 9.00 до 20.00 (без перерыва), суббота с 9.00 до 17.00 (без перерыва), выходной: воскресенье                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/55192/">Кредитно-кассовый офис «Новокузнецкий–2»</a></strong></big></p>
                    <p><big><strong>654041, г. Новокузнецк, пр. Бардина, 2</strong></big></p>
                    <p>
                        (3843) 76-17-09<br />

                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Физические лица: понедельник — воскресенье с 10.00 до 20.00, перерыв с 13.00 до 14.00                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Барнаул</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/12758/">Операционный офис &quot;Барнаульский&quot;</a></strong></big></p>
                    <p><big><strong>656056 г. Барнаул, пр. Ленина, 29</strong></big></p>
                    <p>
                        (3852) 22-90-70, 22-90-71, 22-90-72<br />
   <a href="mailto:brpuv@nskbl.ru">brpuv@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 9.00 до 20.00 (без перерыва), в субботу с 9.00 до 17.00 (без перерыва)
Для юридических лиц: понедельник-пятница с 9.00 до 17.00 (без перерыва)                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/35605/">Кредитно–кассовый офис «Барнаульский-2» </a></strong></big></p>
                    <p><big><strong>656023, г. Барнаул, пр. Космонавтов, 59</strong></big></p>
                    <p>
                        (3852) 337-309<br />

                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 9.00 до 17.00 часов, выходные дни – суббота, воскресенье.                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Красноярск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/15286/">Операционный офис &quot;Красноярский&quot;</a></strong></big></p>
                    <p><big><strong>660049 г. Красноярск, Урицкого ул., 52</strong></big></p>
                    <p>
                        (391) 265-35-35, 265-35-25, 265-35-05<br />
   <a href="mailto:krshoa@nskbl.ru">krshoa@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Юридические лица: понедельник — пятница с 9.00 до 17.00 (без перерыва), выходной: суббота и воскресенье 
Физические лица: понедельник — пятница с 9.00 до 20.00 (без перерыва), суббота с 9.00 до 17.00 (без перерыва), выходной: воскресенье                </div>
            </div>


            <div class="spacer"></div>
            <h2>Томск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/32393/">Операционный офис &quot;Томский&quot;</a></strong></big></p>
                    <p><big><strong>634009 г. Томск, Совпартшкольный переулок, 13</strong></big></p>
                    <p>
                        (3822) 900-410, 512-845, 512-865<br />
   <a href="mailto:tmnta@nskbl.ru">tmnta@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    обслуживание юридических лиц: понедельник-пятница с 9.00 до 17.00, выходные дни – суббота, воскресенье;
обслуживание физических лиц: понедельник-пятница с 9.00 до 20.00, суббота с 9.00 до 17.00, выходной день – воскресенье.                </div>
            </div>


            <div class="spacer"></div>
            <h2>Обь</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/956/">Дополнительный офис в г. Обь</a></strong></big></p>
                    <p><big><strong>633103, НСО, г. Обь, ул. ЖКО Аэропорта, 24</strong></big></p>
                    <p>
                        (383) 3-600-900<br />
   <a href="mailto:kmvl@nskbl.ru">kmvl@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/948/">Кредитно-кассовый офис «Толмачево»</a></strong></big></p>
                    <p><big><strong>633103, НСО, г. Обь, ул. Аэропорта, 1</strong></big></p>
                    <p>
                        (383) 216-99-32<br />
   <a href="mailto:desktlm@nskbl.ru">desktlm@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Бердск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/949/">Дополнительный офис «Бердский»</a></strong></big></p>
                    <p><big><strong>Россия, 633009 Новосибирская область, г. Бердск ул. Рогачева, 1</strong></big></p>
                    <p>
                        (383) 258-19-57 <br />
(383) 258-19-55 Отдел расчетного обслуживания юридических лиц<br />
(383-41) 48-284 Отдел расчетного обслуживания физических лиц<br />
(383) 204-91-53  Кредитный отдел<br />
   <a href="mailto:basv@nskbl.ru">basv@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/951/">Дополнительный офис «Бердский-2» </a></strong></big></p>
                    <p><big><strong>633010, НСО, г. Бердск, ул. Максима Горького, 3</strong></big></p>
                    <p>
                        (383-41) 22-585 Начальник дополнительного офиса <br />
(383) 335-69-12<br />
   <a href="mailto:bmvv@nskbl.ru">bmvv@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/950/">Дополнительный офис «Бердский-3»</a></strong></big></p>
                    <p><big><strong>633010, НСО, г. Бердск, ул. Ленина, 69</strong></big></p>
                    <p>
                        (383-41) 29-630 Начальник дополнительного офиса<br />
(383-41) 29-640<br />
(383-41) 29-664<br />
   <a href="mailto:bslv@nskbl.ru">bslv@nskbl.ru</a> 
    
                    </p>
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Баган</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/965/">Дополнительный офис «Баганский»</a></strong></big></p>
                    <p><big><strong>632770, НСО, с. Баган, ул. М. Горького, 25а</strong></big></p>
                    <p>
                        (383-53) 22-444 начальник дополнительного офиса<br />
(383-53) 21-104<br />
(383-53) 22-451<br />
   <a href="mailto:901boss@nskbl.ru">901boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Барабинск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/1290/">Дополнительный офис «Барабинский»</a></strong></big></p>
                    <p><big><strong>632336, НСО, г. Барабинск, ул. Ульяновская, 60</strong></big></p>
                    <p>
                        (383-61) 23-167 начальник дополнительного офиса,<br />
(383-61) 25-778,<br />
(383-61) 25-526<br />
   <a href="mailto:902boss@nskbl.ru">902boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресение
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Болотное</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/966/">Дополнительный офис «Болотнинский»</a></strong></big></p>
                    <p><big><strong>633340, НСО, г. Болотное, ул. М. Горького, 33</strong></big></p>
                    <p>
                        (383-49) 25-100 начальник дополнительного офиса<br />
(383-49) 24-452<br />
(383-49) 24-453<br />
   <a href="mailto:903boss@nskbl.ru">903boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Венгерово</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/967/">Дополнительный офис «Венгеровский»</a></strong></big></p>
                    <p><big><strong>632240, НСО, с. Венгерово, ул. Ленина, 63</strong></big></p>
                    <p>
                        (383-69) 22-602 начальник дополнительного офиса<br />
(383-69) 22-603<br />
   <a href="mailto:904boss@nskbl.ru">904boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Довольное</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/968/">Дополнительный офис «Доволенский»</a></strong></big></p>
                    <p><big><strong>632450, НСО, с. Довольное, ул. Мичурина, 14а</strong></big></p>
                    <p>
                        (383-54) 20-360 начальник дополнительного офиса<br />
(383-54) 20-361<br />
(383-54) 20-362<br />
   <a href="mailto:905boss@nskbl.ru ">905boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Здвинск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/969/">Дополнительный офис «Здвинский»</a></strong></big></p>
                    <p><big><strong>632951, НСО, с. Здвинск, ул. Калинина, 41</strong></big></p>
                    <p>
                        (383-63) 22-569<br />
(383-63) 22-560<br />
(383-63) 22-509<br />
   <a href="mailto:906boss@nskbl.ru ">906boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Искитим</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/964/">Дополнительный офис «Искитимский»</a></strong></big></p>
                    <p><big><strong>633210, НСО, г. Искитим, ул. Пушкина, 91</strong></big></p>
                    <p>
                        (383-43) 22-024<br />
(383-43) 22-009<br />
(383-43) 22-212<br />
   <a href="mailto:907boss@nskbl.ru ">907boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    для физических лиц:понедельник - пятница  с 8.30 до 19.00 (без перерыва); суббота с 9.00 до 17.00 (перерыв с 13.00 до 13.30); выходной: воскресенье.
для юридических лиц: понедельник - пятница  с 8.30 до 17-00; выходной: суббота, воскресенье.                </div>
            </div>

            <div class="spacer"></div>

            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/953/">Кредитно-кассовый офис «Искитимский»</a></strong></big></p>
                    <p><big><strong>630090, НСО, г. Искитим, ул. Пушкина, 28Б</strong></big></p>
                    <p>
                        (38343) 4-25-72<br />

                    </p>
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Карасук</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/970/">Дополнительный офис «Карасукский»</a></strong></big></p>
                    <p><big><strong>632865, НСО, г. Карасук, ул. Ленина, 37</strong></big></p>
                    <p>
                        (383-55) 33-050 начальник дополнительного офиса<br />
(383-55) 33-892<br />
(383-55) 33-465<br />
   <a href="mailto:908boss@nskbl.ru ">908boss@nskbl.ru </a> 
    
                    </p>
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/15284/">Удаленное рабочее место по выдаче потребительских кредитов</a></strong></big></p>
                    <p><big><strong>г. Карасук, Пархоменко ул. , 7</strong></big></p>
                    <p>

                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    в понедельник, четверг и пятницу с 9.00 до 18.00, в субботу и воскресение с 9.00 до 16.00, выходной: вторник и среда                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Каргат</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/971/">Дополнительный офис «Каргатский»</a></strong></big></p>
                    <p><big><strong>632402, НСО, г. Каргат, ул. Советская, 158</strong></big></p>
                    <p>
                        (383-65) 21-683 начальник дополнительного офиса<br />
(383-65) 21-064<br />
   <a href="mailto:909boss@nskbl.ru ">909boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Колывань</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/972/">Дополнительный офис «Колыванский»</a></strong></big></p>
                    <p><big><strong>633160, НСО, р.п. Колывань, ул. Советская, 56/1</strong></big></p>
                    <p>
                        (383-52) 51-846 начальник дополнительного офиса<br />
(383-52) 51-628<br />
   <a href="mailto:910boss@nskbl.ru ">910boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Коченево</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/973/">Дополнительный офис «Коченевский»</a></strong></big></p>
                    <p><big><strong>632640, НСО, р. п. Коченево, ул. Саратовская, 57</strong></big></p>
                    <p>
                        (383-51) 27-177 начальник дополнительного офиса<br />
(383-51) 27-208<br />
(383-51) 24-630<br />
   <a href="mailto:911boss@nskbl.ru ">911boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Кочки</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/974/">Дополнительный офис «Кочковский»</a></strong></big></p>
                    <p><big><strong>632490, НСО, с. Кочки, ул. Советская, 24</strong></big></p>
                    <p>
                        (383-56) 22-403 начальник дополнительного офиса<br />
(383-56) 22-146<br />
   <a href="mailto:912boss@nskbl.ru ">912boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Краснозёрское</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/975/">Дополнительный офис «Краснозерский»</a></strong></big></p>
                    <p><big><strong>632902, НСО, р. п. Краснозёрское, ул. Чкалова, 8</strong></big></p>
                    <p>
                        (383-57) 41-019 начальник дополнительного офиса<br />
(383-57) 41-093<br />
   <a href="mailto:913boss@nskbl.ru">913boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/13269/">Удаленное рабочее место</a></strong></big></p>
                    <p><big><strong>р.п. Краснозерское, ул. Чкалова, 1</strong></big></p>
                    <p>

                    </p>
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Куйбышев</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/976/">Дополнительный офис «Куйбышевский»</a></strong></big></p>
                    <p><big><strong>632383, НСО, г. Куйбышев, Квартал 11, д. 20</strong></big></p>
                    <p>
                        (383-62) 23-575 начальник дополнительного офиса<br />
(383-62) 22-531<br />
(383-62) 22-738<br />
   <a href="mailto:914boss@nskbl.ru">914boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Купино</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/977/">Дополнительный офис «Купинский»</a></strong></big></p>
                    <p><big><strong>632735, НСО, г. Купино, ул. Советов, 97а</strong></big></p>
                    <p>
                        (383-58) 20-410 начальник дополнительного офиса<br />
(383-58) 20-238<br />
   <a href="mailto:915boss@nskbl.ru">915boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Кыштовка</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/978/">Дополнительный офис «Кыштовский»</a></strong></big></p>
                    <p><big><strong>632270, НСО, с. Кыштовка, ул. Садовая, 1</strong></big></p>
                    <p>
                        (383-71) 21-156 начальник дополнительного офиса<br />
(383-71) 21-587<br />
   <a href="mailto:916boss@nskbl.ru ">916boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>


            <div class="col2">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/about/opinions/53280/">Коваленок Ирина Игоревна</a></strong></big></p>
                    <p><big><strong></strong></big></p>
                    <p>

                    </p>
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Линево</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/13982/">Удаленное рабочее место по выдаче кредитов малому бизнесу</a></strong></big></p>
                    <p><big><strong>пос. Линёво, пр. Коммунистический, 2</strong></big></p>
                    <p>

                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    понедельник-пятница с 9.00 до 18.00                </div>
            </div>


            <div class="spacer"></div>
            <h2>Маслянино</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/979/">Дополнительный офис «Маслянинский»</a></strong></big></p>
                    <p><big><strong>633564, НСО, р. п. Маслянино, ул. Партизанская, 9</strong></big></p>
                    <p>
                        (383-47) 21-265<br />
(383-47) 21-707<br />
   <a href="mailto:917boss@nskbl.ru    ">917boss@nskbl.ru    </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Мошково</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/980/">Дополнительный офис «Мошковский»</a></strong></big></p>
                    <p><big><strong>633131, НСО, р. п. Мошково, ул. Советская, 4</strong></big></p>
                    <p>
                        (383-48) 23-251 начальник дополнительного офиса<br />
(383-48) 23-252<br />
   <a href="mailto:918boss@nskbl.ru ">918boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Ордынское</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/981/">Дополнительный офис «Ордынский»</a></strong></big></p>
                    <p><big><strong>633261, НСО, р. п. Ордынское, ул. Ленина, 17</strong></big></p>
                    <p>
                        (383-59) 23-661 Начальник дополнительного офиса<br />
(383-59) 23-669<br />
   <a href="mailto:920boss@nskbl.ru ">920boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Сузун</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/933/">Дополнительный офис «Сузунский»</a></strong></big></p>
                    <p><big><strong>633623, НСО, р. п. Сузун, ул. Ленина, 58</strong></big></p>
                    <p>
                        (383-46) 22-256 начальник дополнительного офиса<br />
(383-46) 21-471<br />
(383-46) 21-352<br />
   <a href="mailto:922boss@nskbl.ru ">922boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)
                </div>
            </div>


            <div class="spacer"></div>
            <h2>Татарск</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/982/">Дополнительный офис «Татарский»</a></strong></big></p>
                    <p><big><strong>632122, НСО, г. Татарск, ул. Ленина, 61a</strong></big></p>
                    <p>
                        (383-64) 20-729 начальник дополнительного офиса<br />
(383-64) 20-729<br />
(383-64) 23-743<br />
(383-64) 21-737 (факс)<br />
   <a href="mailto:923boss@nskbl.ru">923boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Тогучин</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/983/">Дополнительный офис «Тогучинский»</a></strong></big></p>
                    <p><big><strong>633456, НСО, г. Тогучин, ул. Лапина, 21</strong></big></p>
                    <p>
                        (383-40) 28-561 начальник дополнительного офиса<br />
(383-40) 63-027<br />
(383-40) 21-671 (факс)<br />
   <a href="mailto:924boss@nskbl.ru ">924boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Убинское</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/984/">Дополнительный офис «Убинский»</a></strong></big></p>
                    <p><big><strong>632520, НСО, с. Убинское, ул. Ленина, 21а</strong></big></p>
                    <p>
                        (383-66) 21-796 начальник дополнительного офиса<br />
(383-66) 21-857<br />
   <a href="mailto:925boss@nskbl.ru">925boss@nskbl.ru</a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Усть-Тарка</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/985/">Дополнительный офис «Усть-Таркский»</a></strong></big></p>
                    <p><big><strong>632160, НСО, с. Усть-Тарка, ул. Дзержинского, 10</strong></big></p>
                    <p>
                        (383-72) 22-892 начальник дополнительного офиса<br />
(383-72) 22-874<br />
   <a href="mailto:926boss@nskbl.ru  ">926boss@nskbl.ru  </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Чаны</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/986/">Дополнительный офис «Чановский»</a></strong></big></p>
                    <p><big><strong>63221, НСО, р.п. Чаны, ул. Советская, 189</strong></big></p>
                    <p>
                        (383-67) 22-728 начальник дополнительного офиса<br />
(383-67) 22-729<br />
   <a href="mailto:927boss@nskbl.ru     ">927boss@nskbl.ru     </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Черепаново</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/987/">Дополнительный офис «Черепановский»</a></strong></big></p>
                    <p><big><strong>633525, НСО, г. Черепаново, ул. Партизанская, 23</strong></big></p>
                    <p>
                        (383-45) 21-206 начальник дополнительного офиса<br />
(383-45) 21-003<br />
   <a href="mailto:928boss@nskbl.ru ">928boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 19.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>
            <h2>Чистоозёрное</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/988/">Дополнительный офис «Чистоозерный»</a></strong></big></p>
                    <p><big><strong>632721, НСО, р.п. Чистоозёрное, ул. Дзержинского, 26/1</strong></big></p>
                    <p>
                        (383-68) 97-040  начальник дополнительного офиса<br />
(383-68) 97-041<br />
   <a href="mailto:929boss@nskbl.ru ">929boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва), выходной: суббота, воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>

            <div class="spacer"></div>

            <div class="spacer"></div>
            <h2>Чулым</h2>
            <div class="col1">
                <div class="officeBox">
                    <p class="iconsBox">
                    </p>
                    <p><big><strong><a href="/offices_terminals/offices/989/">Дополнительный офис «Чулымский»</a></strong></big></p>
                    <p><big><strong>632551, НСО, г. Чулым, ул. Чулымская, 20</strong></big></p>
                    <p>
                        (383-50) 22-730 начальник дополнительного офиса<br />
(383-50) 21-054<br />
(383-50) 22-749 операционист по работе с физическими лицами<br />
   <a href="mailto:930boss@nskbl.ru ">930boss@nskbl.ru </a> 
    
                    </p>
                    <p><strong class="c-grey">Режим работы:</strong></p>
                    Для физических лиц: понедельник-пятница с 8.30 до 18.00 (без перерыва), суббота: с 8.45 до 16.30 (перерыв с 13.00 до 13.30), выходной: воскресенье
Для юридических лиц: понедельник-пятница с 8.30 до 17.00 (без перерыва)                </div>
            </div>


            <div class="spacer"></div>"""
branches_re = re.compile("""pointsList = {(.+?)\};""", re.I | re.U | re.S)


def fix_json(text):
    text = text.replace("\n","").replace("\t","").replace("  "," ")
    text = re.sub("'(\d+)': {", r' "\1":{', text, 0,  re.I | re.U | re.S)
    text = re.sub("\s*(\w+)\s*:", r"'\1':", text, 0,  re.I | re.U | re.S)
    #text = re.sub(":\s*'(.+?)'\s*(,|})\s*", r': "\1"\2', text,0,  re.I | re.U | re.S)
    return text

def get_field(regexp, text):
    r = re.findall(regexp,text)
    if len(r)>0:
        r = r[0]
    else:
        r = ''
    return r

def get_branch_data(html=''):
    branch_name = get_field(r'class="colBox">.*?<h1>(.+?)</h1',html)
    address = get_field(r'photoArchive-inner">.*?<p>.*?<strong>(.+?)</strong',html)
    latlon = get_field(r"ll=(.+?)&",html)

    if latlon != "": 
        lat = latlon.split(",")[0]
        lon = latlon.split(",")[1]
    else:
        lat = ''
        lon = ''

    return {'lat':lat,'lon':lon, 'branch_name':branch_name , 'address': address }


# get HTML code of the page
branches = re.findall(r'class="officeBox">(.+?)</div', html, re.I|re.U|re.S)


i=0
for branch in branches:

    data = {'url': '', 'id':-1, 'lat':'','lon':'', 'city':'', 'branch_url': '', 'branch_name':'' , 'address':'', 'address2': '' }
    
    branch_data = re.findall(r'<p>.*?<big>.*?<strong>(.+?)</strong', branch)
    if len(branch_data) < 2: continue

    branch_name = get_field(r'<a.+?>(.+?)</a', branch_data[0])
    branch_url = get_field(r'<a href="(.+?)"', branch_data[0])
    address = branch_data[1]

    data = get_branch_data(scraperwiki.scrape("http://www.nskbl.ru" + branch_url ))
    i+=1
    data = {'id':i, 'lat':data['lat'], 'lon':data['lon'],  \
            'branch_url': branch_url, 'branch_name': branch_name , 'address2':data['address'], 'address':address }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")


