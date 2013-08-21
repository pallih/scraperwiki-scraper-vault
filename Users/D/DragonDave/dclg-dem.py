import scraperwiki
import requests
# Blank Python

baseurl='http://www.communities.gov.uk/corporate/publications/consultations/'
r=requests.get(baseurl)
headers={'Cookie':r.headers['Set-Cookie']}
#exit()

url='http://www.communities.gov.uk/corporate/publications/consultations/?doPaging=true&resultsPerPage=20&sortBy=publicationDate&currentPageNumber=5'
#headers={'Cookie':'__utmz=247696897.1345451021.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); JSESSIONID=J79xQ09GzGWjLr2LBP3LNGZwLyJXBV9Y0mtdxlzkGhgCMwFRRSCy!-464166355; __utma=247696897.317724708.1345451021.1345451021.1345633538.2; __utmc=247696897; __utmb=247696897'} # screw you, cookies! bet this'll break!

#headers=dict([[h.partition(':')[0], h.partition(':')[2]] for h in rawheaders.split('\n')])
print headers
r=requests.get(url,headers=headers)
html= r.content
print html
assert 'Best Value' in html
