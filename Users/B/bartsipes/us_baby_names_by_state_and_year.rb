require 'nokogiri'

state_abbreviations = <<eos
AL
AK
AZ
AR
CA
CO
CT
DE
FL
GA
HI
ID
IL
IN
IA
KS
KY
LA
ME
MD
MA
MI
MN
MS
MO
MT
NE
NV
NH
NJ
NM
NY
NC
ND
OH
OK
OR
PA
RI
SC
SD
TN
TX
UT
VT
VA
WA
WV
WI
WY
eos
state_abbreviations = state_abbreviations.split("\n")

for state in state_abbreviations
  for year in 1971..1980
    html = ScraperWiki.scrape("http://www.socialsecurity.gov/cgi-bin/namesbystate.cgi", {"year"=>year, "state"=>state})

    doc = Nokogiri::HTML(html)
    for v in doc.search("table[@bordercolor='#aaabbb'] tr[@align='right']")
      cells = v.search('td')
      data = {
        'year' => year,
        'state' => state,
        'rank' => cells[0].inner_html,
        'male_name' => cells[1].inner_html,
        'male_count' => cells[2].inner_html,
        'female_name' => cells[3].inner_html,
        'female_count' => cells[4].inner_html
      }
      ScraperWiki.save_sqlite(unique_keys=['year','rank'], data=data)
    end
  end
end

