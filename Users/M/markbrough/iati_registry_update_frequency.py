import scraperwiki
import urllib2
import json
import datetime

PACKAGESEARCH_URL = "http://iatiregistry.org/api/2/search/dataset?fl=id,name,groups,title,ckan_url&limit=1000&offset=%s"
PACKAGEGROUPS_URL="http://iatiregistry.org/api/2/rest/group/"
PACKAGEGROUP_URL="http://iatiregistry.org/api/2/rest/group/%s"
PACKAGES_URL="http://iatiregistry.org/api/2/rest/package/"
PACKAGE_URL="http://iatiregistry.org/api/2/rest/package/%s"
REVISIONS_URL="http://iatiregistry.org/api/2/search/revision?since_time=%s"
REVISION_URL="http://iatiregistry.org/api/2/rest/revision/%s"

current_revisions = scraperwiki.sqlite.execute("select id from revisions")
current_packages = scraperwiki.sqlite.execute("select id from packages")
current_packagegroups = scraperwiki.sqlite.execute("select id from packagegroups")

def get_packagegroups():
    packagegroups_list_req = urllib2.Request(PACKAGEGROUPS_URL)
    packagegroups_list_webfile = urllib2.urlopen(packagegroups_list_req)
    packagegroups_list = json.loads(packagegroups_list_webfile.read())
    
    for packagegroup in packagegroups_list:
        if [packagegroup] in current_packagegroups['data']:
            continue
        packagegroup_req = urllib2.Request(PACKAGEGROUP_URL % (packagegroup))
        packagegroup_webfile = urllib2.urlopen(packagegroup_req)
        packagegroup_data = json.loads(packagegroup_webfile.read())
    
        scraperwiki.sqlite.save(unique_keys=["id"],
                data=packagegroup_data,
                table_name="packagegroups")

def get_packages():
    offset = 0
    keepgoing = True
    while keepgoing:
        packages_list_req = urllib2.Request(PACKAGESEARCH_URL % (offset))
        packages_list_webfile = urllib2.urlopen(packages_list_req)
        packages_list = json.loads(packages_list_webfile.read())
    
        
        if (("results" in packages_list) and (packages_list["results"])):
        
            for package in packages_list["results"]:
                if [package['id']] in current_packages['data']:
                    continue
                try:
                    package["packagegroup_name"] = package["groups"][0]
                except IndexError:
                    pass
                except KeyError:
                    pass
                scraperwiki.sqlite.save(unique_keys=["id"],
                        data=package,
                        table_name="packages")
            offset +=1000
        else:
            keepgoing = False
    

def get_package_id(revision_data):
    try:
        return revision_data['packages'][0]
    except KeyError:
        pass
    except IndexError:
        pass
    except TypeError:
        pass

def get_packagegroup_id(revision_data):
    try:
        return revision_data['groups'][0]
    except KeyError:
        pass
    except IndexError:
        pass
    except TypeError:
        pass

def get_revision_type(revision_message):
    try:
        data = revision_message.split(": ")
        return {"type": data[0],
                "text": data[1] }
    except Exception:
        return {"type": "",
                "text": ""}

def get_revisions():
    revisions_list_req = urllib2.Request(REVISIONS_URL % ("2010-01-01"))
    revisions_list_webfile = urllib2.urlopen(revisions_list_req)
    revisions_list = json.loads(revisions_list_webfile.read())
    
    
    for revision in revisions_list:
        if [revision] in current_revisions['data']:
            continue
        revision_req = urllib2.Request(REVISION_URL % (revision))
        revision_webfile = urllib2.urlopen(revision_req)
        revision_data = json.loads(revision_webfile.read())
        revision_message = get_revision_type(revision_data["message"])
        revision_datetime = datetime.datetime.strptime(revision_data["timestamp"], "%Y-%m-%dT%H:%M:%S.%f")
        revision_date = revision_datetime.date()
        save_revision_data = {
            'id': revision_data["id"],
            'timestamp': revision_datetime,
            'date': revision_date,
            'package_id': get_package_id(revision_data),
            'group_id': get_packagegroup_id(revision_data),
            'author': revision_data["author"],
            'message': revision_data["message"],
            'message_type': revision_message["type"],
            'messsage_text': revision_message["text"]
        }
        scraperwiki.sqlite.save(unique_keys=["id"],
                data=save_revision_data,
                table_name="revisions")

print "getting packages..."
get_packages()
print "getting packagegroups..."
get_packagegroups()
print "getting revisions..."
get_revisions()
