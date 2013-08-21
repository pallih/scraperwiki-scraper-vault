import scraperwiki

# Blank Python

newbills = ['HF 2337','SF 1656','HF 8','HF 203','HF 1870']


fixedbills = []

for e in newbills:
    fixedbills.append(e[0:2]+e[3:])

newbills = []


for bill in fixedbills:
    url = "https://www.revisor.mn.gov/revisor/pages/search_status/status_detail.php?b=House&f="+bill+"&ssn=0&y=2012"
    html = scraperwiki.scrape(url)
    companionloc = html.index('Companion:')
    companionbill = html[companionloc+11:companionloc+17]
    data = {'main_bill':bill,'main_bill_url':url,'companion_bill':companionbill}
    scraperwiki.sqlite.save(unique_keys=['main_bill'], data=data)
    newbills.append([bill,companionbill])

print newbills

