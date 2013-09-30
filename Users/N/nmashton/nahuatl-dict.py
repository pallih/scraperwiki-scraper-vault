import scraperwiki
import lxml.html
import re

# the index of initial letters covered by the dictionary.
letters_index = scraperwiki.scrape("http://whp.uoregon.edu/dictionaries/nahuatl/index.lasso?&dowhat=ChooseLetter&spnloan=yes")
li_root = lxml.html.fromstring(letters_index)

# an array of the initial letters.
initial_letters = []
for a in li_root.cssselect("a"):
    url = a.get("href")
    if url and url.startswith("index.lasso?&dowhat=ChooseLetter&theLetter="):
        the_letter = url.split("theLetter=")[1]
        initial_letters.append(the_letter)

# an array of all the words and the IDs you can use to grab them.
words = []
for letter in initial_letters:
    let_list = scraperwiki.scrape("http://whp.uoregon.edu/dictionaries/nahuatl/index.lasso?&dowhat=ChooseLetter&theLetter=" + letter)
    let_root = lxml.html.fromstring(let_list)
    for a in let_root.cssselect("a"):
        url = a.get("href")
        if url and url.startswith("index.lasso?&dowhat=FindJustOne"):
            eq_s = url.split("=")
            id = eq_s[2].split("&")[0]
            word = eq_s[3].split(".")[0]
            words.append({"id":id,"word":word})

p = re.compile("[^a-zA-Z0-9_ \t\n\r\f\v]+")

# now let's scrape this motherfscker.
for word in words:
    datum = {}
    word_str = "&theRecID=" + word["id"] + "&theWord=" + word["word"] + "."
    word_page = scraperwiki.scrape("http://whp.uoregon.edu/dictionaries/nahuatl/index.lasso?&dowhat=FindJustOne" + word_str)
    word_root = lxml.html.fromstring(word_page)
    for tr in word_root.cssselect("tr"):
        tds = tr.cssselect("td")
        if tds and len(tds) == 2:
            spans = tds[0].cssselect("span")
            if spans:   
                row_name_raw = spans[0].text_content().strip()
                row_name = p.sub("",row_name_raw)
                row_content = tds[1].text_content().strip()
                datum[row_name] = row_content
                datum["id"] = word["id"]
    if datum:
        scraperwiki.sqlite.save(unique_keys=["id"], data=datum)import scraperwiki
import lxml.html
import re

# the index of initial letters covered by the dictionary.
letters_index = scraperwiki.scrape("http://whp.uoregon.edu/dictionaries/nahuatl/index.lasso?&dowhat=ChooseLetter&spnloan=yes")
li_root = lxml.html.fromstring(letters_index)

# an array of the initial letters.
initial_letters = []
for a in li_root.cssselect("a"):
    url = a.get("href")
    if url and url.startswith("index.lasso?&dowhat=ChooseLetter&theLetter="):
        the_letter = url.split("theLetter=")[1]
        initial_letters.append(the_letter)

# an array of all the words and the IDs you can use to grab them.
words = []
for letter in initial_letters:
    let_list = scraperwiki.scrape("http://whp.uoregon.edu/dictionaries/nahuatl/index.lasso?&dowhat=ChooseLetter&theLetter=" + letter)
    let_root = lxml.html.fromstring(let_list)
    for a in let_root.cssselect("a"):
        url = a.get("href")
        if url and url.startswith("index.lasso?&dowhat=FindJustOne"):
            eq_s = url.split("=")
            id = eq_s[2].split("&")[0]
            word = eq_s[3].split(".")[0]
            words.append({"id":id,"word":word})

p = re.compile("[^a-zA-Z0-9_ \t\n\r\f\v]+")

# now let's scrape this motherfscker.
for word in words:
    datum = {}
    word_str = "&theRecID=" + word["id"] + "&theWord=" + word["word"] + "."
    word_page = scraperwiki.scrape("http://whp.uoregon.edu/dictionaries/nahuatl/index.lasso?&dowhat=FindJustOne" + word_str)
    word_root = lxml.html.fromstring(word_page)
    for tr in word_root.cssselect("tr"):
        tds = tr.cssselect("td")
        if tds and len(tds) == 2:
            spans = tds[0].cssselect("span")
            if spans:   
                row_name_raw = spans[0].text_content().strip()
                row_name = p.sub("",row_name_raw)
                row_content = tds[1].text_content().strip()
                datum[row_name] = row_content
                datum["id"] = word["id"]
    if datum:
        scraperwiki.sqlite.save(unique_keys=["id"], data=datum)