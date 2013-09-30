import scraperwiki
import xlrd

def main():
    f = scraperwiki.scrape("http://www.erpho.org.uk/download.aspx?urlid=20010&urlt=1")
    w = xlrd.open_workbook(file_contents = f)
    s = w.sheets()[1]

    for i in xrange(s.nrows):
        l = s.row_values(i)
        name = l[1].strip()
        if name == "Rhondda, Cynon, Taff":
            name = "Rhondda Cynon Taf"
        if name[-4:] == " UA3":
            name = name[:-4]
        if name[-3:] == " UA":
            name = name[:-3]
        if name != "":
            try:
                pop = int(round(float(l[6])*1000))
                scraperwiki.sqlite.save(unique_keys=["name"],data={"name":name,"population":pop})
            except ValueError:
                pass

main()
import scraperwiki
import xlrd

def main():
    f = scraperwiki.scrape("http://www.erpho.org.uk/download.aspx?urlid=20010&urlt=1")
    w = xlrd.open_workbook(file_contents = f)
    s = w.sheets()[1]

    for i in xrange(s.nrows):
        l = s.row_values(i)
        name = l[1].strip()
        if name == "Rhondda, Cynon, Taff":
            name = "Rhondda Cynon Taf"
        if name[-4:] == " UA3":
            name = name[:-4]
        if name[-3:] == " UA":
            name = name[:-3]
        if name != "":
            try:
                pop = int(round(float(l[6])*1000))
                scraperwiki.sqlite.save(unique_keys=["name"],data={"name":name,"population":pop})
            except ValueError:
                pass

main()
