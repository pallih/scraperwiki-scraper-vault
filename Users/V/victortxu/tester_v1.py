import scraperwiki
#import urlparse
import lxml.html
import re
from BeautifulSoup import BeautifulSoup




url = "http://www.shortoftheweek.com/2012/07/06/the-chase-2/"
htmlFitxa = scraperwiki.scrape(url)
#print htmlFitxa
    
soupFitxa = BeautifulSoup(htmlFitxa)
print soupFitxa


video = soupFitxa.find('a', {'class': 'fancybox-video'})['href']
print '---> video \n', video
#data['video_url'] = video



'''
data = {}
data['url_fitxa'] = url

titol = soupFitxa.h1.contents[0]
print titol
data['title'] = titol


    
#rootFitxa = lxml.html.fromstring(htmlFitxa)
#print rootFitxa
    
    
#allTags = soupFitxa.findAll(True)
#print allTags

any = soupFitxa.right.ul.li.a.contents[0]
#print any
data['year'] = any

director = soupFitxa.right.ul('li')[1].a.contents[0]
#print director
data['director'] = director

productor = soupFitxa.right.ul('li')[2].a.contents[0]
#print productor
data['productor'] = productor        

guion = soupFitxa.right.ul('li')[3].a.contents[0]
#print guion
data['writer'] = guion 

pAny = re.compile('^Año:*')



for dades in soupFitxa.findAll('ul', id="review-tags-list"):
    print dades
    for dades_li in dades.findAll('li'):
        print dades_li, '>> dades_li'
        print dades_li.text , '>> dades_li.text'
        #print dades_li.contents[0] '>> dades_li.contents[0]'
        txtval = dades_li.text
        



        pp= txtval.split(':')
        #pp = re.sub(ur''^Año:'', ur'''''', u''Año:2012'')
        print pp[0]
        print pp[1]
        if pp[0] == 'Año':
            print "pillo Any", pp[1]
            data['year'] = pp[1] 
        elif pp[0] == 'Actor':
            print "pillo Actor", pp[1]
            data['cast'] = pp[1]
        elif pp[0] == 'País':
            print "pillo pais", pp[1]
            data['country'] = pp[1]

        #if m:
        #    print 'Match found: ', m.group()
        #else:
        #    print 'No match'



        #print txtval
        #pp = dades_li.find(text=re.compile("^Año:*"))
        #print pp

    #soup.body.p.b.string
    #for xx in dades_li.findAll('strong')
       # print xx


    


#dades_any = dades_li[0].findAll('strong', text=re.compile("Año:"))
#print dades_any


#for table in soup.findAll('table', {'class':'theclass'} ):
#    links=table.findAll('a')


#dades = soupFitxa.findAll('ul', id="review-tags-list")
#dades_li = dades[0].findAll('li')
#print dades_li
#dades_any = dades_li[0].findAll('strong', text=re.compile("Año:"))
#print dades_any
#for li in dades:
#    li = dades.






#dades = soupFitxa.find('li', text=re.compile("Año:"))
#print dades
#dades_any = dades.find('li', text=re.compile("Año:")
#print dades_any
    
#actor = soupFitxa.right.ul('li')[4].a.contents[0]
#print actor
#data['cast'] = actor 

#pais = soupFitxa.right.ul('li')[5].a.contents[0]
#print pais
#data['year'] = pais 

#plot = soupFitxa.find('p', text=re.compile("Sinopsis cortometraje:"))
#print plot
#data['plot'] = plot

#plot2 = soupFitxa.findAll('p', text=re.compile("Sinopsis cortometraje:"))
#print plot2

scraperwiki.sqlite.save(['url_fitxa'], data)
'''