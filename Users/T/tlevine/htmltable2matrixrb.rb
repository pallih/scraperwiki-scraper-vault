def test()
  require 'open-uri'
  doc = Nokogiri::HTML(open("http://www.coachusa.com/shortline/ss.details.asp?action=Lookup&c1=Ithaca&s1=NY&c2=New+York&s2=NY"))


def htmltable2matrix(ng,cell_xpath=None)
  #Takes an lxml tree whose current node is the table of interest
  trs=ng.xpath('tr')
  tablematrix=[]
  for tr in trs
    tablematrix_row=[]
    tds=tr.xpath('td')
    for td in tds:
      #If it has a colspan attribute, repeat that many times
      if 'colspan' in [key.lower() for key in td.attrib.keys()]:
        repeats=int(td.attrib['colspan'])
      else:
        repeats=1
      for r in range(repeats):
        if cell_xpath==None:
          cell=content_nodes(td)
        else:
          cell=''.join(td.xpath(cell_xpath))
        tablematrix_row.append(cell)
    tablematrix.append(tablematrix_row)
    del(tds)
  return tablematrixdef test()
  require 'open-uri'
  doc = Nokogiri::HTML(open("http://www.coachusa.com/shortline/ss.details.asp?action=Lookup&c1=Ithaca&s1=NY&c2=New+York&s2=NY"))


def htmltable2matrix(ng,cell_xpath=None)
  #Takes an lxml tree whose current node is the table of interest
  trs=ng.xpath('tr')
  tablematrix=[]
  for tr in trs
    tablematrix_row=[]
    tds=tr.xpath('td')
    for td in tds:
      #If it has a colspan attribute, repeat that many times
      if 'colspan' in [key.lower() for key in td.attrib.keys()]:
        repeats=int(td.attrib['colspan'])
      else:
        repeats=1
      for r in range(repeats):
        if cell_xpath==None:
          cell=content_nodes(td)
        else:
          cell=''.join(td.xpath(cell_xpath))
        tablematrix_row.append(cell)
    tablematrix.append(tablematrix_row)
    del(tds)
  return tablematrix