import scraperwiki

#############################################################################################
# this executes an import from the code at http://scraperwiki.com/scrapers/ckanclient/edit/
# In the future there may be a slick way to overload __import__, but this does the job for now
ckanclient = scraperwiki.utils.swimport('ckanclient')

base_location = "http://catalogue.data.gov.uk/api/2"

ckan = ckanclient.CkanClient(base_location=base_location)
package_list = ckan.package_register_get()
stats = [0, 0]
for pkg_id in package_list:
    res = ckan.package_entity_get(pkg_id)
    if ckan.last_status == 200:
        pkg = res
        # tidy fields for nicer display
        for extra_field, value in pkg.get('extras', {}).items():
            pkg[extra_field] = value
        del pkg['extras']
        pkg['tags'] = ' '.join(pkg['tags'])
        scraperwiki.datastore.save(unique_keys=['id'], data=pkg)
        stats[0] += 1
    else:
        print "Error with getting package %s: %r" % (pkg_id, res)
        stats[1] += 1
print "Finished with:\n%i packages got successfully\n%i packages with errors" % tuple(stats)
import scraperwiki

#############################################################################################
# this executes an import from the code at http://scraperwiki.com/scrapers/ckanclient/edit/
# In the future there may be a slick way to overload __import__, but this does the job for now
ckanclient = scraperwiki.utils.swimport('ckanclient')

base_location = "http://catalogue.data.gov.uk/api/2"

ckan = ckanclient.CkanClient(base_location=base_location)
package_list = ckan.package_register_get()
stats = [0, 0]
for pkg_id in package_list:
    res = ckan.package_entity_get(pkg_id)
    if ckan.last_status == 200:
        pkg = res
        # tidy fields for nicer display
        for extra_field, value in pkg.get('extras', {}).items():
            pkg[extra_field] = value
        del pkg['extras']
        pkg['tags'] = ' '.join(pkg['tags'])
        scraperwiki.datastore.save(unique_keys=['id'], data=pkg)
        stats[0] += 1
    else:
        print "Error with getting package %s: %r" % (pkg_id, res)
        stats[1] += 1
print "Finished with:\n%i packages got successfully\n%i packages with errors" % tuple(stats)
import scraperwiki

#############################################################################################
# this executes an import from the code at http://scraperwiki.com/scrapers/ckanclient/edit/
# In the future there may be a slick way to overload __import__, but this does the job for now
ckanclient = scraperwiki.utils.swimport('ckanclient')

base_location = "http://catalogue.data.gov.uk/api/2"

ckan = ckanclient.CkanClient(base_location=base_location)
package_list = ckan.package_register_get()
stats = [0, 0]
for pkg_id in package_list:
    res = ckan.package_entity_get(pkg_id)
    if ckan.last_status == 200:
        pkg = res
        # tidy fields for nicer display
        for extra_field, value in pkg.get('extras', {}).items():
            pkg[extra_field] = value
        del pkg['extras']
        pkg['tags'] = ' '.join(pkg['tags'])
        scraperwiki.datastore.save(unique_keys=['id'], data=pkg)
        stats[0] += 1
    else:
        print "Error with getting package %s: %r" % (pkg_id, res)
        stats[1] += 1
print "Finished with:\n%i packages got successfully\n%i packages with errors" % tuple(stats)
