import scraperwiki, csv, re, sys

#data = scraperwiki.scrape("http://img1.buyersbestfriend.com/eng/sf_list.csv")
data = scraperwiki.scrape("http://img1.buyersbestfriend.com/eng/aim_li.csv")

print data
recs = []
reader = csv.DictReader(data.splitlines())

n = 0
have = 0
for i, row in enumerate(reader):
    have += 1
    new_row = dict((re.sub(" ", "", key.lower().strip()), val.strip()) for key, val in row.items() if key and val and key != "")
    if 'companyname' not in new_row.keys():
        print new_row
        n+=1
        continue
    recs.append(new_row)
print "lost:" + str(n)
print "have:" + str(have)
scraperwiki.sqlite.save(unique_keys=['companyname', 'contact1last'], data=recs)import scraperwiki, csv, re, sys

#data = scraperwiki.scrape("http://img1.buyersbestfriend.com/eng/sf_list.csv")
data = scraperwiki.scrape("http://img1.buyersbestfriend.com/eng/aim_li.csv")

print data
recs = []
reader = csv.DictReader(data.splitlines())

n = 0
have = 0
for i, row in enumerate(reader):
    have += 1
    new_row = dict((re.sub(" ", "", key.lower().strip()), val.strip()) for key, val in row.items() if key and val and key != "")
    if 'companyname' not in new_row.keys():
        print new_row
        n+=1
        continue
    recs.append(new_row)
print "lost:" + str(n)
print "have:" + str(have)
scraperwiki.sqlite.save(unique_keys=['companyname', 'contact1last'], data=recs)