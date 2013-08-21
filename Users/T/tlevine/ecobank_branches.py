from lxml.html import fromstring,tostring
from mechanize import Browser
from scraperwiki import swimport
keyify=swimport('keyify').keyify
URL="http://www.ecobank.com/branches.aspx?btype=3&rt=0&cid=74075"

def main():
  responses=download()
  for response in responses:
    d=parse(response)
    #save([],d)

def download():
  b=Browser()
  b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

  r1=b.open(URL)

  b.select_form(nr=0)
  b.set_all_readonly(False)
  b["__EVENTTARGET"] = "ctl00$CPH1$dgMain"
  b["__EVENTARGUMENT"] = "Page$2"
  b.find_control("ctl00$CPH1$tbSearch").disabled=True

  r2=b.submit()

  return [r1,r2]

def parse(response):
  x=fromstring(response.read())
  print tostring(x)
  tables=x.xpath('//table[@style="border-top:solid 1px #0076AF;"]')

  print map(tostring,tables)
  #assert 2==len(tables)

  #trs=tables[0].xpath('tr')
  #print reduce(reshape_branch_tr,trs,[])

  cells=[td.text_content() for td in tables[0].cssselect('td')]
  print cells
  print reduce(reshape_branch_cell,cells,[])

def reshape_branch_cell(reshaped,cell):
  if cell=="Branch area:":
    reshaped.append([])

  if 1==len(reshaped[-1]):
    reshaped[-1][-1]=cell
  elif 2==len(reshaped[-1]):
    reshaped[-1].append([keyify(cell)])
  return reshaped


def reshape_branch_tr(reshaped,tr):
  cells=[td.text_content() for td in tr.xpath('td')]
  assert 2==len(cells)

  if cells[0]=="Branch area:":
    reshaped.append({})


  reshaped[-1][keyify(cells[0])]=cells[1]
  return reshaped

main()