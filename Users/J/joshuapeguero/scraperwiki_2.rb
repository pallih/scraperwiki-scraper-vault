# Blank Ruby

require 'open-uri'
require 'scraperwiki'
require 'nokogiri'

COLNAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

URL='http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'

def parseTable(url)
  download = open(URL)

  html = Nokogiri::HTML(download)
  tables = html.search('table')
  table = tables[2]

  trs = table.search('tr')

  trs.shift
  for tr in trs
    cells = tr.search('td,th')
    values = cells.map{|cell| cell.text}
    data = Hash[COLNAMES.zip(values)]
    puts data
    data['num_workers'] = Integer(data['num_workers'])
    data['state'] = data['location'][0.1]
    if [
      'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
      'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
      'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
      'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
      'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
     ].include? data['state']
       data['state']='unknown'
      end
      data['expiration_date'] = Date.strptime(data['expiration_date'],"%m-%d-%y")
      ScraperWiki.save([],data)
   end
end

def sector(a)
  href=a.attributes['href']
  if href[0..4]=="Cba_"
    return "private"
  elsif href[0..5]=="Cbau_"
    return "public"
  else
    return 'NA'
  end
end

menu=open('http://www.dol.gov/olms/regs/compliance/cba/')
html=Nokogiri::HTML(menu)
linknodes=html.search('#content > p > a')

relativeLinks=linknodes.map{|thelink| thelink.attributes['href']}
absoluteUrls=relativeLinks.map{|link| 'http://www.dol.gov/olms/regs/compliance/cba/'+link}

for url in absoluteUrls
  parseTable(url)
end
