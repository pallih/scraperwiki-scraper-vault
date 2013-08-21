import scraperwiki

# testing
# Blank Python

import lxml.html

#parse url

scraperwiki.sqlite.execute("drop table if exists swdata")

years = ['2009','2010','2011','2012']

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']

recno = 0

for year in years:
    print year

    for month in months:
        print month
        #recno = recno + 1
        print recno

        baseurl = "http://www.sharetips365.co.uk/"
        url = baseurl + year + '/' + month 
        print url

        root = lxml.html.parse(url).getroot()
        #print root

        #some basic manipulations
        docstr = lxml.html.tostring(root)
        #print docstr
        docxml = lxml.html.document_fromstring(docstr)
        #print docxml


        div = root.xpath( '//div[@id="main"]' )

            
        fulldate = root.xpath('//div[@id="main"]/descendant::h2')
        newspaper = root.xpath('//div[@id="main"]/descendant::h2/following-sibling::h4')
        tips = root.xpath('//div[@id="main"]/descendant::h2/following-sibling::p')
        indtips = root.xpath('//div[@id="main"]/descendant::h2/following-sibling::p/descendant::br')

        #for tip in tips:
        #    print tip.text_content()
        #    #print tip.xpath('br[1]::node').text_content()


        for tip in tips:
            for node in tip.xpath('node()'):
                if getattr(node, 'tag', None) <> 'br':    
                    #print node,tip.xpath('./ancestor::h4')
                    #print node,",",tip.getprevious().text_content(),",",tip.getprevious().getprevious().text_content()
                    if tip.getprevious().getprevious().text_content().find(year) <> -1:
                        recno = recno + 1
                        #print node,",",tip.getprevious().text_content(),",",tip.getprevious().getprevious().text_content()
                        #print ""
                        scraperwiki.sqlite.save(unique_keys=['recno'], data={"recno":recno,"tip":node, "paper":tip.getprevious().text_content(), "period":tip.getprevious().getprevious().text_content()})



# working
#for tip in tips:
#    for node in tip.xpath('node()'):
#        if getattr(node, 'tag', None) == 'br':
#            print 'br'
#        else:
#            #print node,tip.xpath('./ancestor::h4')
#           print node,",",tip.getprevious().text_content(),",",tip.getprevious().getprevious().text_content()

#parent = node.getparent()
#        if parent is not None:
#            links[id(node)] = id(parent)


#if el.text<>"None": 
#    scraperwiki.sqlite.save(unique_keys=["a"], data={"a":el.text, "bbb":el.text})

      
