import scraperwiki
#import lxml.html
#import re, mechanize
#from BeautifulSoup import BeautifulSoup
from scrapemark import scrape

# Blank Python

homepage = scraperwiki.scrape("http://www.chicagononprofit.org/non_profits")
#print homepage

list_scrape = scrape("""
    <div id="non_profit_list">
        {*
        <li><a href="{{[links].url}}">{{[links].title}}</a></li>
        *}
    """,
    homepage)['links']

full_list = {}

for item in list_scrape:
    target_np = scraperwiki.scrape(item['url'])
    # print item['url']
    np_data = scrape("""
        {* <div class="span-6 user_data"><h2>{{[np].org_name}}</h2>
        *}
        {* <div class="bio">
        <p>{{[np].org_desc}}</p>
        </div>
        *}
        {* <strong>Address:</strong></td>
        <td class="data">{{[np].org_address}}</td>
        *}
        {* <strong>City:</strong></td>
        <td class="data">{{[np].org_city}}Chicago</td>
        *}
        {* <strong>Zip Code:</strong></td>
        <td class="data">{{[np].org_zip}}</td>
        *}
        {* <strong>Phone:</strong></td>
        <td class="data">{{[np].org_phone}}</td>
        *}
        {* <strong>Email:</strong>
        <td><a>{{[np].org_email}}</a></td>
        *}
        {* <strong>Website:</strong></td>
        <td class="data"><a>{{[np].org_website}}</a></td>
        *}
        {* <strong>Key Contact:</strong></td>
        <td class="data"><a>{{[np].key_contact_email}}</a><br/>
        *}
        {* <strong>Volunteer Coordinator:</strong></td>
        <td class="data"><strong>{{[np].vol_coord_name}}</strong><br/>
        <a>{{[np].vol_coord_email}}</a><br/>
        *}
        {* <strong>Key Contact:</strong></td>
        <td class="data"><strong>{{[np].key_contact_name}}</strong><br/>
        <a>{{[np].key_contact_email}}</a><br/>
        {{[np].key_contact_phone}}<br/></td>
        *}
        {* <strong>Administrative Contact:</strong></td>
        <td class="data"><strong>{{[np].admin_contact_name}}</strong><br/>
        <a>{{[np].admin_contact_email}}</a><br/>
        {{[np].admin_contact_phone}}<br/></td>
        *}
        {* <strong>Executive Director:</strong></td>
        <td class="data"><strong>{{[np].exec_dir_name}}</strong><br/>
        <a>{{[np].exec_dir_email}}</a><br/>
        {{[np].exec_dir_phone}}<br/></td>
        *}
        """,
        target_np)['np']
    # print np_data[0]['org_name']
    scraperwiki.sqlite.save(unique_keys=['org_name'], data=np_data[0])


