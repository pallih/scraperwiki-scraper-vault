# Doctors in Ireland - from medicalcouncil.ie
import lxml.html
import scraperwiki

#Iterate over all possible MCRN
#for mcrn in range(1000000): #eg. [401997, 358497]:#ie all possible 6 digit numbers

mcrn = scraperwiki.sqlite.get_var("mcrn", 0)

while mcrn<1000000:
    mcrn = "%06d" % (mcrn) #format them all to have 6 digits - adding leading 0s as necessary

    #Generate URL for the page of the doctor with that MCRN
#   url = "http://www.medicalcouncil.ie/Registration/Search-for-a-doctor/Search-Results/?regno="+mcrn
    url = "http://www.medicalcouncil.ie/Public-Information/Check-the-Register/Search-Results/?regno="+mcrn
    print url #for debugging and tracking

    #fetch and open the html from the url
    root = lxml.html.parse(url).getroot()

    #Check whether there are any records
    if root.cssselect('.errorMsg')[0].text=="There are no records for this registration number":
        break

    table = root.cssselect("table.checkdetails")[0]#should only get one table
    

    trs = table.cssselect("tr")

    data = {"mcrn": mcrn}
    blankflag = False

    for tr in trs:
        th = tr.cssselect("th")[0]#should only get one
        td = tr.cssselect("td")[0]#should only get one

        if th.text == "Registration Number:" and not td.text:
            blankflag = True
            break

        if td.cssselect("ul"):
            subdata = {"mcrn": mcrn}
            ul_number = 1
            for ul in td.cssselect("ul"):
                subdata["ul_number"] = ul_number
                for li in ul.cssselect("li"):
                    li_split = li.text.split(":", 1)
                    li_title = li_split[0]
                    li_value = li_split[1]
                    subdata[li_title.replace(" ", "")] = li_value
                scraperwiki.sqlite.save(unique_keys=["mcrn", "ul_number"], table_name=th.text, data=subdata)
                ul_number += 1
        else:
            data[th.text.replace(" ", "").replace(":", "").replace("'", "")] = td.text

    if not blankflag:
        scraperwiki.sqlite.save(unique_keys=["mcrn"], table_name="Doctors", data=data) 
 
    mcrn = int(mcrn)+1
    scraperwiki.sqlite.save_var("mcrn", mcrn) #save the last completed mcrn, so we can take up where we left off