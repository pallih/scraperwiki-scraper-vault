# PLEASE READ THIS BEFORE EDITING
#
# This script generates your email alerts, to tell you when your scrapers
# are broken or someone has edited them.
#
# It works by emailing you the output of this script. If you read the code and
# know what you're doing, you can customise it, and make it send other emails
# for other purposes.

import scraperwiki
import ckanclient


ckan = ckanclient.CkanClient(base_location='https://www.govdata.de/ckan/api', api_key='')


package_list = ckan.package_register_get()
i = 0

for p in package_list:
     try:
        ckan.package_entity_get(p)
        package_entity = ckan.last_message
        print package_entity['groups']
        
        record = {}
        record['title'] = package_entity['title']
        record['cat'] = package_entity['groups']
        record['url'] = package_entity['id']  
        


        if 'bildung_wissenschaft' in package_entity['groups']:
            scraperwiki.sqlite.save(['title'], data=record)  
     except:
          print 'error'
 
