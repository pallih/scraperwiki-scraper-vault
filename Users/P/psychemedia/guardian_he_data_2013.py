import scraperwiki, csv,urllib

urlstub='http://spreadsheets.google.com/tq?tqx=out:csv&tq=select%20*%20where%20B%21%3D%27%27&key=0AonYZs4MzlZbdG1PRER2ZXZTNy1veDJDU2hrNU9PdkE&gid='

gid=[(2,"Medicine"), (3,"Dentistry"), (4,"Veterinary Science"), (5,"Anatomy"), (6,"Nursing"), (7,"Social work"), (8,"Psychology"), (9,"Pharmacy and Pharmacology"), (10,"Biosciences"), (11,"Chemistry"), (12,"Physics"), (13,"Agriculture, Forestry and Food"), (14,"Earth and Marine Sciences"), (15,"General Engineering"), (16,"Chemical Engineering"), (17,"Materials and Mineral Engineering"), (18,"Civil Engineering"), (19,"Electronic and Electrical Engineering"),(20,"Mechanical Engineering"), (21,"Mathematics"), (22,"Computer Sciences and IT"), (23,"Business and Management Studies"), (24,"Tourism, Transport and Travel"), (25,"Geography and Environmental Sciences"), (26,"Social Policy and Administration"), (27,"Anthropology"), (28,"Media Studies/Communications/Librarianship"), (29,"Education"), (30,"Modern Languages/Linguistics"), (31,"Archaeology"), (32,"Law"), (33,"Sociology"), (34,"Politics"), (35,"Economics"), (36,"English"), (37,"Art and Design"), (39,"Drama and Dance"), (40,"Architecture"), (41,"Philosophy"), (42,"Classics"), (43,"Religious Studies/Theology"), (44,"American Studies"), (45,"History/History of Art"), (46,"Sports Science"), (47,"Planning"), (48,"Music")]

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
