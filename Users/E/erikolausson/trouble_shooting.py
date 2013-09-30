import scraperwiki
import lxml
from mechanize import Browser

br = Browser()

for count in range(10):
    data ={'Nr' : count}
    scraperwiki.sqllite.save(unique_keys="Nr", data=data)


#br.open("http://www.allabolag.se")

#br.select_form(name="f_search")

#br.set_handle_robots(False)

#br.open("https://sokarende.bolagsverket.se/mia/")

#br.select_form(name="arende-sok-form")
#f = open("bolag.txt", "w")

#br.open("http://www.allabolag.se")

#br.select_form(nr=0)

#br.open("http://www.proff.se")
#br.select_form(name="input")
#br["q"]="556458-0578"
#response = br.submit()
#print response

#print br
import scraperwiki
import lxml
from mechanize import Browser

br = Browser()

for count in range(10):
    data ={'Nr' : count}
    scraperwiki.sqllite.save(unique_keys="Nr", data=data)


#br.open("http://www.allabolag.se")

#br.select_form(name="f_search")

#br.set_handle_robots(False)

#br.open("https://sokarende.bolagsverket.se/mia/")

#br.select_form(name="arende-sok-form")
#f = open("bolag.txt", "w")

#br.open("http://www.allabolag.se")

#br.select_form(nr=0)

#br.open("http://www.proff.se")
#br.select_form(name="input")
#br["q"]="556458-0578"
#response = br.submit()
#print response

#print br
