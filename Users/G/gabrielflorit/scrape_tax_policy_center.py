###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html
import scraperwiki

taxUrlA = "http://calculator2.taxpolicycenter.org/calculator_basecase.cfm?basecaseid="
taxUrlB = "&simlaw=1&simyear=2013&amtpatch=1&CALCULATE=GO"

for demographicIndex in ['1','2','3','4','5','6']:

    for incomeIndex in ['1','2','3','4','5']:

        taxUrl = taxUrlA + demographicIndex + incomeIndex + taxUrlB
        br = mechanize.Browser()
        response = br.open(taxUrl)
        br.select_form(name="MyForm")
        response = br.submit()
        html = response.read()
        root = lxml.html.fromstring(html)
        
        #html = scraperwiki.scrape("http://livecoding.io/s/4383366")
        #root = lxml.html.fromstring(html)
        
        plan = root.cssselect(".TaxCalcResults h3 a")[0].text
        demographic = root.cssselect(".TaxCalcResults h3")[0].text
        income = root.cssselect("td[title='cashinc']")[0].getparent().cssselect("td")[1].text
        currentplan = root.cssselect("td[title='deficitp']")[0].getparent().cssselect("td")[1].text
        fiscalcliff = root.cssselect("td[title='deficitp']")[0].getparent().cssselect("td")[2].text
        
        data = {
            "plan": plan,
            "demographic": demographic,
            "income": income,
            "currentplan": currentplan,
            "fiscalcliff": fiscalcliff
        }
        
        scraperwiki.sqlite.save(['demographic', 'income'], data)

