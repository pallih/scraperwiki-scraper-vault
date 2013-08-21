#!/usr/bin/env python2
from urllib2 import urlopen
from urllib import urlencode

CSS = '''
<link rel="stylesheet" href="http://southafrica.mixmarket.org/css/reset.css" type="text/css">
<!-- <link rel="stylesheet" href="http://southafrica.mixmarket.org/css/style.css" type="text/css"> -->

<style>
h1, h2, h3, h4, h5 {
  color: #3C5E84;
}
body {
  font: 14px/21px Arial,sans-serif;
  color: #282828;
}
html, body {
  width: 100%;
  height: 100%;
  background-color: #F6F6F6;
}

#spreadsheets tr {
  border-top: 1px #DDD solid;
  border-bottom: 1px #DDD solid;
  padding: 2px;
  margin: 2px;
}
#spreadsheets{
  margin:3em auto;
  width: 50%%;
}
#spreadsheets th {
  text-align: left;
  font-family: Georgia, serif;
  color: #2D69A6;
  font-style: italic;
}

#main {
  max-width: 800px;
  margin: auto;
  display: block;
  margin-top: 2em;
  margin-bottom: 5em;
}
h1 { font-size: 26px; line-height: 39px; }
h2 { font-size: 22px; line-height: 33px; }
h3 { font-size: 18px; line-height: 27px; }
</style>
'''

SCRAPERS=[
  #Kenya
  {
    "slug":"amfikenya",
    "columns_sql":{
      "date": '`date_scraped`',
      "source": '"AMFI"',
      "source-type": '"Cooperatives"',

      "entity": '`name`',
      'entity-type': '`type`',
      "location-type": '"Headquarters"',

      "url": '`url`',
      "country": '`country`',
      "source-type": '`source`',
      "phone": '`contact`',
      "fax": '`contact`',
      'full-address': '`address`',

    },
    'table_name': '`swdata`'
  },
  {
    "slug":"central_bank_of_kenya",
    "columns_sql":{
      "date": '`date_scraped`',
      "source": '"CBK"',
      "source-type": '"Regulator"',

      "fax": '`Fax`',
      "phone": 'coalesce(`Telephone`, `Cell - phone`)',
      "email": '`Email`',

      "entity": '`entity`',
      "entity-type": '"Micro-Enterprise Lender"',
      "location-type": '"Headquarters"',

      "full-address": 'coalesce(`Physical Address`, `Postal Address`)',
      "country": '"Kenya"',
      "url": '"http://www.centralbank.go.ke/financialsystem/microfinance/deposittaking.aspx"',
    },
    'table_name': '`swdata`'
  }

, {
    "slug":"sasra2",
    "columns_sql":{
      "date": '`date_scraped`'
    , "source": '"SASRA"'
    , "source-type": '"Regulator"'
    , "entity":'`NAME_OF_SOCIETY`'
    , 'entity-type': '"Cooperatives"'

    , "location-type": '"Headquarters"'

# `page-problems` text, `DATE_LICENSED`
    , "url": '"http://www.sasra.go.ke/downloads/licensedsaccos.pdf"'

    , "country": '"Kenya"'
    , 'town': '`city`'
    , 'postal-code': '`postal-code`'

    , 'full-address': '`POSTAL_ADDRESS`'

    },
    'table_name': '`societies`'
  }
, {
    "slug":"safaricom",
    "columns_sql":{
      "date": '`date_scraped`'
    , "source": '"Safaricom"'
    , "source-type": '"Development Finance Institution"'
    , "entity":'`Dealer`'
    , 'entity-type': '"Development Finance Institution"'

    , "location-type": '"NA"'

    , "country": '"Kenya"'
    , 'town': '`Town`'

    , 'url': '`url`'
    , 'province': '`Region`'
    , 'street-address': '`Physical Address`'

    },
    'table_name': '`parsed`'
  }

  #Rwanda
, {
    "slug":"rwandamicrofinance",
    "columns_sql":{
      "date": '`date_scraped`',
      "source": '"AMIR"',
      "source-type": '"Cooperatives"',

      "country": '"Rwanda"',
      "email": '`email`',
      'town': '`place`'
    , "entity":'`name`'
    , 'entity-type': '`standardtype`'

    , "location-type": '"NA"'

    },
    'table_name': '`swdata`'
  }
, {
    "slug": "bank_of_kigali",
    "columns_sql": {
      "date":'`date-scraped`'

    , "source":'"Bank of Kigali"'
    , "source-type":'"Banks"'
    , "entity":'"Bank of Kigali"'
    , "entity-type":'"Banks"'
    , "location-type":'"Branch"'

    , "url":'`url`'

    , "town":'`town`'
    , "country":'"Rwanda"'
    , "street-address":'`street-address`'

    , "phone":'coalesce(`phone`, `mob`)'
    },
    "table_name": '`parsed`'
  },
  {
    "slug":"banque_commerciale_du_rwanda_ltd"
  , "columns_sql":{
      "date":'`date_scraped`'

    , "source":'"BCR"'
    , "source-type":'"Banks"'
    , "entity":'"BCR"'
    , "entity-type":'"Banks"'
    , "location-type":'"Branch"'

    , "url":'"http://www.bcr.co.rw/index.php/site-map/our-branch-network"'


    , "street-address": '`street_address`'
    , "town":'`BRANCH-NAME`'
    , "province": '`province`'
    , "district": '`district`'
    , "subdistrict": '`sector`'
    , "country":'"Rwanda"'
    , "full-address":'`address`'

    , "phone":'`CONTACTS`'

    }
  , "table_name":'`swdata`'
  }
, {
    "slug":"national_bank_of_rwanda"
  , "columns_sql":{
      "date":'`date_scraped`'

    , "source":'"BNR"'
    , "source-type":'"Banks"'
    , "entity":'`name`'
    , "entity-type":'"Banks"'

    , "location-type":'"Headquarters"'

    , "url":'"http://www.bnr.rw/supervision/bankregister.aspx"'

    , "country":'"Rwanda"'
    , "full-address":'`address`'

    , "phone":'`phone`'

    }
  , "table_name":'`institutions`'
  }
, {
    "slug":"banque_populaire_du_rwanda_ltd"
  , "columns_sql":{
      "date":'`date_scraped`'

    , "source":'"BPR"'
    , "source-type":'"Banks"'
    , "entity":'"BPR"'
    , "entity-type":'"Banks"'
    , "location-type":'"Branch"'

    , "url":'"http://www.bpr.rw/" || `href`'

    , "town":'`name`'
    , "country":'"Rwanda"'
    , "full-address":'`name` || ", " || `region`'

    , "phone":'`Tel`'
    , "fax":'`Fax`'

    }
  , "table_name":'`branches`'
  }
, {
    "slug":"finabank_cash",
    "columns_sql":{
      "date": '`date_scraped`'
    , "country": '"Rwanda"'
    , "phone": '`phone`'
    , "fax": '`fax`'

    , 'street-address': '`street-address`'
    , 'town': '`town`'

    , "entity":'"Fina Bank"'
    , "entity-type": '"Banks"'

    , "source": '"Fina Bank"'
    , "source-type": '"Banks"'

    , 'location-type': '"ATM"'
    },
    'table_name': '`swdata`'
  }
, {
    "slug": "uob"
  , "columns_sql":{
      "date": '`date_scraped`',
      "source": '"UOB"',
      "source-type": '"Banks"',
      "entity": '"UOB"',
      "entity-type": '"Banks"',
      "location-type": '"Branch"'


    , "town": 'coalesce(`town`, `branch-name`)'
    , "province": 'coalesce(`town`, `branch-name`)' #See Scott's notes in column N

    , "district": '`district`'
    , "country": '"Rwanda"'
    , "phone": '`phone`'
    , "full-address": '`full-address`'
    , "street-address": '`street-address`'
    }
  , "table_name": '`swdata`'
  }
  #South Africa
, {
    "slug":"absa3"
  , "columns_sql":{
      "date":'`date_scraped`'

    , "source":'"Absa Bank"'
    , "source-type":'"Banks"'
    , "entity":'"Absa Bank"'
    , "entity-type":'"Banks"'
    , "location-type":'"Branch"'

    , "url":'"http://www.absa.co.za/Absacoza/Contact-Us"'

    , "street-address":'`Street_Address`'
    , "town":'`City`'
    , "district":'`Name`'
    , "country":'"South Africa"'
    , "full-address":'`Street_Address` || ", " || `City`'

    , "phone":'`Tel`'

    }
  , "table_name":'`initial`'
  }
, {
    "slug":"african_bank"
  , "columns_sql":{
      "date":'`date_scraped`'
    , "entity":'"African Bank"'
    , "entity-type":'"Banks"'

    , "source":'"African Bank"'
    , "source-type":'"Banks"'

    , "location-type":'"Branch"'

    , "url":'"https://www.africanbank.co.za/default9.jsf"'


    , "phone":'`Telephone`'

    , "street-address":'`Street_Address`'
    , "town":'`CityName`'
    , "province":'`provinceName`'
    , "country":'"South Africa"'
    , "full-address":'`Street_Address` || ", " || `CityName` || ", " || `provinceName`'
    }
  , "table_name":'`branches`'
  }
, {
    "slug":"bidvest_bank"
  , "columns_sql":{
      "date":'`date_scraped`'
    , "source":'"Bidvest Bank"'
    , "source-type":'"Banks"'
    , "entity":'"Bidvest Bank"'
    , "entity-type":'"Banks"'
    , "location-type":'"Branch"'

    , "full-address":'`Address_`'
    , "phone":'`Tel_`'
    , "fax":'`Fax_`'
    , "province":'`regionName`'

    , "url":'"http://www.bidvestbank.co.za/contact-us/Branch-Locator.aspx"'
    , "country":'"South Africa"'

    , "street-address":'`street-address`'
    , "postal-code":'`postal-code`'
    , "town":'`town`'
    }
  , "table_name": '`final`'
  }
, {
    "slug": 'blue_financial_services'
  , "columns_sql": {
      "date": '`DATE_SCRAPED`'
    , "source": '"Blue Financial Services"'
    , "source-type": '"Development Finance Institutions"'
    , "entity": '"Blue Financial Services"'
    , "entity-type": '"Development Finance Institutions"'
    , "location-type": '"Branch"'

    , "url": '"http://www.blue.co.za/"'

    , "full-address": '`ADDRESS`'
    , "fax": '`FAX`'

    , "phone": '`TELEPHONE`'

    , "town": '`TOWN`'
    , "country": '`COUNTRY`'

    , "email": '`EMAIL`'
    }
  , "table_name":'`swdata`'
  }
, {
    "slug":"capitec_bank"
  , "columns_sql":{
      "date":'`date-scraped`'
    , "source":'"Capitec Bank"'
    , "source-type":'"Banks"'
    , "entity":'"Capitec Bank"'
    , "entity-type":'"Banks"'
    , "location-type":'"Branch"'

    , "phone":'`phone`'
    , "email":'`email`'

    , "full-address":'`address`'
    , "town":'`branchName`'
    , "province":'`provinceName`'
    , "country":'"South Africa"'

    , "url":'"http://www.capitecbank.co.za/contact-us/branch-locator/"'

   , "latitude-scrape":'`latitude`'
   , "longitude-scrape":'`longitude`'

    }
  , "table_name":'`branches`'
  }
, {
    "slug":"fnb_south_africa"
  , "columns_sql":{
      "date":'`date_scraped`'

    , "source":'"First National Bank"'
    , "source-type":'"Banks"'

    , "entity":'"First National Bank"'
    , "entity-type":'"Banks"'
    , "location-type":'"Branch"'

    , "url":'"https://www.fnb.co.za/contact-us/locators/branchLocator/frontEndEnh.html"'

    , "street-address":'`Street_Address`'
    , "town":'`name`'
    , "postal-code":'`postcode`'
    , "country":'"South Africa"'

    , "full-address":'`Postal_Address`'


    , "phone":'`Telephone_Number`'
    , "fax":'`Fax_Number`'
    }
  , "table_name":'`final`'
  }
, {
    "slug":"gbsbank"
  , "columns_sql":{
      "date":'`date_scraped`'
    , "source":'"GBS Mutual Bank"'
    , "source-type":'"Cooperatives"'

    , "entity":'"GBS Mutual Bank"'
    , "entity-type":'"Cooperatives"'

    , "location-type":'`office-type`'

    , "full-address":'`street-address`'
    , "street-address":'`street-address`'

    , "url":'`url`'
    , "country":'"South Africa"'

    , "email":'`email`'
    , "phone":'`phone`'
    }
  , "table_name":'`final`'
  }
, {
    "slug": 'ithala_finance_corporates_-_branches'
  , "columns_sql": {
      "date": '`DATE-SCRAPED`'
    , "source": '"Ithala Development Finance Corporation"'
    , "source-type": '"Development Finance Corporations"'
    , "entity": '"Ithala Development Finance Corporation"'
    , "entity-type": '"Development Finance Corporations"'
    , "location-type": '"Branch"'
    , "url": '"http://www.ithala.co.za/Ithala_Limited/LocateBranch/Pages/default.aspx"'

    , "full-address": '`PHYSICAL_ADDRESS`'
    , "fax": '`FACSIMILE_NUMBER`'
    , "phone": '`TELEPHONE_NUMBER`'

    , "street-address": '`BRANCH_NAME`'
    , "town": '`TOWN`'
    , "province": '"KwaZulu Natal"'
    , "postal-code": '`POSTAL-CODE`'
    , "country": '"South Africa"'

    , "email": '`BRANCH_MANAGER_EMAIL`'
    }
  , "table_name":'`swdata`'
  }
, {
    "slug":"khula"
  , "columns_sql":{
      "date":'`date_scraped`'

    , "entity":'"Khula"'
    , "source-type":'"Development finance institutions"'
    , "entity":'"Khula"'
    , "entity-type":'"Development finance institutions"'

    , "location-type":'"Regional Office"'

    , "full-address":'`Address`'
    , "phone":'`Telephone_Number`'
    , "fax":'`Fax_Number`'
    , "province":'`province`'
    , "country":'"South Africa"'

    , "url":'"http://www.khula.org.za/Admin/Contacts/RegionalContacts.aspx"'
    , "country":'"South Africa"'

    , "street-address":'`street-address`'
    , "town":'replace(`town`, ".", "") '
    }
  }
, {
    "slug":"landbank_satellite_branches"
  , "columns_sql":{
      "date":'`date_scraped`'
    , "source":'"Land Bank"'
    , "source-type":'"Banks"'
    , "entity":'"Land Bank"'
    , "entity-type":'"Banks"'
    , "url":'"http://www.landbank.co.za/contact/satellite_branches.php"'

    , "town":'`satellite`'
    , "country":'"South Africa"'
    , "full-address":'`satellite`'
    , "location-type":'"Satellite Branch"'
    }
  , "table_name":'`final`'
  }
, {
    "slug":"landbank_branches"
  , "columns_sql":{
      "date":'`date_scraped`'
    , "source":'"Land Bank"'
    , "source-type":'"Banks"'

    , "entity":'"Land Bank"'
    , "entity-type":'"Banks"'
    , "location-type":'"Branch"'

    , "url":'"http://www.landbank.co.za/contact/branches.php"'

    , "full-address":'`address`'
    , "street-address":'`street-address`'
    , "town":'`branchName`'
    , "postal-code":'`postcode`'

    , "country":'"South Africa"'

    , "phone":'`Tel`'
    , "fax":'`Fax`'
    }
  , "table_name":'`branches`'
  }
, {
    "slug":"marang_offices"
  , "title":"marang branches"
  , "columns_sql":{
      "date":'`date_scraped`'

    , "source":'"Marang"'
    , "source-type":'"Microenterprise Lenders"'

    , "entity":'"Marang"'
    , "entity-type":'"Microenterprise Lenders"'

    , "location-type":'"Branch"'

    , "url":'`url`'

    , "full-address":'`full-address`'
    , "street-address":'`street-address`'
    , "postal-code":'`postal-code`'
    , "province":'replace(replace(`region`,"branch-",""),".asp","")'
    , "country":'"South Africa"'


    , "phone":'`Tel_No`'
    , "fax":'`Fax_No`'
    , "email":'`Email`'

    }
  , "table_name":'`branches`'
  }
, {
    "slug":"marang_offices"
  , "title":"marang regional offices"
  , "columns_sql":{
      "date":'`date_scraped`'
    , "url":'`url`'

    , "source":'"Marang"'
    , "source-type":'"Development Finance Institutions"'
    , "entity":'"Marang"'
    , "entity-type":'"Development Finance Institutions"'
    , "location-type":'"Regional office"'

    , "country":'"South Africa"'
    , "province":'replace(`Regional_Offices`," Regional Office","")'


    , "phone":'`Contact_No`'

    , "full-address":'`Address`'
    }
  , "table_name":'`regional_offices`'
  }
, {
    "slug":"ncr5"
  , "columns_sql":{
      "date":'`ScraperRun`'

    , "source":'"NCR"'
    , "source-type":'"Regulator"'

    , "entity":'`Name`'
#   , "entity-type":'`registrant-type`'
    , "entity-type":'"Other Credit Providers"'

    , "location-type": '"Headquarters"'

    , "url":'"http://www.ncr.org.za/register_of_registrants/cp.php"'
  
    , "license-number":'`NCRNumber`'
  
    , "full-address":'`PhysicalAddress`'
  
    , "town":'`Town`'
    , "phone":'`Phone`'
    , "fax":'`Fax`'
    , "country":'"South Africa"'
    }
  , "table_name":'`Registrant`'
  }
, {
    "slug":"nedbank_branches2"
  , "columns_sql":{
      "date":'provinces.scraperrun'
    , "url":'`branchUrl`'

    , "source":'"Nedbank"'
    , "source-type":'"Banks"'

    , "entity":'"Nedbank"'
    , "entity-type":'"Banks"'
    , "location-type":'"Branch"'

    , "country":'"South Africa"'
    , "province":'`provinceName`'
    , "town":'`cityName`'
    , "district":'`subtown`'

    , "phone":'`Tel_No`'
    , "email":'`Email`'

    , "full-address":'`address`'
    , "street-address":'`street-address`'

    , "latitude-scrape": '`map_Latitude_`'
    , "longitude-scrape": '`map_Longitude_`'

    }
  , "table_name": 'branches '
      'join cities on branches.cityUrl = cities.cityUrl '
      'join provinces on cities.provinceUrl = provinces.provinceUrl '
  }
, {
    "slug":"nyda"
  , "columns_sql":{
      "date":'`provinces`.`date_scraped`'
    , "url":'`provinceUrl`'

    , "source":'"NYDA"'
    , "source-type":'"Development Finance Institutions"'

    , "entity":'"NYDA"'
    , "entity-type":'"Development Finance Institutions"'

    , "location-type":'"Branch"'

    , "country":'"South Africa"'
    , "province":'`provinces`.`province`'

    , "full-address": '`Physical_Address`'
    , "postal-code":'`postal-code`'

    , "phone":'`Telephone`'
    , "fax": '`fax`'

    , "full-address":'`Physical_Address`'
    }
  , "table_name":'`locations` JOIN `provinces` ON `locations`.`provinceUrl` = `provinces`.`url`'
  }
, {
    "slug":"south_africa_postbank"
  , "columns_sql":{
      "date":'`branch_info`.`date_scraped`'
    , "url":'"http://www.postbank.co.za/contact.aspx?ID=3"'

    , "source":'"Postbank"'
    , "source-type":'"Postbanks"'
    , "entity":'"Postbank"'
    , "entity-type":'"Postbanks"'

    , "location-type":'"Branch"'

    , "country":'"South Africa"'
    , "town":'`loc1`'
    , "district":'`loc2`'
    , "province":'`loc2`'

    # No province :(

    , "phone":'`Tel`'
    , "fax":'`Fax`'

    , "full-address":'`Address`'
    }
  , "table_name":'`branch_info` join `branch_names` on `branch_info`.`branchId`=`branch_names`.`branchId`'
  }
, {
    "slug":"realpeople"
  , "columns_sql":{
      "date":'`date_scraped`'
    , "url":'"http://www.realpeople.co.za/Downloads/COR%200275%20BRANCH%20LIST.pdf"'

    , "source":'"Real People"'
    , "source-type":'"Other Credit Providers"'
    , "entity":'"Real People"'
    , "entity-type":'"Other Credit Providers"'

    , "location-type":'"Branch"'

    , "country":'"South Africa"'
    , "province":'`PROVINCE`'
    , "town": '`town`'
    , "street-address": '`street-address`'

    , "phone":'`TELEPHONE`'
    , "fax":'`FAX`'
    , "email": '`E-MAIL ADDRESSES`'

    , "full-address":'`ADDRESS`'
    }
  , "table_name":'`swdata`'
  }
, {
    "slug":"saccos2"
  , "columns_sql":{
      "date":'`date_scraped`'
    , "source":'"SACCOL"'
    , "source-type":'"Cooperatives"'
    , "entity":'`SACCO`'
    , "entity-type":'"Cooperatives"'
    , "location-type":'"Contact person?"'

    , "url":'"http://www.saccol.org.za/saccos_in_saccol.php"'

    , "street-address":'`street-address`'
    , "town":'`town`'
    , "postal-code":'`postal-code`'
    , "country":'"South Africa"'

    , "full-address":'`street-address`||", "||`town`||", "||`postal-code`'


    , "phone":'`phone`'
    }
  , "table_name":'`final`'
  }
, {
    "slug":"standardbank"
  , "columns_sql": {"date": 0}
  , "display_links": False
  , "table_name": '`branches`'
  }
, {
    "slug":"sasfin"
  , "columns_sql":{
      "date":'`date_scraped`'
    , "source":'"Sasfin bank"'
    , "source-type":'"Banks"'
    , "entity":'"Sasfin bank"'
    , "url":'`url`'

    , "full-address":'`Physical_address`'

    , "entity-type":'"Banks"'
    , "location-type":'"Office"'

    , "phone":'`Contact_Details`'
    , "country":'"South Africa"'
    }
  , "table_name":'`officeinfo`'
  }
, {
    "slug":"tebabank_branch"
  , "columns_sql":{
      "date":'`date_scraped`'

    , "source":'"U Bank"'
    , "source-type":'"Banks"'
    , "entity":'"U Bank"'
    , "entity-type":'"Banks"'
    , "location-type":'"Branch"'

    , "full-address":'`address`'

    , "url":'"http://www.tebabank.co.za/dist_branch_locs.php"'
    , "country":'"South Africa"'
    , "town":'`town`'
    , "phone":'`phone`'
    }
  , "table_name":'`swdata`'
  }
, {
    "slug":"tebabank_atm"
  , "columns_sql":{
      "date":'`date_scraped`'
    , "source":'"U Bank"'
    , "source-type":'"Banks"'

    , "entity":'"U Bank"'
    , "entity-type":'"Banks"'
    , "location-type":'"ATM"'

    , "full-address":'`address`'
    , "town": '`town`'

    , "url":'"http://www.tebabank.co.za/dist_atm.php"'
    , "country":'"South Africa"'
    }
  , "table_name":'`swdata`'
  }
, {
    "slug": "thuthukani_financial_services"
  , "columns_sql": {
      "date":'`date_scraped`'
    , "source":'"Thuthukani Financial Services"'
    , "source-type":'"Other credit providers"'

    , "entity":'"Thuthukani Financial Services"'
    , "entity-type":'"Other credit providers"'
    , "location-type":'"Branch"'

    , "url": '`url`'
    , "full-address":'`full-address`'

    , "street-address": '`street_address`'
    , "town": '`town`'
    , "province": '`province`'
    , "postal-code": '`postcode`'
    , "country": '"South Africa"'

    , "email": '`email`'
    }
  , "table_name": '`swdata`'
  }
]


geocoded_spreadsheet = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=geocode_all_mix_scrapers_final_for_south_africa&query=SELECT%0A%20%20%60Date_data_was_extracted%60%20AS%20%22Date%20data%20was%20extracted%22%2C%0A%20%20%60Name_of_data_source%60%20AS%20%22Name%20of%20data%20source%22%2C%0A%20%20%60URL_of_data_source%60%20AS%20%22URL%20of%20data%20source%22%2C%0A%20%20%60Name_of_entity%60%20AS%20%22Name%20of%20entity%22%2C%0A%20%20%60Location_type%60%20AS%20%22Location%20type%22%2C%0A%20%20%60Address%60%20AS%20%22Address%22%2C%0A%20%20%60Telephone%60%20AS%20%22Telephone%22%2C%0A%20%20%60Fax%60%20AS%20%22Fax%22%2C%0A%20%20%60Email%60%20AS%20%22Email%22%2C%0A%20%20%60License_number%60%20AS%20%22License%20number%22%2C%0A%20%20%60Type_of_entity%60%20AS%20%22Type%20of%20entity%22%2C%0A%20%20%60Country%60%20AS%20%22Country%22%2C%0A%20%20%60Province%60%20AS%20%22Province%22%2C%0A%20%20%60Sub-district%60%20AS%20%22Sub-district%22%2C%0A%20%20%60Town%60%20AS%20%22Town%22%2C%0A%20%20%60Street_address%60%20AS%20%22Street%20address%22%2C%0A%20%20%60Postal_code%60%20AS%20%22Postal%20code%22%2C%0A%20%20%60latitude%60%20AS%20%22Latitude%22%2C%0A%20%20%60longitude%60%20AS%20%22Longitude%22%2C%0A%20%20%60latitude-scraped%60%20AS%20%22Latitude%20(Scraped)%22%2C%0A%20%20%60longitude-scraped%60%20AS%20%22Longitude%20(Scraped)%22%2C%0A%20%20%60latitude-geocode%60%20AS%20%22Latitude%20(Geocoded)%22%2C%0A%20%20%60longitude-geocode%60%20AS%20%22Longitude%20(Geocoded)%22%0AFROM%20%60final%60%3B'

APIURL="https://api.scraperwiki.com/api/1.0/datastore/sqlite?"
ORDERED_KEYS=(
  "date"
, "source"
, "source-type"
, "url"
, "entity"
, "entity-type"
, "location-type"
, "full-address"
, "phone"
, "fax"
, "email"
, "license-number"
, "license-date"
, "country"
, "province"
, "district"
, "subdistrict"
, "town"
, "street-address"
, "postal-code"
, "latitude-scrape"
, "longitude-scrape"
)

def main():
  links=[]
  for scraper in SCRAPERS:
    s=Spreadsheet(scraper['slug'])
    s.setsql(scraper['columns_sql'])
    url= s.geturl(table_name=scraper['table_name'],date_scraped=scraper['columns_sql']['date']) if scraper.has_key('table_name') else s.geturl()

    link={"slug":scraper['slug'],"url":url}
    link['title']=scraper['title'] if scraper.has_key('title') else scraper['slug']
    link['display_links'] = scraper.get('display_links', True)
    links.append(link)

  print '<html>'
  print '<head>'
  print CSS
  print '</head>'
  print '<body><div id="main">'
  print """<h1 style="text-align: center;">Financial inclusion data scrapers</h1>
    <p style="margin: 0.7em 25%; text-align: center;">
      Developed by <a href="http://thomaslevine.com">Thomas Levine</a> for the 
      <a href="http://www.themix.org/">Microfinance Information Exchange</a>'s
      <a href="http://southafrica.mixmarket.org/">South Africa Map of Financial Inclusion</a>
    </p>
    <p>
      Locations of various South African, Kenyan and Rwandan financial providers
      are extracted from dozens of websites and presented in the spreadsheets below.
      These data power a <a href="http://southafrica.mixmarket.org/">map</a> of financial inclusion.
    </p>
"""
  printlinks(links)
  #printrcode([link['url'].replace('https','http').replace('htmltable','csv') for link in links]) 
  printdocs()

def printrcode(urls):
  print """
<h2>All as one sheet</h2>
<p>
  Download all of these spreadsheets plus the manual data spreadsheet as one csv from
  <a href="https://views.scraperwiki.com/run/combine_mix_scraper_spreadsheets/">this link</a>.
  It only combines the spreadsheets after you click, so it takes a few seconds.
</p>

<p>
  Alternatively, paste the contents of the text box below into an R shell
  to load the combined data for all of the scrapers.
  They will be combined into one data frame named "df".
</p>
"""
  print """<textarea readonly style="width:100%;height:800px">"""
  print "urls<-c('%s')" % "','".join(urls)
  print "df<-Reduce(function(a,b){rbind(a,read.csv(b))},urls,init=read.csv('http://api.scraperwiki.com/api/1.0/datastore/sqlite?query=SELECT+%60date_scraped%60+as+%22Date+data+was+extracted%22%2C%22ubank%22+as+%22Name+of+data+source%22%2C%22http%3A%2F%2Fwww.tebabank.co.za%2Fdist_branch_locs.php%22+as+%22URL+of+data+source%22%2C%22Ubank%22+as+%22Name+of+entity%22%2C%22branch%22+as+%22Location+type%22%2C%60address%60+as+%22Address%22%2C%60phone%60+as+%22Telephone%22%2C%22NA%22+as+%22Fax%22%2C%22NA%22+as+%22Email%22%2C%22NA%22+as+%22License+number%22%2C%22NA%22+as+%22License+date%22%2C%22bank%22+as+%22Type+of+entity%22%2C%22South+Africa%22+as+%22Country%22%2C%22NA%22+as+%22Province%22%2C%22NA%22+as+%22District%22%2C%22NA%22+as+%22Sub-district%22%2C%60town%60+as+%22Town%22%2C%22NA%22+as+%22Street+address%22%2C%22NA%22+as+%22Postal+code%22+FROM+swdata+WHERE+date_scraped%3D%28SELECT+max%28date_scraped%29+from+%60swdata%60%29%20limit%200%3B&name=tebabank_branch&format=csv'))"
  print "df$Date.data.was.extracted<a-as.POSIXlt(df$Date.data.was.extracted,origin='1970-01-01')"
  print "</textarea>"

def printlinks(links):
  print """
<h2>Individual scraper spreadsheets</h2>
<p>
  The table below links to automatically updated spreadsheets from each of the scrapers.
  Use html to view in a web browser, and use csv to load into a spreadsheet program.
  The <a href="https://scraperwiki.com/scrapers/ncr5/">NCR business premises scraper</a>
  is not included in this list because it probably duplicates much of the data.
</p>
"""
  table_rows = []
  for link in links:
    if link['display_links']:
      template = '<tr><td><a href="%s">%s</a></td><td><a href="%s">html</a></td><td><a href="%s">csv</a></td></tr>'
      table_rows.append(template % ("https://scraperwiki.com/scrapers/%s/"%link['slug'],link['title'],link['url'],link['url'].replace('htmltable','csv')) )
    else:
      template = '<tr><td><a href="%s">%s</a><td colspan = "2">must run locally</td></tr>'
      table_rows.append(template % ("https://scraperwiki.com/scrapers/%s/"%link['slug'],link['title']) )

  print """
<table id="spreadsheets">
  <thead>
    <tr><th>Scraper</th><th colspan="2">Spreadsheet</th></tr>
  </thead>
  <tbody>
%s
  </tbody>
</table>
""" % ''.join(table_rows)
  
def printdocs():
  print '''
<h2>Technical documentation</h2>
<h3>Architecture</h3>
<p>
  Dozens of independent scraper scripts scrape the various webpages.
  The current page transforms the script output into a standard format, which you can download by clicking the "html" or "csv"  links.
  <a href="https://scraperwiki.com/scrapers/combine_mix_scraper_spreadsheets_1/edit/">A separate script</a>
  combines all of the data on the present page, plus a few datasets hosted on <a href="http://hacks.thomaslevine.com">Tom's website</a>, into
  <a href="https://views.scraperwiki.com/run/combine_mix_scraper_spreadsheets/">one long spreadsheet</a>.
  The <a href="https://scraperwiki.com/scrapers/geocode_all_mix_scrapers_final_for_south_africa/">geocoder</a>
  downloads this spreadsheet, runs various address fields through various geocoding services
  and results in <a href="''' + geocoded_spreadsheet + '''">this</a> spreadsheet.
</p>
<h3>Adding scripts</h3>
<p>
  Add a script by creating a new "scraper" on ScraperWiki and adding an entry for it in the present page.
  To create the entry, <a href="https://scraperwiki.com/views/mix_scraper_spreadsheets/edit/">edit the current page</a>
  and add a dictionary to the SCRAPERS list. The dictionary must be in the following format.
</p>
<pre>
  {
    "slug": 'foo'
  , "title": 'bar'
  , "columns_sql": {
      "date": '"NA"'
    , "source": '"NA"'
    , "source-type": '"NA"'
    , "url": '"NA"'
    , "entity": '"NA"'
    , "entity-type": '"NA"'
    , "location-type": '"NA"'
    , "full-address": '"NA"'
    , "phone": '"NA"'
    , "fax": '"NA"'
    , "email": '"NA"'
    , "license-number": '"NA"'
    , "license-date": '"NA"'
    , "country": '"NA"'
    , "province": '"NA"'
    , "district": '"NA"'
    , "subdistrict": '"NA"'
    , "town": '"NA"'
    , "street-address": '"NA"'
    , "postal-code": '"NA"'
    , "latitude-scrape": '"NA"'
    , "longitude-scrape": '"NA"'
    }
  , "table_name":'`swdata`'
  }
</pre>
<p>
  The "slug" field is necessary, and the "title" field is an optional name in case the slug is not explanatory.
  Aside from these, all fields are SQL fragments corresponding to either a column or a table, and
  any field that is omitted will be replaced with a default (usually "NA").
</p>
<h3>Running and editing scripts</h3>
<p>
  Click on the link in the first column of the table above to run or edit a script.
  To run them, click the "Run Now" button or set the schedule; if you set the schedule, the scripts will run periodically but not necessarily right away.
  The scripts have "protected" permissions, so Tom needs to add you as an editor for you to run or edit them.
</p>
<h3>Backing up data</h3>
<p>
  Each scraper script has an associated database that stores its own backups,
  and the <a href="https://scraperwiki.com/scrapers/combine_mix_scraper_spreadsheets_1/">spreadsheet combiner</a>
  makes weekly backups of the combined spreadsheet.
  In order to back up the data off of ScraperWiki, periodically download the
  <a href="https://scraperwiki.com/views/combine_mix_scraper_spreadsheets/">current combined spreadsheet</a>
  and the <a href="https://scraperwiki.com/scrapers/export_sqlite/combine_mix_scraper_spreadsheets_1/">database of past spreadsheets</a>.
  The MIX staff should understand how to use the former backup, and a programmer will be able to use the latter.
</p>

<h3>Backing up scripts</h3>
<p>
  Click <a href="https://views.scraperwiki.com/run/retrieve-mix-scrapers/">here</a> to download an archive of all of the scripts.
  You will probably only need this if ScraperWiki drastically changes or goes out of business.
  The scripts will need to be slighly altered in order to run without ScraperWiki,
  but my <a href="github.com/tlevine/dumptruck">DumpTruck</a> library should help with that.
</p>

<script>
<!-- Turn the "Powered by ScraperWiki" into an edit link -->
setTimeout(function(){
  document.getElementById('scraperwikipane').children[0].href='https://scraperwiki.com/scrapers/mix_scraper_spreadsheets/edit/'
}, 1000)
</script>
'''
  print '</div></body>'
  print '</html>'

class Spreadsheet:
  def __init__(self,scraper_slug):
    """columns_sql is the sql for each column; it should be formatted like so
    {"date":"date_scraped","source":'"bidvest"',"full-address":"Address_"}
    """
    self.columns=self.defaultcolumns()
    self.scraper_slug=scraper_slug

  def setsql(self,columns_sql):
    #Check that the columns_sql has identifiers
    #print self.columns
    #print columns_sql
    assert set(self.columns.keys()).issuperset(set(columns_sql.keys()))

    for key in columns_sql.keys():
      self.columns[key]['sql']=columns_sql[key]

  def geturl(self,format="htmltable",table_name='final',date_scraped='`date_scraped`'):
    "Get the second-most-recent date scraped; this ignores partial scrapes"
    query_end="FROM %s WHERE %s=(SELECT %s FROM %s ORDER BY %s DESC LIMIT 1 OFFSET 1);" % (table_name,date_scraped,date_scraped,table_name,date_scraped)
    params={
      "format":format
    , "name":self.scraper_slug
    , "query":self.build_query(query_end)
    }
    #print params
    return "%s%s" % (APIURL,urlencode(params))

  def build_query(self,query_end):
    select_columns=','.join(["%s as \"%s\"" % (c['sql'],c['longname']) for c in [self.columns[k] for k in ORDERED_KEYS]])
    return "SELECT %s %s" % (select_columns,query_end)

  @staticmethod
  def defaultcolumns():
    columns={
      "date":{
        "longname":"Date data was extracted"
      }
    , "source":{
         "longname":"Name of data source"
      }
    , "url":{
         "longname":"URL of data source"
      }
    , "entity":{
         "longname":"Name of entity"
      }
    , "location-type":{
         "longname":"Location type"
      }
    , "full-address":{
         "longname":"Address"
      }
    , "phone":{
         "longname":"Telephone"
      }
    , "fax":{
         "longname":"Fax"
      }
    , "email":{
         "longname":"Email"
      }
    , "license-number":{
         "longname":"License number"
      }
    , "license-date":{
         "longname":"License date"
      }
    , "source-type":{
         "longname":"Type of source"
      }
    , "entity-type":{
         "longname":"Type of entity"
      }
    , "country":{
         "longname":"Country"
      }
    , "province":{
         "longname":"Province"
      }
    , "district":{
         "longname":"District"
      }
    , "subdistrict":{
         "longname":"Sub-district"
      }
    , "town":{
         "longname":"Town"
      }
    , "street-address":{
         "longname":"Street address"
      }
    , "postal-code":{
         "longname":"Postal code"
      }
    , "latitude-scrape":{
        "longname":"latitude-scraped"
      }
    , "longitude-scrape":{
        "longname":"longitude-scraped"
      }
    }

    for key in columns.keys():
      columns[key]['sql']='"NA"'
    return columns

main()
