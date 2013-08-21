# Blank Ruby

require 'uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'
agent = Mechanize.new
#agent.user_agent = 'Friendly Mechanize Script"
#agent.user_agent_alias = 'Mac Safari'
agent.get('http://www.all-in.de/allgaeu_freizeit/kino/')

doc=agent.page.form_with('kinosrch').submit

for kino in doc.search('div[@class="box art"]')
  node = kino.at('div[@class="ressort"]')
  if (node == nil)
    puts "nil"
    daydate=""
  else
    dayarr = node.text.split
    day = dayarr[2]
    daydate = Date.strptime(day, "%d.%m.%Y")
    puts daydate
  end

  node = kino.at('h3/a')
  if (node == nil)
    puts "nil"
    dKino=""
    dOrt=""
  else
    temp = node.text
    temparr = temp.split(", ")
    dKino= temparr[0]
    dOrt = temparr[1]
    puts dKino
  end 

  node1 = kino.at('table/tbody')
  for movie in node1.search('tr')
    v = movie.at('td[1]')
    dFilm = v.search("strong").text
    puts dFilm
    alter= v.search("small").text
    dAlter= alter.to_s

    for i in 0..6 do
      v = movie.at('td['+(2+i).to_s()+']')
      dDatum = daydate+i
      timearr=v.inner_html.split("<br>")
      for onetime in timearr
        onetime = onetime.strip
        if onetime.length == 5
          dZeit = onetime

        data = {
          'kino' => dKino,
          'ort' => dOrt,
          'film' => dFilm,
          'alter' => dAlter[1..dAlter.length-2],
          'datum' => dDatum,
          'uhrzeit' => dZeit
        }
      puts data.to_json
      ScraperWiki.save_sqlite(unique_keys=['kino', 'film', 'datum', 'uhrzeit'], data=data) 
        else
          dZeit = "err"
        end
      end

    end
  end
puts "naechstes Kino"
#http://rubyforge.org/projects/instantrails/
end# Blank Ruby

require 'uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'
agent = Mechanize.new
#agent.user_agent = 'Friendly Mechanize Script"
#agent.user_agent_alias = 'Mac Safari'
agent.get('http://www.all-in.de/allgaeu_freizeit/kino/')

doc=agent.page.form_with('kinosrch').submit

for kino in doc.search('div[@class="box art"]')
  node = kino.at('div[@class="ressort"]')
  if (node == nil)
    puts "nil"
    daydate=""
  else
    dayarr = node.text.split
    day = dayarr[2]
    daydate = Date.strptime(day, "%d.%m.%Y")
    puts daydate
  end

  node = kino.at('h3/a')
  if (node == nil)
    puts "nil"
    dKino=""
    dOrt=""
  else
    temp = node.text
    temparr = temp.split(", ")
    dKino= temparr[0]
    dOrt = temparr[1]
    puts dKino
  end 

  node1 = kino.at('table/tbody')
  for movie in node1.search('tr')
    v = movie.at('td[1]')
    dFilm = v.search("strong").text
    puts dFilm
    alter= v.search("small").text
    dAlter= alter.to_s

    for i in 0..6 do
      v = movie.at('td['+(2+i).to_s()+']')
      dDatum = daydate+i
      timearr=v.inner_html.split("<br>")
      for onetime in timearr
        onetime = onetime.strip
        if onetime.length == 5
          dZeit = onetime

        data = {
          'kino' => dKino,
          'ort' => dOrt,
          'film' => dFilm,
          'alter' => dAlter[1..dAlter.length-2],
          'datum' => dDatum,
          'uhrzeit' => dZeit
        }
      puts data.to_json
      ScraperWiki.save_sqlite(unique_keys=['kino', 'film', 'datum', 'uhrzeit'], data=data) 
        else
          dZeit = "err"
        end
      end

    end
  end
puts "naechstes Kino"
#http://rubyforge.org/projects/instantrails/
end