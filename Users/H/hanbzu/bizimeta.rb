# Source configuration
@url = "http://bizimeta.dyndns.org/cgi-vel/KOOPERIABIZI/mapa-eus.pro"
@marker_regex = /var marker = createMarker\(point,'(\w+)<BR>(.+)<BR>(\d+) Bizi arrunta<BR>(\d+) Bizi elektrikoa<BR>'\)/

# The station codes are defined here
@codes = {
  ["BARRIKA", "Goierri errepidea (Eskola)"] => "BAR1",
  ["BARRIKA", "Aula de Cultura (Udaletxeko errep. 2)"] => "BAR2",
  ["BERANGO", "Simon Otxandategi Etorb. (Skate Park)"] => "BER1",
  ["BERANGO", "Metro Berango (Sabino Arana kalea)"] => "BER2",
  ["GORLIZ", "Errementari Bidea (Of. Turismo)"] => "GOR1",
  ["GORLIZ", "Paseo de Astondo (SOS Playa)"] => "GOR2",
  ["GORLIZ", "Uresarantze (Estrada de Landabarri, 3)"] => "GOR3",
  ["LEMOIZ", "Atalaia kalea z/g"] => "LEM1",
  ["PLENTZIA", "Ondarreta pasealekua (Plentzia)"] => "PLE2",
  ["PLENTZIA", "Metro Plentzia (Plazatxoa)"] => "PLE1",
  ["SOPELANA", "Metro Larrabasterra (Gatzarrine kalea)"] => "SOP1",
  ["SOPELANA", "Piscinas Sopelana (Trav. Etxebarri, s/n)"] => "SOP2",
  ["SOPELANA", "Sabino Arana (Ayuntamiento)"] => "SOP3",
  ["SOPELANA", "Kurtzio Kulturetxea (Mendieta, 10)"] => "SOP4",
  ["SOPELANA", "Playa Arriatera (Sopelana)"] => "SOP5",
  ["URDULIZ", "Elorza, 1 (Udaletxea)"] => "URD1",
  ["URDULIZ", "Metro Urduliz"] => "URD2"
}

@bike_counts = {}
@bike_counts[:a_time] = Time.now.gmtime

# Check & save data in hash
def parse_data(town, location, normal_bikes, electric_bikes)
  code = @codes[[town, location]]
  if code then
    @bike_counts[code] = normal_bikes + electric_bikes 
  else
    p "Code not found for #{town} & #{location}" unless code
  end
end

# Load HTML
html = ScraperWiki::scrape(@url)

# Parse meaningful lines
html.each_line do |line|
  if line =~ @marker_regex
    parse_data $1, $2, $3.to_i, $4.to_i
  end
end

# Save data
ScraperWiki::save_sqlite(unique_keys=['a_time'], data=@bike_counts)
# Source configuration
@url = "http://bizimeta.dyndns.org/cgi-vel/KOOPERIABIZI/mapa-eus.pro"
@marker_regex = /var marker = createMarker\(point,'(\w+)<BR>(.+)<BR>(\d+) Bizi arrunta<BR>(\d+) Bizi elektrikoa<BR>'\)/

# The station codes are defined here
@codes = {
  ["BARRIKA", "Goierri errepidea (Eskola)"] => "BAR1",
  ["BARRIKA", "Aula de Cultura (Udaletxeko errep. 2)"] => "BAR2",
  ["BERANGO", "Simon Otxandategi Etorb. (Skate Park)"] => "BER1",
  ["BERANGO", "Metro Berango (Sabino Arana kalea)"] => "BER2",
  ["GORLIZ", "Errementari Bidea (Of. Turismo)"] => "GOR1",
  ["GORLIZ", "Paseo de Astondo (SOS Playa)"] => "GOR2",
  ["GORLIZ", "Uresarantze (Estrada de Landabarri, 3)"] => "GOR3",
  ["LEMOIZ", "Atalaia kalea z/g"] => "LEM1",
  ["PLENTZIA", "Ondarreta pasealekua (Plentzia)"] => "PLE2",
  ["PLENTZIA", "Metro Plentzia (Plazatxoa)"] => "PLE1",
  ["SOPELANA", "Metro Larrabasterra (Gatzarrine kalea)"] => "SOP1",
  ["SOPELANA", "Piscinas Sopelana (Trav. Etxebarri, s/n)"] => "SOP2",
  ["SOPELANA", "Sabino Arana (Ayuntamiento)"] => "SOP3",
  ["SOPELANA", "Kurtzio Kulturetxea (Mendieta, 10)"] => "SOP4",
  ["SOPELANA", "Playa Arriatera (Sopelana)"] => "SOP5",
  ["URDULIZ", "Elorza, 1 (Udaletxea)"] => "URD1",
  ["URDULIZ", "Metro Urduliz"] => "URD2"
}

@bike_counts = {}
@bike_counts[:a_time] = Time.now.gmtime

# Check & save data in hash
def parse_data(town, location, normal_bikes, electric_bikes)
  code = @codes[[town, location]]
  if code then
    @bike_counts[code] = normal_bikes + electric_bikes 
  else
    p "Code not found for #{town} & #{location}" unless code
  end
end

# Load HTML
html = ScraperWiki::scrape(@url)

# Parse meaningful lines
html.each_line do |line|
  if line =~ @marker_regex
    parse_data $1, $2, $3.to_i, $4.to_i
  end
end

# Save data
ScraperWiki::save_sqlite(unique_keys=['a_time'], data=@bike_counts)
