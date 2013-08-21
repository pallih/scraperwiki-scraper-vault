import scraperwiki
html = scraperwiki.scrape("http://www.imdb.com/search/title?genres=action&sort=moviemeter,asc&start=1'&title_type=feature")
import lxml.html           
root = lxml.html.fromstring(html)


for td in root.cssselect("td.title"):
    title = td.cssselect("a")[0].text_content()
    year= td.cssselect("span.year_type")[0].text_content()[1:-1]

    desc = td.cssselect("span.outline")
    if desc.__len__() > 0:
        descr = desc[0].text_content()
    credit = td.cssselect("span.credit a")[0].text_content()
    generes = td.cssselect("span.genre a")
    rating = td.cssselect("div[class='rating rating-list']")
    try:   
        rate =  rating[0].attrib['title'].replace(' - click stars to rate','')
    except:
        rate =  td.cssselect("div.rating-ineligible")[0].text_content()
    
    genere = []
    for g in generes:
        genere.append( g.text_content())
    data = {
        'title' :title,
        'year' : year,
        'descr':descr,
        'credit':credit,
        'genere':str(genere)[1:-1],
        'rating':rate

   }
    print data
    scraperwiki.sqlite.save(unique_keys=['title'], data=data)


## Original requirement by a client to get links of Feature Films done using sgmlLib
# import sgmllib
# class MyParser(sgmllib.SGMLParser):

    # def parse(self, s):
        # self.feed(s)
        # self.close()
        
    # def __init__(self, verbose=0):
        # sgmllib.SGMLParser.__init__(self, verbose)
        # self.hyperlinks = []
        # self.tddescriptions = []
        # self.trdescriptions = []
        # self.descriptions = []
        # self.inside_a_element = 0
        # self.inside_tr_element = 0
        # self.inside_td_element = 0
        # self.inside_div=0
        # self.counter = 0
        # self.countert = 0
        # self.inside_ul=0
        # self.inside_span=0
        
    # def get_hyperlinks(self):
        # return self.hyperlinks
    
    # def start_a(self, attributes):
        # if self.inside_td_element:
            # for name,value in attributes:
                # if name=='href' and value.__contains__('title') and self.countert:
                    # self.hyperlinks.append(value)
                    # self.inside_a_element =1
                    # self.countert = 0    
    
    # def handle_data(self, data):
        # if self.inside_a_element and self.counter:
            # self.descriptions.append(data)
            # self.counter=0

    # def end_a(self):
        # self.inside_a_element = 0

    # def get_descriptions(self):     
        # return self.descriptions
        
    # def start_td(self,attributes):
        # for name, value in attributes:
                # if name =="class" and value=="title":
                    # self.inside_td_element = 1
                    # self.counter=1
                    # self.countert = 1

    # def end_td(self):
        # self.inside_td_element = 0
    # def start_div(self,attributes):
        # for name,value in attributes:
            # if name == "class" and value == "listingName paragraph":
                # self.inside_div=1
            
    # def end_div(self):
        # self.inside_div=0

    # def start_span(self,attributes):
        # for name, value in attributes:
            # if name== 'class' and value == 'showLruLink':
                # self.inside_span =1
    # def end_span(self):
        # self.inside_span=0


        
        
# import urllib2
# for i in range(1,100):
    # url='http://www.imdb.com/search/title?genres=action&sort=moviemeter,asc&start='+str(j)+'&title_type=feature'
    # req = urllib2.Request(url,None,headers)
    # f = urllib2.urlopen(req)
    # s = f.read()
    # myparser = MyParser()
    # myparser.parse(s)
    # sd= myparser.get_descriptions()
    # for q in range(sa.__len__()):
        # print str(sd[q])+': ' + 'http://www.imdb.com'+str(sa[q])
        

    
    
    
