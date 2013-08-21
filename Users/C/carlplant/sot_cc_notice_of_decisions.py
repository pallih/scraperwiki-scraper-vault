import scraperwiki
import urlparse
import lxml.html
import re

url = "http://www.moderngov.stoke.gov.uk/mgListPlans.aspx?RPId=564&RD=0"
record ={}
def scrape_page(link):
    html3 = scraperwiki.scrape(link)
    root3 = lxml.html.fromstring(html3)
    info = root3.cssselect("div.mgFieldGroup")
    print info
    for rows in info:
        
        table_cell2 = rows.cssselect('p')
        print table_cell2[5].text_content()
        if table_cell2:
            
            leadMeme = table_cell2[4].text_content()
            cell_splitlm = re.split('\Councillor ',leadMeme)
            dectype = table_cell2[0].text_content()
            cell_splitdt = re.split('\Decision type: ',dectype)
            wardaffect = table_cell2[2].text_content()
            #print wardaffect
            cell_splitwa = re.split('\: ',wardaffect)
            #print cell_splitwa[1]
            decstatus = table_cell2[1].text_content()
            cell_splitds = re.split('\Decision status: ',decstatus)
            #print decstatus
            decdue = table_cell2[4].text_content()
            cell_splitdd = re.split('\Decision due: ',decdue)
            #print decstatus
            dept = table_cell2[4].text_content()
            cell_splitdept = re.split('\Department: ',dept)
            contact = table_cell2[8].text_content()
            cell_splitcon = re.split(',',contact)
            docsc = table_cell2[6].text_content()
            cell_splitdocsc = re.split('\:',docsc)
            planrefer = table_cell2[5].text_content()
            cell_splitplan = re.split(' ',planrefer)
            
            record['DecisionType']= cell_splitdt[1]
            record['WardsAffected']= cell_splitwa[1]
            record['DecisionStatus']= cell_splitds[1]
            record['DecisionDue']= cell_splitdd[1]
            record['Contact']= cell_splitcon[0]
            record['docsConsidered']= cell_splitdocsc[1]
            record['planRef']= cell_splitplan[3]
            print cell_splitplan[3]
        

            ''' PlanRefer = rows.cssselect('br')
            if PlanRefer:
            text = PlanRefer[0].tail
            cell_splittext = re.split('\:',text)
            record['planRef']= cell_splittext[1]'''
        

            scraperwiki.sqlite.save(unique_keys=['planRef'], data=record)           

def mainLists(mainPage):
    #icPage = 'http://www.ic.nhs.uk/'
    html2 = scraperwiki.scrape(mainPage)
    root2 = lxml.html.fromstring(html2)
    cellLink = root2.cssselect("table#mgTable1")
    #print cellLink
    for cells in cellLink:
        
        table_cell = cells.cssselect('tr td p a')
        if table_cell:
            record['Title']= table_cell[0].text_content()
            print table_cell[0].text_content()
            link = urlparse.urljoin(webPage, table_cell[0].attrib.get('href'))
            #print link
            scrape_page(link)
             
            

webPage = 'http://www.moderngov.stoke.gov.uk'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
mainlink = root.cssselect("li.mgTableEvenRow a")
mainPage = urlparse.urljoin(webPage, mainlink[0].attrib.get('href'))
#print mainPage
mainLists(mainPage)


