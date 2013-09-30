require 'open-uri'
require 'scraperwiki'
require 'nokogiri'

# http://nokogiri.org/

  #  <a href="/brewer/1">3 Fonteinen</a>
  # <a href="/beer/1">Oude Geuze Vintage </a>

def get_content(fragment)
  frag = Nokogiri::Slop(fragment);
  title= frag.a.content
  id= frag.a["href"].split('/')[2].to_i
  return [id,title]
end


#e = get_content("<a href='/brewer/1'>3 Fonteinen</a>")
#puts e[0]
#puts e[1]


def scrape_venue()
  doc = Nokogiri::HTML(open("http://www.alehunt.com/venue/"))
  table = doc.search("table[@id='venue-table']")
  trs = table.search('tr')
  trs.shift
  for tr in trs
    cells = tr.search('td')
    urlparts = get_content(cells[0].inner_html)
    data = {
      'id' => urlparts[0],
      'name' => urlparts[1],
      'city' => cells[1].inner_html.strip,
      'country' => cells[2].inner_html.strip,
      'nr_of_beers' => cells[3].inner_html.to_i
    }
    ScraperWiki.save_sqlite(unique_keys=['id'], data=data, table_name="venue", verbose=0)
    #ScraperWiki.save_sqlite(unique_keys, data, table_name="swdata", verbose=2)
  end
end

def scrape_beer()
  doc = Nokogiri::HTML(open("http://www.alehunt.com/beer/"))
  table = doc.search("table[@id='beer-table']")
  trs = table.search('tr')
  trs.shift
  for tr in trs
    cells = tr.search('td')
#            <a href="/brewer/1">3 Fonteinen</a>
#            <a href="/beer/1">Oude Geuze Vintage </a>
    urlpartsBrewery = get_content(cells[0].inner_html)
    urlpartsBeer = get_content(cells[1].inner_html)
    data = {
      'brewery_id' => urlpartsBrewery[0],
      'brewery' => urlpartsBrewery[1],
      'beer_id' => urlpartsBeer[0],
      'beer' => urlpartsBeer[1],
      'style' => cells[2].inner_html.strip
    }
    ScraperWiki.save_sqlite(unique_keys=['brewery_id','beer_id'], data=data, table_name="beer", verbose=0)
  end
end

def scrape_brewer()
  doc = Nokogiri::HTML(open("http://www.alehunt.com/brewer/"))
  table = doc.search("table[@id='brewer-table']")
  trs = table.search('tr')
  trs.shift
  for tr in trs
    cells = tr.search('td')
    urlpartsBrewer = get_content(cells[0].inner_html)
#            <img src="/content/images/flags/be.png" alt="be" />            Belgium        </td>
    frag = Nokogiri::HTML.fragment(cells[1].inner_html);
    data = {
      'brewer_id' => urlpartsBrewer[0],
      'brewer' => urlpartsBrewer[1],
      'country' => frag.text.strip,
      'nr_of_beers' => cells[2].inner_html.strip.to_i
    }
    ScraperWiki.save_sqlite(unique_keys=['brewer_id'], data=data, table_name="brewer", verbose=0)
  end
end

def scrape_style()
  doc = Nokogiri::HTML(open("http://www.alehunt.com/beerType/"))
  table = doc.search("table[@id='beer-table']")
  trs = table.search('tr')
  trs.shift
  for tr in trs
    cells = tr.search('td')
    urlparts = get_content(cells[0].inner_html)
    data = {
      'style_id' => urlparts[0],
      'style' => urlparts[1],
      'nr_of_beers' => cells[1].inner_html.strip.to_i
    }
    ScraperWiki.save_sqlite(unique_keys=['style_id'], data=data, table_name="style", verbose=0)
  end
end


## http://www.alehunt.com/venue/28

def scrape_one_venue(nr)
# Fanene som er tilgjengelige:


# først finne keg: <div class="tab-pane active" id="keg">
# <div class="tab-pane active" id="keg">
# som har sin table:
# <table id="beer-table" class="table table-striped table-condensed">

# keg og bottle har samme format

# keg">Keg (14)</a></li>
#  Hornbeer  Blonde   Abbey Blonde   today
# Brewery
# Beer
# Style
# Updated

#<tr>
#    <td>
#        <img src="/content/images/flags/us.png" alt="us" />  <a href="/brewer/176">Rogue Ales</a>
#    </td>
#    <td>
#        <a href="/beer/931">Mogul Madness</a>
#    </td>
#    <td>
#        Black India Pale Ale    </td>
#    <td>
#        yesterday    </td>
#    <td>
#        </td>
#</tr>


# bottle">Bottle (57)</a></li>
#  Beer Here  Black Cat   Black India Pale Ale   Friday

# Brewery
# Beer
# Style
# Updated

#<tr>
#    <td>
#        <img src="/content/images/flags/dk.png" alt="dk" />  <a href="/brewer/29">Beer Here</a>
#    </td>
#    <td>
#        <a href="/beer/1055">Weed</a>
#    </td>
#    <td>
#        Smoked    </td>
#    <td>
#        about three weeks ago    </td>
#    <td>
#        </td>
#</tr>

# cask">Cask (0)</a></li>



######################

# history">History (46)</a></li>
# Keg   Schouskjelleren Mikrobryggeri  Cascale   Golden Ale/Blond Ale   yesterday

# <th>On</th>
# <th>Brewery</th>
# <th>Beer</th>
# <th>Style</th>
# <th>Removed</th>

#format:
#<tr>
#    <td>
#        Keg    </td>
#    <td>
#        <img src="/content/images/flags/gb.png" alt="gb" />  <a href="/brewer/70">Thornbridge Brewery</a>
#    </td>
#    <td>
#        <a href="/beer/1044">Versa</a>
#    </td>
#    <td>
#        German Hefeweizen    </td>
#    <td>
#        about three weeks ago    </td>
#</tr>    

######################
# info">Place info</a></li>
# denne har bare en stor html blobb, lagre hele

end

scrape_one_venue(28)



#scrape_venue()
#scrape_beer()
#scrape_brewer()
# scrape_style()require 'open-uri'
require 'scraperwiki'
require 'nokogiri'

# http://nokogiri.org/

  #  <a href="/brewer/1">3 Fonteinen</a>
  # <a href="/beer/1">Oude Geuze Vintage </a>

def get_content(fragment)
  frag = Nokogiri::Slop(fragment);
  title= frag.a.content
  id= frag.a["href"].split('/')[2].to_i
  return [id,title]
end


#e = get_content("<a href='/brewer/1'>3 Fonteinen</a>")
#puts e[0]
#puts e[1]


def scrape_venue()
  doc = Nokogiri::HTML(open("http://www.alehunt.com/venue/"))
  table = doc.search("table[@id='venue-table']")
  trs = table.search('tr')
  trs.shift
  for tr in trs
    cells = tr.search('td')
    urlparts = get_content(cells[0].inner_html)
    data = {
      'id' => urlparts[0],
      'name' => urlparts[1],
      'city' => cells[1].inner_html.strip,
      'country' => cells[2].inner_html.strip,
      'nr_of_beers' => cells[3].inner_html.to_i
    }
    ScraperWiki.save_sqlite(unique_keys=['id'], data=data, table_name="venue", verbose=0)
    #ScraperWiki.save_sqlite(unique_keys, data, table_name="swdata", verbose=2)
  end
end

def scrape_beer()
  doc = Nokogiri::HTML(open("http://www.alehunt.com/beer/"))
  table = doc.search("table[@id='beer-table']")
  trs = table.search('tr')
  trs.shift
  for tr in trs
    cells = tr.search('td')
#            <a href="/brewer/1">3 Fonteinen</a>
#            <a href="/beer/1">Oude Geuze Vintage </a>
    urlpartsBrewery = get_content(cells[0].inner_html)
    urlpartsBeer = get_content(cells[1].inner_html)
    data = {
      'brewery_id' => urlpartsBrewery[0],
      'brewery' => urlpartsBrewery[1],
      'beer_id' => urlpartsBeer[0],
      'beer' => urlpartsBeer[1],
      'style' => cells[2].inner_html.strip
    }
    ScraperWiki.save_sqlite(unique_keys=['brewery_id','beer_id'], data=data, table_name="beer", verbose=0)
  end
end

def scrape_brewer()
  doc = Nokogiri::HTML(open("http://www.alehunt.com/brewer/"))
  table = doc.search("table[@id='brewer-table']")
  trs = table.search('tr')
  trs.shift
  for tr in trs
    cells = tr.search('td')
    urlpartsBrewer = get_content(cells[0].inner_html)
#            <img src="/content/images/flags/be.png" alt="be" />            Belgium        </td>
    frag = Nokogiri::HTML.fragment(cells[1].inner_html);
    data = {
      'brewer_id' => urlpartsBrewer[0],
      'brewer' => urlpartsBrewer[1],
      'country' => frag.text.strip,
      'nr_of_beers' => cells[2].inner_html.strip.to_i
    }
    ScraperWiki.save_sqlite(unique_keys=['brewer_id'], data=data, table_name="brewer", verbose=0)
  end
end

def scrape_style()
  doc = Nokogiri::HTML(open("http://www.alehunt.com/beerType/"))
  table = doc.search("table[@id='beer-table']")
  trs = table.search('tr')
  trs.shift
  for tr in trs
    cells = tr.search('td')
    urlparts = get_content(cells[0].inner_html)
    data = {
      'style_id' => urlparts[0],
      'style' => urlparts[1],
      'nr_of_beers' => cells[1].inner_html.strip.to_i
    }
    ScraperWiki.save_sqlite(unique_keys=['style_id'], data=data, table_name="style", verbose=0)
  end
end


## http://www.alehunt.com/venue/28

def scrape_one_venue(nr)
# Fanene som er tilgjengelige:


# først finne keg: <div class="tab-pane active" id="keg">
# <div class="tab-pane active" id="keg">
# som har sin table:
# <table id="beer-table" class="table table-striped table-condensed">

# keg og bottle har samme format

# keg">Keg (14)</a></li>
#  Hornbeer  Blonde   Abbey Blonde   today
# Brewery
# Beer
# Style
# Updated

#<tr>
#    <td>
#        <img src="/content/images/flags/us.png" alt="us" />  <a href="/brewer/176">Rogue Ales</a>
#    </td>
#    <td>
#        <a href="/beer/931">Mogul Madness</a>
#    </td>
#    <td>
#        Black India Pale Ale    </td>
#    <td>
#        yesterday    </td>
#    <td>
#        </td>
#</tr>


# bottle">Bottle (57)</a></li>
#  Beer Here  Black Cat   Black India Pale Ale   Friday

# Brewery
# Beer
# Style
# Updated

#<tr>
#    <td>
#        <img src="/content/images/flags/dk.png" alt="dk" />  <a href="/brewer/29">Beer Here</a>
#    </td>
#    <td>
#        <a href="/beer/1055">Weed</a>
#    </td>
#    <td>
#        Smoked    </td>
#    <td>
#        about three weeks ago    </td>
#    <td>
#        </td>
#</tr>

# cask">Cask (0)</a></li>



######################

# history">History (46)</a></li>
# Keg   Schouskjelleren Mikrobryggeri  Cascale   Golden Ale/Blond Ale   yesterday

# <th>On</th>
# <th>Brewery</th>
# <th>Beer</th>
# <th>Style</th>
# <th>Removed</th>

#format:
#<tr>
#    <td>
#        Keg    </td>
#    <td>
#        <img src="/content/images/flags/gb.png" alt="gb" />  <a href="/brewer/70">Thornbridge Brewery</a>
#    </td>
#    <td>
#        <a href="/beer/1044">Versa</a>
#    </td>
#    <td>
#        German Hefeweizen    </td>
#    <td>
#        about three weeks ago    </td>
#</tr>    

######################
# info">Place info</a></li>
# denne har bare en stor html blobb, lagre hele

end

scrape_one_venue(28)



#scrape_venue()
#scrape_beer()
#scrape_brewer()
# scrape_style()