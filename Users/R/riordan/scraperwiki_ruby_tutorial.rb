require 'open-uri'
require 'scraperwiki'
require 'nokogiri'


COLNAMES =   [
      'employer','download','location','union',
      'local', 'naics', 'num_workers', 'expiration_date'
  ]


URL='http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'

#get URLs from table



def parseTable(url)

  download = open(url)
  #puts download.read

  html = Nokogiri::HTML(download)
  tables = html.search('table')
  table = tables[2]

  trs = table.search('tr')

  trs.shift #pop the first item off. there must be a better way to do this and iterate withouththe first in a list
  for tr in trs[0..4]
    cells = tr.search('td,th')
    values = cells.map{|cell| cell.text}
    #puts COLNAMES.join(',')
    #puts values.join(',')
    data = Hash[COLNAMES.zip(values)]
    data['num_workers'] = Integer(data['num_workers']) #cleans up number of workers so its an integer
    data['state'] = data['location'][0..1]
      if not [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    ].include? data['state']
        data['state'] = 'unknown'
    end

    data['expiration_date'] = Date.strptime(data['expiration_date'], "%m-%d-%y")

    ScraperWiki.save([],data)
  end
end




#parseTable(URL)


cbapage = open('http://www.dol.gov/olms/regs/compliance/cba/')
html = Nokogiri::HTML(cbapage)
puts html