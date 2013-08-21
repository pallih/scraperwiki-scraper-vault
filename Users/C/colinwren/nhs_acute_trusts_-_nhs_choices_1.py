import scraperwiki
import lxml.html
import json
import re


html = scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=nhs_acute_trusts_-_nhs_choices&query=select%20*%20from%20%60swdata%60")     
root = json.loads(html)
for site in root:
    website = site['trust-url']
    website_name = site['name']
    if website != "parser issue :(":
        try:
            trust_html_get = scraperwiki.scrape(website)
            trust_html = lxml.html.fromstring(trust_html_get)
            trust_css = trust_html.cssselect("link")
            for link in trust_css:
                try:
                    link_type = link.attrib['rel'].decode()
                    if link_type == "stylesheet":
                        link_url = link.attrib['href'].decode()
                        css_root = scraperwiki.scrape(link_url)
                        regex = re.finditer('(?P<tag>[.a-z-#_\.^{]+)\s*\{\s*(?P<styles>[^}]+)\s*}', css_root)
                        for style in regex:
                            #print style.group('tag')+' : '+style.group('styles')
                            key_val = re.finditer('(?P<key>[.a-z-^:]+)\s*:\s*(?P<value>[^;]+)\s*;',style.group('styles'))
                            for inner_style in key_val:
                                if inner_style.group('key') == 'font-size':
                                    print website_name+' use a font-size of '+inner_style.group('value')+' on their "'+style.group('tag')+'" elements'
                                    data = {
                                        'website' : website_name,
                                        'element' : style.group('tag'),
                                        'font-size' : inner_style.group('value')
                                        }
                                    scraperwiki.sqlite.save(unique_keys=['website'], data=data)
                except:
                    link_type = "no"
        except:
            print '500 error'
