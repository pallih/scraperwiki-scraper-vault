# Blank Ruby

marcas = [
"6"   => "Chevrolet",
"7"   => "Citroen",
"14"  => "Fiat",
"15"  => "Ford",
"16"  => "Honda",
"17"  => "Hyundai",
"20"  => "Kia",
"27"  => "Mitsubishi",
"28"  => "Nissan",
"29"  => "Peugeot",
"31"  => "Renault",
"35"  => "Toyota",
"36"  => "Volkswagen",
"53"  => "Acura",
"1"   => "Alfa Romeo",
"2"   => "Asia",
"99"  => "Aston Martin",
"3"   => "Audi",
"104" => "Bentley",
"4"   => "BMW",
"108" => "Buick",
"94"  => "Cadillac",
"230" => "Carver Concept",
"88"  => "Chana",
"100" => "Chery",
"6"   => "Chrysler",
"97"  => "CN Auto",
"66"  => "Crosslander",
"10"  => "Daewoo",
"11"  => "Daihatsu",
"12"  => "Dodge",
"91"  => "Effa",
"67"  => "Engesa",
"68"  => "Envemo",
"13"  => "Ferrari",
"69"  => "GMC",
"98"  => "Great Wall",
"50"  => "Gurgel",
"93"  => "Hafei (Towner)",
"83"  => "Hummer",
"95"  => "Infiniti",
"102" => "Isuzu",
"71"  => "Iveco",
"228" => "JAC",
"18"  => "Jaguar",
"19"  => "Jeep",
"96"  => "Jinbei (Topic)",
"48"  => "JPX",
"21"  => "Lada",
"52"  => "Lamborghini",
"22"  => "Land Rover",
"23"  => "Lexus",
"106" => "Lifan",
"51"  => "Lincoln",
"105" => "Lobini",
"89"  => "Lotus",
"86"  => "Mahindra",
"24"  => "Maserati",
"72"  => "Matra",
"25"  => "Mazda",
"26"  => "Mercedes-Benz",
"229" => "MG Motors",
"56"  => "MINI",
"85"  => "Oldsmobile",
"90"  => "Pagani",
"57"  => "Plymouth",
"58"  => "Pontiac",
"30"  => "Porsche",
"84"  => "Saab",
"60"  => "Saturn",
"32"  => "Seat",
"61"  => "smart",
"101" => "Spyker",
"41"  => "SsangYong",
"33"  => "Subaru",
"34"  => "Suzuki",
"107" => "TAC",
"47"  => "Troller",
"38"  => "Volvo",
"103" => "AC Cars",
"87"  => "Buggy BRM",
"54"  => "Chamonix",
"92"  => "MG Spayc",
"40"  => "Outras"]

marcas.first.each do |id, marca|
   params = "{id:2,method:\"JsRPC.getModelosByMarca\",params:[#{id}]}\" \"http://www.icarros.com.br/Icarros/JSON-RPC;jsessionid=qVJqnMG2o-y5SGr3MhDGv68q\""
   _modelos = ScraperWiki.scrape("http://www.icarros.com.br/Icarros/JSON-RPC;jsessionid=qVJqnMG2o-y5SGr3MhDGv68q", params).match(/result":"(.*)"/)[1].split("||")
   
   
   i = 0
   modelos = []
   _modelos.each do |modelo|
     if i % 2 == 0 
       puts modelo
       modelos[modelo] = ""
     end

     i = i+1
   end

   puts modelos
   
  break
end
