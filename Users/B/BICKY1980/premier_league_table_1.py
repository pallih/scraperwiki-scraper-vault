import csv, sys
from webscraping import download, xpath
D = download.Download()


class WritableObject:
    def __init__(self):
        self.content = []
    def write(self, string):
        self.content.append(string)

csv_file = csv.reader(open('urls-test2.csv', 'rb'), delimiter=',')

names = []
for data in csv_file:
    names.append(data[0])

for name in names:
   html = D.get(name);
   html2 = html
   param = '<br />';
   html2 = html2.replace("<br />", " | ")
   print name

   c = csv.writer(open("darkgrey.csv", "a"))
   for row in xpath.search(html2, '//table/tr[@class="bgdarkgrey"]'):
       cols = xpath.search(row, '/td')
       if len(cols) >= 5:
           c.writerow([cols[0], cols[1], cols[2], cols[3], cols[4]])

   q = csv.writer(open("lightgrey.csv", "a"))
   for row2 in xpath.search(html2, '//table/tr[@class="bglightgrey"]'):
       cols2 = xpath.search(row2, '/td')
       if len(cols) >= 5:
           q.writerow([cols2[0], cols2[1], cols2[2], cols2[3], cols2[4]])

csv_file.close()
