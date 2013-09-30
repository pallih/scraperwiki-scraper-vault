import scraperwiki
import urllib2
import string

try:
    scraperwiki.sqlite.execute("""
        create table magic
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."

#these are the starting points - the script runs forward in time for each year until it can't find a page, then goes back a year
u = 2012
v = 1


def scrapethat(u,v):
    def oneline(start,end,g,h):
#this identifies where 'for the' is located (html[ft])- this script assumes each representative line includes such a reference
        ref = '['+str(g)+'] HCA '+str(h)
        ft = html.find('for the',start)
        if ft == -1:
            print 'ft was not found'
            return
        if ft > end:
            print 'ft is after catchwords/interveners'
            return
#this creates the line, using brackets as delimiters (seems common in austlii)
        open = html.rfind('>',0,ft)
        shut = html.find('<',ft)
        line = html[open+1:shut]
#this line finds 'for the' in the line
        ftinline = line.find('for the')
#this splits up the line, thereby assuming the barristers are at the start
        bars = line[:ftinline]  
        barscomma = bars.find(',')
        print line    
        if barscomma == -1:
            reps = bars
        else:
            reps = bars[:barscomma]
        if ' with ' in reps:        
            wid = bars.find(' with ')
            rep1 = bars[:wid]
            rep2 = bars[wid+6:]
            rep3 = 'N/A'
            if ' and ' in rep2:
                und = bars[wid+6:].find(' and ')
                rep2 = bars[wid+6:][:und]
                rep3 = bars[wid+6:][und+5:]
            if ' and ' in rep1:
                ond = bars.find(' and ')
                rep3 = rep2
                rep2 = bars[ond+5:wid]
                rep1 = bars[:ond]
        else:
            rep1 = reps
            rep2 = 'N/A'
            rep3 = 'N/A'
        print 'Barrister:',rep1
        latewith = line.find('with')
        lateand = line.find(' and')
        if rep2 != 'N/A':
            print 'With:',rep2
        else:
            if 'with' in line:
                x = latewith + 4
                while line[x].islower() != True:
                    x = x + 1
                while line[x].isspace() != True:
                    x = x + 1
                rep2 = line[latewith+4:x]
                print 'With:',rep2
            if ' and' in line:
                print 'GOTCHA3'
                z = lateand + 4
                while line[z].islower() != True:
                    z = z + 1
                while line[z].isspace() != True:
                    z = z + 1
                rep3 = line[lateand+4:z]
        if rep3 != 'N/A':
            print 'And:',rep3
        else:
            backline = line[latewith:]
            if ' and' in line[latewith:] and line[latewith:].find(' and') < ftinline:
                print 'GOTCHA2',backline
                latewith2 = backline.find(' and')
                y = latewith2 + 3
                while backline[y].islower() != True:
                    y = y + 1
                while backline[y].isspace() != True:
                    print y,backline[y]
                    y = y + 1
                rep3 = backline[latewith2+4:y]
                print 'And:',rep3
        ib = line.find('nstructed')
        if ib == -1:
            firm = 'N/A'
        else:
            firm = line[ib+13:-1]
        if latewith > ftinline:
            lateft = line.find('for the',latewith)
            if lateft == -1:
                lateft = line.find('of the',latewith)
            forthe = line[lateft+7:ib-3]
        elif lateand > ftinline:
            lateft = line.find('for the',lateand)
            forthe = line[lateft+7:ib-3]
            if len(line[lateand+4:ib-3]) < 12:
                forthe = line[ftinline+8:ib-3]
        else:
            forthe = line[ftinline+8:ib-3]
        print 'For the:',forthe
        prob = 0
        instr = 0
        data = {
          'ref' : ref,
          'rep' : rep1,
          'for' : forthe,
          'instr' : prob,
          'prob' : instr
        }
        scraperwiki.sqlite.save(unique_keys=[],data=data,table_name='magic')
        if rep2 != 'N/A':
            data = {
              'ref' : ref,
              'rep' : rep2,
              'for' : forthe,
              'instr' : prob,
              'prob' : instr
            }
            scraperwiki.sqlite.save(unique_keys=[],data=data,table_name='magic')
        if rep3 != 'N/A':
            data = {
              'ref' : ref,
              'rep' : rep3,
              'for' : forthe,
              'instr' : prob,
              'prob' : instr
            }
            scraperwiki.sqlite.save(unique_keys=[],data=data,table_name='magic')             
        print 'Instructed by:',firm
        oneline(shut,end,g,h)
    try:
        baseurl = 'http://www.austlii.edu.au/au/cases/cth/HCA/%(year)d/%(number)d.html' % {"year":u,"number":v}
        html = scraperwiki.scrape(baseurl)
        print baseurl
        low = html.lower()
        x = low.find('order')        
        cw = low.find('catchwords')
        r = low.find('representation')
        i = low.find('interveners')
        if low.find('catchwords') == -1:
            cw = 999999999999999999999
        if low.find('interveners') == -1:
            i = 999999999999999999999
        print 'i is',i
        print 'cw is',cw
        if cw <= i:
            cwi = cw
        else:
            cwi = i
        print 'cwi is',cwi
        oneline(r,cwi,u,v)
        return True
    except:
        return False

def allcases(u,v):
    while True:
        if scrapethat(u,v) == False:
            return False
        v = v + 1

while True:
    if allcases(u,v) == False:
        u = u - 1
        v = 1    

print 'done!'


import scraperwiki
import urllib2
import string

try:
    scraperwiki.sqlite.execute("""
        create table magic
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."

#these are the starting points - the script runs forward in time for each year until it can't find a page, then goes back a year
u = 2012
v = 1


def scrapethat(u,v):
    def oneline(start,end,g,h):
#this identifies where 'for the' is located (html[ft])- this script assumes each representative line includes such a reference
        ref = '['+str(g)+'] HCA '+str(h)
        ft = html.find('for the',start)
        if ft == -1:
            print 'ft was not found'
            return
        if ft > end:
            print 'ft is after catchwords/interveners'
            return
#this creates the line, using brackets as delimiters (seems common in austlii)
        open = html.rfind('>',0,ft)
        shut = html.find('<',ft)
        line = html[open+1:shut]
#this line finds 'for the' in the line
        ftinline = line.find('for the')
#this splits up the line, thereby assuming the barristers are at the start
        bars = line[:ftinline]  
        barscomma = bars.find(',')
        print line    
        if barscomma == -1:
            reps = bars
        else:
            reps = bars[:barscomma]
        if ' with ' in reps:        
            wid = bars.find(' with ')
            rep1 = bars[:wid]
            rep2 = bars[wid+6:]
            rep3 = 'N/A'
            if ' and ' in rep2:
                und = bars[wid+6:].find(' and ')
                rep2 = bars[wid+6:][:und]
                rep3 = bars[wid+6:][und+5:]
            if ' and ' in rep1:
                ond = bars.find(' and ')
                rep3 = rep2
                rep2 = bars[ond+5:wid]
                rep1 = bars[:ond]
        else:
            rep1 = reps
            rep2 = 'N/A'
            rep3 = 'N/A'
        print 'Barrister:',rep1
        latewith = line.find('with')
        lateand = line.find(' and')
        if rep2 != 'N/A':
            print 'With:',rep2
        else:
            if 'with' in line:
                x = latewith + 4
                while line[x].islower() != True:
                    x = x + 1
                while line[x].isspace() != True:
                    x = x + 1
                rep2 = line[latewith+4:x]
                print 'With:',rep2
            if ' and' in line:
                print 'GOTCHA3'
                z = lateand + 4
                while line[z].islower() != True:
                    z = z + 1
                while line[z].isspace() != True:
                    z = z + 1
                rep3 = line[lateand+4:z]
        if rep3 != 'N/A':
            print 'And:',rep3
        else:
            backline = line[latewith:]
            if ' and' in line[latewith:] and line[latewith:].find(' and') < ftinline:
                print 'GOTCHA2',backline
                latewith2 = backline.find(' and')
                y = latewith2 + 3
                while backline[y].islower() != True:
                    y = y + 1
                while backline[y].isspace() != True:
                    print y,backline[y]
                    y = y + 1
                rep3 = backline[latewith2+4:y]
                print 'And:',rep3
        ib = line.find('nstructed')
        if ib == -1:
            firm = 'N/A'
        else:
            firm = line[ib+13:-1]
        if latewith > ftinline:
            lateft = line.find('for the',latewith)
            if lateft == -1:
                lateft = line.find('of the',latewith)
            forthe = line[lateft+7:ib-3]
        elif lateand > ftinline:
            lateft = line.find('for the',lateand)
            forthe = line[lateft+7:ib-3]
            if len(line[lateand+4:ib-3]) < 12:
                forthe = line[ftinline+8:ib-3]
        else:
            forthe = line[ftinline+8:ib-3]
        print 'For the:',forthe
        prob = 0
        instr = 0
        data = {
          'ref' : ref,
          'rep' : rep1,
          'for' : forthe,
          'instr' : prob,
          'prob' : instr
        }
        scraperwiki.sqlite.save(unique_keys=[],data=data,table_name='magic')
        if rep2 != 'N/A':
            data = {
              'ref' : ref,
              'rep' : rep2,
              'for' : forthe,
              'instr' : prob,
              'prob' : instr
            }
            scraperwiki.sqlite.save(unique_keys=[],data=data,table_name='magic')
        if rep3 != 'N/A':
            data = {
              'ref' : ref,
              'rep' : rep3,
              'for' : forthe,
              'instr' : prob,
              'prob' : instr
            }
            scraperwiki.sqlite.save(unique_keys=[],data=data,table_name='magic')             
        print 'Instructed by:',firm
        oneline(shut,end,g,h)
    try:
        baseurl = 'http://www.austlii.edu.au/au/cases/cth/HCA/%(year)d/%(number)d.html' % {"year":u,"number":v}
        html = scraperwiki.scrape(baseurl)
        print baseurl
        low = html.lower()
        x = low.find('order')        
        cw = low.find('catchwords')
        r = low.find('representation')
        i = low.find('interveners')
        if low.find('catchwords') == -1:
            cw = 999999999999999999999
        if low.find('interveners') == -1:
            i = 999999999999999999999
        print 'i is',i
        print 'cw is',cw
        if cw <= i:
            cwi = cw
        else:
            cwi = i
        print 'cwi is',cwi
        oneline(r,cwi,u,v)
        return True
    except:
        return False

def allcases(u,v):
    while True:
        if scrapethat(u,v) == False:
            return False
        v = v + 1

while True:
    if allcases(u,v) == False:
        u = u - 1
        v = 1    

print 'done!'


