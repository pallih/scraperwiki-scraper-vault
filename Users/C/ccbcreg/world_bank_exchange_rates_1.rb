require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
require "rubygems"
require 'open-uri'
require 'json'

def country_to_currency
  {"PG"=>{:currency_id=>"146", :id=>"7152"}, "SE"=>{:currency_id=>"68", :id=>"7184"}, "LU"=>{:currency_id=>"26", :id=>"7113"}, "GM"=>{:currency_id=>"119", :id=>"7070"}, "DO"=>{:currency_id=>"115", :id=>"7054"}, "BD"=>{:currency_id=>"100", :id=>"7015"}, "PH"=>{:currency_id=>"60", :id=>"7155"}, "LV"=>{:currency_id=>"46", :id=>"7106"}, "EC"=>{:currency_id=>"81", :id=>"7055"}, "VE"=>{:currency_id=>"174", :id=>"7206"}, "RS"=>{:currency_id=>"151", :id=>"7210"}, "GN"=>{:currency_id=>"122", :id=>"7080"}, "BE"=>{:currency_id=>"26", :id=>"7018"}, "MK"=>{:currency_id=>"90", :id=>"7248"}, "AR"=>{:currency_id=>"3", :id=>"7006"}, "SG"=>{:currency_id=>"69", :id=>"7173"}, "SH"=>{:currency_id=>"148", :id=>"7265"}, "JM"=>{:currency_id=>"127", :id=>"7095"}, "BF"=>{:currency_id=>"13", :id=>"7029"}, "US"=>{:currency_id=>"81", :id=>"7202"}, "ML"=>{:currency_id=>"13", :id=>"7120"}, "LY"=>{:currency_id=>"133", :id=>"7247"}, "GP"=>{:currency_id=>"26", :id=>"7078"}, "PK"=>{:currency_id=>"61", :id=>"7148"}, "YE"=>{:currency_id=>"85", :id=>"7209"}, "EE"=>{:currency_id=>"26", :id=>"7060"}, "RU"=>{:currency_id=>"66", :id=>"7257"}, "AT"=>{:currency_id=>"26", :id=>"7011"}, "SI"=>{:currency_id=>"26", :id=>"7175"}, "BG"=>{:currency_id=>"5", :id=>"7028"}, "MM"=>{:currency_id=>"173", :id=>"7134"}, "GQ"=>{:currency_id=>"93", :id=>"7058"}, "PL"=>{:currency_id=>"62", :id=>"7156"}, "NA"=>{:currency_id=>"52", :id=>"7135"}, "AU"=>{:currency_id=>"4", :id=>"7010"}, "JO"=>{:currency_id=>"39", :id=>"7097"}, "BH"=>{:currency_id=>"6", :id=>"7014"}, "RW"=>{:currency_id=>"147", :id=>"7163"}, "MN"=>{:currency_id=>"141", :id=>"7131"}, "BI"=>{:currency_id=>"107", :id=>"7030"}, "GR"=>{:currency_id=>"26", :id=>"7075"}, "EG"=>{:currency_id=>"88", :id=>"7056"}, "JP"=>{:currency_id=>"40", :id=>"7096"}, "SK"=>{:currency_id=>"26", :id=>"7263"}, "SL"=>{:currency_id=>"153", :id=>"7172"}, "MO"=>{:currency_id=>"134", :id=>"7114"}, "AW"=>{:currency_id=>"97", :id=>"7008"}, "QA"=>{:currency_id=>"64", :id=>"7159"}, "EH"=>{:currency_id=>"47", :id=>"7280"}, "BJ"=>{:currency_id=>"13", :id=>"7020"}, "KE"=>{:currency_id=>"41", :id=>"7099"}, "GT"=>{:currency_id=>"29", :id=>"7079"}, "KG"=>{:currency_id=>"129", :id=>"7104"}, "NE"=>{:currency_id=>"13", :id=>"7143"}, "SN"=>{:currency_id=>"13", :id=>"7170"}, "AZ"=>{:currency_id=>"169", :id=>"7012"}, "SO"=>{:currency_id=>"155", :id=>"7177"}, "MR"=>{:currency_id=>"139", :id=>"7124"}, "KH"=>{:currency_id=>"108", :id=>"7031"}, "BM"=>{:currency_id=>"104", :id=>"7021"}, "UY"=>{:currency_id=>"82", :id=>"7203"}, "CA"=>{:currency_id=>"11", :id=>"7033"}, "UZ"=>{:currency_id=>"164", :id=>"7204"}, "BN"=>{:currency_id=>"106", :id=>"7228"}, "VN"=>{:currency_id=>"84", :id=>"7276"}, "NG"=>{:currency_id=>"53", :id=>"7144"}, "KI"=>{:currency_id=>"4", :id=>"7100"}, "GW"=>{:currency_id=>"13", :id=>"7081"}, "TD"=>{:currency_id=>"93", :id=>"7037"}, "DZ"=>{:currency_id=>"22", :id=>"7002"}, "MT"=>{:currency_id=>"26", :id=>"7121"}, "BO"=>{:currency_id=>"7", :id=>"7023"}, "PR"=>{:currency_id=>"81", :id=>"7158"}, "HK"=>{:currency_id=>"30", :id=>"7085"}, "SR"=>{:currency_id=>"157", :id=>"7182"}, "GY"=>{:currency_id=>"124", :id=>"7082"}, "MU"=>{:currency_id=>"48", :id=>"7125"}, "NI"=>{:currency_id=>"54", :id=>"7142"}, "CC"=>{:currency_id=>"4", :id=>"7231"}, "PS"=>{:currency_id=>"39", :id=>"7254"}, "ZA"=>{:currency_id=>"86", :id=>"7178"}, "MV"=>{:currency_id=>"137", :id=>"7119"}, "CD"=>{:currency_id=>"12", :id=>"7233"}, "PT"=>{:currency_id=>"26", :id=>"7157"}, "MW"=>{:currency_id=>"136", :id=>"7117"}, "BR"=>{:currency_id=>"8", :id=>"7026"}, "TG"=>{:currency_id=>"13", :id=>"7191"}, "HN"=>{:currency_id=>"31", :id=>"7084"}, "ST"=>{:currency_id=>"150", :id=>"7262"}, "LA"=>{:currency_id=>"130", :id=>"7246"}, "KM"=>{:currency_id=>"111", :id=>"7041"}, "BS"=>{:currency_id=>"99", :id=>"7013"}, "CF"=>{:currency_id=>"93", :id=>"7229"}, "NL"=>{:currency_id=>"26", :id=>"7138"}, "TH"=>{:currency_id=>"74", :id=>"7190"}, "MX"=>{:currency_id=>"49", :id=>"7127"}, "ER"=>{:currency_id=>"116", :id=>"7059"}, "BT"=>{:currency_id=>"105", :id=>"7022"}, "CG"=>{:currency_id=>"93", :id=>"7232"}, "LB"=>{:currency_id=>"44", :id=>"7107"}, "MY"=>{:currency_id=>"50", :id=>"7118"}, "ID"=>{:currency_id=>"34", :id=>"7089"}, "MZ"=>{:currency_id=>"171", :id=>"7133"}, "VU"=>{:currency_id=>"165", :id=>"7205"}, "TJ"=>{:currency_id=>"159", :id=>"7188"}, "SV"=>{:currency_id=>"81", :id=>"7057"}, "CH"=>{:currency_id=>"14", :id=>"7185"}, "IE"=>{:currency_id=>"26", :id=>"7092"}, "ES"=>{:currency_id=>"26", :id=>"7179"}, "KP"=>{:currency_id=>"145", :id=>"7244"}, "CI"=>{:currency_id=>"13", :id=>"7234"}, "PY"=>{:currency_id=>"63", :id=>"7153"}, "HR"=>{:currency_id=>"32", :id=>"7235"}, "ET"=>{:currency_id=>"25", :id=>"7061"}, "BW"=>{:currency_id=>"9", :id=>"7025"}, "NO"=>{:currency_id=>"55", :id=>"7146"}, "TM"=>{:currency_id=>"162", :id=>"7196"}, "NP"=>{:currency_id=>"143", :id=>"7137"}, "HT"=>{:currency_id=>"125", :id=>"7083"}, "KR"=>{:currency_id=>"42", :id=>"7245"}, "CK"=>{:currency_id=>"56", :id=>"7044"}, "FI"=>{:currency_id=>"26", :id=>"7065"}, "SY"=>{:currency_id=>"73", :id=>"7268"}, "SZ"=>{:currency_id=>"158", :id=>"7183"}, "FJ"=>{:currency_id=>"118", :id=>"7064"}, "BY"=>{:currency_id=>"102", :id=>"7017"}, "TN"=>{:currency_id=>"75", :id=>"7194"}, "CL"=>{:currency_id=>"15", :id=>"7038"}, "UA"=>{:currency_id=>"80", :id=>"7199"}, "HU"=>{:currency_id=>"33", :id=>"7086"}, "TO"=>{:currency_id=>"160", :id=>"7192"}, "FK"=>{:currency_id=>"117", :id=>"7237"}, "BZ"=>{:currency_id=>"103", :id=>"7019"}, "CM"=>{:currency_id=>"93", :id=>"7032"}, "CN"=>{:currency_id=>"16", :id=>"7039"}, "LI"=>{:currency_id=>"14", :id=>"7111"}, "ZM"=>{:currency_id=>"166", :id=>"7211"}, "GA"=>{:currency_id=>"93", :id=>"7069"}, "CO"=>{:currency_id=>"17", :id=>"7040"}, "LK"=>{:currency_id=>"89", :id=>"7180"}, "IL"=>{:currency_id=>"35", :id=>"7093"}, "AE"=>{:currency_id=>"1", :id=>"7200"}, "KW"=>{:currency_id=>"43", :id=>"7103"}, "GB"=>{:currency_id=>"27", :id=>"7201"}, "TR"=>{:currency_id=>"76", :id=>"7195"}, "AF"=>{:currency_id=>"2", :id=>"7000"}, "UG"=>{:currency_id=>"163", :id=>"7198"}, "AG"=>{:currency_id=>"114", :id=>"7224"}, "KY"=>{:currency_id=>"110", :id=>"7035"}, "DE"=>{:currency_id=>"26", :id=>"7072"}, "IN"=>{:currency_id=>"36", :id=>"7088"}, "CR"=>{:currency_id=>"18", :id=>"7045"}, "TT"=>{:currency_id=>"161", :id=>"7272"}, "WS"=>{:currency_id=>"149", :id=>"7260"}, "KZ"=>{:currency_id=>"128", :id=>"7098"}, "GE"=>{:currency_id=>"120", :id=>"7071"}, "MA"=>{:currency_id=>"47", :id=>"7132"}, "AI"=>{:currency_id=>"114", :id=>"7213"}, "FR"=>{:currency_id=>"26", :id=>"7066"}, "OM"=>{:currency_id=>"57", :id=>"7147"}, "IQ"=>{:currency_id=>"170", :id=>"7091"}, "CU"=>{:currency_id=>"112", :id=>"7048"}, "MC"=>{:currency_id=>"26", :id=>"7130"}, "NZ"=>{:currency_id=>"56", :id=>"7141"}, "PA"=>{:currency_id=>"58", :id=>"7151"}, "MD"=>{:currency_id=>"140", :id=>"7250"}, "CV"=>{:currency_id=>"109", :id=>"7034"}, "IR"=>{:currency_id=>"38", :id=>"7243"}, "TW"=>{:currency_id=>"77", :id=>"7269"}, "IS"=>{:currency_id=>"126", :id=>"7087"}, "DJ"=>{:currency_id=>"113", :id=>"7052"}, "AL"=>{:currency_id=>"94", :id=>"7001"}, "SA"=>{:currency_id=>"67", :id=>"7169"}, "GH"=>{:currency_id=>"28", :id=>"7073"}, "ME"=>{:currency_id=>"26", :id=>"7281"}, "BA"=>{:currency_id=>"167", :id=>"7225"}, "SB"=>{:currency_id=>"154", :id=>"7176"}, "LR"=>{:currency_id=>"132", :id=>"7109"}, "GI"=>{:currency_id=>"121", :id=>"7074"}, "AM"=>{:currency_id=>"96", :id=>"7007"}, "RO"=>{:currency_id=>"65", :id=>"7161"}, "DK"=>{:currency_id=>"21", :id=>"7051"}, "IT"=>{:currency_id=>"26", :id=>"7094"}, "SC"=>{:currency_id=>"152", :id=>"7171"}, "AN"=>{:currency_id=>"144", :id=>"7139"}, "MG"=>{:currency_id=>"135", :id=>"7116"}, "LS"=>{:currency_id=>"131", :id=>"7108"}, "TZ"=>{:currency_id=>"78", :id=>"7270"}, "PE"=>{:currency_id=>"59", :id=>"7154"}, "CY"=>{:currency_id=>"26", :id=>"7049"}, "ZW"=>{:currency_id=>"87", :id=>"7212"}, "AO"=>{:currency_id=>"172", :id=>"7004"}, "SD"=>{:currency_id=>"156", :id=>"7181"}, "DM"=>{:currency_id=>"114", :id=>"7053"}, "BB"=>{:currency_id=>"101", :id=>"7016"}, "CZ"=>{:currency_id=>"20", :id=>"7050"}, "LT"=>{:currency_id=>"45", :id=>"7112"}}
end


def quarters_to_date(val)
  val.gsub("Q1","-03-31").gsub("Q2","-06-30").gsub("Q3","-09-30").gsub("Q4","-12-31")
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def exchange_rate_url(country, date)
  "http://api.worldbank.org/countries/#{country}/indicators/DPANUSLCU?per_page=100&format=json&date=" + date
end

def download_exchange_rates
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    [{:type => "annual", :value => "2000:#{Time.now.year}"}, {:type => "quarterly", :value => "2007Q1:#{Time.now.year}Q4"}].each do |exrate|
      puts exchange_rate_url(country, exrate[:value])
      
      begin
        rates = JSON.parse(open(exchange_rate_url(country, exrate[:value])) {|f| f.read})
        rates = rates[1]
        unless !rates || rates.empty? 
          # puts rates.inspect
          rates.each do |rate|
            r = {
              "id" => x,
              "currency_id" => country_to_currency[country][:currency_id],
              "country_id" => country_to_currency[country][:id],
              "iso2code" => rate["country"]["id"],
              "type" => exrate[:type],
              "name" => rate["country"]["value"],
              "exchange_rate" => rate["value"],
              "decimal" => rate["decimal"],
              "date" => quarters_to_date(rate["date"])
            }
            puts r.inspect
            ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
            x = x + 1
          end
        end
      rescue Exception => e
        puts "There was a problem downloading #{exchange_rate_url(country, exrate[:value])} : #{e}"
      end
      
    end
  end
end

download_exchange_rates
