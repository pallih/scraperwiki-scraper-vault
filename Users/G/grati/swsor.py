import scraperwiki
import mechanize

# Blank Python
#html = scraperwiki.scrape("http://www.sws.or.at/Wlist.asp",  "Miet");
#print html

br = mechanize.Browser()
br.open("http://www.sws.or.at/Wausw2.asp")
br.select_form("Auswahl2")
br.set_all_readonly(False)

br["prov"] = "0"
br["Miet"] = "700"
br["Gr"] = "1"
br["GesK"] = "0"
br["zanz"] = "1"
br["Bez"] = "5"
br["WArt"] = "1"
br["Ausw3"] = "2"
br["a15"] = "0"

response = br.submit()
print response.read()

#print br.form

#http://www.sws.or.at/Wlist.asp?self=-1&Bez=5&sBez=-1&Miet=700&Gr=1&zanz=1&GesK=0&prov=0&Ort=Alle&WArt=1&Ausw3=2&a15=0&Seite=1
#http://www.sws.or.at/Wlist.asp?self=-1&Bez=5&sBez=-1&Miet=700&Gr=1&zanz=1&GesK=0&prov=0&Ort=&WArt=1&Ausw3=&a15=0&Seite=2
