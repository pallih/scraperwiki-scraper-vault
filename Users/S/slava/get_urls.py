import scraperwiki
import re

text = """<tr valign="top"><td><ul class="nobullets city-list"><li><a href="/samara/russia/arhangelsk/">Архангельск</a>
            &nbsp;<span class="atm-count">2</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/astrakhan/">Астрахань</a>
            &nbsp;<span class="atm-count">1</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/barnaul/">Барнаул</a>
            &nbsp;<span class="atm-count">8</span><ul class="nobullets"><li><a href="/samara/russia/biysk/">Бийск</a>
            &nbsp;<span class="atm-count">1</span></li></ul></li><li><a href="/samara/russia/belgorod/">Белгород</a>
            &nbsp;<span class="atm-count">2</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/vladivostok/">Владивосток</a>
            &nbsp;<span class="atm-count">5</span><ul class="nobullets"><li><a href="/samara/russia/nakhodka/">Находка</a>
            &nbsp;<span class="atm-count">1</span></li></ul></li><li><a href="/samara/russia/vladimir/">Владимир</a>
            &nbsp;<span class="atm-count">1</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/volgograd/">Волгоград</a>
            &nbsp;<span class="atm-count">7</span><ul class="nobullets"><li><a href="/samara/russia/volzhsky/">Волжский</a>
            &nbsp;<span class="atm-count">2</span></li></ul></li><li><a href="/samara/russia/vologda/">Вологда</a>
            &nbsp;<span class="atm-count">1</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/voronezh/">Воронеж</a>
            &nbsp;<span class="atm-count">3</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/ekaterinburg/">Екатеринбург</a>
            &nbsp;<span class="atm-count">19</span><ul class="nobullets"><li><a href="/samara/russia/kamensk-uralsky/">Каменск-Уральский</a>
            &nbsp;<span class="atm-count">4</span></li><li><a href="/samara/russia/nizhny_tagil/">Нижний Тагил</a>
            &nbsp;<span class="atm-count">5</span></li><li><a href="/samara/russia/pervouralsk/">Первоуральск</a>
            &nbsp;<span class="atm-count">2</span></li></ul></li><li><a href="/samara/russia/ivanovo/">Иваново</a>
            &nbsp;<span class="atm-count">1</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/izhevsk/">Ижевск</a>
            &nbsp;<span class="atm-count">5</span><ul class="nobullets"><li><a href="/samara/russia/glazov/">Глазов</a>
            &nbsp;<span class="atm-count">1</span></li></ul></li><li><a href="/samara/russia/irkutsk/">Иркутск</a>
            &nbsp;<span class="atm-count">6</span><ul class="nobullets"><li><a href="/samara/russia/angarsk/">Ангарск</a>
            &nbsp;<span class="atm-count">2</span></li><li><a href="/samara/russia/usolye-sibirskoe/">Усолье-Сибирское</a>
            &nbsp;<span class="atm-count">1</span></li></ul></li><li><a href="/samara/russia/kazan/">Казань</a>
            &nbsp;<span class="atm-count">8</span><ul class="nobullets"><li><a href="/samara/russia/almetyevsk/">Альметьевск</a>
            &nbsp;<span class="atm-count">1</span></li><li><a href="/samara/russia/nabchelny/">Набережные Челны</a>
            &nbsp;<span class="atm-count">2</span></li></ul></li><li><a href="/samara/russia/kaliningrad/">Калининград</a>
            &nbsp;<span class="atm-count">5</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/kaluga/">Калуга</a>
            &nbsp;<span class="atm-count">1</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/kemerovo/">Кемерово</a>
            &nbsp;<span class="atm-count">4</span><ul class="nobullets"><li><a href="/samara/russia/novokuznetsk/">Новокузнецк</a>
            &nbsp;<span class="atm-count">4</span></li><li><a href="/samara/russia/yurga/">Юрга</a>
            &nbsp;<span class="atm-count">1</span></li></ul></li></ul></td><td><ul class="nobullets city-list"><li><a href="/samara/russia/krasnodar/">Краснодар</a>
            &nbsp;<span class="atm-count">6</span><ul class="nobullets"><li><a href="/samara/russia/novorossiisk/">Новороссийск</a>
            &nbsp;<span class="atm-count">1</span></li><li><a href="/samara/russia/sochi/">Сочи</a>
            &nbsp;<span class="atm-count">2</span></li><li><a href="/samara/russia/tuapse/">Туапсе</a>
            &nbsp;<span class="atm-count">1</span></li></ul></li><li><a href="/samara/russia/krasnoyarsk/">Красноярск</a>
            &nbsp;<span class="atm-count">9</span><ul class="nobullets"><li><a href="/samara/russia/abakan/">Абакан</a>
            &nbsp;<span class="atm-count">1</span></li><li><a href="/samara/russia/zheleznogorsk/">Железногорск</a>
            &nbsp;<span class="atm-count">2</span></li></ul></li><li><a href="/samara/russia/kurgan/">Курган</a>
            &nbsp;<span class="atm-count">2</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/kursk/">Курск</a>
            &nbsp;<span class="atm-count">1</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/lipetsk/">Липецк</a>
            &nbsp;<span class="atm-count">6</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/moscow/">Москва</a>
            &nbsp;<span class="atm-count">74</span><ul class="nobullets"><li><a href="/samara/russia/balashiha/">Балашиха</a>
            &nbsp;<span class="atm-count">2</span></li><li><a href="/samara/russia/korolev/">Королев</a>
            &nbsp;<span class="atm-count">2</span></li><li><a href="/samara/russia/odintsovo/">Одинцово</a>
            &nbsp;<span class="atm-count">2</span></li><li><a href="/samara/russia/khimki/">Химки</a>
            &nbsp;<span class="atm-count">2</span></li></ul></li><li><a href="/samara/russia/murmansk/">Мурманск</a>
            &nbsp;<span class="atm-count">5</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/nizhnevartovsk/">Нижневартовск</a>
            &nbsp;<span class="atm-count">3</span><ul class="nobullets"><li><a href="/samara/russia/megion/">Мегион</a>
            &nbsp;<span class="atm-count">2</span></li><li><a href="/samara/russia/raduzhniy/">Радужный</a>
            &nbsp;<span class="atm-count">1</span></li><li><a href="/samara/russia/surgut/">Сургут</a>
            &nbsp;<span class="atm-count">3</span></li></ul></li><li><a href="/samara/russia/nizhninovgorod/">Нижний Новгород</a>
            &nbsp;<span class="atm-count">10</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/novosibirsk/">Новосибирск</a>
            &nbsp;<span class="atm-count">17</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/omsk/">Омск</a>
            &nbsp;<span class="atm-count">9</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/orenburg/">Оренбург</a>
            &nbsp;<span class="atm-count">3</span><ul class="nobullets"><li><a href="/samara/russia/buzuluk/">Бузулук</a>
            &nbsp;<span class="atm-count">2</span></li><li><a href="/samara/russia/novotroitsk/">Новотроицк</a>
            &nbsp;<span class="atm-count">2</span></li><li><a href="/samara/russia/orsk/">Орск</a>
            &nbsp;<span class="atm-count">2</span></li></ul></li><li><a href="/samara/russia/penza/">Пенза</a>
            &nbsp;<span class="atm-count">1</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/perm/">Пермь</a>
            &nbsp;<span class="atm-count">8</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/rostov/">Ростов-на-Дону</a>
            &nbsp;<span class="atm-count">11</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/ryazan/">Рязань</a>
            &nbsp;<span class="atm-count">1</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/samara/">Самара</a>
            &nbsp;<span class="atm-count">6</span><ul class="nobullets"><li><a href="/samara/russia/tolyatti/">Тольятти</a>
            &nbsp;<span class="atm-count">2</span></li></ul></li></ul></td><td><ul class="nobullets city-list"><li><a href="/samara/russia/peterburg/">Санкт-Петербург</a>
            &nbsp;<span class="atm-count">30</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/saratov/">Саратов</a>
            &nbsp;<span class="atm-count">3</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/stavropol/">Ставрополь</a>
            &nbsp;<span class="atm-count">3</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/syktyvkar/">Сыктывкар</a>
            &nbsp;<span class="atm-count">2</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/tambov/">Тамбов</a>
            &nbsp;<span class="atm-count">1</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/tomsk/">Томск</a>
            &nbsp;<span class="atm-count">4</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/tula/">Тула</a>
            &nbsp;<span class="atm-count">3</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/tyumen/">Тюмень</a>
            &nbsp;<span class="atm-count">9</span><ul class="nobullets"><li><a href="/samara/russia/new_urengoy/">Новый Уренгой</a>
            &nbsp;<span class="atm-count">1</span></li></ul></li><li><a href="/samara/russia/ulyanovsk/">Ульяновск</a>
            &nbsp;<span class="atm-count">1</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/ufa/">Уфа</a>
            &nbsp;<span class="atm-count">12</span><ul class="nobullets"><li><a href="/samara/russia/sterlitamak/">Стерлитамак</a>
            &nbsp;<span class="atm-count">1</span></li></ul></li><li><a href="/samara/russia/khabarovsk/">Хабаровск</a>
            &nbsp;<span class="atm-count">3</span><ul class="nobullets"><li><a href="/samara/russia/komsomolsk_na_amure/">Комсомольск-на-Амуре</a>
            &nbsp;<span class="atm-count">1</span></li><li><a href="/samara/russia/yakutsk/">Якутск</a>
            &nbsp;<span class="atm-count">1</span></li></ul></li><li><a href="/samara/russia/cheboksary/">Чебоксары</a>
            &nbsp;<span class="atm-count">2</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/chelyabinsk/">Челябинск</a>
            &nbsp;<span class="atm-count">17</span><ul class="nobullets"><li><a href="/samara/russia/magnitogorsk/">Магнитогорск</a>
            &nbsp;<span class="atm-count">3</span></li></ul></li><li><a href="/samara/russia/yuzhnosakhalinsk/">Южно-Сахалинск</a>
            &nbsp;<span class="atm-count">2</span><ul class="nobullets"></ul></li><li><a href="/samara/russia/yaroslavl/">Ярославль</a>
            &nbsp;<span class="atm-count">2</span><ul class="nobullets"></ul></li></ul></td></tr>"""
# Blank Python

out = re.findall(r'href="(.+?)"',text, re.I | re.U | re.S)
print out

