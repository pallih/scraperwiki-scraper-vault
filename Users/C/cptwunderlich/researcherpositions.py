import scraperwiki
import lxml.html 

data = dict()
researchers = scraperwiki.scrape("http://www.euro.centre.org/people_list.php?pt_id=2&pt_name=Researchers")
resroot = lxml.html.fromstring(researchers)

# loop over names
for a in resroot.cssselect("a.index_link_list"):
    detailp = scraperwiki.scrape("http://www.euro.centre.org/" + a.attrib['href'])
    detailroot = lxml.html.fromstring(detailp)

    # in detail page
    for div in detailroot.cssselect("div#main_col"):
        posflag = False
        # look for 'position' headline
        for span in div.cssselect("span"):
            if posflag == False:
                if span.text == "Position" or span.text == "Current Position":
                    # Found position headline, next column contains position name
                    posflag = True
            else:
                # Transform name from "lastname, firstname" to "firstname lastname"
                parts = a.text.strip().encode("utf-8").replace("- Executive Director", "").split(",")
                parts.reverse()
                data['name'] = " ".join(parts)
                
                # Get position and put it in dict
                data['pos'] = span.text.strip().replace('.', '')
                # Save to DB
                scraperwiki.sqlite.save(unique_keys=["name"], data=data)
                break

import scraperwiki
import lxml.html 

data = dict()
researchers = scraperwiki.scrape("http://www.euro.centre.org/people_list.php?pt_id=2&pt_name=Researchers")
resroot = lxml.html.fromstring(researchers)

# loop over names
for a in resroot.cssselect("a.index_link_list"):
    detailp = scraperwiki.scrape("http://www.euro.centre.org/" + a.attrib['href'])
    detailroot = lxml.html.fromstring(detailp)

    # in detail page
    for div in detailroot.cssselect("div#main_col"):
        posflag = False
        # look for 'position' headline
        for span in div.cssselect("span"):
            if posflag == False:
                if span.text == "Position" or span.text == "Current Position":
                    # Found position headline, next column contains position name
                    posflag = True
            else:
                # Transform name from "lastname, firstname" to "firstname lastname"
                parts = a.text.strip().encode("utf-8").replace("- Executive Director", "").split(",")
                parts.reverse()
                data['name'] = " ".join(parts)
                
                # Get position and put it in dict
                data['pos'] = span.text.strip().replace('.', '')
                # Save to DB
                scraperwiki.sqlite.save(unique_keys=["name"], data=data)
                break

