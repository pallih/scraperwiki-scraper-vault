import scraperwiki
import lxml.html
import lxml.etree

# example using lxml to pull out three tables

url = "http://www.unpri.org/signatories/"  

# stands for Principles of Responsible Investment
# the principles are here:  http://www.unpri.org/principles/
# signatories means we can hold the investors to account
# according to these principles

doc = lxml.html.parse(url)
root = doc.getroot()

signatorytables = root.cssselect("table.signatories")
for table in signatorytables:

    h2 = table
    while h2.tag != "h2":
        h2 = h2.getprevious()
    signatorycategory = h2.text  # Asset owners, Investment managers, Professional service partners
    signatorycategory = signatorycategory.replace(" signatories", "")

    signatoryrows = table.cssselect("tr")
    for tr in signatoryrows[1:]:
        row = tr.cssselect("td")
        assert len(row) == 3
        assert row[1].text == u'\xa0'
        tdlink = row[1].cssselect("a")

        link = tdlink and tdlink[0].get("href") or ""
        country = row[2].text
        data = { "company":row[0].text, "country":country, "link":link, "signatorycategory":signatorycategory }
        scraperwiki.datastore.save(unique_keys=["company"], data=data)



import scraperwiki
import lxml.html
import lxml.etree

# example using lxml to pull out three tables

url = "http://www.unpri.org/signatories/"  

# stands for Principles of Responsible Investment
# the principles are here:  http://www.unpri.org/principles/
# signatories means we can hold the investors to account
# according to these principles

doc = lxml.html.parse(url)
root = doc.getroot()

signatorytables = root.cssselect("table.signatories")
for table in signatorytables:

    h2 = table
    while h2.tag != "h2":
        h2 = h2.getprevious()
    signatorycategory = h2.text  # Asset owners, Investment managers, Professional service partners
    signatorycategory = signatorycategory.replace(" signatories", "")

    signatoryrows = table.cssselect("tr")
    for tr in signatoryrows[1:]:
        row = tr.cssselect("td")
        assert len(row) == 3
        assert row[1].text == u'\xa0'
        tdlink = row[1].cssselect("a")

        link = tdlink and tdlink[0].get("href") or ""
        country = row[2].text
        data = { "company":row[0].text, "country":country, "link":link, "signatorycategory":signatorycategory }
        scraperwiki.datastore.save(unique_keys=["company"], data=data)



import scraperwiki
import lxml.html
import lxml.etree

# example using lxml to pull out three tables

url = "http://www.unpri.org/signatories/"  

# stands for Principles of Responsible Investment
# the principles are here:  http://www.unpri.org/principles/
# signatories means we can hold the investors to account
# according to these principles

doc = lxml.html.parse(url)
root = doc.getroot()

signatorytables = root.cssselect("table.signatories")
for table in signatorytables:

    h2 = table
    while h2.tag != "h2":
        h2 = h2.getprevious()
    signatorycategory = h2.text  # Asset owners, Investment managers, Professional service partners
    signatorycategory = signatorycategory.replace(" signatories", "")

    signatoryrows = table.cssselect("tr")
    for tr in signatoryrows[1:]:
        row = tr.cssselect("td")
        assert len(row) == 3
        assert row[1].text == u'\xa0'
        tdlink = row[1].cssselect("a")

        link = tdlink and tdlink[0].get("href") or ""
        country = row[2].text
        data = { "company":row[0].text, "country":country, "link":link, "signatorycategory":signatorycategory }
        scraperwiki.datastore.save(unique_keys=["company"], data=data)



import scraperwiki
import lxml.html
import lxml.etree

# example using lxml to pull out three tables

url = "http://www.unpri.org/signatories/"  

# stands for Principles of Responsible Investment
# the principles are here:  http://www.unpri.org/principles/
# signatories means we can hold the investors to account
# according to these principles

doc = lxml.html.parse(url)
root = doc.getroot()

signatorytables = root.cssselect("table.signatories")
for table in signatorytables:

    h2 = table
    while h2.tag != "h2":
        h2 = h2.getprevious()
    signatorycategory = h2.text  # Asset owners, Investment managers, Professional service partners
    signatorycategory = signatorycategory.replace(" signatories", "")

    signatoryrows = table.cssselect("tr")
    for tr in signatoryrows[1:]:
        row = tr.cssselect("td")
        assert len(row) == 3
        assert row[1].text == u'\xa0'
        tdlink = row[1].cssselect("a")

        link = tdlink and tdlink[0].get("href") or ""
        country = row[2].text
        data = { "company":row[0].text, "country":country, "link":link, "signatorycategory":signatorycategory }
        scraperwiki.datastore.save(unique_keys=["company"], data=data)



import scraperwiki
import lxml.html
import lxml.etree

# example using lxml to pull out three tables

url = "http://www.unpri.org/signatories/"  

# stands for Principles of Responsible Investment
# the principles are here:  http://www.unpri.org/principles/
# signatories means we can hold the investors to account
# according to these principles

doc = lxml.html.parse(url)
root = doc.getroot()

signatorytables = root.cssselect("table.signatories")
for table in signatorytables:

    h2 = table
    while h2.tag != "h2":
        h2 = h2.getprevious()
    signatorycategory = h2.text  # Asset owners, Investment managers, Professional service partners
    signatorycategory = signatorycategory.replace(" signatories", "")

    signatoryrows = table.cssselect("tr")
    for tr in signatoryrows[1:]:
        row = tr.cssselect("td")
        assert len(row) == 3
        assert row[1].text == u'\xa0'
        tdlink = row[1].cssselect("a")

        link = tdlink and tdlink[0].get("href") or ""
        country = row[2].text
        data = { "company":row[0].text, "country":country, "link":link, "signatorycategory":signatorycategory }
        scraperwiki.datastore.save(unique_keys=["company"], data=data)



import scraperwiki
import lxml.html
import lxml.etree

# example using lxml to pull out three tables

url = "http://www.unpri.org/signatories/"  

# stands for Principles of Responsible Investment
# the principles are here:  http://www.unpri.org/principles/
# signatories means we can hold the investors to account
# according to these principles

doc = lxml.html.parse(url)
root = doc.getroot()

signatorytables = root.cssselect("table.signatories")
for table in signatorytables:

    h2 = table
    while h2.tag != "h2":
        h2 = h2.getprevious()
    signatorycategory = h2.text  # Asset owners, Investment managers, Professional service partners
    signatorycategory = signatorycategory.replace(" signatories", "")

    signatoryrows = table.cssselect("tr")
    for tr in signatoryrows[1:]:
        row = tr.cssselect("td")
        assert len(row) == 3
        assert row[1].text == u'\xa0'
        tdlink = row[1].cssselect("a")

        link = tdlink and tdlink[0].get("href") or ""
        country = row[2].text
        data = { "company":row[0].text, "country":country, "link":link, "signatorycategory":signatorycategory }
        scraperwiki.datastore.save(unique_keys=["company"], data=data)



import scraperwiki
import lxml.html
import lxml.etree

# example using lxml to pull out three tables

url = "http://www.unpri.org/signatories/"  

# stands for Principles of Responsible Investment
# the principles are here:  http://www.unpri.org/principles/
# signatories means we can hold the investors to account
# according to these principles

doc = lxml.html.parse(url)
root = doc.getroot()

signatorytables = root.cssselect("table.signatories")
for table in signatorytables:

    h2 = table
    while h2.tag != "h2":
        h2 = h2.getprevious()
    signatorycategory = h2.text  # Asset owners, Investment managers, Professional service partners
    signatorycategory = signatorycategory.replace(" signatories", "")

    signatoryrows = table.cssselect("tr")
    for tr in signatoryrows[1:]:
        row = tr.cssselect("td")
        assert len(row) == 3
        assert row[1].text == u'\xa0'
        tdlink = row[1].cssselect("a")

        link = tdlink and tdlink[0].get("href") or ""
        country = row[2].text
        data = { "company":row[0].text, "country":country, "link":link, "signatorycategory":signatorycategory }
        scraperwiki.datastore.save(unique_keys=["company"], data=data)



