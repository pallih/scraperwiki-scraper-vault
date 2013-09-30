import scraperwiki, csv, urllib

urlstub='http://spreadsheets.google.com/tq?tqx=out:csv&tq=select%20*%20where%20B%21%3D%27%27&key=0AonYZs4MzlZbdG1PRER2ZXZTNy1veDJDU2hrNU9PdkE&gid='

gid=[(7,"Social work"), (8,"Psychology"), (21,"Mathematics"), (22,"Computer Sciences and IT"), (23,"Business and Management Studies"), (25,"Geography and Environmental Sciences"), (26,"Social Policy and Administration"), (27,"Anthropology"), (28,"Media Studies/Communications/Librarianship"), (32,"Law"), (33,"Sociology"), (34,"Politics"), (35,"Economics"), (41,"Philosophy"), (45,"History/History of Art")]

def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass

dropper('unidata')

for (i,subj) in gid:
    url=urlstub+str(i)
    print i,subj

    nReader = csv.DictReader(urllib.urlopen(url))
    
    for nrow in nReader:
        datarow={'Subject':subj}
        for h in nrow:
            if nrow[h]=='null': nrow[h]=''
            if h.find(' Rank')!=-1:
                datarow['Rank']=nrow[h]
                datarow['Header Subject']=h.replace(' Rank','').strip()
            else:
                key=h.replace('%','').strip()
                key=key.replace('/10','').strip()
                key=key.replace(':',' to ').strip()
                key=key.replace('student (FTE)','FTE student').strip()
                datarow[key]=nrow[h]
        scraperwiki.sqlite.save(unique_keys=[], table_name='unidata', data=datarow)
import scraperwiki, csv, urllib

urlstub='http://spreadsheets.google.com/tq?tqx=out:csv&tq=select%20*%20where%20B%21%3D%27%27&key=0AonYZs4MzlZbdG1PRER2ZXZTNy1veDJDU2hrNU9PdkE&gid='

gid=[(7,"Social work"), (8,"Psychology"), (21,"Mathematics"), (22,"Computer Sciences and IT"), (23,"Business and Management Studies"), (25,"Geography and Environmental Sciences"), (26,"Social Policy and Administration"), (27,"Anthropology"), (28,"Media Studies/Communications/Librarianship"), (32,"Law"), (33,"Sociology"), (34,"Politics"), (35,"Economics"), (41,"Philosophy"), (45,"History/History of Art")]

def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass

dropper('unidata')

for (i,subj) in gid:
    url=urlstub+str(i)
    print i,subj

    nReader = csv.DictReader(urllib.urlopen(url))
    
    for nrow in nReader:
        datarow={'Subject':subj}
        for h in nrow:
            if nrow[h]=='null': nrow[h]=''
            if h.find(' Rank')!=-1:
                datarow['Rank']=nrow[h]
                datarow['Header Subject']=h.replace(' Rank','').strip()
            else:
                key=h.replace('%','').strip()
                key=key.replace('/10','').strip()
                key=key.replace(':',' to ').strip()
                key=key.replace('student (FTE)','FTE student').strip()
                datarow[key]=nrow[h]
        scraperwiki.sqlite.save(unique_keys=[], table_name='unidata', data=datarow)
