import scraperwiki
from scrapemark import scrape
import scraperwiki

for page in range(1,10):
  URL = "http://technorati.com/blogs/directory/overall/page-"+str(page)
  
  print URL
  html = scraperwiki.scrape(URL)
  scrape_data = scrape("""
   {*
 <td class="site-details">
 <h3>
 <a href="{{ [mobile].[link] }}">{{ [mobile].[name] }}</a>
 </h3>

   *}
   """, html=html);

  data = [{'URL':p['link'][0], 'Title':p['name'][0]} for p in scrape_data['mobile']]

  scraperwiki.sqlite.save(unique_keys=["URL"], data=data)
