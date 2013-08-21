require 'scraperwiki'
require 'open-uri'
require 'nokogiri'

COLNAMES = [
  'Employer Name', 'Format', 'Location', 'Union', 'Local',
  'NAICS', 'NumberWrkrs', 'Expiration Date', 'Number Pages', 'OLMS File Number'
]

STATES = [
  'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

def OnePage(url)
  f = open(url)
  r = Nokogiri::HTML(f)
  tables = r.search("table")
  datatable = tables[2]
  rows = datatable.search("tr")
  zlist = rows[0].search("th")
  headers = zlist.map { |z| z.text.strip.gsub("#", "Number").gsub("*", "")  }

  if /Employer\s*Name/ =~ headers[0]
    headers[0] = 'Employer Name'
  elsif /NumberWorkers/ =~ headers[6]
    headers[6] = 'NumberWrkrs'
  elsif /Expiration\s*Date/ =~ headers[7]
    headers[7] = 'Expiration Date'
  elsif /Number\s*Pages/ =~ headers[8]
    headers[8] = 'Number Pages'
  end

  #assert(headers == COLNAMES, headers)
    
  data = [ ]
  rows.shift
  for row in rows
    cells = row.search('td,th')
    values = cells.map{ |cell| cell.text.strip }
    datum = Hash[COLNAMES.zip(values)]

    begin
      datum['NumberWrkrs'] = Integer(datum['NumberWrkrs'])
    rescue
      datum['NumberWrkrs'] = nil
    end

    begin
      datum['expiration_date'] = Date.strptime(datum['expiration_date'],"%m-%d-%y")
    rescue
      datum['expiration_date'] = nil
    end

    datum['state'] = datum['Location'][0..1]
    if datum['Location'] == "National"
      datum['state'] = ''
    elsif not STATES.include? datum['state']
      datum['state']='unknown'
    else
      data.push(datum)
    end
  end

  ScraperWiki.save([],data)
  #ScraperWiki.save(["OLMS File Number"],data)

end



url = "http://www.dol.gov/olms/regs/compliance/cba/"
fin = open(url)
r = Nokogiri::HTML(fin)
for a in r.search("div#content a")
  ah = String(a.attribute("href"))
  if ah != nil and ah[-3,3] == "htm"
    puts ah
    OnePage("http://www.dol.gov/olms/regs/compliance/cba/"+ah)
    sleep(4)
  end
end