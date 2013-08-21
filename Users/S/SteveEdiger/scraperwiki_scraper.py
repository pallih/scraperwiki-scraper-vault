import scraperwiki
import lxml.html

page_num = 1
max_page = 1
while True:
    #html = scraperwiki.scrape("https://scraperwiki.com/browse/scrapers/?page=%d" % (page_num))
    html = lxml.html.fromstring('''\
    <li class="code_object_line">
    
        <table class="code_about" cellspacing="0" cellpadding="0">
            
              <tr class="codewiki_type scraper">
                <td class="label">Type</td>
                <td class="link">scraper</td>
              </tr>
            
    
            <tr class="language python">
              <td class="label">Language</td>
              <td class="link"><a href="/scrapers/datenbank_pressemitteilungen_der_bremer_polizei/edit/" title="Edit this scraper">python</a></td>
            </tr>
            
            
            <tr class="status protected">
              <td class="label">Status</td>
              <td class="link">Protected</td>
            </tr>
            
            
                
                
            
    
            
            
        </table>
        
        <a href="/scrapers/datenbank_pressemitteilungen_der_bremer_polizei/" class="screenshot"><img src="https://media.scraperwiki.com/images/testcard_small.png" title="Screenshot not generated yet" alt="Screenshot not generated yet"/></a>
        
        <h3>
          <a class="owner" href="/profiles/suzanak/">Suzana K</a> / <a href="/scrapers/datenbank_pressemitteilungen_der_bremer_polizei/">Datenbank Pressemitteilungen der Bremer Polizei</a>
        </h3>
        
        <p class="context">
            
                58 lines of code.
            
            
                
                    3 rows of data.
                
             
        </p>
        <p class="context">
            Created 2 hours, 51 minutes ago.
        </p>
        
        <p class="description">This scraper collects the daily press releases of the police in Bremen, Germany. The descriptions of the incidents can later be used to train a classifier for information extraction, entity recognition, etc.</p>
        
        <span class="clear"></span>
        
    </li>
    ''')  

    page = lxml.html.fromstring(html) 
        
    navAnchors = page.cssselect("div.pagination a")
    max_page = int(navAnchors[len(navAnchors) - 2].text)
    for project in page.cssselect("li.code_object_line"):
        print project.text
        proj = project.cssselect("h3 a")[1]
        proj_name = proj.text
        proj_id = proj.attrib["href"].split("/")[-2]
    
        author = project.cssselect("h3 a.owner")[0].text
        code_data = project.cssselect("context")[0].text
        desc = project.find_class('description')
        status = project.cssselect("tr.status td.link")[0].text
        item_type = project.cssselect("tr.codewiki_type td.link")[0].text
        proj_lang = project.cssselect("tr.language td.link a")[0].text
        #proj_code = scraperwiki.scrape("https://scraperwiki.com/editor/raw/%s" % (proj_id))
        record = {
            "id" : proj_id,
            "name" : proj_name,
            "lang" : proj_lang,
            #"code" : proj_code,
            "author" : author,
            "status" : status,
            "code_data" : code_data,
            "desc" : desc,
            "item_type" : item_type
        }
        scraperwiki.sqlite.save(["id"], record)
    if max_page == page_num: break
    page_num += 1     