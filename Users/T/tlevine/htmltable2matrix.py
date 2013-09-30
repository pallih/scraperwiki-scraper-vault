from lxml.html import fromstring,tostring

def htmltable2matrix(tablehtml,cell_xpath=None):
    """
    Takes an html table or an lxml tree whose current node is the table of interest

    Optionally takes an xpath to be applied at the cell level
    """
    if type(tablehtml) in [str, unicode]:
        tablehtml=fromstring(tablehtml)
    trs=tablehtml.cssselect('tr')
    tablematrix=[]
    for tr in trs:
        tablematrix_row=[]
        tds=tr.cssselect('td')
        for td in tds:
            #If it has a colspan attribute, repeat that many times
            if 'colspan' in [key.lower() for key in td.attrib.keys()]:
                repeats=int(td.attrib['colspan'])
            else:
                repeats=1

            for r in range(repeats):
                if cell_xpath==None:
                    cell=td.text_content()
                else:
                    cell=''.join(td.xpath(cell_xpath))
                tablematrix_row.append(cell)

        tablematrix.append(tablematrix_row)

    return tablematrix
from lxml.html import fromstring,tostring

def htmltable2matrix(tablehtml,cell_xpath=None):
    """
    Takes an html table or an lxml tree whose current node is the table of interest

    Optionally takes an xpath to be applied at the cell level
    """
    if type(tablehtml) in [str, unicode]:
        tablehtml=fromstring(tablehtml)
    trs=tablehtml.cssselect('tr')
    tablematrix=[]
    for tr in trs:
        tablematrix_row=[]
        tds=tr.cssselect('td')
        for td in tds:
            #If it has a colspan attribute, repeat that many times
            if 'colspan' in [key.lower() for key in td.attrib.keys()]:
                repeats=int(td.attrib['colspan'])
            else:
                repeats=1

            for r in range(repeats):
                if cell_xpath==None:
                    cell=td.text_content()
                else:
                    cell=''.join(td.xpath(cell_xpath))
                tablematrix_row.append(cell)

        tablematrix.append(tablematrix_row)

    return tablematrix
