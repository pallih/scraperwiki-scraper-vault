
print 'hello world'
from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring, tostring

COLNAMES=[
    'employer', 


url='http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'

labor=scrape(url)
print labor
banana=fromstring(labor)
print banana

print tostring(banana)
tea=banana.cssselect('table')
#for t in tea:
 #   print tostring(t)

you = tea[2]
print you
marcus=you.cssselect('tr')
for jay in marcus:
    tractor = jay.cssselect('tr')
    aidan = [apple.text_content() for apple in tractor]
    data=dict(zip(COLNAMES,aidan))
    save([],data)


