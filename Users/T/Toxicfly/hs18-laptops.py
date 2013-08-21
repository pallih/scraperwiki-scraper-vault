import scraperwiki
from scrapemark import scrape


for page in range(1,3):
    html = scraperwiki.scrape("http://www.junglee.com/mn/search/junglee/ref=sr_pg_"+str(page)+"?rh=n%3A783367031%2Cn%3A%21783368031%2Cn%3A803540031%2Cp_87%3A1365979031&page="+str(page)+"&bbn=803540031&ie=UTF8&qid=1337943480")
#html= scraperwiki.scrape("http://www.junglee.com/s?rh=n%3A803540031%2Cp_87%3A1365979031&page="+str(page))\\\

print html
scrape_data = scrape("""
{* 
<div class="data">
<h3 class="title">
<a class="title" href="{{ [mobile].[link] }}">{{ [mobile].[name] }}</a>
</h3><div class="prodAds">
<span class="from">Starts at </span>
<span class="price"><span class="rupeeCurrency"></span>{{ [mobile].[price] }}</span>
</div>
*}
""", html=html);
data =[{'url':p['link'][0],'name':p['name'][0],'price':p['price'][0]} for p in scrape_data['mobile']]

scraperwiki.sqlite.save(unique_keys=["name"], data=data)

