import scraperwiki
import lxml.html

#html = scraperwiki.scrape("https://scraperwiki.com/")
#root = lxml.html.fromstring(html)
#for el in root.cssselect("div.tags li"):
#    print el.text_content()

html =scraperwiki.scrape("http://www.deliveryhero.com.au/sydney/the-darling/#")
root = lxml.html.fromstring(html)


for sections in root.cssselect("div.menu_row"):

    for menuGroup in sections.cssselect("div[class='section']"):

        menuGroupName = menuGroup.cssselect("h3")[0].text_content()
        print "Menu Name: ", menuGroupName

        for menuItem in menuGroup.cssselect("ul li"):

            menuItemName = menuItem.cssselect("div.name")[0].text_content()
            menuItemPrice = menuItem.cssselect("span.price")[0].text_content()
            print "- Menu Item: ", menuItemName , menuItemPrice

            descriptionElement = menuItem.cssselect("p")
            if (len(descriptionElement) > 0):
                menuItemDescription = descriptionElement[0].text_content()
                print "---- Description: ", menuItemDescription
            else:
                menuItemDescription = ""


import scraperwiki
import lxml.html

#html = scraperwiki.scrape("https://scraperwiki.com/")
#root = lxml.html.fromstring(html)
#for el in root.cssselect("div.tags li"):
#    print el.text_content()

html =scraperwiki.scrape("http://www.deliveryhero.com.au/sydney/the-darling/#")
root = lxml.html.fromstring(html)


for sections in root.cssselect("div.menu_row"):

    for menuGroup in sections.cssselect("div[class='section']"):

        menuGroupName = menuGroup.cssselect("h3")[0].text_content()
        print "Menu Name: ", menuGroupName

        for menuItem in menuGroup.cssselect("ul li"):

            menuItemName = menuItem.cssselect("div.name")[0].text_content()
            menuItemPrice = menuItem.cssselect("span.price")[0].text_content()
            print "- Menu Item: ", menuItemName , menuItemPrice

            descriptionElement = menuItem.cssselect("p")
            if (len(descriptionElement) > 0):
                menuItemDescription = descriptionElement[0].text_content()
                print "---- Description: ", menuItemDescription
            else:
                menuItemDescription = ""


