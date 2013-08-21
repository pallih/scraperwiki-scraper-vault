require 'open-uri'
require 'scraperwiki'
require 'nokogiri'

MENU="http://www.dol.gov/olms/regs/compliance/cba/"
URL="http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm"

def slugify(text)
  text=text
    .gsub('#','num')
    .gsub(' ','_')
    .gsub(/[*\r\n]/,'')
  return text
end

def getTable(tree)
  tables=tree.search('table')
  table=tables[2]
  return table
end

def getRowText(tableRow)
  cells=tableRow.search('td,th')
  rowText=cells.map {|cell| cell.text}
  return rowText
end

def saveTable(table)
  tableRows=table.search('tr')

  header=tableRows.shift
  headerText=getRowText(header)
  columnNames=headerText.map{|cellText| slugify(cellText)}

  for tableRow in tableRows
    rowText=getRowText(tableRow)
    data=Hash[columnNames.zip(rowText)]
    data['pdf']=tableRow.search('a')[0].attributes()['href']
    ScraperWiki.save([],data,'listings')
  end
end

def parseListingsPage(url)
  raw=open(url)
  tree=Nokogiri::HTML(raw)
  table=getTable(tree)

  #Save the table
  saveTable(table)
end

def sector(href)
  if href[3,4]=="a_"
    return "private"
  else if href[3,4]=="au"
    return "public"
  end
end

def parseMenuPage(menuurl)
  raw=open(url)
  tree=Nokogiri::HTML(raw)
  data=[]
  links=tree.search('#content > p > a')
  links.map{|a| {
    "range"=>a.text,
    "href"=>a.attributes()['href'],
    "sector"=>sector(a)
  } }
  save(['href'],links,'menu')
end

parseMenuPage(MENU)
hrefs=ScraperWiki.Select('`href` from `menu`')
#for href in hrefs
#  parseListingsPage(href)
#end