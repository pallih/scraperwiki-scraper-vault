#### Blank Ruby# Blank Ruby
require 'nokogiri'
require 'open-uri'

## url = http://en.wikipedia.org/wiki/List_of_telephone_operating_companies
## data = Nokogiri::HTML(open(url))

require 'net/http'
source = Net::HTTP.get('en.wikipedia.org','/wiki/List_of_telephone_operating_companies')
url = source.gsub('<h2>','<h1>cblock<h1><h2>')
data = Nokogiri::HTML(url)

# data = Nokogiri::HTML(open("c:/downloads/test2.htm"))

count = 0
for el in data.css('h1').children 
  count = count + 1   
  next if count < 3
  next if el.text.length < 2
  next if el.text.index("List of")
  ### break if count > 100   ### this is a limiter
#puts ">>>>> " + el + " <<<<<"
  if el.text.index(" [edit]")
    result = el.text.sub(" [edit]","")
    if el.text.downcase.index("operator")
      otype = result.split[0]
#puts "otype > " + result
    else
      country = result
#puts "country > " + country
      break if country == "See also"
    end
    next
  end
  for el2 in el.children
    next if el2.text.length < 2 or el2.text == "[edit]"
#puts "** > " + el2
    optext = el2.text+"//"
    optext = optext.gsub(/[()]/, '/')
    opname = optext.split("/")
    operator = opname[0]
    parent = opname[1]
#puts "op > " + el2.text
    if not el2.css('a').first.nil? 
      link = el2.css('a').first.attributes["href"].value
#puts "link > " + link
    else
      link = ""
    end
    if not operator.nil? 
      company = {
        operator: operator,
        parent: parent,
        link: link,
        otype: otype, 
        country: country
      }
puts operator +" : "+link+" : "+otype+" : "+country
      ScraperWiki::save_sqlite(['operator'], company)
    end
  end

end
#### Blank Ruby# Blank Ruby
require 'nokogiri'
require 'open-uri'

## url = http://en.wikipedia.org/wiki/List_of_telephone_operating_companies
## data = Nokogiri::HTML(open(url))

require 'net/http'
source = Net::HTTP.get('en.wikipedia.org','/wiki/List_of_telephone_operating_companies')
url = source.gsub('<h2>','<h1>cblock<h1><h2>')
data = Nokogiri::HTML(url)

# data = Nokogiri::HTML(open("c:/downloads/test2.htm"))

count = 0
for el in data.css('h1').children 
  count = count + 1   
  next if count < 3
  next if el.text.length < 2
  next if el.text.index("List of")
  ### break if count > 100   ### this is a limiter
#puts ">>>>> " + el + " <<<<<"
  if el.text.index(" [edit]")
    result = el.text.sub(" [edit]","")
    if el.text.downcase.index("operator")
      otype = result.split[0]
#puts "otype > " + result
    else
      country = result
#puts "country > " + country
      break if country == "See also"
    end
    next
  end
  for el2 in el.children
    next if el2.text.length < 2 or el2.text == "[edit]"
#puts "** > " + el2
    optext = el2.text+"//"
    optext = optext.gsub(/[()]/, '/')
    opname = optext.split("/")
    operator = opname[0]
    parent = opname[1]
#puts "op > " + el2.text
    if not el2.css('a').first.nil? 
      link = el2.css('a').first.attributes["href"].value
#puts "link > " + link
    else
      link = ""
    end
    if not operator.nil? 
      company = {
        operator: operator,
        parent: parent,
        link: link,
        otype: otype, 
        country: country
      }
puts operator +" : "+link+" : "+otype+" : "+country
      ScraperWiki::save_sqlite(['operator'], company)
    end
  end

end
