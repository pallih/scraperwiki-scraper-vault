import scraperwiki
import lxml.html


def get_html(url, localFile=True):
    if localFile:
        with open(url, 'r') as f:
            html = f.read()
    else:
        html = scraperwiki.scrape(url)

    return html


def read_total_unidades_educativas_por_provincia(url=None):
    html = get_html(url, localFile=False)
    root = lxml.html.fromstring(html)
    mainTable = root.cssselect('body > div > table')[2]

    for (index, tr) in enumerate(mainTable.cssselect('tr')):
        if index > 0:
            tds = tr.cssselect('td')
            if 6 == len(tds):
                link = tds[5].cssselect('a')[0].attrib['href']
                data = {
                    'nro': int(tds[0].text),
                    'departamento': tds[1].text,
                    'provincia': tds[2].text,
                    'localidad': tds[3].text,
                    'distrito': tds[4].text,
                    'cantidad': int(tds[5].text_content()),
                    'url': 'http://www.mirabolivia.com/edu/' + link
                }
                scraperwiki.sqlite.save(unique_keys=['nro'], data=data, table_name='ueducativas_por_provincia')


def read_unidad_educativa_data():
    ue_por_provincia = scraperwiki.sqlite.select(" * from ueducativas_por_provincia")
    for ue in ue_por_provincia:
        print ue
        html = get_html(url=ue['url'], localFile=False)
        root = lxml.html.fromstring(html)
        mainTable = root.cssselect('body > div > table')[2]

        ueducativa_data = []
        for (index, tr) in enumerate(mainTable.cssselect('tr')):
            if index > 0:
                tds = tr.cssselect('td')
                if 12 == len(tds):
                    url = tds[2].cssselect('a')[0].attrib['href']
                    data = {
                        'id': int(tds[1].text),
                        'unidad_educativa': tds[2].text_content(),
                        'direccion': tds[3].text,
                        'zona': tds[4].text,
                        'distrito': tds[5].text,
                        'departamento': tds[6].text,
                        'provincia': tds[7].text,
                        'seccion': tds[8].text,
                        'canton': tds[9].text,
                        'localidad': tds[10].text,
                        'total_alumnos': tds[11].text,
                        'url': 'http://www.mirabolivia.com/edu/' + url
                    }
                    ueducativa_data.append(data)

        for ueducativa in ueducativa_data:
            html = scraperwiki.scrape(ueducativa['url'])
            root = lxml.html.fromstring(html)
            infoTable = root.cssselect('body > div > table')[2]
            trs = infoTable.cssselect('tr')
            ueducativa['codigo_unidad_educativa'] = trs[2].cssselect('td')[1].text
            ueducativa['codigo_edificio'] = trs[5].cssselect('td')[1].text

            dataTable = root.cssselect('body > div > table')[3]
            trs = dataTable.cssselect('tr')
            tdsInicial = trs[1].cssselect('td')
            ueducativa['inicial_efectivos'] = tdsInicial[1].text
            ueducativa['inicial_retirados'] = tdsInicial[2].text
            ueducativa['inicial_total'] = tdsInicial[3].text

            tdsPrimaria = trs[2].cssselect('td')
            ueducativa['primaria_efectivos'] = tdsPrimaria[1].text
            ueducativa['primaria_retirados'] = tdsPrimaria[2].text
            ueducativa['primaria_total'] = tdsPrimaria[3].text

            tdsSecundaria = trs[3].cssselect('td')
            ueducativa['secundaria_efectivos'] = tdsSecundaria[1].text
            ueducativa['secundaria_retirados'] = tdsSecundaria[2].text
            ueducativa['secundaria_total'] = tdsSecundaria[3].text

            tdsTotal = trs[4].cssselect('td')
            ueducativa['total_efectivos'] = tdsTotal[1].text
            ueducativa['total_retirados'] = tdsTotal[2].text
            ueducativa['total_alumnos'] = tdsTotal[3].text

            scraperwiki.sqlite.save(unique_keys=['id'], data=ueducativa, table_name='ueducativas_data')


urlbase = 'http://www.mirabolivia.com/edu/ueducativa_listaprovloc.php'
read_total_unidades_educativas_por_provincia(urlbase)
read_unidad_educativa_data()

