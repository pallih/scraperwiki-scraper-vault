import scraperwiki
import lxml.html


def create_table_provincias():
    query = 'drop table if exists unidades_educativas_por_provincia;'
    scraperwiki.sqlite.execute(query)

    query = 'create table unidades_educativas_por_provincia ' \
            ' ( nro int, ' \
            ' departamento string, ' \
            ' provincia string, ' \
            ' localidad string, ' \
            ' distrito string, ' \
            ' cantidad int, ' \
            ' url string ); '

    scraperwiki.sqlite.execute(query, verbose=True)


def insert_data_unidades_educativas_por_provincia(data):
    query = ' insert into unidades_educativas_por_provincia ' \
            ' (nro, departamento, provincia, localidad, distrito, cantidad, url ) ' \
            ' values (?,  ?, ?, ?, ?, ?, ?) '
    params = (
        data['nro'], data['departamento'], data['provincia'], data['localidad'],
        data['distrito'], data['cantidad'], data['url']
    )

    print data
    scraperwiki.sqlite.execute(query, params, verbose=True)
    scraperwiki.sqlite.commit(True)


def read_html(url=None):
    if None == url:
        with open('ueducativa.html', 'r') as f:
            html = f.read()
    else:
        html = scraperwiki.scrape(url)

    return html


def get_unidades_educativas_por_provincia(url=None):
    html = read_html(url)
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
                insert_data_unidades_educativas_por_provincia(data)


url = 'http://www.mirabolivia.com/edu/ueducativa_listaprovloc.php'

create_table_provincias()
get_unidades_educativas_por_provincia(url)


import scraperwiki
import lxml.html


def create_table_provincias():
    query = 'drop table if exists unidades_educativas_por_provincia;'
    scraperwiki.sqlite.execute(query)

    query = 'create table unidades_educativas_por_provincia ' \
            ' ( nro int, ' \
            ' departamento string, ' \
            ' provincia string, ' \
            ' localidad string, ' \
            ' distrito string, ' \
            ' cantidad int, ' \
            ' url string ); '

    scraperwiki.sqlite.execute(query, verbose=True)


def insert_data_unidades_educativas_por_provincia(data):
    query = ' insert into unidades_educativas_por_provincia ' \
            ' (nro, departamento, provincia, localidad, distrito, cantidad, url ) ' \
            ' values (?,  ?, ?, ?, ?, ?, ?) '
    params = (
        data['nro'], data['departamento'], data['provincia'], data['localidad'],
        data['distrito'], data['cantidad'], data['url']
    )

    print data
    scraperwiki.sqlite.execute(query, params, verbose=True)
    scraperwiki.sqlite.commit(True)


def read_html(url=None):
    if None == url:
        with open('ueducativa.html', 'r') as f:
            html = f.read()
    else:
        html = scraperwiki.scrape(url)

    return html


def get_unidades_educativas_por_provincia(url=None):
    html = read_html(url)
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
                insert_data_unidades_educativas_por_provincia(data)


url = 'http://www.mirabolivia.com/edu/ueducativa_listaprovloc.php'

create_table_provincias()
get_unidades_educativas_por_provincia(url)


import scraperwiki
import lxml.html


def create_table_provincias():
    query = 'drop table if exists unidades_educativas_por_provincia;'
    scraperwiki.sqlite.execute(query)

    query = 'create table unidades_educativas_por_provincia ' \
            ' ( nro int, ' \
            ' departamento string, ' \
            ' provincia string, ' \
            ' localidad string, ' \
            ' distrito string, ' \
            ' cantidad int, ' \
            ' url string ); '

    scraperwiki.sqlite.execute(query, verbose=True)


def insert_data_unidades_educativas_por_provincia(data):
    query = ' insert into unidades_educativas_por_provincia ' \
            ' (nro, departamento, provincia, localidad, distrito, cantidad, url ) ' \
            ' values (?,  ?, ?, ?, ?, ?, ?) '
    params = (
        data['nro'], data['departamento'], data['provincia'], data['localidad'],
        data['distrito'], data['cantidad'], data['url']
    )

    print data
    scraperwiki.sqlite.execute(query, params, verbose=True)
    scraperwiki.sqlite.commit(True)


def read_html(url=None):
    if None == url:
        with open('ueducativa.html', 'r') as f:
            html = f.read()
    else:
        html = scraperwiki.scrape(url)

    return html


def get_unidades_educativas_por_provincia(url=None):
    html = read_html(url)
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
                insert_data_unidades_educativas_por_provincia(data)


url = 'http://www.mirabolivia.com/edu/ueducativa_listaprovloc.php'

create_table_provincias()
get_unidades_educativas_por_provincia(url)


import scraperwiki
import lxml.html


def create_table_provincias():
    query = 'drop table if exists unidades_educativas_por_provincia;'
    scraperwiki.sqlite.execute(query)

    query = 'create table unidades_educativas_por_provincia ' \
            ' ( nro int, ' \
            ' departamento string, ' \
            ' provincia string, ' \
            ' localidad string, ' \
            ' distrito string, ' \
            ' cantidad int, ' \
            ' url string ); '

    scraperwiki.sqlite.execute(query, verbose=True)


def insert_data_unidades_educativas_por_provincia(data):
    query = ' insert into unidades_educativas_por_provincia ' \
            ' (nro, departamento, provincia, localidad, distrito, cantidad, url ) ' \
            ' values (?,  ?, ?, ?, ?, ?, ?) '
    params = (
        data['nro'], data['departamento'], data['provincia'], data['localidad'],
        data['distrito'], data['cantidad'], data['url']
    )

    print data
    scraperwiki.sqlite.execute(query, params, verbose=True)
    scraperwiki.sqlite.commit(True)


def read_html(url=None):
    if None == url:
        with open('ueducativa.html', 'r') as f:
            html = f.read()
    else:
        html = scraperwiki.scrape(url)

    return html


def get_unidades_educativas_por_provincia(url=None):
    html = read_html(url)
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
                insert_data_unidades_educativas_por_provincia(data)


url = 'http://www.mirabolivia.com/edu/ueducativa_listaprovloc.php'

create_table_provincias()
get_unidades_educativas_por_provincia(url)


