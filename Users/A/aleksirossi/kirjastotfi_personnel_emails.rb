#encoding: UTF-8
require 'nokogiri'
require 'json'

$fetch_scraping = false
$save_scraping  = true

def fetch(url)
  if $fetch_scraping
    Nokogiri::HTML ScraperWiki::scrape(url)
  else
    require 'httparty'
    Nokogiri::HTML HTTParty.get(url).body
  end
end

def save(unique_keys, data, table_name="swdata")
  puts "Save into #{table_name}: #{unique_keys}: #{data}"
  if $save_scraping
    ScraperWiki::save_sqlite(unique_keys, data, table_name)
  end
end

def inner(doc, css)
  inner = ""
  doc.css(css).each do |a|
    inner = a.inner_html
  end
  inner
end

def href(doc, css)
  href = ""
  doc.css(css).each do |a|
    href = a["href"]
  end
  href
end

def email(names, email, reverse=false)
  if names =~ /\w/
    email.gsub(/etunimi.sukunimi/) do
        # small caps, no scandinavian chars, first space into dot and remove all other spaces
        name = names.downcase
        name.gsub!(/ä/, "a")
        name.gsub!(/Ä/, "A")
        name.gsub!(/ö/, "o")
        name.gsub!(/Ö/, "O")
        name.gsub!(/å/, "a")
        name.gsub!(/Å/, "A")
        parts = name.split(/ /)
        parts = parts.reverse if reverse
        parts[0] + "." + parts[1..-1].join("")
    end
  else
    email
  end
end

def fetch_locations(locations, municipality_name)
  locations.map do |url, location_name|
    puts url
    doc = fetch(url)
    address         = inner(doc, "span#ctl00_body_ctl00_extra_ctl00_fieldAddress")
    postOffice      = inner(doc, "span#ctl00_body_ctl00_extra_ctl00_fieldPostOffice")
    postalCode      = inner(doc, "span#ctl00_body_ctl00_extra_ctl00_fieldPostalCode")
    postalAddress   = inner(doc, "span#ctl00_body_ctl00_extra_ctl00_fieldPostalAddress")
    location_email  = inner(doc, "a#ctl00_body_ctl00_extra_ctl00_hyperLinkEmail")

    names           = doc.css("table#ctl00_body_ctl00_extra_ctl00_listPersonnel_dataGridData tr td.name a").map {|a| a.inner_html }
    position        = doc.css("table#ctl00_body_ctl00_extra_ctl00_listPersonnel_dataGridData tr td.position").map {|a| a.inner_html }
    email           = doc.css("table#ctl00_body_ctl00_extra_ctl00_listPersonnel_dataGridData tr td.email span").map {|a| a.inner_html }

    personnel = []
    unless names.empty?
      personnel = names.zip(position[1..-1], email[1..-1])
    end
    # try to convert etunimi.sukunimi@email.com by guessing it from person real name
    personnel.each{|person| person[2] = email(person[0], person[2], true)}

#    puts "\nLocation: #{url}"
#    p [address, postOffice, postalCode, postalAddress, location_email]
#    puts personnel.map{|per| sprintf("        %-30s %-30s %-30s", per[0], per[1], per[2])}
#    puts "\n\n\n"

    save(["municipality_name", "location_name"], 
        { :municipality_name => municipality_name, :location_name => location_name,
          :address => address, :postOffice => postOffice, :postalCode => postalCode, :postalAddress => postalAddress, :location_email => location_email}, 
        "location_details") 

#    p personnel
#    p personnel.sort{|p1, p2| title_order(p1[1]) <=> title_order(p2[1]) }
#    p personnel.map{|p1| title_order(p1[1])}
    personnel.sort{|p1, p2| title_order(p1[1]) <=> title_order(p2[1]) }.each_with_index do |person, i|
      save(["municipality_name", "location_name", "person_name"], 
              { :municipality_name => municipality_name, :location_name => location_name, :person_name => person[0],
                :position => person[1], :email => person[2], :highest_ranking_officer => i+1, :title_order => title_order(person[1])},
              "location_personnel") 
    end       

    [address, postOffice, postalCode, postalAddress, location_email, personnel]
  end
end

def fetch_manager_email(url)
  doc = fetch("http://www.kirjastot.fi" + url)
  manager_email = inner(doc, "a#ctl00_body_ctl00_extra_ctl00_hyperLinkEmail")
end

def fetch_municipalities(muns)
  muns.each do |url, municipality_name|
    library_email, manager_email = nil, nil
    puts url
    doc = fetch(url)
    library_email = inner(doc, "a#ctl00_body_ctl00_extra_ctl00_hyperLinkEmail")
    manager_name  = inner(doc, "a#ctl00_body_ctl00_extra_ctl00_hyperLinkLibraryManagerEmail")
    manager_href  =  href(doc, "a#ctl00_body_ctl00_extra_ctl00_hyperLinkLibraryManagerEmail")

    manager_email = email(manager_name, fetch_manager_email(manager_href))

    save(["municipality_name"], {:municipality_name => municipality_name, 
      :library_email => library_email, :manager_name => manager_name, :manager_email => manager_email}, 
      "library_emails")

    locations = doc.css("table#ctl00_body_ctl00_extra_ctl00_listOffices_dataGridData tr td.name a").map do |a|
      ["http://www.kirjastot.fi" + a["href"], a.inner_html]
    end

    locs = fetch_locations(locations, municipality_name)
#    p library_email, manager_email
#    p locations
  end
end

def title_order(title)
  order = [
    "Aluekirjastonjohtaja",
    "kirjastopalveluiden aluejohtaja",

    "kirjastotimenjohtaja",
    "kirjastotoimen johtaja",
    "kirjastotoimenjohtaja",
    "kirjatotoimenjohtaja",
    "Kirjastontoimenjohtaja",
    "Kirjastotoimen johtaja",
    "Kirjastotoimen johtaja (poissa 1.1.-30.6. ja 1.8.-31.12.2012)",
    "Kirjastotoimenjohtaja",
    "Kirjastotoimenjohtaja va.",
    "Kirjastotoimenjohtaja, palvelupäällikkö",
    "Kulttuuri- ja kansalaistoimen johtaja / Kirjastotoimen johtaja",
    "kirjasto- ja kulttuuritoimenjohtaha",
    "kirjasto- ja kulttuuritoimenjohtaja",
    "kirjasto-kulttuuritoimen johtaja",
    "vt. kirjastotoimenjohtaja/osastonjohtaja",
    "vt.kirjastotoimenjohtaja",
    "Kirjastonhoitaja (v.s. kirjastonjohtaja 9.2.2012 alkaen)",
    "biblioteksdirektör",
    "vs. kirjastotoimenjohtaja",
    "vs. kirjastotoimenjohtaja, informaatikko, henkilöstövastaava",

    "Kirjastojohtaja",
    "Kirjaston johtaja",
    "Kirjastonjohtaja",
    "Kirjastonjohtaja (Työvapaa 1.3.2010-31.3.2013)",
    "Kirjastonjohtaja, vs",
    "Kirjastonjohtajan sijainen 31.8.2012 asti",
    "Kirjastopalveluiden aluejohtaja",
    "Kirjastopalvelujohtaja",
    "Vs. kirjastonjohtaja 1.3.2010-31.3.2013",
    "Vt. kirjastonjohtaja",
    "kirjastojohtaja",
    "kirjastonjohtaja",
    "kirjastonjohtaja - virkavapaa",
    "kirjastonjohtaja, Vuotalon johtaja",
    "kirjastonjohtaja, osa-aik.",
    "ma. kirjastonjohtaja",
    "vs. kirjastonjohtaja",
    "vt. kirjastonjohtaja",
    "johtaja",
    "Bibliotekarie / Kirjastonhoitaja,  tf. biblioteksdirektör / vs. kirjastotoimenjohtaja",
    "Kirjastonhoitaja, vs. kirjastotoimenjohtaja 1.1.-30.6. ja 1.8.-31.12.2012",
    "Bibliotekschef",
    "bibliotekschef",

    "Osastonjohtaja",
    "Osastonjohtaja (poissa)",
    "Osastonjohtaja / musiikki",
    "Palvelujohtaja",
    "musiikkiosaston johtaja",
    "osastonjohtaja",
    "osastonjohtajan",
    "palvelujohtaja",
    "vs. osastonjohtaja",

    "Johtava informaatikko",
    "Johtava kirjastonhoitaja",
    "Johtava kirjastovirkailija",

    " Kirjastopäällikkö",
    "Kirjastopäällikkö vs.",
    "Palvelupäällikkö",

    "Erikoiskirjastonhoitaja",
    "Erikoiskirjastonhoitaja.",
    "Erikoiskirjastovirkailija",
    "Erikoiskirjastovirkailija (perhevapaalla)",
    "Erikoiskirjastovirkailija (poissa 11.8.2013 saakka)",
    "Erikoiskirjastovirkailija (virkavapaalla)",
    "Erikoiskirjastovirkailija suunnittelijan toimin",
    "Erikoiskirjastovirkailija, mikrotuki",
    "Erikoiskirjastovirkaililja",
    "erikoiskirjastonhoitaja",
    "erikoiskirjastotovirkailija",
    "erikoiskirjastovirkailija",
    "erikoiskirjastovirkailija (lasten- ja nuortenkirjalisuus)",
    "erikoiskirjastovirkailija (opintovapaalla)",
    "erikoissuunnittelija",

    "informaatikko",
    "informaatikko / informatiker",

    "Kirjastovirkailija",
    "Kirjastovirkailija (oppisopimusopiskelija)",
    "Kirjastovirkailija (osa-aikaeläkkeellä)",
    "Kirjastovirkailija (osa-aikainen)",
    "Kirjastovirkailija (perhevapaalla)",
    "Kirjastovirkailija (sijainen)",
    "Kirjastovirkailija (työlomalla)",
    "Kirjastovirkailija (virkavapaa 1.7.2012 - 30.6.2013)",
    "Kirjastovirkailija - kirjastoauto",
    "Kirjastovirkailija / Oppisopimuskoulutettava",
    "Kirjastovirkailija ts.",
    "Kirjastovirkailija virkavapaalla",
    "Kirjastovirkailija, Atk-vastaava",
    "Kirjastovirkailija, hoitovapaalla 31.12.2012 saakka",
    "Kirjastovirkailija, määräaikainen 31.3.13 asti",
    "Kirjastovirkailija, va",
    "Kirjastovirkailija, virkavapaa",
    "Kirjastovirkailija, vs. kirjastonhoitaja 17.6.2012 saakka",
    "Kirjastovirkailija-autonkuljettaja",
    "Kirjastovirkailija-kuljettaja",
    "Kirjastovirkailija-vahtimestari",
    "Kirjastovirkailija/ kirjankorjaus",
    "Kirjastovirkailija/atk-vastaava",
    "Kirjastovirkailija/tuntiopettaja",
    "Kirjastovirkailijan sijainen",
    "Kirjastovirkailja",
    "Kirjastovirkailjia",
    "Kirjastovirkaillija",
    "Kirjastovirkalija",
    "Biblioteksfunktionär",
    "Biblioteksfunktionär (moderskapsledig)",
    "Biblioteksfunktionär / Kirjastovirkailija",
    "Biblioteksfunktionär / Kirjastovirkailja",
    "Biblioteksfunktionär, t.f. bibliotekarie",
    "Biblioteksfunktionär-bokbusschaufför",
    "Vs. kirjastovirkailija 1.12.2012 saakka",
    "Vs. kirjastovirkailija 31.12.2012 saakka",
    "Vs. kirjastovirkailija, oppisopimus 31.12.2012 saakka",
    "Vt. kirjastovirkailija 1.7.2012-30.6.2013",
    "biblioteksfunktionär",
    "kirjastovirkailija",
    "kirjastovirkailija (oppisopimus)",
    "kirjastovirkailija (osa-aika eläkkeellä)",
    "kirjastovirkailija (osa-aikainen)",
    "kirjastovirkailija (vaihdossa Roihuvuoren kirjastossa 31.3.2013 asti)",
    "kirjastovirkailija 0,2 htv",
    "kirjastovirkailija 1.6.-31.8.2012",
    "kirjastovirkailija vs.",
    "kirjastovirkailija, 2 päivää viikossa",
    "kirjastovirkailija, VIRKAVAPAALLA",
    "kirjastovirkailija, ma",
    "kirjastovirkailija, osa-aikainen",
    "kirjastovirkailija, työlomalla",
    "kirjastovirkailija, äitiyslomalla",
    "kirjastovirkailija-autonkuljettaja",
    "kirjastovirkailija-kuljettaja",
    "kirjastovirkailija/atk-vastaava",
    "Ts. kirjastovirkailija",
    "vastaava kirjastovirkailija",

    "Kirjastonhoitaja",
    "Kirjastonhoitaja  / bibl.",
    "Kirjastonhoitaja - hoitovapaalla 31.8.2011 saakka",
    "Kirjastonhoitaja - lasten- ja nuortenosasto",
    "Kirjastonhoitaja ts.",
    "Kirjastonhoitaja virkavapaalla",
    "Kirjastonhoitaja, va",
    "Kirjastonhoitaja, virkavapaalla",
    "Kirjastonhoitaja-kulttuurisihteeri, museonhoitaja",
    "Kirjastonhoitajan sijainen",
    "Bibliotekarie",
    "Bibliotekarie / Kirjastonhoitaja",
    "Bibliotekarie / Kirjastonhoitaja (Vikarie / Sijainen)",
    "Bibliotekarie / Kirjastonhoitaja (vikarie för Rebecka Fokin)",
    "Bibliotekarie / Kirjastonhoitaja, (tjänstledig 2012, vikarie Jolanda Tirkkonen)",
    "Bibliotekarie för Högskolan på Åland",
    "Bibliotekarie tj.led.",
    "bibliotekarie",
    "bibliotekarie/servicerådgivare",
    "kirjastonhoitaja",
    "kirjastonhoitaja / lastenosastovastaava",
    "kirjastonhoitaja toimivapaalla 30.4.2012 saakka",
    "kirjastonhoitaja ts.",
    "kirjastonhoitaja, lasten ja nuorten osasto",
    "kirjastonhoitaja, sijainen",
    "kirjastonhoitaja, toimivapaalla",
    "kirjastonhoitaja-kulttuurisihteeri",
    "kirjastonhoitajan sijainen 1.2. - 1.6.2012",
    "kirjastonhoitja",
    "tp. kirjastonhoitaja",
    "ts kirjastonhoitaja",
    "ts. kirjastonhoitaja",
    "ts. kirjastovirkailija",
    "va. kirjastonhoitaja",
    "vastaava kirjastonhoitaja",
    "vastaava kirjastonhoitaja, ts",

    "Vastaava kirjastonhoitaja",
    "Vastaava kirjastonhoitaja (virkavapaalla)",
    "Vastaava kirjastonhoitaja ts.",

    "Kirjastoapulainen",
    "Kirjastoapulainen, oppisopimus",

    "Kirjastoautokuljettaja-virkailija",
    "Kirjastoauton kuljettaja",
    "Kirjastoauton kuljettaja-virkailija",
    "Kirjastoautonkuljettaja",
    "Kirjastoautonkuljettaja - kirjastovirkailija",
    "Kirjastoautonkuljettaja-virkailija",
    "Kirjastoautonkuljettaja/kirjastovirkailija",
    "Kirjastoautonkuljettaja/virkailija",
    "Kirjastoautopalvelujen hoitaja",
    "Kirjastoautosihteeri",
    "Kirjastoautovirkailija",
    "Kirjastoautovirkailija-kuljettaja",

    "Kirjastoavustaja",
    "Kirjastoavustaja ",

    "johtava virastomestari",
    "Aineistonkäsittelijä",
    "Aluelastenkirjastonhoitaja",
    "Asiakaspalvelusihteeri",
    "Asiakaspalveluvirkailija",
    "Autokirjastonhoitaja",
    "Barn- och ungdomsbibliotekarie",
    "Barnbibliotekarie, kommunens webmaster",
    "Bokbusschaufför",
    "Bokbusschaufför/biblioteksfunktionär",
    "Harjoittelija",
    "IT-tuki",
    "IT-tuki sijainen",
    "IT-tukihenkilö",
    "IT-tukihenkilö (Kallion kirjastossa 21.6.2010 - 31.12.2011)",
    "Informaatikko",
    "It-tukihenkilö",
    "Järjestelyapulainen",
    "Järjestelyapulainen (virkavapaalla)",
    "Kirjansitoja",

    "Kirjastosihteeri",
    "Kirjastotyöntekijä",
    "Kulttuurituottaja",
    "Kulturchef",
    "Lainauspalveluesimies",
    "Lasten- ja nuortenohjaaja",
    "Lehtisalivalvoja",
    "Lähikirjastovastaava",
    "Media-assistentti (oppisopimus)",
    "Mediatuottaja",
    "Musiikin informaatikko",
    "Musikbibliotekarie",
    "Oppisopimusopiskelija",
    "Osastosihteeri",
    "Palveluesimies",
    "Palvelukoordinaattori",
    "Palvelusihteeri",
    "Palveluvirkailija",
    "Pedagoginen informaatikko",
    "Pedagoginen informaatikko,  pääkirjasto ja Mediamaja 14.12.12 asti",
    "Projektikirjastonhoitaja",
    "Projektityöntekijä",
    "Siivooja",
    "Siivooja-vahtimestari",
    "Siviilipalvelusmies",
    "Suunnittelija",
    "Talonmies",
    "Tapahtumakoordinaattori",
    "Tietopalvelukonsultti",
    "Tietopalveluvirkailija",
    "Tietotekniikkasuunnittelija",
    "Tietotekniikkavirkailija",
    "Tietotekniikkavirkailija (opintovapaalla 10.8. 2009 lähtien)",
    "Toimistoesimies",
    "Toimistopäällikkö",
    "Toimistosihteeri",
    "Toimistovirkailija",
    "Toimistovirkailija/ atk-vastaava",
    "Vahtimestari",
    "Vahtimestari / TEKME",
    "Vastaava kirjastoautonkuljettaja",
    "Vastaava kirjastovirkailija",
    "Vastaava vahtimestari",
    "Vik. biblioteksfunktionär",
    "Virastomestari",
    "Virastomestari / Asiakaspalveluvirkailija",
    "asiakaspalveluvirkailija",
    "asiakaspalveluvirkailija (Oulunkylässä 29.5.2011 asti)",
    "asiakassihteeri",
    "autokirjastonhoitaja",
    "autokirjastovirkailija",
    "erikoistoimistonhoitaja",
    "järjestelyapulainen",
    "kanslisti",
    "kanslisti ",
    "kirjastoapulainen",
    "kirjastoauton kuljettajavirkailija",
    "kirjastoautonkuljettaja",
    "kirjastoautonkuljettaja-virkailija",
    "kirjastoautonkuljettaja-virkailija, osa-aikainen",
    "kirjastoautonkuljettaja/virkailija",
    "kirjastoautovirkailija",
    "kirjastoautovirkailija-kuljettaja",
    "kirjastoautovirkailijan sijainen",
    "kirjastoavustaja",
    "kirjastoirkailija",
    "kirjastonvirkailija",
    "kirjastopalvelusihteeri",
    "kirjastosihteeri",
    "kirjastosihteeri - virkavapaa",
    "kirjastotyöntekijä",
    "kirjstonhoitaja",
    "lainausapulainen",
    "lainausasemanhoitaja",
    "lainaustoimistonhoitaja",
    "ma. kirjastovirkailija",
    "ma. kirjastovirkailija-kirjastoauton kuljettaja",
    "matkailusihteeri",
    "musiikkiosaston erikoiskirjastonhoitaja",
    "oppisopimusopiskelija",
    "palveluesimies",
    "palvelupäällikkö",
    "palvelusihteeri",
    "palveluvirkailija",
    "pedagoginen informaatikko",
    "pedagoginen informaatikko - pedagogisk informatiker",
    "position",
    "sihteeri",
    "siistijä",
    "siviilipalvelusmies",
    "t.f. bibliotekarie",
    "tietoasiantuntija",
    "tietopalveluvirkailija",
    "tietopalveluvirkailija/ viestintävastaava",
    "tietotekniikkavirkailija",
    "toimistoesimies",
    "toimistosihteeeri",
    "toimistosihteeri",
    "toimistosihteeri - virkavapaa",
    "toimistovirkailija",
    "vahtimestari",
    "virastomestari",
    "virastomestari (oppisopimusopiskelija)",
    "vs. kirjastosihteeri",
    "vs. kirjastovirkailija",
    "vs. toimistosihteeri",
    "vt. vastaava kirjastonhoitaja",
  ]
  if title
    title_as_regexp = Regexp.new(title)
    match = order.find {|o| o =~ title_as_regexp}
    if match
      order.index(match)
    else
      1000  # big number to sort as last
    end
  else
    1000
  end
end


([ "%C4", # 'Ä'
   "%D6", # 'Ö'
   "%C5", # 'Å'
] + ('A'..'Z').to_a ).each do |letter|
  url = "http://www.kirjastot.fi/fi-FI/kirjastot/kunnan-ja-kaupunginkirjastot/?selectedLetter=#{letter}"
  puts url
  doc = fetch(url)
  municipalities = doc.css("#mainContent div.content tr td.name a").map do |a|
    ["http://www.kirjastot.fi" + a["href"], a.inner_html]
  end

  fetch_municipalities(municipalities)
#  exit
end#encoding: UTF-8
require 'nokogiri'
require 'json'

$fetch_scraping = false
$save_scraping  = true

def fetch(url)
  if $fetch_scraping
    Nokogiri::HTML ScraperWiki::scrape(url)
  else
    require 'httparty'
    Nokogiri::HTML HTTParty.get(url).body
  end
end

def save(unique_keys, data, table_name="swdata")
  puts "Save into #{table_name}: #{unique_keys}: #{data}"
  if $save_scraping
    ScraperWiki::save_sqlite(unique_keys, data, table_name)
  end
end

def inner(doc, css)
  inner = ""
  doc.css(css).each do |a|
    inner = a.inner_html
  end
  inner
end

def href(doc, css)
  href = ""
  doc.css(css).each do |a|
    href = a["href"]
  end
  href
end

def email(names, email, reverse=false)
  if names =~ /\w/
    email.gsub(/etunimi.sukunimi/) do
        # small caps, no scandinavian chars, first space into dot and remove all other spaces
        name = names.downcase
        name.gsub!(/ä/, "a")
        name.gsub!(/Ä/, "A")
        name.gsub!(/ö/, "o")
        name.gsub!(/Ö/, "O")
        name.gsub!(/å/, "a")
        name.gsub!(/Å/, "A")
        parts = name.split(/ /)
        parts = parts.reverse if reverse
        parts[0] + "." + parts[1..-1].join("")
    end
  else
    email
  end
end

def fetch_locations(locations, municipality_name)
  locations.map do |url, location_name|
    puts url
    doc = fetch(url)
    address         = inner(doc, "span#ctl00_body_ctl00_extra_ctl00_fieldAddress")
    postOffice      = inner(doc, "span#ctl00_body_ctl00_extra_ctl00_fieldPostOffice")
    postalCode      = inner(doc, "span#ctl00_body_ctl00_extra_ctl00_fieldPostalCode")
    postalAddress   = inner(doc, "span#ctl00_body_ctl00_extra_ctl00_fieldPostalAddress")
    location_email  = inner(doc, "a#ctl00_body_ctl00_extra_ctl00_hyperLinkEmail")

    names           = doc.css("table#ctl00_body_ctl00_extra_ctl00_listPersonnel_dataGridData tr td.name a").map {|a| a.inner_html }
    position        = doc.css("table#ctl00_body_ctl00_extra_ctl00_listPersonnel_dataGridData tr td.position").map {|a| a.inner_html }
    email           = doc.css("table#ctl00_body_ctl00_extra_ctl00_listPersonnel_dataGridData tr td.email span").map {|a| a.inner_html }

    personnel = []
    unless names.empty?
      personnel = names.zip(position[1..-1], email[1..-1])
    end
    # try to convert etunimi.sukunimi@email.com by guessing it from person real name
    personnel.each{|person| person[2] = email(person[0], person[2], true)}

#    puts "\nLocation: #{url}"
#    p [address, postOffice, postalCode, postalAddress, location_email]
#    puts personnel.map{|per| sprintf("        %-30s %-30s %-30s", per[0], per[1], per[2])}
#    puts "\n\n\n"

    save(["municipality_name", "location_name"], 
        { :municipality_name => municipality_name, :location_name => location_name,
          :address => address, :postOffice => postOffice, :postalCode => postalCode, :postalAddress => postalAddress, :location_email => location_email}, 
        "location_details") 

#    p personnel
#    p personnel.sort{|p1, p2| title_order(p1[1]) <=> title_order(p2[1]) }
#    p personnel.map{|p1| title_order(p1[1])}
    personnel.sort{|p1, p2| title_order(p1[1]) <=> title_order(p2[1]) }.each_with_index do |person, i|
      save(["municipality_name", "location_name", "person_name"], 
              { :municipality_name => municipality_name, :location_name => location_name, :person_name => person[0],
                :position => person[1], :email => person[2], :highest_ranking_officer => i+1, :title_order => title_order(person[1])},
              "location_personnel") 
    end       

    [address, postOffice, postalCode, postalAddress, location_email, personnel]
  end
end

def fetch_manager_email(url)
  doc = fetch("http://www.kirjastot.fi" + url)
  manager_email = inner(doc, "a#ctl00_body_ctl00_extra_ctl00_hyperLinkEmail")
end

def fetch_municipalities(muns)
  muns.each do |url, municipality_name|
    library_email, manager_email = nil, nil
    puts url
    doc = fetch(url)
    library_email = inner(doc, "a#ctl00_body_ctl00_extra_ctl00_hyperLinkEmail")
    manager_name  = inner(doc, "a#ctl00_body_ctl00_extra_ctl00_hyperLinkLibraryManagerEmail")
    manager_href  =  href(doc, "a#ctl00_body_ctl00_extra_ctl00_hyperLinkLibraryManagerEmail")

    manager_email = email(manager_name, fetch_manager_email(manager_href))

    save(["municipality_name"], {:municipality_name => municipality_name, 
      :library_email => library_email, :manager_name => manager_name, :manager_email => manager_email}, 
      "library_emails")

    locations = doc.css("table#ctl00_body_ctl00_extra_ctl00_listOffices_dataGridData tr td.name a").map do |a|
      ["http://www.kirjastot.fi" + a["href"], a.inner_html]
    end

    locs = fetch_locations(locations, municipality_name)
#    p library_email, manager_email
#    p locations
  end
end

def title_order(title)
  order = [
    "Aluekirjastonjohtaja",
    "kirjastopalveluiden aluejohtaja",

    "kirjastotimenjohtaja",
    "kirjastotoimen johtaja",
    "kirjastotoimenjohtaja",
    "kirjatotoimenjohtaja",
    "Kirjastontoimenjohtaja",
    "Kirjastotoimen johtaja",
    "Kirjastotoimen johtaja (poissa 1.1.-30.6. ja 1.8.-31.12.2012)",
    "Kirjastotoimenjohtaja",
    "Kirjastotoimenjohtaja va.",
    "Kirjastotoimenjohtaja, palvelupäällikkö",
    "Kulttuuri- ja kansalaistoimen johtaja / Kirjastotoimen johtaja",
    "kirjasto- ja kulttuuritoimenjohtaha",
    "kirjasto- ja kulttuuritoimenjohtaja",
    "kirjasto-kulttuuritoimen johtaja",
    "vt. kirjastotoimenjohtaja/osastonjohtaja",
    "vt.kirjastotoimenjohtaja",
    "Kirjastonhoitaja (v.s. kirjastonjohtaja 9.2.2012 alkaen)",
    "biblioteksdirektör",
    "vs. kirjastotoimenjohtaja",
    "vs. kirjastotoimenjohtaja, informaatikko, henkilöstövastaava",

    "Kirjastojohtaja",
    "Kirjaston johtaja",
    "Kirjastonjohtaja",
    "Kirjastonjohtaja (Työvapaa 1.3.2010-31.3.2013)",
    "Kirjastonjohtaja, vs",
    "Kirjastonjohtajan sijainen 31.8.2012 asti",
    "Kirjastopalveluiden aluejohtaja",
    "Kirjastopalvelujohtaja",
    "Vs. kirjastonjohtaja 1.3.2010-31.3.2013",
    "Vt. kirjastonjohtaja",
    "kirjastojohtaja",
    "kirjastonjohtaja",
    "kirjastonjohtaja - virkavapaa",
    "kirjastonjohtaja, Vuotalon johtaja",
    "kirjastonjohtaja, osa-aik.",
    "ma. kirjastonjohtaja",
    "vs. kirjastonjohtaja",
    "vt. kirjastonjohtaja",
    "johtaja",
    "Bibliotekarie / Kirjastonhoitaja,  tf. biblioteksdirektör / vs. kirjastotoimenjohtaja",
    "Kirjastonhoitaja, vs. kirjastotoimenjohtaja 1.1.-30.6. ja 1.8.-31.12.2012",
    "Bibliotekschef",
    "bibliotekschef",

    "Osastonjohtaja",
    "Osastonjohtaja (poissa)",
    "Osastonjohtaja / musiikki",
    "Palvelujohtaja",
    "musiikkiosaston johtaja",
    "osastonjohtaja",
    "osastonjohtajan",
    "palvelujohtaja",
    "vs. osastonjohtaja",

    "Johtava informaatikko",
    "Johtava kirjastonhoitaja",
    "Johtava kirjastovirkailija",

    " Kirjastopäällikkö",
    "Kirjastopäällikkö vs.",
    "Palvelupäällikkö",

    "Erikoiskirjastonhoitaja",
    "Erikoiskirjastonhoitaja.",
    "Erikoiskirjastovirkailija",
    "Erikoiskirjastovirkailija (perhevapaalla)",
    "Erikoiskirjastovirkailija (poissa 11.8.2013 saakka)",
    "Erikoiskirjastovirkailija (virkavapaalla)",
    "Erikoiskirjastovirkailija suunnittelijan toimin",
    "Erikoiskirjastovirkailija, mikrotuki",
    "Erikoiskirjastovirkaililja",
    "erikoiskirjastonhoitaja",
    "erikoiskirjastotovirkailija",
    "erikoiskirjastovirkailija",
    "erikoiskirjastovirkailija (lasten- ja nuortenkirjalisuus)",
    "erikoiskirjastovirkailija (opintovapaalla)",
    "erikoissuunnittelija",

    "informaatikko",
    "informaatikko / informatiker",

    "Kirjastovirkailija",
    "Kirjastovirkailija (oppisopimusopiskelija)",
    "Kirjastovirkailija (osa-aikaeläkkeellä)",
    "Kirjastovirkailija (osa-aikainen)",
    "Kirjastovirkailija (perhevapaalla)",
    "Kirjastovirkailija (sijainen)",
    "Kirjastovirkailija (työlomalla)",
    "Kirjastovirkailija (virkavapaa 1.7.2012 - 30.6.2013)",
    "Kirjastovirkailija - kirjastoauto",
    "Kirjastovirkailija / Oppisopimuskoulutettava",
    "Kirjastovirkailija ts.",
    "Kirjastovirkailija virkavapaalla",
    "Kirjastovirkailija, Atk-vastaava",
    "Kirjastovirkailija, hoitovapaalla 31.12.2012 saakka",
    "Kirjastovirkailija, määräaikainen 31.3.13 asti",
    "Kirjastovirkailija, va",
    "Kirjastovirkailija, virkavapaa",
    "Kirjastovirkailija, vs. kirjastonhoitaja 17.6.2012 saakka",
    "Kirjastovirkailija-autonkuljettaja",
    "Kirjastovirkailija-kuljettaja",
    "Kirjastovirkailija-vahtimestari",
    "Kirjastovirkailija/ kirjankorjaus",
    "Kirjastovirkailija/atk-vastaava",
    "Kirjastovirkailija/tuntiopettaja",
    "Kirjastovirkailijan sijainen",
    "Kirjastovirkailja",
    "Kirjastovirkailjia",
    "Kirjastovirkaillija",
    "Kirjastovirkalija",
    "Biblioteksfunktionär",
    "Biblioteksfunktionär (moderskapsledig)",
    "Biblioteksfunktionär / Kirjastovirkailija",
    "Biblioteksfunktionär / Kirjastovirkailja",
    "Biblioteksfunktionär, t.f. bibliotekarie",
    "Biblioteksfunktionär-bokbusschaufför",
    "Vs. kirjastovirkailija 1.12.2012 saakka",
    "Vs. kirjastovirkailija 31.12.2012 saakka",
    "Vs. kirjastovirkailija, oppisopimus 31.12.2012 saakka",
    "Vt. kirjastovirkailija 1.7.2012-30.6.2013",
    "biblioteksfunktionär",
    "kirjastovirkailija",
    "kirjastovirkailija (oppisopimus)",
    "kirjastovirkailija (osa-aika eläkkeellä)",
    "kirjastovirkailija (osa-aikainen)",
    "kirjastovirkailija (vaihdossa Roihuvuoren kirjastossa 31.3.2013 asti)",
    "kirjastovirkailija 0,2 htv",
    "kirjastovirkailija 1.6.-31.8.2012",
    "kirjastovirkailija vs.",
    "kirjastovirkailija, 2 päivää viikossa",
    "kirjastovirkailija, VIRKAVAPAALLA",
    "kirjastovirkailija, ma",
    "kirjastovirkailija, osa-aikainen",
    "kirjastovirkailija, työlomalla",
    "kirjastovirkailija, äitiyslomalla",
    "kirjastovirkailija-autonkuljettaja",
    "kirjastovirkailija-kuljettaja",
    "kirjastovirkailija/atk-vastaava",
    "Ts. kirjastovirkailija",
    "vastaava kirjastovirkailija",

    "Kirjastonhoitaja",
    "Kirjastonhoitaja  / bibl.",
    "Kirjastonhoitaja - hoitovapaalla 31.8.2011 saakka",
    "Kirjastonhoitaja - lasten- ja nuortenosasto",
    "Kirjastonhoitaja ts.",
    "Kirjastonhoitaja virkavapaalla",
    "Kirjastonhoitaja, va",
    "Kirjastonhoitaja, virkavapaalla",
    "Kirjastonhoitaja-kulttuurisihteeri, museonhoitaja",
    "Kirjastonhoitajan sijainen",
    "Bibliotekarie",
    "Bibliotekarie / Kirjastonhoitaja",
    "Bibliotekarie / Kirjastonhoitaja (Vikarie / Sijainen)",
    "Bibliotekarie / Kirjastonhoitaja (vikarie för Rebecka Fokin)",
    "Bibliotekarie / Kirjastonhoitaja, (tjänstledig 2012, vikarie Jolanda Tirkkonen)",
    "Bibliotekarie för Högskolan på Åland",
    "Bibliotekarie tj.led.",
    "bibliotekarie",
    "bibliotekarie/servicerådgivare",
    "kirjastonhoitaja",
    "kirjastonhoitaja / lastenosastovastaava",
    "kirjastonhoitaja toimivapaalla 30.4.2012 saakka",
    "kirjastonhoitaja ts.",
    "kirjastonhoitaja, lasten ja nuorten osasto",
    "kirjastonhoitaja, sijainen",
    "kirjastonhoitaja, toimivapaalla",
    "kirjastonhoitaja-kulttuurisihteeri",
    "kirjastonhoitajan sijainen 1.2. - 1.6.2012",
    "kirjastonhoitja",
    "tp. kirjastonhoitaja",
    "ts kirjastonhoitaja",
    "ts. kirjastonhoitaja",
    "ts. kirjastovirkailija",
    "va. kirjastonhoitaja",
    "vastaava kirjastonhoitaja",
    "vastaava kirjastonhoitaja, ts",

    "Vastaava kirjastonhoitaja",
    "Vastaava kirjastonhoitaja (virkavapaalla)",
    "Vastaava kirjastonhoitaja ts.",

    "Kirjastoapulainen",
    "Kirjastoapulainen, oppisopimus",

    "Kirjastoautokuljettaja-virkailija",
    "Kirjastoauton kuljettaja",
    "Kirjastoauton kuljettaja-virkailija",
    "Kirjastoautonkuljettaja",
    "Kirjastoautonkuljettaja - kirjastovirkailija",
    "Kirjastoautonkuljettaja-virkailija",
    "Kirjastoautonkuljettaja/kirjastovirkailija",
    "Kirjastoautonkuljettaja/virkailija",
    "Kirjastoautopalvelujen hoitaja",
    "Kirjastoautosihteeri",
    "Kirjastoautovirkailija",
    "Kirjastoautovirkailija-kuljettaja",

    "Kirjastoavustaja",
    "Kirjastoavustaja ",

    "johtava virastomestari",
    "Aineistonkäsittelijä",
    "Aluelastenkirjastonhoitaja",
    "Asiakaspalvelusihteeri",
    "Asiakaspalveluvirkailija",
    "Autokirjastonhoitaja",
    "Barn- och ungdomsbibliotekarie",
    "Barnbibliotekarie, kommunens webmaster",
    "Bokbusschaufför",
    "Bokbusschaufför/biblioteksfunktionär",
    "Harjoittelija",
    "IT-tuki",
    "IT-tuki sijainen",
    "IT-tukihenkilö",
    "IT-tukihenkilö (Kallion kirjastossa 21.6.2010 - 31.12.2011)",
    "Informaatikko",
    "It-tukihenkilö",
    "Järjestelyapulainen",
    "Järjestelyapulainen (virkavapaalla)",
    "Kirjansitoja",

    "Kirjastosihteeri",
    "Kirjastotyöntekijä",
    "Kulttuurituottaja",
    "Kulturchef",
    "Lainauspalveluesimies",
    "Lasten- ja nuortenohjaaja",
    "Lehtisalivalvoja",
    "Lähikirjastovastaava",
    "Media-assistentti (oppisopimus)",
    "Mediatuottaja",
    "Musiikin informaatikko",
    "Musikbibliotekarie",
    "Oppisopimusopiskelija",
    "Osastosihteeri",
    "Palveluesimies",
    "Palvelukoordinaattori",
    "Palvelusihteeri",
    "Palveluvirkailija",
    "Pedagoginen informaatikko",
    "Pedagoginen informaatikko,  pääkirjasto ja Mediamaja 14.12.12 asti",
    "Projektikirjastonhoitaja",
    "Projektityöntekijä",
    "Siivooja",
    "Siivooja-vahtimestari",
    "Siviilipalvelusmies",
    "Suunnittelija",
    "Talonmies",
    "Tapahtumakoordinaattori",
    "Tietopalvelukonsultti",
    "Tietopalveluvirkailija",
    "Tietotekniikkasuunnittelija",
    "Tietotekniikkavirkailija",
    "Tietotekniikkavirkailija (opintovapaalla 10.8. 2009 lähtien)",
    "Toimistoesimies",
    "Toimistopäällikkö",
    "Toimistosihteeri",
    "Toimistovirkailija",
    "Toimistovirkailija/ atk-vastaava",
    "Vahtimestari",
    "Vahtimestari / TEKME",
    "Vastaava kirjastoautonkuljettaja",
    "Vastaava kirjastovirkailija",
    "Vastaava vahtimestari",
    "Vik. biblioteksfunktionär",
    "Virastomestari",
    "Virastomestari / Asiakaspalveluvirkailija",
    "asiakaspalveluvirkailija",
    "asiakaspalveluvirkailija (Oulunkylässä 29.5.2011 asti)",
    "asiakassihteeri",
    "autokirjastonhoitaja",
    "autokirjastovirkailija",
    "erikoistoimistonhoitaja",
    "järjestelyapulainen",
    "kanslisti",
    "kanslisti ",
    "kirjastoapulainen",
    "kirjastoauton kuljettajavirkailija",
    "kirjastoautonkuljettaja",
    "kirjastoautonkuljettaja-virkailija",
    "kirjastoautonkuljettaja-virkailija, osa-aikainen",
    "kirjastoautonkuljettaja/virkailija",
    "kirjastoautovirkailija",
    "kirjastoautovirkailija-kuljettaja",
    "kirjastoautovirkailijan sijainen",
    "kirjastoavustaja",
    "kirjastoirkailija",
    "kirjastonvirkailija",
    "kirjastopalvelusihteeri",
    "kirjastosihteeri",
    "kirjastosihteeri - virkavapaa",
    "kirjastotyöntekijä",
    "kirjstonhoitaja",
    "lainausapulainen",
    "lainausasemanhoitaja",
    "lainaustoimistonhoitaja",
    "ma. kirjastovirkailija",
    "ma. kirjastovirkailija-kirjastoauton kuljettaja",
    "matkailusihteeri",
    "musiikkiosaston erikoiskirjastonhoitaja",
    "oppisopimusopiskelija",
    "palveluesimies",
    "palvelupäällikkö",
    "palvelusihteeri",
    "palveluvirkailija",
    "pedagoginen informaatikko",
    "pedagoginen informaatikko - pedagogisk informatiker",
    "position",
    "sihteeri",
    "siistijä",
    "siviilipalvelusmies",
    "t.f. bibliotekarie",
    "tietoasiantuntija",
    "tietopalveluvirkailija",
    "tietopalveluvirkailija/ viestintävastaava",
    "tietotekniikkavirkailija",
    "toimistoesimies",
    "toimistosihteeeri",
    "toimistosihteeri",
    "toimistosihteeri - virkavapaa",
    "toimistovirkailija",
    "vahtimestari",
    "virastomestari",
    "virastomestari (oppisopimusopiskelija)",
    "vs. kirjastosihteeri",
    "vs. kirjastovirkailija",
    "vs. toimistosihteeri",
    "vt. vastaava kirjastonhoitaja",
  ]
  if title
    title_as_regexp = Regexp.new(title)
    match = order.find {|o| o =~ title_as_regexp}
    if match
      order.index(match)
    else
      1000  # big number to sort as last
    end
  else
    1000
  end
end


([ "%C4", # 'Ä'
   "%D6", # 'Ö'
   "%C5", # 'Å'
] + ('A'..'Z').to_a ).each do |letter|
  url = "http://www.kirjastot.fi/fi-FI/kirjastot/kunnan-ja-kaupunginkirjastot/?selectedLetter=#{letter}"
  puts url
  doc = fetch(url)
  municipalities = doc.css("#mainContent div.content tr td.name a").map do |a|
    ["http://www.kirjastot.fi" + a["href"], a.inner_html]
  end

  fetch_municipalities(municipalities)
#  exit
end