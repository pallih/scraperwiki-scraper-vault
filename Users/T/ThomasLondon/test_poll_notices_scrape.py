import scraperwiki
import urllib2, lxml.etree


url='http://www.worcestershire.gov.uk/cms/pdf/Notice%20of%20Poll%20and%20Situation%20of%20Polling%20Stations%20Worcester%20City%20Area%20Divisions%20PDF%20185%20KB.pdf'
#Archive copy: https://dl.dropboxusercontent.com/u/1156404/1174-Notice%20of%20Poll%20-%20IOWC%20May%202013.pdf

pdfdata = urllib2.urlopen(url).read()

xmldata = scraperwiki.pdftoxml(pdfdata)

root = lxml.etree.fromstring(xmldata)
pages = list(root)


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res).strip()


#print pages
for page in pages:
    data={'stations':[]}
    phase=0
    for el in page:
        #print el.attrib, gettext_with_bi_tags(el)
        if gettext_with_bi_tags(el).startswith('Election of'):
            phase=1
            continue
        tmp=gettext_with_bi_tags(el)
        if phase==1:
            if tmp.strip()=='':pass
            else:
                data['ward']=tmp
                phase=phase+1
        elif phase==2:
            if tmp.startswith('Proposers'):
                phase=3
                record={'candidate':[],'address':[],'desc':[],'proposers':[],'seconders':[]}
                data['list']=[]
                continue
        elif phase==3:
            if tmp.strip()=='':
                phase=4
                print '-------------------------------'
                data['list'].append(record)
                continue
            elif int(el.attrib['left'])<100:
                if record['address']!=[]:
                    data['list'].append(record)
                    record={'candidate':[],'address':[],'desc':[],'proposers':[],'seconders':[]}
                record['candidate'].append(tmp)
            elif int(el.attrib['left'])<300: record['address'].append(tmp)
            elif int(el.attrib['left'])<450: record['desc'].append(tmp)
            elif int(el.attrib['left'])<600:
                if tmp.startswith('('): record['proposers'][-1]=record['proposers'][-1]+' '+tmp
                elif len(record['proposers'])>0 and record['proposers'][-1].strip().endswith('-'): record['proposers'][-1]=record['proposers'][-1]+tmp
                elif len(record['proposers'])>0 and record['proposers'][-1].strip().endswith('.'): record['proposers'][-1]=record['proposers'][-1]+' '+tmp
                else: record['proposers'].append(tmp)
            elif int(el.attrib['left'])<750:
                if tmp.startswith('('): record['seconders'][-1]=record['seconders'][-1]+' '+tmp
                elif len(record['seconders'])>0 and record['seconders'][-1].strip().endswith('-'): record['seconders'][-1]=record['seconders'][-1]+tmp
                elif len(record['seconders'])>0 and record['seconders'][-1].strip().endswith('.'): record['seconders'][-1]=record['seconders'][-1]+' '+tmp
                else: record['seconders'].append(tmp)
        elif phase==4:
            if tmp.startswith('persons entitled to vote'):
                phase=5
                record={'station':[],'range':[]}
                continue
        elif phase==5:
            if tmp.strip()=='':
                data['stations'].append(record)
                break
            elif int(el.attrib['left'])<100:
                if record['range']!=[]:
                    data['stations'].append(record)
                    record={'station':[],'range':[]}
                record['station'].append(tmp)
            elif int(el.attrib['left'])>300:
                record['range'].append(tmp)
    print data
    tmpdata=[]
    for station in data['stations']:
        tmpdata.append({'ward':data['ward'],'station':' '.join(station['station']),'range':' '.join(station['range'])})
    scraperwiki.sqlite.save(unique_keys=[], table_name='stations', data=tmpdata)
    tmpdata=[]
    tmpdata2=[]

    for candidate in data['list']:
        tmpdata.append( {'ward':data['ward'],'candidate':' '.join(candidate['candidate']), 'address':' '.join(candidate['address']),'desc':' '.join(candidate['desc']) } )
        party=' '.join(candidate['desc']).replace('Candidate','').strip()
        cand=' '.join(candidate['candidate'])
        cs=cand.strip(' ').split(' ')
        if len(cs)>2:
            cand2=cs[:2]
            for ci in cs[2:]:
                cand2.append(ci[0]+'.')
        else: cand2=cs
        ctmp=cand2[0]
        cand2.remove(ctmp)
        cand2.append(ctmp.title())
        candi=' '.join(cand2)
        for proposer in candidate['proposers']:
            if proposer.find('(+)')>-1:
                proposer=proposer.replace('(+)','').strip()
                typ='proposer'
            else:typ='assentor'
            tmpdata2.append({ 'ward':data['ward'],'candidate':cand, 'candinit':candi, 'support':proposer,'role':'proposal', 'typ':typ, 'desc':party }.copy())
        for seconder in candidate['seconders']:
            if seconder.find('(++)')>-1:
                seconder=seconder.replace('(++)','').strip()
                typ='seconder'
            else:typ='assentor'
            tmpdata2.append({ 'ward':data['ward'],'candidate':cand, 'candinit':candi, 'support':seconder,'role':'seconding', 'typ':typ, 'desc':party }.copy())

    scraperwiki.sqlite.save(unique_keys=[], table_name='candidates', data=tmpdata)
    scraperwiki.sqlite.save(unique_keys=[], table_name='support', data=tmpdata2)