"""
Obtains Lincolnshire Council school data

The .xls file was found linked to at:
  http://www.lincolnshire.gov.uk/section.asp?catid=17201&docid=64613

"No man has a good enough memory to make a successful liar."
 - Abraham Lincoln
"""


from scraperwiki import datastore, scrape
import xlrd


def main():
    w = xlrd.open_workbook(file_contents=scrape("http://uk.sitestat.com/lincolnshire/lincolnshire/s?Home.A_Parent.School_Admissions.All_About_Your_Local_Schools.A__Z_List_of_Schools.AZ_List_of_Schools.xls&ns_type=pdf&ns_url=http://www.lincolnshire.gov.uk/upload/public/attachments/1172/AZ_List_of_Schools.xls"))
    s = w.sheet_by_index(0)

    keys = [str(c.value) for c in s.row(0)]
    schoolname = keys[1]

    for i in range(1,s.nrows):
        r = s.row(i)
        if sum([len(c.value) for c in r[1:]]) == 0:
            # want to test that all the rows are empty, but the tests don't work
            # this is just an extra heading row; we don't need it
            pass
        else:
            keyvalues = {}
            for (k,c) in zip(keys,r):
                v = str(c.value.replace(u'\u2019',"'"))
                if v != "":
                    keyvalues[k] = v
            datastore.save(unique_keys=[schoolname],data=keyvalues)


main()
