import urllib
import csv

# fill in the input file here
url = "http://www.espnstar.com/motorsport/f1/teams/"

fin = urllib.urlopen(url)
lines = fin.readlines()
for line in lines:
    print line

clist = list(csv.reader(lines))

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist[:10]:
    print dict(zip(headers, row))


def formula1():
    import scraperwiki
    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"Red Bull","Races":"107", "Wins":"15","Champion Ships":"1","Drivers":"S.Vettel,M.Webber"}) 

    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"McLaren","Races":"684", "Wins":"169","Champion Ships":"8","Drivers":"L.Hamilton,J.Button"})

    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"Ferrari","Races":"812", "Wins":"215","Champion Ships":"16","Drivers":"F.Alonso,F.Massa"})
    
    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"Mercedes GP","Races":"19", "Wins":"0","Champion Ships":"0","Drivers":"M.Schumacher,N.Rosberg"})
    
    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"Renault","Races":"281", "Wins":"35","Champion Ships":"2","Drivers":"R.Kubica,V.Petrov"})

    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"Williams","Races":"553", "Wins":"113","Champion Ships":"9","Drivers":"R.Barrichello,P.Maldonado"})

    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"Force India","Races":"54", "Wins":"0","Champion Ships":"0","Drivers":""})

    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"Sauber","Races":"234", "Wins":"0","Champion Ships":"0","Drivers":"K.Kobayashi,S.Perez"})

    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"Toro Rosso","Races":"89", "Wins":"1","Champion Ships":"0","Drivers":"S.Buemi,J.Alguersuari"})

    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"HRT F1","Races":"19", "Wins":"0","Champion Ships":"0","Drivers":"N.Karthikeyan"})

    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"Virgin Racing","Races":"19", "Wins":"0","Champion Ships":"0","Drivers":"T.Glock,J.d'Ambrosio"})

    scraperwiki.datastore.save(unique_keys=["Team"], data={"Team":"Team Lotus","Races":"19", "Wins":"0","Champion Ships":"0","Drivers":"J.Trulli,H.Kovalainen"})
formula1()


