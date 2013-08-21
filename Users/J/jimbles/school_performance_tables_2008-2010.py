import scraperwiki
import mechanize
import lxml.html
import string
from collections import defaultdict
import urlparse

lea_national = 971   #NB non-standard code
lea_maintained = 970

def checkpoint_set (newstate, newpoint):
    global state, point
    state = newstate
    point = newpoint
    scraperwiki.sqlite.save_var ('state', state, verbose=0)
    scraperwiki.sqlite.save_var ('point', point, verbose=0)
def checkpoint_get ():
    global state, point
    state = scraperwiki.sqlite.get_var ('state', 'get', verbose=0)
    point = scraperwiki.sqlite.get_var ('point', 0, verbose=0)

def headers_from_table (table):
# Takes lxml.html tree node that points to a table element, parses out <th> elements, takes account of rowspan
# <thead><tr><th rowspan="...">...</th>...</tr>...</thead>

    #http://stackoverflow.com/questions/9978445/parsing-a-table-with-rowspan-and-colspan
    def table_to_list(table):
        dct = table_to_2d_dict(table)
        return list(iter_2d_dict(dct))
    
    def table_to_2d_dict(table):
        result = defaultdict(lambda : defaultdict(unicode))
        for row_i, row in enumerate(table.xpath('./tr')):
            for col_i, col in enumerate(row.xpath('./td|./th')):
                colspan = int(col.get('colspan', 1))
                rowspan = int(col.get('rowspan', 1))
                col_data = col.text_content()
                while row_i in result and col_i in result[row_i]:
                    col_i += 1
                for i in range(row_i, row_i + rowspan):
                    for j in range(col_i, col_i + colspan):
                        result[i][j] = col_data
        return result
    
    def iter_2d_dict(dct):
        for i, row in sorted(dct.items()):
            cols = []
            for j, col in sorted(row.items()):
                cols.append(col)
            yield cols

    thead = table.xpath('//thead')[0]
    d = table_to_2d_dict (thead)

    headers = []
    prev = []
    for r, row in enumerate(iter_2d_dict(d)):
        for c, cell in enumerate(row):
            if r == 0:
                headers.append(cell)
                prev.append(cell)
            elif prev[c] != cell:
                headers[c] += ' '+cell
                prev[c] = cell
    return headers

header_trans_data = {
    'p' : [ #KS2
    ('Total number of pupils on roll',                                            'TOTPUPS'), #Background
    ('pupils with SEN with statements or supported at School Action Plus Number', 'TSENSAP'),
    ('pupils with SEN with statements or supported at School Action Plus %',      'PSENSAP'),
    ('pupils with SEN supported at School Action Number',                    'TSENA'),
    ('pupils with SEN supported at School Action %',                         'PSENA'),
    ('Number of pupils on roll aged 10',                                          'TPUPYEAR'),
    ('KS1-2 CVA Score' ,                     'EMVAMEAS'), #CVA #FIXME: check: does this include science too?
    ('CVA Confidence interval Lower Limit' , 'EMLCONF'),
    ('CVA Confidence interval Upper Limit' , 'EMUCONF'),
    ('Contextual Value Added Coverage',      'VACOV'),
    ('Pupils eligible for Key Stage 2 assessment total',                                 'TELIG'), #KS2 Results
    ('Pupils eligible for Key Stage 2 assessment With SEN with statements or supported', 'SENELS'),
    ('Pupils eligible for Key Stage 2 assessment With SEN with statements or supported', 'PSENELS'),
    ('Pupils eligible for Key Stage 2 assessment With SEN supported',                    'SENELA'), #non-standard name
    ('Pupils eligible for Key Stage 2 assessment With SEN supported',                    'PSENELA'), #non-standard name
    ('English L4+',                      'PTENGX'),
    ('English L5',                       'PTENGAX'),
    ('English A/T',                      'PTENGAT'),
    ('Mathematics L4+',                  'PTMATX'),
    ('Mathematics L5',                   'PTMATAX'),
    ('Mathematics A/T',                  'PTMATAT'),
    ('Science L4+',                      'PTSCIX'),
    ('Science L5',                       'PTSCIAX'),
    ('Science A/T',                      'PTSCIAT'),
    ('both English and Mathematics L4+', 'PTENGMATX'),
    ('Average point score',              'TAPS'),
    ('% making expected progress in English',             'PTENG12'), #Progress measures
    ('% of eligible pupils included in English progress', 'COVENG12'),
    ('% making expected progress in maths',               'PTMATH12'),
    ('% of eligible pupils included in maths progress',   'COVMATH12'),
    ('Overall absence',    'PERCTOT'), #Absence
    ('Persistent absence', 'PERCUA')],
    's' : [ #KS4
    ('Number of pupils at the end of Key Stage 4', ''),
    ('% of pupils at the end of Key Stage 4 aged 14 or less',               ''), #Cohort
    ('% of pupils at the end of Key Stage 4 aged 15',                       ''),
    ('with SEN, with statements or supported at School Action Plus Number', ''), 
    ('with SEN, with statements or supported at School Action Plus %',      ''),
    ('with SEN, supported at School Action Number',                         ''),
    ('with SEN, supported at School Action %',                              ''),
    ('% of pupils achieving Level 2 (5+ A*-C) including English and Maths GCSEs', ''), #KS4 Results
    ('% of pupils achieving English and maths Skills at Level 2',                 ''),
    ('% of pupils achieving English and maths Skills at Level 1',                 ''),
    ('% of pupils achieving Level 2 (5+ A*-C)',                                   ''),
    ('% of pupils achieving Level 1 (5+ A*-G)',                                   ''),
    ('% of pupils achieving 2 grades A*-C in science',                            ''),
    ('% of pupils achieving A*-C in a modern foreign language',                   ''), 
    ('% of pupils achieving at least one qualification',                          ''),
    ('Average total point score',                                                 ''),
    ('CVA measure based on progress between Key Stage 2 and Key Stage 4',                    ''), #KS2-4 CVA
    ('Limit of Key Stage 2 to 4 CVA Confidence Intervals Upper',                             ''),
    ('Limit of Key Stage 2 to 4 CVA Confidence Intervals Lower',                             ''),
    ('% of pupils at the end of Key Stage 4 included in CVA calculation',                    ''),
    ('Average number of qualifications taken by pupils in Key Stage 2 to 4 CVA calculation', ''),
    ('% making the expected level of progress in English',                                                ''), #KS4 progress
    ('% of pupils at the end of Key Stage 4 included in the calculation of the English progress measure', ''),
    ('% making the expected level of progress in maths',                                                  ''),
    ('% of pupils at the end of Key Stage 4 included in the calculation of the maths progress measure',   ''),
    ('Total number of pupils (all ages)',                                         ''), #Background
    ('Pupils with SEN with statements or supported at School Action Plus Number', ''),
    ('Pupils with SEN with statements or supported at School Action Plus %',      ''),
    ('Pupils with SEN Supported at School Action Number',                         ''),
    ('Pupils with SEN Supported at School Action %',                              ''),
    ('Maintained mainstream schools only overall absence',    ''), #Absence
    ('Maintained mainstream schools only persistent absence', '')],
    '2' : [ #KS5
    ('Number of students aged 16-18', ''),
    ('General and Applied A/AS or Equivalent Achievement Number at end of A/AS', ''),
    ('General and Applied A/AS or Equivalent Achievement Average point score per student', ''),
    ('General and Applied A/AS or Equivalent Achievement Average point score per examination entry', ''),
    ('VA score', ''),
    ('Key Stage 4 to 5 VA Confidence Interval Upper', ''),
    ('Key Stage 4 to 5 VA Confidence Interval Lower', ''),
    ('Coverage indicator', '')]
}
def header_trans (src, phase):
    global header_trans_data
    out = []
    for hdr in src:
        hdr = hdr.lower()
        var = '?'
        for rule, rule_var in header_trans_data[phase]:
            rule = rule.lower()
            try:
                i = hdr.index(rule) #throws ValueError if not found
                if not(rule_var in out):
                    var = rule_var
                break
            except ValueError:
                pass
        if var == '?':
            print 'Unknown: %s' % (hdr)
        out.append (var)
    out[0] = 'Description'
    return out

# (1) Get LEAs
br = mechanize.Browser(factory=mechanize.RobustFactory())
las = []
for r in range(1,10):
    br.open('http://www.education.gov.uk/performancetables/primary_08/region'+str(r)+'.shtml')
    for link in br.links(url_regex='group_'):
        p = urlparse.parse_qs(link.url)
        if ('No' in p):
            las.append(p['No'][0])
        else:
            print p.url
    break #FIXME: testing only
las.sort()

checkpoint_get ()
if state == 'get':
##
    years = [2008, 2009]
    urls  = ['http://www.education.gov.uk/cgi-bin/performancetables/group_08.pl?Mode=Z&Type=LA&Begin=s&F=1&L=100000&Year=08&','http://www.education.gov.uk/cgi-bin/performancetables/group_09.pl?Mode=Z&Type=LA&Begin=s&F=1&L=100000&Year=09&']
    bases = {'p':['d','v','p','a'], 's':['a','b','g','e','m','d'], '2':['a','b']}
    tables = {'la':{'p':'ks2_la', 's':'ks4_la', '2':'ks5_la'}, 'school':{'p':'ks2_school','s':'ks4_school','2':'ks5_school'}}
    for la in las:
        for phase in ['p', 's', '2']: #p = Primary, s = Secondary, 2 = Post-16
            for y in range(0,len(years)):
                #Base for KS2 (p)
                # d: Background
                # v: Contextual value added
                # p: KS2 Results
                # a: Absence
                #Base for KS4 (s)
                # a: Background
                # b: Cohort
                # g: KS4 results
                # e: Contextual value added
                # m: KS2-4 expected progress
                # d: Absence
                #Base for KS5 (2)
                # a: KS5 results
                # b: CVA
                out_estab = dict()
                out_la = dict()
                for base in bases[phase]:
                    year = years[y]
                    url = urls[y]+'&Phase='+phase+'&Base='+base+'&No='+str(la)
                    data = scraperwiki.scrape (url)
                    root = lxml.html.fromstring (data)
                    table = root.xpath('//table')[0]
                    headers = header_trans(headers_from_table (table), phase)
                    for row in table.xpath('//tbody/tr'):
                        cols = [col.text_content() for col in row.xpath('.//td') for n in range(0,int(col.get('colspan','1')))]
                        d = dict(zip(headers, cols))

                        if row.get('class','') == 'averages':
                            if d['Description'] == 'Local Authority Average':
                                d['LEA'] = str(la)
                            elif d['Description'] == 'England (maintained schools only)':
                                d['LEA'] = str(lea_maintained)
                            elif d['Description'] == 'England (all schools)':
                                d['LEA'] = str(lea_national)
                        else:
                            try:
                                link = row.xpath('.//a')[0].get('href','')
                                qp = urlparse.parse_qs (link)
                                d['LEA'] = qp['No'][0][:3]
                                d['ESTAB'] = qp['No'][0][3:]
                            except:
                                pass

                        del d['Description'] #Arbitrary name for all cols[0] by header_trans()

                        for k in d.keys():
                            while d[k][-1:] == ' ':
                                d[k] = d[k][:-1] #strip trailing spaces
                            try:
                                if d[k][-1:] == '%':
                                    d[k] = float(d[k][:-1])/100
                                else:
                                    d[k] = int(d[k])
                            except:
                                del d[k]

                        d['YEAR'] = year

                        if 'ESTAB' in d:
                            if d['ESTAB'] in out_estab:
                                out_estab[d['ESTAB']] = dict(out_estab[d['ESTAB']].items() + d.items())
                            else:
                                out_estab[d['ESTAB']] = d
                        elif 'LEA' in d:
                            if d['LEA'] in out_la:
                                out_la[d['LEA']] = dict(out_la[d['LEA']].items() + d.items())
                            else:
                                out_la[d['LEA']] = d

                    #/for row   
                #/for base

                for e in out_estab:
                    scraperwiki.sqlite.save (unique_keys=['LEA','ESTAB','YEAR'], data=out_estab[e], table_name=tables['school'][phase], verbose=0)
                for l in out_la: 
                    scraperwiki.sqlite.save (unique_keys=['LEA', 'YEAR'], data=out_la[l], table_name=tables['la'][phase], verbose=0)

                break #FIXME: testing only
            #/for year
            break #FIXME: testing only
        #/for phase
        break #FIXME: testing only
    #/for la