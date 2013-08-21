import scraperwiki
import lxml.html

designer_types = [ "players",
                   "rookies",
                   "prospects"]

for dtype in designer_types:
    for ii in range(1, 100):
        html = scraperwiki.scrape("http://dribbble.com/designers/{0}?page={1}".format(dtype, ii))
        root = lxml.html.fromstring(html)

        for shot in root.cssselect("div.dribbble-shot"):
            vcard = shot.cssselect(".vcard a")
            followers = shot.cssselect("li.stat-followers")
            shots = shot.cssselect("li.stat-shots")
            tags = shot.cssselect("span.skills .skill")
            prev = shot.getprevious()

            link = "http://dribbble.com{0}/click".format(vcard[0].attrib['href'])
            full_name = vcard[0].text_content()
            location = "-"

            try:
                location = vcard[1].text
            except IndexError:
                pass
        
            try:
                followers = followers[0].text_content()
            except IndexError:
                followers = 0

            try:
                shots = shots[0].text_content()
            except:
                shots = 0

            availability = "taken"
            if prev:
                if prev.tag == 'span' and prev.attrib['class'] == "freeagent-mark":
                    availability = "free"
            skills = ""
            for tag in tags:
                skills = skills + tag.text + ", "

            data = {
                'full_name': full_name,
                'location': location,
                'followers': followers,
                'shots': shots,
                'availability': availability,
                'type': dtype,
                'link': link,
                'skills': skills
            }
            scraperwiki.sqlite.save(unique_keys=["full_name"], data=data)
