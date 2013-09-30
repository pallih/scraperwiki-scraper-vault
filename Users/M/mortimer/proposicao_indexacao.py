import scraperwiki
import string

params = scraperwiki.utils.GET()
start = int(params.get("d_id", "522187"))

sourcescraper = 'camara_proposicoes_br'
scraperwiki.sqlite.attach(sourcescraper, "src")
scraperwiki.sqlite.attach('votacao_deputado_br')

sdata = scraperwiki.sqlite.execute("select keyword, count(distinct proposicao_id), vote as c from `indexacao` as i, votacao_deputado_br.votacao as v where  i.tipo=v.type and i.ano=v.year and i.numero=v.number and v.deputado_id=%d group by lower(keyword), vote" % (start) ) 

rows = sdata.get("data")

no_html = ""
yes_html = ""
o_html=""
a_html=""

for row in rows:
    #TODO cache this
    #norm = scraperwiki.sqlite.execute("select count(distinct proposicao_id) from `indexacao` where keyword='%s'" % (row[0]) ).get("data")
    try:
        if(row[1] > 0):
            #val = "{:20,.2f}".format(float(row[1])*2/float(norm[0][0]))
            val = row[1]
            if(row[2] == 'S'): 
                yes_html +="<span style='font-size:%sem'>%s</span>" % (val, row[0])
            elif(row[2] == 'N'): 
                no_html +="<span style='font-size:%sem'>%s</span>" % (val, row[0])
            elif(row[2] == 'O'): 
                o_html +="<span style='font-size:%sem'>%s</span>" % (val, row[0])
            else:
                a_html +="<span style='font-size:%sem'>%s</span>" % (val, row[0])
    except Exception, ex:
        print "Error", ex


alld = scraperwiki.sqlite.execute("select name, id from votacao_deputado_br.deputados order by name" ).get("data")
options = ""
for d in alld:
    if(d[1] == start): options += "<option value='%s' selected='true'>%s</option>"%(d[1],d[0])
    else: options += "<option value='%s' selected='true'>%s</option>"%(d[1],d[0])

ddata = scraperwiki.sqlite.execute("select name from votacao_deputado_br.deputados where id=%d" % (start)  ).get("data")

print "<html><head><style>span {margin: 10px;}\n#yes {color:green; width:40%;float:left;}\n#no {color:red;width:40%;float:right;}\n#obs {color:purple;}\n#a {color:grey;}   \n body,html {margin:0; padding:0 5em; background:#f0f0f0; }</style></head><body><h1>"+ddata[0][0]+"</h1><div id='yes'><p>"+yes_html+"</p></div><div id='no'><p>"+no_html+"</p></div><br clear='both'><div id='obs'><p>"+o_html+"</p></div><div id='a'><p>"+a_html+"</p></div><form><select name='d_id'>"+options+"</select><input type='submit' value='Click!' /></form></body></html>"



import scraperwiki
import string

params = scraperwiki.utils.GET()
start = int(params.get("d_id", "522187"))

sourcescraper = 'camara_proposicoes_br'
scraperwiki.sqlite.attach(sourcescraper, "src")
scraperwiki.sqlite.attach('votacao_deputado_br')

sdata = scraperwiki.sqlite.execute("select keyword, count(distinct proposicao_id), vote as c from `indexacao` as i, votacao_deputado_br.votacao as v where  i.tipo=v.type and i.ano=v.year and i.numero=v.number and v.deputado_id=%d group by lower(keyword), vote" % (start) ) 

rows = sdata.get("data")

no_html = ""
yes_html = ""
o_html=""
a_html=""

for row in rows:
    #TODO cache this
    #norm = scraperwiki.sqlite.execute("select count(distinct proposicao_id) from `indexacao` where keyword='%s'" % (row[0]) ).get("data")
    try:
        if(row[1] > 0):
            #val = "{:20,.2f}".format(float(row[1])*2/float(norm[0][0]))
            val = row[1]
            if(row[2] == 'S'): 
                yes_html +="<span style='font-size:%sem'>%s</span>" % (val, row[0])
            elif(row[2] == 'N'): 
                no_html +="<span style='font-size:%sem'>%s</span>" % (val, row[0])
            elif(row[2] == 'O'): 
                o_html +="<span style='font-size:%sem'>%s</span>" % (val, row[0])
            else:
                a_html +="<span style='font-size:%sem'>%s</span>" % (val, row[0])
    except Exception, ex:
        print "Error", ex


alld = scraperwiki.sqlite.execute("select name, id from votacao_deputado_br.deputados order by name" ).get("data")
options = ""
for d in alld:
    if(d[1] == start): options += "<option value='%s' selected='true'>%s</option>"%(d[1],d[0])
    else: options += "<option value='%s' selected='true'>%s</option>"%(d[1],d[0])

ddata = scraperwiki.sqlite.execute("select name from votacao_deputado_br.deputados where id=%d" % (start)  ).get("data")

print "<html><head><style>span {margin: 10px;}\n#yes {color:green; width:40%;float:left;}\n#no {color:red;width:40%;float:right;}\n#obs {color:purple;}\n#a {color:grey;}   \n body,html {margin:0; padding:0 5em; background:#f0f0f0; }</style></head><body><h1>"+ddata[0][0]+"</h1><div id='yes'><p>"+yes_html+"</p></div><div id='no'><p>"+no_html+"</p></div><br clear='both'><div id='obs'><p>"+o_html+"</p></div><div id='a'><p>"+a_html+"</p></div><form><select name='d_id'>"+options+"</select><input type='submit' value='Click!' /></form></body></html>"



