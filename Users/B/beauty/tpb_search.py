import scraperwiki
import lxml.html
import urllib

host = "http://thepiratebay.se"
base_url = "http://thepiratebay.se/search/%s/0/99/201"

list = ["meek's cutoff", "beyond the black rainbow", "sunshine", "the sound of my voice", "the untouchables", "moonrise kingdom", "cosmopolis", "holy motors", "On the Road", "Reality", "The Paperboy", "43,000 Feet", "Any Day Now", "As Luck Would Have It", "Babygirl", "Una Noche", "A Better Life", "La suerte en tus manos", "Beyond the Hill", "Caroline and Jackie", "Certain People", "Cheerful Weather for the Wedding", "Deadfall", "Death of a Superhero", "Elles", "First Winter", "The Five-Year Engagement", "The Fourth Dimension", "Freaky Deaky", "Free Samples", "Future Weather", "The Giant Mechanical Man", "Hysteria", "Jack and Diane", "Knife Fight", "Lola Versus", "Nancy, Please", "The Playroom", "Polisse", "Rat King", "Replicas", "Rubberneck", "The Russian Winter", "Sexy Baby", "Sleepless Night", "Take This Waltz", "Town of Runners", "Unit 7", "While We Were Here", "Whole Lotta Sole", "Celeste and Jesse Forever", "Red Hook Summer", "2 Days In New York", "Black Rock", "Compliance", "Detropia", "The End of Love", "Ethel", "The First Time", "Hello I Must Be Going", "Lay The Favorite", "Liberal Arts", "Luv", "Nobody Walks", "Red Lights", "Shadow Dancer", "Slavery By Another Name", "The Surrogate", "Shut Up and Play the Hits", "Something From Nothing: The Art of Rap", "That's What She Said", "Tim and Eric's Billion Dollar Movie", "Safety Not Guaranteed", "Predisposed", "Price Check", "Your Sister's Sister", "For a Good Time, Call...", "Sleepwalk With Me", "For Ellen", "John Dies At the End", "5 Broken Cameras", "Bachelorette", "Smashed", "The Words", "The Orator", "28 Hotel Rooms", "Goats", "Robot And Frank", "Wrong", "Save the Date", "V/H/S", "Keep The Lights On", "Mosquita y Mari", "My Best Day", "My Brother the Devil", "Young and Wild"]

for movie in list:
    term = urllib.quote_plus(movie)
    url = base_url % term
    print url
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for tr in root.cssselect("div#main-content tr"):
        tds = tr.cssselect("td[class!='vertTh']")
        if len(tds)==3:
            links = tds[0].cssselect("a")
            name = links[0].text
            detailsLink = host + links[0].attrib["href"]
            link = links[2].attrib["href"]
            seeders = tds[1].text
            leechers = tds[2].text
            print "%s|%s|%s|%s" % (detailsLink, seeders, leechers, link)
            try:
                scraperwiki.sqlite.save(unique_keys=["link"], data={"searchTerm": movie, "name": name, "detailsLink": detailsLink, "seeders": seeders, "leechers": leechers, "link": link,})    
            except:
                passimport scraperwiki
import lxml.html
import urllib

host = "http://thepiratebay.se"
base_url = "http://thepiratebay.se/search/%s/0/99/201"

list = ["meek's cutoff", "beyond the black rainbow", "sunshine", "the sound of my voice", "the untouchables", "moonrise kingdom", "cosmopolis", "holy motors", "On the Road", "Reality", "The Paperboy", "43,000 Feet", "Any Day Now", "As Luck Would Have It", "Babygirl", "Una Noche", "A Better Life", "La suerte en tus manos", "Beyond the Hill", "Caroline and Jackie", "Certain People", "Cheerful Weather for the Wedding", "Deadfall", "Death of a Superhero", "Elles", "First Winter", "The Five-Year Engagement", "The Fourth Dimension", "Freaky Deaky", "Free Samples", "Future Weather", "The Giant Mechanical Man", "Hysteria", "Jack and Diane", "Knife Fight", "Lola Versus", "Nancy, Please", "The Playroom", "Polisse", "Rat King", "Replicas", "Rubberneck", "The Russian Winter", "Sexy Baby", "Sleepless Night", "Take This Waltz", "Town of Runners", "Unit 7", "While We Were Here", "Whole Lotta Sole", "Celeste and Jesse Forever", "Red Hook Summer", "2 Days In New York", "Black Rock", "Compliance", "Detropia", "The End of Love", "Ethel", "The First Time", "Hello I Must Be Going", "Lay The Favorite", "Liberal Arts", "Luv", "Nobody Walks", "Red Lights", "Shadow Dancer", "Slavery By Another Name", "The Surrogate", "Shut Up and Play the Hits", "Something From Nothing: The Art of Rap", "That's What She Said", "Tim and Eric's Billion Dollar Movie", "Safety Not Guaranteed", "Predisposed", "Price Check", "Your Sister's Sister", "For a Good Time, Call...", "Sleepwalk With Me", "For Ellen", "John Dies At the End", "5 Broken Cameras", "Bachelorette", "Smashed", "The Words", "The Orator", "28 Hotel Rooms", "Goats", "Robot And Frank", "Wrong", "Save the Date", "V/H/S", "Keep The Lights On", "Mosquita y Mari", "My Best Day", "My Brother the Devil", "Young and Wild"]

for movie in list:
    term = urllib.quote_plus(movie)
    url = base_url % term
    print url
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for tr in root.cssselect("div#main-content tr"):
        tds = tr.cssselect("td[class!='vertTh']")
        if len(tds)==3:
            links = tds[0].cssselect("a")
            name = links[0].text
            detailsLink = host + links[0].attrib["href"]
            link = links[2].attrib["href"]
            seeders = tds[1].text
            leechers = tds[2].text
            print "%s|%s|%s|%s" % (detailsLink, seeders, leechers, link)
            try:
                scraperwiki.sqlite.save(unique_keys=["link"], data={"searchTerm": movie, "name": name, "detailsLink": detailsLink, "seeders": seeders, "leechers": leechers, "link": link,})    
            except:
                pass