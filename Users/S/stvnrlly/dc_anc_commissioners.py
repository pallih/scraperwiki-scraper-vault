import scraperwiki
import lxml.html

scraperwiki.sqlite.execute("create table if not exists `swdata` (`SMD` text, `First Name` text, `Nickname` text, `Middle Name` text, `Last Name` text, `Suffix` text, `Address` text, `Zip` text, `Phone` text, `Email` text)")
ANC = ["1A", "1B", "1C", "1D", "2A", "2B", "2C", "2D", "2E", "2F", "3B", "3C", "3D", "3E", "3F", "3G", "4A", "4B", "4C", "4D", "5A", "5B", "5C", "5D", "5E", "6A", "6B", "6C", "6D", "6E", "7B", "7C", "7D", "7E", "7F", "8A", "8B", "8C", "8D", "8E"]
for anc in ANC:
    url = "http://www.dcboee.org/candidate_info/anc/anc_list.asp?smd=" + anc
    html = scraperwiki.scrape(url)           
    root = lxml.html.fromstring(html)
    trs = root.cssselect("div#main_content tr")
    for tr in trs[1:]:
        td = tr.cssselect("td")
        records = {}
        records["SMD"] = td[0].text_content().rstrip("\r\n")
        def name_split(name):   #Separates name into proper fields
            records["First Name"] = name[0]
            if name[len(name) - 1] in ["Jr", "Jr.", "Sr.", "Sr", "I", "II", "III"]:
                records["Suffix"] = name[len(name) - 1]
                records["Last Name"] = name[len(name) - 2]
            else:
                records["Suffix"] = ""
                records["Last Name"] = name[len(name) - 1]
            for word in name[1:len(name) - 1]:    #Nickname or Middle Name?
                if word[0] == '"' or word[0] == "(":
                    records["Nickname"] = word
                else: 
                    if word != records["Last Name"]:
                        records["Middle Name"] = word
            if records["Suffix"] in ["Jr", "Sr"]:
                records["Suffix"] += "."
            if (records["Suffix"] in ["Jr.", "Sr.", "I", "II", "III"]) & (records["Last Name"][len(records["Last Name"]) - 1] != ","):
                records["Last Name"] += ","
        name_split(td[1].text_content().split())
        records["Address"] = td[2].text_content().rstrip("\r\n")
        records["Zip"] = td[3].text_content()
        def area_coder(phone):    #Adds (202) area code, if necessary
            if len(phone) == 8:
                records["Phone"] = "202-" + phone
            else:
                records["Phone"] = phone
        area_coder(td[4].text_content())
        records["Email"] = td[5].text_content()
        scraperwiki.sqlite.save(["SMD"], records)