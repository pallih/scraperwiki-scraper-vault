import scraperwiki 
import scraperwiki
import requests
import openpyxl
import tempfile
import pprint


#setup sqlite
scraperwiki.sqlite.execute('DROP TABLE IF EXISTS `local_laws`')
scraperwiki.sqlite.execute('CREATE TABLE `local_laws` (`papid` text primary key, `source` text, `publiclawno` text, `year` text, `congress` text, `wordcount` text)')
scraperwiki.sqlite.commit()

raw = requests.get("https://dl.dropboxusercontent.com/s/q371890nsfkn5xj/pllist_forwordcountcollection_1995to2011.xlsx?token_hash=AAEQAQo7AAs79AjIlgrxBmtcWirEm2rotzxbXH1gy_Gqnw&dl=1", verify=False).content

f = tempfile.NamedTemporaryFile('wb')
f.write(raw)
f.seek(0)
wb = openpyxl.load_workbook(f.name)
f.close()

sheet = wb.get_sheet_by_name(name = 'Sheet1')
source = [[cell.value for cell in row] for row in sheet.rows]

pprint.pprint(source)


for i in range(15,395):
#papid` text primary key, `source` text, `publiclawno` text, `year` text, `congress` text, `wordcount` text)')
    if i > 0:
        
        local_laws = []
        local_laws.append({
                'papid': source[i][0],
                'source': source[i][1],
                'publiclawno': source[i][2],
                'year': source[i][3],
                'congress': source[i][4],
                'wordcount': '1'
            })
    

        scraperwiki.sqlite.save(['papid'], local_laws, 'local_laws')


