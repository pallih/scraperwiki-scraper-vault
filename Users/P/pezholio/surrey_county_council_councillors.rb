require 'mechanize'
require 'nokogiri'
require 'yaml'

divisions = {}

divisions["Worplesdon"] =  14074
divisions["Farnham South"] = 14181
divisions["Earlswood and Reigate South"] = 13878
divisions["Epsom and Ewell North East"] = 13952
divisions["Ashtead"] = 13941
divisions["Redhill"] = 42744
divisions["Bisley, Chobham and West End"] = 14142
divisions["Guildford West"] = 42812
divisions["Camberley West"] = 14159
divisions["Waverley Eastern Villages"] = 14090
divisions["Dorking and the Holmwoods"] = 13907
divisions["Guildford South-West"] = 14077
divisions["Hersham"] = 13982
divisions["Windlesham"] = 14154
divisions["Caterham Hill"] = 13867
divisions["Cobham"] = 13985
divisions["Chertsey"] = 42824
divisions["Godalming North"] = 42747
divisions["Englefield Green"] = 14175
divisions["Dorking Rural"] = 13902
divisions["Guildford East"] = 13994
divisions["Ashford"] = 42786
divisions["Dorking Hills"] = 42777
divisions["Banstead East"] = 13955
divisions["Horsleys"] = 14013
divisions["Staines"] = 42784
divisions["Woking South"] = 14016
divisions["Haslemere"] = 14122
divisions["Horley East"] = 42742
divisions["Banstead South"] = 13895
divisions["Bookham and Fetcham West"] = 13967
divisions["Frimley Green and Mytchett"] = 14139
divisions["Epsom and Ewell West"] = 13971
divisions["Shere"] = 14007
divisions["Guildford South-East"] = 42810
divisions["Walton South & Oatlands"] = 14052
divisions["The Dittons"] = 13958
divisions["Guildford North"] = 42813
divisions["Waverley Western Villages"] = 14116
divisions["Caterham Valley"] = 13860
divisions["East Molesey and Esher"] = 14032
divisions["St Johns and Brookwood"] = 42787
divisions["Farnham Central"] = 14182
divisions["Horsell"] = 14019
divisions["Walton"] = 14037
divisions["Foxhills and Virginia Water"] = 42822
divisions["Knaphill"] = 14141
divisions["Epsom and Ewell South East"] = 13942
divisions["Cranleigh & Ewhurst"] = 42745
divisions["Pyrford"] = 14023
divisions["Stanwell and Stanwell Moor"] = 14041
divisions["Epsom and Ewell North"] = 13974
divisions["Woking Central"] = 14069
divisions["Godstone"] = 13872
divisions["Hinchley Wood, Claygate and Oxshott"] = 13960
divisions["West Molesey"] = 13977
divisions["Banstead West"] = 13890
divisions["Warlingham"] = 13859
divisions["Heatherside and Parkside"] = 14150
divisions["Sunbury Common & Ashford Common"] = 14035
divisions["Horley West"] = 42743
divisions["Leatherhead and Fetcham East"] = 42778
divisions["Farnham North"] = 14188
divisions["The Byfleets"] = 13989
divisions["Lower Sunbury and Halliford"] = 42782
divisions["Egham Hythe and Thorpe"] = 14179
divisions["Merstham and Reigate Hill"] = 13910
divisions["Camberley East"] = 14160
divisions["Ash"] = 42811
divisions["Oxted"] = 13854
divisions["Lingfield"] = 13840
divisions["Reigate Central"] = 13887
divisions["Weybridge"] = 14026
divisions["Staines South and Ashford West"] = 42785
divisions["Addlestone"] = 14058
divisions["Shalford"] = 42809
divisions["Woodham and New Haw"] = 42823
divisions["Godalming South, Milford & Witley"] = 42746
divisions["Epsom and Ewell South West"] = 42814
divisions["Laleham and Shepperton"] = 42783

BASE_URL = 'http://mycouncil.surreycc.gov.uk/'

url = BASE_URL + 'mgMemberIndex.aspx?VW=TABLE&PIC=1&FN=ALPHA' 

agent = Mechanize.new

page = agent.get(url)

doc = Nokogiri.HTML(page.content)

councillors = doc.search('.mgStatsTable tr')

councillors.shift

councillors.each do |councillor|
  
  details = {}

  url = BASE_URL + councillor.search('a')[0][:href]

  details["Name"] = councillor.search('a')[0].inner_text
  details[:url] = url
  details["Party"] = councillor.search('td')[2].inner_text
  details["Division"] = councillor.search('td')[3].inner_text
  details["DivisionID"] = divisions[councillor.search('td')[3].inner_text.strip]
  
  page = agent.get(url)
 
  doc = Nokogiri.HTML(page.content)

  ps = doc.search('//div[4]/p')

  ps.each do |p|
    if p.search('span').count > 0
      details[p.search('span').inner_text.force_encoding("BINARY").gsub(/\xC2\xA0/, '').gsub(/[^a-z]/i, '')] = Nokogiri.HTML(p.inner_html.gsub(p.search('span').inner_html.strip, '').strip.gsub('<br>', ' ')).inner_text.strip
    end
  end
  
  ScraperWiki.save([:url], details)

endrequire 'mechanize'
require 'nokogiri'
require 'yaml'

divisions = {}

divisions["Worplesdon"] =  14074
divisions["Farnham South"] = 14181
divisions["Earlswood and Reigate South"] = 13878
divisions["Epsom and Ewell North East"] = 13952
divisions["Ashtead"] = 13941
divisions["Redhill"] = 42744
divisions["Bisley, Chobham and West End"] = 14142
divisions["Guildford West"] = 42812
divisions["Camberley West"] = 14159
divisions["Waverley Eastern Villages"] = 14090
divisions["Dorking and the Holmwoods"] = 13907
divisions["Guildford South-West"] = 14077
divisions["Hersham"] = 13982
divisions["Windlesham"] = 14154
divisions["Caterham Hill"] = 13867
divisions["Cobham"] = 13985
divisions["Chertsey"] = 42824
divisions["Godalming North"] = 42747
divisions["Englefield Green"] = 14175
divisions["Dorking Rural"] = 13902
divisions["Guildford East"] = 13994
divisions["Ashford"] = 42786
divisions["Dorking Hills"] = 42777
divisions["Banstead East"] = 13955
divisions["Horsleys"] = 14013
divisions["Staines"] = 42784
divisions["Woking South"] = 14016
divisions["Haslemere"] = 14122
divisions["Horley East"] = 42742
divisions["Banstead South"] = 13895
divisions["Bookham and Fetcham West"] = 13967
divisions["Frimley Green and Mytchett"] = 14139
divisions["Epsom and Ewell West"] = 13971
divisions["Shere"] = 14007
divisions["Guildford South-East"] = 42810
divisions["Walton South & Oatlands"] = 14052
divisions["The Dittons"] = 13958
divisions["Guildford North"] = 42813
divisions["Waverley Western Villages"] = 14116
divisions["Caterham Valley"] = 13860
divisions["East Molesey and Esher"] = 14032
divisions["St Johns and Brookwood"] = 42787
divisions["Farnham Central"] = 14182
divisions["Horsell"] = 14019
divisions["Walton"] = 14037
divisions["Foxhills and Virginia Water"] = 42822
divisions["Knaphill"] = 14141
divisions["Epsom and Ewell South East"] = 13942
divisions["Cranleigh & Ewhurst"] = 42745
divisions["Pyrford"] = 14023
divisions["Stanwell and Stanwell Moor"] = 14041
divisions["Epsom and Ewell North"] = 13974
divisions["Woking Central"] = 14069
divisions["Godstone"] = 13872
divisions["Hinchley Wood, Claygate and Oxshott"] = 13960
divisions["West Molesey"] = 13977
divisions["Banstead West"] = 13890
divisions["Warlingham"] = 13859
divisions["Heatherside and Parkside"] = 14150
divisions["Sunbury Common & Ashford Common"] = 14035
divisions["Horley West"] = 42743
divisions["Leatherhead and Fetcham East"] = 42778
divisions["Farnham North"] = 14188
divisions["The Byfleets"] = 13989
divisions["Lower Sunbury and Halliford"] = 42782
divisions["Egham Hythe and Thorpe"] = 14179
divisions["Merstham and Reigate Hill"] = 13910
divisions["Camberley East"] = 14160
divisions["Ash"] = 42811
divisions["Oxted"] = 13854
divisions["Lingfield"] = 13840
divisions["Reigate Central"] = 13887
divisions["Weybridge"] = 14026
divisions["Staines South and Ashford West"] = 42785
divisions["Addlestone"] = 14058
divisions["Shalford"] = 42809
divisions["Woodham and New Haw"] = 42823
divisions["Godalming South, Milford & Witley"] = 42746
divisions["Epsom and Ewell South West"] = 42814
divisions["Laleham and Shepperton"] = 42783

BASE_URL = 'http://mycouncil.surreycc.gov.uk/'

url = BASE_URL + 'mgMemberIndex.aspx?VW=TABLE&PIC=1&FN=ALPHA' 

agent = Mechanize.new

page = agent.get(url)

doc = Nokogiri.HTML(page.content)

councillors = doc.search('.mgStatsTable tr')

councillors.shift

councillors.each do |councillor|
  
  details = {}

  url = BASE_URL + councillor.search('a')[0][:href]

  details["Name"] = councillor.search('a')[0].inner_text
  details[:url] = url
  details["Party"] = councillor.search('td')[2].inner_text
  details["Division"] = councillor.search('td')[3].inner_text
  details["DivisionID"] = divisions[councillor.search('td')[3].inner_text.strip]
  
  page = agent.get(url)
 
  doc = Nokogiri.HTML(page.content)

  ps = doc.search('//div[4]/p')

  ps.each do |p|
    if p.search('span').count > 0
      details[p.search('span').inner_text.force_encoding("BINARY").gsub(/\xC2\xA0/, '').gsub(/[^a-z]/i, '')] = Nokogiri.HTML(p.inner_html.gsub(p.search('span').inner_html.strip, '').strip.gsub('<br>', ' ')).inner_text.strip
    end
  end
  
  ScraperWiki.save([:url], details)

end