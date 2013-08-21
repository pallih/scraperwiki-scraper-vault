import scraperwiki
import lxml.html           
from urlparse import urljoin


def scrape_all(page, typ):
    print "Scraping all " + typ
    
    html = scraperwiki.scrape(page)
        
    root = lxml.html.fromstring(html)
        
    project_links = root.cssselect(".views-row")

    for project in project_links:        
        module_link = project.cssselect("a")[0]
        module_name = module_link.text_content()
    
        module_url = module_link.attrib.get('href')
    
        module_model = { "url" : module_url, "name" : module_name, "link_type" : typ}
        
        scraperwiki.sqlite.save(unique_keys=["url"], table_name="drupals", data=module_model)

modules = "http://drupal.org/project/modules/index?project-status=0&drupal_core=All"
themes = "http://drupal.org/project/themes/index?project-status=0&drupal_core=All"
profiles = "http://drupal.org/project/installation%2Bprofiles/index?project-status=0&drupal_core=All"

scrape_all(modules, 'modules')
scrape_all(themes, 'themes')
scrape_all(profiles, 'profiles')