<!doctype html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!-- Consider adding a manifest.appcache: h5bp.com/d/Offline -->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title></title>
  <meta name="description" content="">

  <!-- Mobile viewport optimized: h5bp.com/viewport -->
  <meta name="viewport" content="width=device-width">

    <link rel="stylesheet" href="http://tablesorter.com/themes/blue/style.css" />

    <style type="text/css">

        table.tablesorter { width: auto; }
        table.tablesorter tbody td { min-width:150px; }

    </style>

  <link rel="stylesheet" href="css/style.css" />
    <script src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
    <script src="http://tablesorter.com/__jquery.tablesorter.min.js"></script>


<script>

    $(document).ready(function() {
        $("table.tablesorter").tablesorter();
    });

</script>

</head>
<body>
  <header>

  </header>
  <div role="main">



<?php
# Blank PHP
/*

// för varje aktie
//   för varje mäklare
//      för varje rek, starta en månad tillbaka
//        jämför rek med kurs när nästa rek inträffar (endast vid ändring av rek), eller nuvarande kurs om endast en rek

*/

require 'scraperwiki/simple_html_dom.php';  

$stocks = array("AAK - AarhusKarlshamn" => "SSE36273",
"ABB - ABB Ltd" => "SSE3966",
"ABB U - ABB Ltd U" => "SSE81849",
"ACAN B - Acando B" => "SSE981",
"ACAP A - ACAP Invest A" => "SSE20016",
"ACAP B - ACAP Invest B" => "SSE20017",
"ACOM - A-Com" => "SSE4287",
"ACTI - Active Biotech" => "SSE877",
"ANOD B - Addnode B" => "SSE3887",
"ADDT B - Addtech B" => "SSE14336",
"AERO B - Aerocrine B" => "SSE41047",
"ALFA - Alfa Laval" => "SSE18634",
"ALNX - Allenex" => "SSE37656",
"AOIL SDB - Alliance Oil Company SDB" => "SSE40583",
"ATEL - AllTele" => "SSE66668",
"ANOT - Anoto Group" => "SSE5110",
"AWP - Arise Windpower" => "SSE74570",
"ARTI B - Artimplant B" => "SSE953",
"ASP - Aspiro" => "SSE13291",
"ASSA B - ASSA ABLOY B" => "SSE402",
"AZN - AstraZeneca" => "SSE3524",
"ATCO A - Atlas Copco A" => "SSE45",
"ATCO B - Atlas Copco B" => "SSE46",
"LJGR B - Atrium Ljungberg B" => "SSE1011",
"ALIV SDB - Autoliv SDB" => "SSE47",
"AZA - Avanza Bank Holding" => "SSE988",
"AVEG B - Avega Group B" => "SSE43396",
"AXFO - Axfood" => "SSE4590",
"AXIS - Axis" => "SSE5150",
"BBTO B - B&B TOOLS B" => "SSE793",
"BEGR - BE Group" => "SSE37309",
"BEIA B - Beijer Alma B" => "SSE875",
"BEIJ B - Beijer B" => "SSE792",
"BELE - Beijer Electronics" => "SSE5081",
"BRG B - Bergs Timber B" => "SSE891",
"BETS B - Betsson B" => "SSE5121",
"BILI A - Bilia A" => "SSE794",
"BILL - Billerud" => "SSE14922",
"BIOG B - BioGaia B" => "SSE959",
"BINV - BioInvent International" => "SSE13348",
"BIOT - Biotage" => "SSE5209",
"BORG - Björn Borg" => "SSE40286",
"BEF SDB - Black Earth Farming SDB" => "SSE66922",
"BOL - Boliden" => "SSE15285",
"BONG - Bong" => "SSE892",
"BOUL - Boule Diagnostics" => "SSE82889",
"BRIN B - Brinova Fastigheter B" => "SSE22922",
"BTS B - BTS Group B" => "SSE13288",
"BURE - Bure Equity" => "SSE800",
"BMAX - Byggmax Group" => "SSE75712",
"CAST - Castellum" => "SSE966",
"CATE - Catena" => "SSE34362",
"CCC - Cavotec" => "SSE84962",
"CDON - CDON Group" => "SSE79303",
"CEVI - CellaVision" => "SSE40679",
"CSN - Cision" => "SSE1056",
"CLAS B - Clas Ohlson B" => "SSE4145",
"CLA B - Cloetta B" => "SSE63225",
"COA - Coastal Contacts" => "SSE70690",
"COIC - Concentric" => "SSE82656",
"CCOR B - Concordia Maritime B" => "SSE971",
"CNTA - Connecta" => "SSE29954",
"CONS B - Consilium B" => "SSE803",
"CORE - Corem Property Group" => "SSE66929",
"CORE PREF - Corem Property Group Pref" => "SSE74282",
"CTT - CTT Systems" => "SSE3081",
"CYBE - Cybercom Group" => "SSE4345",
"DAG - Dagon" => "SSE19210",
"DEDI - Dedicare B" => "SSE81878",
"DGC - DGC One" => "SSE56154",
"DIAM B - Diamyd Medical B" => "SSE18765",
"DIOS - Diös Fastigheter" => "SSE34271",
"DORO - DORO" => "SSE896",
"DUNI - Duni" => "SSE49775",
"DURC B - Duroc B" => "SSE4005",
"ECEX - East Capital Explorer" => "SSE49615",
"ELAN B - Elanders B" => "SSE897",
"ELEC - Electra Gruppen" => "SSE66436",
"ELUX A - Electrolux A" => "SSE80",
"ELUX B - Electrolux B" => "SSE81",
"EKTA B - Elekta B" => "SSE806",
"ELOS B - Elos B" => "SSE947",
"ENEA - Enea" => "SSE1149",
"ENRO - Eniro" => "SSE11046",
"ENQ - EnQuest PLC" => "SSE75073",
"EPCT - EpiCept" => "SSE32838",
"ERIC A - Ericsson A" => "SSE100",
"ERIC B - Ericsson B" => "SSE101",
"ETX - Etrion" => "SSE78547",
"EWRK - eWork Scandinavia" => "SSE72798",
"FABG - Fabege" => "SSE861",
"FAG - Fagerhult" => "SSE903",
"FPAR - Fast Partner" => "SSE980",
"BALD B - Fast. Balder B" => "SSE4212",
"BALD PREF - Fast. Balder pref" => "SSE82823",
"FEEL - Feelgood Svenska" => "SSE5053",
"FIX B - Fenix Outdoor B" => "SSE905",
"FING B - Fingerprint Cards B" => "SSE4870",
"FBAB - FinnvedenBulten" => "SSE82239",
"FPIP - FormPipe Software" => "SSE72565",
"GETI B - Getinge B" => "SSE812",
"GVKO B - Geveko B" => "SSE813",
"GHP - Global Health Partner" => "SSE59064",
"GUNN - Gunnebo" => "SSE816",
"HAKN - Hakon Invest" => "SSE32443",
"HLDX - Haldex" => "SSE817",
"HAV B - Havsfrun Investment B" => "SSE990",
"HEBA B - HEBA B" => "SSE991",
"HEMX - Hemtex" => "SSE31293",
"HM B - Hennes & Mauritz B" => "SSE992",
"HEXA B - Hexagon B" => "SSE819",
"HPOL B - HEXPOL B" => "SSE55907",
"HIQ - HiQ International" => "SSE3540",
"HMS - HMS Networks" => "SSE43302",
"HOLM A - Holmen A" => "SSE221",
"HOLM B - Holmen B" => "SSE222",
"HUFV A - Hufvudstaden A" => "SSE820",
"HUFV C - Hufvudstaden C" => "SSE821",
"HUSQ A - Husqvarna A" => "SSE34913",
"HUSQ B - Husqvarna B" => "SSE34915",
"HOGA B - Höganäs B" => "SSE824",
"IAR B - I.A.R Systems Group" => "SSE2346",
"IS - Image Systems" => "SSE3571",
"IFS A - Industrial & Financial Syst. A" => "SSE994",
"IFS B - Industrial & Financial Syst. B" => "SSE995",
"INDU A - Industrivärden A" => "SSE142",
"INDU C - Industrivärden C" => "SSE143",
"INDT - Indutrade" => "SSE31308",
"ICTA B - Intellecta B" => "SSE941",
"IJ - Intrum Justitia" => "SSE18962",
"INVE A - Investor A" => "SSE160",
"INVE B - Investor B" => "SSE161",
"ITAB B - ITAB Shop Concept B" => "SSE56940",
"JEEV - Jeeves Information Systems" => "SSE3555",
"JM - JM" => "SSE13217",
"KABE B - KABE B" => "SSE912",
"KAHL - KappAhl" => "SSE33359",
"KARO - Karo Bio" => "SSE3927",
"KDEV - Karolinska Development B" => "SSE81547",
"KINV A - Kinnevik A" => "SSE998",
"KINV B - Kinnevik B" => "SSE999",
"KLOV - Klövern" => "SSE19459",
"KLOV PREF - Klövern pref" => "SSE86345",
"KNOW - Know IT" => "SSE3219",
"KLED - Kungsleden" => "SSE3546",
"LAGR B - Lagercrantz Group B" => "SSE14335",
"LAMM B - Lammhults Design Group B" => "SSE1049",
"LATO B - Latour B" => "SSE914",
"LIAB - Lindab International" => "SSE37400",
"LOOM B - Loomis B" => "SSE61536",
"LUND B - Lundbergföretagen B" => "SSE1012",
"LUMI SDB - Lundin Mining Corporation SDB" => "SSE27709",
"LUPE - Lundin Petroleum" => "SSE22335",
"LUXO SDB - Luxonen SDB" => "SSE1014",
"MEAB B - Malmbergs Elektriska B" => "SSE3223",
"MEDA A - Meda  A" => "SSE917",
"MVIR B - Medivir B" => "SSE1020",
"MEKO - Mekonomen" => "SSE4986",
"MELK - Melker Schörling" => "SSE37472",
"MTRO SDB A - Metro International SDB A" => "SSE12429",
"MTRO SDB B - Metro International SDB B" => "SSE12430",
"MSAB B - Micro Systemation B" => "SSE85846",
"MICR - Micronic Mydata AB" => "SSE4714",
"MSON A - Midsona A" => "SSE3921",
"MSON B - Midsona B" => "SSE3922",
"MIDW A - Midway A" => "SSE834",
"MIDW B - Midway B" => "SSE835",
"MIC SDB - Millicom Int. Cellular SDB" => "SSE24507",
"MOB - Moberg Derma" => "SSE79252",
"MTG A - Modern Times Group A" => "SSE3598",
"MTG B - Modern Times Group B" => "SSE3599",
"MORP B - Morphic Technologies B" => "SSE53228",
"MQ - MQ Holding" => "SSE76085",
"MSC B - MSC Konsult B" => "SSE1023",
"MULQ - MultiQ International" => "SSE4359",
"NAXS - NAXS Nordic Access Buyout Fund" => "SSE40342",
"NCC A - NCC A" => "SSE837",
"NCC B - NCC B" => "SSE838",
"NMAN - Nederman Holding" => "SSE40347",
"NET B - Net Entertainment NE B" => "SSE62494",
"NETI B - Net Insight B" => "SSE3871",
"NEWA B - New Wave B" => "SSE920",
"NIBE B - NIBE Industrier B" => "SSE921",
"NOBI - Nobia" => "SSE19095",
"NOLA B - Nolato B" => "SSE923",
"NDA SEK - Nordea Bank" => "SSE220",
"NOMI - Nordic Mines" => "SSE57018",
"NSP B - Nordic Service Partn. Holdings" => "SSE51621",
"NN B - Nordnet B" => "SSE4872",
"NOTE - NOTE" => "SSE25319",
"NOVE - Novestra" => "SSE5116",
"NTEK B - NOVOTEK B" => "SSE4000",
"OASM - Oasmia Pharmaceutical" => "SSE76461",
"ODD - Odd Molly International" => "SSE40936",
"OEM B - OEM International B" => "SSE927",
"OPCO - Opcon" => "SSE2282",
"ORX - Orexo" => "SSE31885",
"ORI SDB - Oriflame, SDB" => "SSE24227",
"ORTI A - Ortivus A" => "SSE1031",
"ORTI B - Ortivus B" => "SSE1032",
"PAR - PA Resources" => "SSE34961",
"PART - PartnerTech" => "SSE1036",
"PEAB B - Peab B" => "SSE928",
"PHON - Phonera" => "SSE5000",
"POOL B - Poolia B" => "SSE3974",
"PREC - Precise Biometrics" => "SSE10751",
"PREV B - Prevas B" => "SSE1039",
"PRIC B - Pricer B" => "SSE1040",
"PACT - Proact IT Group" => "SSE4003",
"PROB - Probi" => "SSE27701",
"PROE B - Proffice B" => "SSE4208",
"PROF B - Profilgruppen B" => "SSE929",
"RATO A - Ratos A" => "SSE1044",
"RATO B - Ratos B" => "SSE1045",
"RAY B - RaySearch Laboratories B" => "SSE1063",
"RSOF B - ReadSoft B" => "SSE3967",
"RABT B - Rederi AB Transatlantic" => "SSE964",
"REJL B - Rejlerkoncernen" => "SSE37758",
"REZT - Rezidor Hotel Group" => "SSE37352",
"RNBS - RNB RETAIL AND BRANDS" => "SSE13467",
"RROS - Rottneros" => "SSE930",
"RTIM B - Rörvik Timber B" => "SSE1050",
"SAAB B - SAAB B" => "SSE1051",
"SAGA - Sagax" => "SSE43045",
"SAGA PREF - Sagax pref" => "SSE43046",
"SAND - Sandvik" => "SSE4928",
"SAS - SAS" => "SSE13557",
"SCA A - SCA A" => "SSE322",
"SCA B - SCA B" => "SSE323",
"SCV A - SCANIA A" => "SSE260",
"SCV B - SCANIA B" => "SSE261",
"SEB A - SEB A" => "SSE281",
"SEB C - SEB C" => "SSE282",
"SECT B - SECTRA B" => "SSE3083",
"SECU B - Securitas B" => "SSE401",
"SMF - Semafo" => "SSE84981",
"SEMC - Semcon" => "SSE1054",
"SENS - Sensys Traffic" => "SSE12241",
"SIGM B - Sigma B" => "SSE14531",
"SINT - SinterCast" => "SSE1058",
"SKA B - Skanska B" => "SSE283",
"SKF A - SKF A" => "SSE284",
"SKF B - SKF B" => "SSE285",
"SKIS B - SkiStar B" => "SSE939",
"SOF B - Softronic B" => "SSE1546",
"SSAB A - SSAB A" => "SSE300",
"SSAB B - SSAB B" => "SSE301",
"STFY - StjärnaFyrkant AB" => "SSE1007",
"STE A - Stora Enso A" => "SSE2169",
"STE R - Stora Enso R" => "SSE2170",
"SVIK - Studsvik" => "SSE13094",
"SHB A - Sv. Handelsbanken A" => "SSE340",
"SHB B - Sv. Handelsbanken B" => "SSE341",
"SWEC A - SWECO A" => "SSE1061",
"SWEC B - SWECO B" => "SSE1062",
"SWED A - Swedbank A" => "SSE120",
"SWED PREF - Swedbank pref" => "SSE61365",
"SVED B - Svedbergs B" => "SSE935",
"SWMA - Swedish Match" => "SSE361",
"SOBI - Swedish Orphan Biovitrum" => "SSE36316",
"SWOL B - Swedol B" => "SSE55913",
"SVOL A - Svolder A" => "SSE936",
"SVOL B - Svolder B" => "SSE937",
"SYSR - Systemair" => "SSE43007",
"TEL2 A - Tele2 A" => "SSE1026",
"TEL2 B - Tele2 B" => "SSE1027",
"TLSN - TeliaSonera" => "SSE5095",
"TIEN - Tieto Oyj" => "SSE4025",
"TRAC B - Traction  B" => "SSE4963",
"TRAD - TradeDoubler" => "SSE31884",
"TWW SDB A - Transcom WorldWide SDB A" => "SSE14353",
"TWW SDB B - Transcom WorldWide SDB B" => "SSE14354",
"TRMO - Transmode Holding" => "SSE82457",
"TREL B - Trelleborg B" => "SSE364",
"TAGR - Trigon Agri" => "SSE40543",
"UNIB SDB - Unibet Group" => "SSE36950",
"UFLX B - Uniflex B" => "SSE36986",
"WALL B - Wallenstam B" => "SSE945",
"VBG B - VBG GROUP B" => "SSE942",
"VRG B - Venue Retail Group B" => "SSE946",
"WIHL - Wihlborgs Fastigheter" => "SSE29759",
"VIT B - Vitec Software Group B" => "SSE5177",
"VITR - Vitrolife" => "SSE13469",
"VOLV A - Volvo A" => "SSE365",
"VOLV B - Volvo B" => "SSE366",
"VNIL SDB - Vostok Nafta Investment, SDB" => "SSE41044",
"XANO B - XANO Industri B" => "SSE1074",
"AF B - ÅF B" => "SSE862",
"ORES - Öresund" => "SSE863");

//exit(0);

$sourcescraper = 'aktietips';

scraperwiki::attach($sourcescraper);           

$data = scraperwiki::select(           
    "stock, by, `to`, date, rec
from `swdata` 
where date > '2011-01-01' and date < '2012-05-01' and stock = 'Volvo'
order by date asc"
);

$search_maklare = array();
for($i = 0; $i<count($data); $i++)
{
    $maklare = $data[$i]["by"];
    if (array_key_exists($maklare, $search_maklare) || $maklare == null || $maklare == "")
        continue;

    $stock = $data[$i]["stock"];
    $mrows = getReksFromMaklare($stock, $maklare, $data);
    print_r("<b>" . $stock . " av " . $maklare . "</b><br />");

    $search_maklare[$maklare] = true;
    $kurs1 = -1;
    $rek1 = null;
    $points = 0;
    
    foreach ($mrows as $row)
    {    
        print_r($row["by"] . " (" . $row["date"] . "), rek: " . $row["rec"] . ", riktkurs: " . $row["to"] . "<br />");
    }

    
    //exit(0);
    
    foreach ($mrows as $row)
    {
        if (!is_null($rek1))
        {
            $rek2 = array("stock" => $row["stock"], "date" => $row["date"], "rec" => $row["rec"]);
            $points += getPoints($rek1, $rek2);
        }
    
        $rek1 = array("stock" => $row["stock"], "date" => $row["date"], "rec" => $row["rec"]);
    }
    
    // nuvarande
    
    if ($rek1 == null)
    {
        print_r("avbryter, inga rekar<br />");
        continue;
    }
    $rek_now = array("stock" => $stock, "date" => "2012-04-27");
    
    $points += getPoints($rek1, $rek_now);
    
    print_r("poäng: " . $points . "<br /><hr />");

    if ($i == 4)
    {
    var_dump($search_maklare);
    exit(0);
    }
}

function getPoints($rek1, $rek2)
{
    // tips sparat från föregående loop
    $kurs1 = getKurs($rek1["stock"], $rek1["date"]);
    $kurs2 = getKurs($rek2["stock"], $rek2["date"]);

    $points = 0;
    $p = ($kurs2 - $kurs1) / $kurs1;
    if ($rek1["rec"] > 0 && $kurs2 > $kurs1*1.05) $points = $p;
    if ($rek1["rec"] > 0 && $kurs2*1.05 < $kurs1) $points = $p;
    
    if ($rek1["rec"] < 0 && $kurs2*1.05 < $kurs1) $points = $p;
    if ($rek1["rec"] < 0 && $kurs2 > $kurs1*1.05) $points = $p;

    print_r($rek1["date"] .  ", rek: " . $rek1["rec"] . ", kurs " . $kurs1 . ".<br />" . $rek2["date"] . ", kurs " .  $kurs2 . " => poäng: " . $points . "<br /><br />");

    return $points;
}

function getReksFromMaklare($stock, $maklare, $data)
{
    $arr = array();
    foreach($data as $row)
    {
        if ($row["by"] == $maklare)
            array_push($arr, $row);
    }

    return $arr;
}

function getKurs($stock, $date)
{
    global $stocks;

    $instrument = null;

    if (isset($stocks[$stock]))
        $instrument = $stocks[$stock];
    else
    {
        foreach($stocks as $key => $value)
        {
            if (stripos(strtolower_utf8($key), $stock) !== false) {
                $instrument = $value;
                $stocks[$stock] = $value;
                break;
            }
                //print_r($key . " => " . $value . "<br />");
        }
    }

    if ($instrument == null)
        throw new Exception("Hittade inte instrument");

    return getKursFromNASDAQ($instrument, $date);
}

$cached_instruments = array();
function getKursFromNASDAQ($instrument, $date)
{
    global $cached_instruments;
    $fromdate = "2011-09-01";
    $todate = "2012-04-27";
    $cache_key = $instrument;
    $html = "";

    if (is_null($instrument) || strlen($instrument) < 4)
        throw new Exception("Ogiltigt instrument: " . $instrument);

    if (isset($cached_instruments[$cache_key]))
        $html = $cached_instruments[$cache_key];
    else
    {

        $url = "http://pitea-tidningentest.teknomedia.se/inc/tinymce/utils/nomxs/default.aspx?instrument=" . $instrument . "&fromdate=" . $fromdate . "&todate=" . $todate;
    
        if (!preg_match("/[\d]{4}-\d{2}-\d{2}/", $date, $matches))
            throw new Exception("Date felaktigt format: " . $date);
    
        $html = file_get_contents($url);
        $cached_instruments[$cache_key] = $html;
        print_r($url . "<br />");
    }
//print_r($url . "<br />html from nasdaq: " . $html . "<br /><br />");
    $dom = new simple_html_dom();
    $dom->load($html);

    $kurs = -1;
    foreach($dom->find("tbody tr") as $tr)
    {
        $datetd = $tr->find("td", 0);
        if (!is_null($datetd) && $datetd->plaintext == $date)
        {
            $kurstd = $tr->find("td", 4);
            if (!is_null($kurstd))
            {
                $kurs = $kurstd->plaintext;
                break;
            }
        }
    }
    //print_r("<br />kurs: " . $kurs . "<br />");
    if ($kurs == -1)
        throw new Exception("Hittade inte kurs i resultatet");

    return $kurs;
}




function do_post_request($url, $data, $optional_headers = null)
{
  $params = array('http' => array(
              'method' => 'POST',
              'content' => $data
            ));
  if ($optional_headers !== null) {
    $params['http']['header'] = $optional_headers;
  }
  $ctx = stream_context_create($params);
  $fp = @fopen($url, 'rb', false, $ctx);
  if (!$fp) {
    throw new Exception("Problem with $url, $php_errormsg");
  }
  $response = @stream_get_contents($fp);
  if ($response === false) {
    throw new Exception("Problem reading data from $url, $php_errormsg");
  }
  return $response;
}

function rest_helper($url, $params = null, $verb = 'GET', $format = 'json')
{
  $cparams = array(
    'http' => array(
      'method' => $verb,
      'ignore_errors' => true
    )
  );
  if ($params !== null) {
    $params = http_build_query($params);
    if ($verb == 'POST') {
      $cparams['http']['content'] = $params;
    } else {
      $url .= '?' . $params;
    }
  }

  $context = stream_context_create($cparams);
  $fp = fopen($url, 'rb', false, $context);
  if (!$fp) {
    $res = false;
  } else {
    // If you're trying to troubleshoot problems, try uncommenting the
    // next two lines; it will show you the HTTP response headers across
    // all the redirects:
    // $meta = stream_get_meta_data($fp);
    // var_dump($meta['wrapper_data']);
    $res = stream_get_contents($fp);
  }

  if ($res === false) {
    throw new Exception("$verb $url failed: $php_errormsg");
  }

  switch ($format) {
    case 'json':
      $r = json_decode($res);
      if ($r === null) {
        throw new Exception("failed to decode $res as json");
      }
      return $r;

    case 'xml':
      $r = simplexml_load_string($res);
      if ($r === null) {
        throw new Exception("failed to decode $res as xml");
      }
      return $r;
  }
  return $res;
}

function strtolower_utf8($string){ 
  $convert_to = array( 
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", 
    "v", "w", "x", "y", "z", "à", "á", "â", "ã", "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï", 
    "ð", "ñ", "ò", "ó", "ô", "õ", "ö", "ø", "ù", "ú", "û", "ü", "ý", "а", "б", "в", "г", "д", "е", "ё", "ж", 
    "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", 
    "ь", "э", "ю", "я" 
  ); 
  $convert_from = array( 
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", 
    "V", "W", "X", "Y", "Z", "À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï", 
    "Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "Ø", "Ù", "Ú", "Û", "Ü", "Ý", "А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", 
    "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ъ", 
    "Ь", "Э", "Ю", "Я" 
  ); 

  return str_replace($convert_from, $convert_to, $string); 
}

?>

</div>
  <footer>

  </footer>


</body>
</html><!doctype html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!-- Consider adding a manifest.appcache: h5bp.com/d/Offline -->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title></title>
  <meta name="description" content="">

  <!-- Mobile viewport optimized: h5bp.com/viewport -->
  <meta name="viewport" content="width=device-width">

    <link rel="stylesheet" href="http://tablesorter.com/themes/blue/style.css" />

    <style type="text/css">

        table.tablesorter { width: auto; }
        table.tablesorter tbody td { min-width:150px; }

    </style>

  <link rel="stylesheet" href="css/style.css" />
    <script src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
    <script src="http://tablesorter.com/__jquery.tablesorter.min.js"></script>


<script>

    $(document).ready(function() {
        $("table.tablesorter").tablesorter();
    });

</script>

</head>
<body>
  <header>

  </header>
  <div role="main">



<?php
# Blank PHP
/*

// för varje aktie
//   för varje mäklare
//      för varje rek, starta en månad tillbaka
//        jämför rek med kurs när nästa rek inträffar (endast vid ändring av rek), eller nuvarande kurs om endast en rek

*/

require 'scraperwiki/simple_html_dom.php';  

$stocks = array("AAK - AarhusKarlshamn" => "SSE36273",
"ABB - ABB Ltd" => "SSE3966",
"ABB U - ABB Ltd U" => "SSE81849",
"ACAN B - Acando B" => "SSE981",
"ACAP A - ACAP Invest A" => "SSE20016",
"ACAP B - ACAP Invest B" => "SSE20017",
"ACOM - A-Com" => "SSE4287",
"ACTI - Active Biotech" => "SSE877",
"ANOD B - Addnode B" => "SSE3887",
"ADDT B - Addtech B" => "SSE14336",
"AERO B - Aerocrine B" => "SSE41047",
"ALFA - Alfa Laval" => "SSE18634",
"ALNX - Allenex" => "SSE37656",
"AOIL SDB - Alliance Oil Company SDB" => "SSE40583",
"ATEL - AllTele" => "SSE66668",
"ANOT - Anoto Group" => "SSE5110",
"AWP - Arise Windpower" => "SSE74570",
"ARTI B - Artimplant B" => "SSE953",
"ASP - Aspiro" => "SSE13291",
"ASSA B - ASSA ABLOY B" => "SSE402",
"AZN - AstraZeneca" => "SSE3524",
"ATCO A - Atlas Copco A" => "SSE45",
"ATCO B - Atlas Copco B" => "SSE46",
"LJGR B - Atrium Ljungberg B" => "SSE1011",
"ALIV SDB - Autoliv SDB" => "SSE47",
"AZA - Avanza Bank Holding" => "SSE988",
"AVEG B - Avega Group B" => "SSE43396",
"AXFO - Axfood" => "SSE4590",
"AXIS - Axis" => "SSE5150",
"BBTO B - B&B TOOLS B" => "SSE793",
"BEGR - BE Group" => "SSE37309",
"BEIA B - Beijer Alma B" => "SSE875",
"BEIJ B - Beijer B" => "SSE792",
"BELE - Beijer Electronics" => "SSE5081",
"BRG B - Bergs Timber B" => "SSE891",
"BETS B - Betsson B" => "SSE5121",
"BILI A - Bilia A" => "SSE794",
"BILL - Billerud" => "SSE14922",
"BIOG B - BioGaia B" => "SSE959",
"BINV - BioInvent International" => "SSE13348",
"BIOT - Biotage" => "SSE5209",
"BORG - Björn Borg" => "SSE40286",
"BEF SDB - Black Earth Farming SDB" => "SSE66922",
"BOL - Boliden" => "SSE15285",
"BONG - Bong" => "SSE892",
"BOUL - Boule Diagnostics" => "SSE82889",
"BRIN B - Brinova Fastigheter B" => "SSE22922",
"BTS B - BTS Group B" => "SSE13288",
"BURE - Bure Equity" => "SSE800",
"BMAX - Byggmax Group" => "SSE75712",
"CAST - Castellum" => "SSE966",
"CATE - Catena" => "SSE34362",
"CCC - Cavotec" => "SSE84962",
"CDON - CDON Group" => "SSE79303",
"CEVI - CellaVision" => "SSE40679",
"CSN - Cision" => "SSE1056",
"CLAS B - Clas Ohlson B" => "SSE4145",
"CLA B - Cloetta B" => "SSE63225",
"COA - Coastal Contacts" => "SSE70690",
"COIC - Concentric" => "SSE82656",
"CCOR B - Concordia Maritime B" => "SSE971",
"CNTA - Connecta" => "SSE29954",
"CONS B - Consilium B" => "SSE803",
"CORE - Corem Property Group" => "SSE66929",
"CORE PREF - Corem Property Group Pref" => "SSE74282",
"CTT - CTT Systems" => "SSE3081",
"CYBE - Cybercom Group" => "SSE4345",
"DAG - Dagon" => "SSE19210",
"DEDI - Dedicare B" => "SSE81878",
"DGC - DGC One" => "SSE56154",
"DIAM B - Diamyd Medical B" => "SSE18765",
"DIOS - Diös Fastigheter" => "SSE34271",
"DORO - DORO" => "SSE896",
"DUNI - Duni" => "SSE49775",
"DURC B - Duroc B" => "SSE4005",
"ECEX - East Capital Explorer" => "SSE49615",
"ELAN B - Elanders B" => "SSE897",
"ELEC - Electra Gruppen" => "SSE66436",
"ELUX A - Electrolux A" => "SSE80",
"ELUX B - Electrolux B" => "SSE81",
"EKTA B - Elekta B" => "SSE806",
"ELOS B - Elos B" => "SSE947",
"ENEA - Enea" => "SSE1149",
"ENRO - Eniro" => "SSE11046",
"ENQ - EnQuest PLC" => "SSE75073",
"EPCT - EpiCept" => "SSE32838",
"ERIC A - Ericsson A" => "SSE100",
"ERIC B - Ericsson B" => "SSE101",
"ETX - Etrion" => "SSE78547",
"EWRK - eWork Scandinavia" => "SSE72798",
"FABG - Fabege" => "SSE861",
"FAG - Fagerhult" => "SSE903",
"FPAR - Fast Partner" => "SSE980",
"BALD B - Fast. Balder B" => "SSE4212",
"BALD PREF - Fast. Balder pref" => "SSE82823",
"FEEL - Feelgood Svenska" => "SSE5053",
"FIX B - Fenix Outdoor B" => "SSE905",
"FING B - Fingerprint Cards B" => "SSE4870",
"FBAB - FinnvedenBulten" => "SSE82239",
"FPIP - FormPipe Software" => "SSE72565",
"GETI B - Getinge B" => "SSE812",
"GVKO B - Geveko B" => "SSE813",
"GHP - Global Health Partner" => "SSE59064",
"GUNN - Gunnebo" => "SSE816",
"HAKN - Hakon Invest" => "SSE32443",
"HLDX - Haldex" => "SSE817",
"HAV B - Havsfrun Investment B" => "SSE990",
"HEBA B - HEBA B" => "SSE991",
"HEMX - Hemtex" => "SSE31293",
"HM B - Hennes & Mauritz B" => "SSE992",
"HEXA B - Hexagon B" => "SSE819",
"HPOL B - HEXPOL B" => "SSE55907",
"HIQ - HiQ International" => "SSE3540",
"HMS - HMS Networks" => "SSE43302",
"HOLM A - Holmen A" => "SSE221",
"HOLM B - Holmen B" => "SSE222",
"HUFV A - Hufvudstaden A" => "SSE820",
"HUFV C - Hufvudstaden C" => "SSE821",
"HUSQ A - Husqvarna A" => "SSE34913",
"HUSQ B - Husqvarna B" => "SSE34915",
"HOGA B - Höganäs B" => "SSE824",
"IAR B - I.A.R Systems Group" => "SSE2346",
"IS - Image Systems" => "SSE3571",
"IFS A - Industrial & Financial Syst. A" => "SSE994",
"IFS B - Industrial & Financial Syst. B" => "SSE995",
"INDU A - Industrivärden A" => "SSE142",
"INDU C - Industrivärden C" => "SSE143",
"INDT - Indutrade" => "SSE31308",
"ICTA B - Intellecta B" => "SSE941",
"IJ - Intrum Justitia" => "SSE18962",
"INVE A - Investor A" => "SSE160",
"INVE B - Investor B" => "SSE161",
"ITAB B - ITAB Shop Concept B" => "SSE56940",
"JEEV - Jeeves Information Systems" => "SSE3555",
"JM - JM" => "SSE13217",
"KABE B - KABE B" => "SSE912",
"KAHL - KappAhl" => "SSE33359",
"KARO - Karo Bio" => "SSE3927",
"KDEV - Karolinska Development B" => "SSE81547",
"KINV A - Kinnevik A" => "SSE998",
"KINV B - Kinnevik B" => "SSE999",
"KLOV - Klövern" => "SSE19459",
"KLOV PREF - Klövern pref" => "SSE86345",
"KNOW - Know IT" => "SSE3219",
"KLED - Kungsleden" => "SSE3546",
"LAGR B - Lagercrantz Group B" => "SSE14335",
"LAMM B - Lammhults Design Group B" => "SSE1049",
"LATO B - Latour B" => "SSE914",
"LIAB - Lindab International" => "SSE37400",
"LOOM B - Loomis B" => "SSE61536",
"LUND B - Lundbergföretagen B" => "SSE1012",
"LUMI SDB - Lundin Mining Corporation SDB" => "SSE27709",
"LUPE - Lundin Petroleum" => "SSE22335",
"LUXO SDB - Luxonen SDB" => "SSE1014",
"MEAB B - Malmbergs Elektriska B" => "SSE3223",
"MEDA A - Meda  A" => "SSE917",
"MVIR B - Medivir B" => "SSE1020",
"MEKO - Mekonomen" => "SSE4986",
"MELK - Melker Schörling" => "SSE37472",
"MTRO SDB A - Metro International SDB A" => "SSE12429",
"MTRO SDB B - Metro International SDB B" => "SSE12430",
"MSAB B - Micro Systemation B" => "SSE85846",
"MICR - Micronic Mydata AB" => "SSE4714",
"MSON A - Midsona A" => "SSE3921",
"MSON B - Midsona B" => "SSE3922",
"MIDW A - Midway A" => "SSE834",
"MIDW B - Midway B" => "SSE835",
"MIC SDB - Millicom Int. Cellular SDB" => "SSE24507",
"MOB - Moberg Derma" => "SSE79252",
"MTG A - Modern Times Group A" => "SSE3598",
"MTG B - Modern Times Group B" => "SSE3599",
"MORP B - Morphic Technologies B" => "SSE53228",
"MQ - MQ Holding" => "SSE76085",
"MSC B - MSC Konsult B" => "SSE1023",
"MULQ - MultiQ International" => "SSE4359",
"NAXS - NAXS Nordic Access Buyout Fund" => "SSE40342",
"NCC A - NCC A" => "SSE837",
"NCC B - NCC B" => "SSE838",
"NMAN - Nederman Holding" => "SSE40347",
"NET B - Net Entertainment NE B" => "SSE62494",
"NETI B - Net Insight B" => "SSE3871",
"NEWA B - New Wave B" => "SSE920",
"NIBE B - NIBE Industrier B" => "SSE921",
"NOBI - Nobia" => "SSE19095",
"NOLA B - Nolato B" => "SSE923",
"NDA SEK - Nordea Bank" => "SSE220",
"NOMI - Nordic Mines" => "SSE57018",
"NSP B - Nordic Service Partn. Holdings" => "SSE51621",
"NN B - Nordnet B" => "SSE4872",
"NOTE - NOTE" => "SSE25319",
"NOVE - Novestra" => "SSE5116",
"NTEK B - NOVOTEK B" => "SSE4000",
"OASM - Oasmia Pharmaceutical" => "SSE76461",
"ODD - Odd Molly International" => "SSE40936",
"OEM B - OEM International B" => "SSE927",
"OPCO - Opcon" => "SSE2282",
"ORX - Orexo" => "SSE31885",
"ORI SDB - Oriflame, SDB" => "SSE24227",
"ORTI A - Ortivus A" => "SSE1031",
"ORTI B - Ortivus B" => "SSE1032",
"PAR - PA Resources" => "SSE34961",
"PART - PartnerTech" => "SSE1036",
"PEAB B - Peab B" => "SSE928",
"PHON - Phonera" => "SSE5000",
"POOL B - Poolia B" => "SSE3974",
"PREC - Precise Biometrics" => "SSE10751",
"PREV B - Prevas B" => "SSE1039",
"PRIC B - Pricer B" => "SSE1040",
"PACT - Proact IT Group" => "SSE4003",
"PROB - Probi" => "SSE27701",
"PROE B - Proffice B" => "SSE4208",
"PROF B - Profilgruppen B" => "SSE929",
"RATO A - Ratos A" => "SSE1044",
"RATO B - Ratos B" => "SSE1045",
"RAY B - RaySearch Laboratories B" => "SSE1063",
"RSOF B - ReadSoft B" => "SSE3967",
"RABT B - Rederi AB Transatlantic" => "SSE964",
"REJL B - Rejlerkoncernen" => "SSE37758",
"REZT - Rezidor Hotel Group" => "SSE37352",
"RNBS - RNB RETAIL AND BRANDS" => "SSE13467",
"RROS - Rottneros" => "SSE930",
"RTIM B - Rörvik Timber B" => "SSE1050",
"SAAB B - SAAB B" => "SSE1051",
"SAGA - Sagax" => "SSE43045",
"SAGA PREF - Sagax pref" => "SSE43046",
"SAND - Sandvik" => "SSE4928",
"SAS - SAS" => "SSE13557",
"SCA A - SCA A" => "SSE322",
"SCA B - SCA B" => "SSE323",
"SCV A - SCANIA A" => "SSE260",
"SCV B - SCANIA B" => "SSE261",
"SEB A - SEB A" => "SSE281",
"SEB C - SEB C" => "SSE282",
"SECT B - SECTRA B" => "SSE3083",
"SECU B - Securitas B" => "SSE401",
"SMF - Semafo" => "SSE84981",
"SEMC - Semcon" => "SSE1054",
"SENS - Sensys Traffic" => "SSE12241",
"SIGM B - Sigma B" => "SSE14531",
"SINT - SinterCast" => "SSE1058",
"SKA B - Skanska B" => "SSE283",
"SKF A - SKF A" => "SSE284",
"SKF B - SKF B" => "SSE285",
"SKIS B - SkiStar B" => "SSE939",
"SOF B - Softronic B" => "SSE1546",
"SSAB A - SSAB A" => "SSE300",
"SSAB B - SSAB B" => "SSE301",
"STFY - StjärnaFyrkant AB" => "SSE1007",
"STE A - Stora Enso A" => "SSE2169",
"STE R - Stora Enso R" => "SSE2170",
"SVIK - Studsvik" => "SSE13094",
"SHB A - Sv. Handelsbanken A" => "SSE340",
"SHB B - Sv. Handelsbanken B" => "SSE341",
"SWEC A - SWECO A" => "SSE1061",
"SWEC B - SWECO B" => "SSE1062",
"SWED A - Swedbank A" => "SSE120",
"SWED PREF - Swedbank pref" => "SSE61365",
"SVED B - Svedbergs B" => "SSE935",
"SWMA - Swedish Match" => "SSE361",
"SOBI - Swedish Orphan Biovitrum" => "SSE36316",
"SWOL B - Swedol B" => "SSE55913",
"SVOL A - Svolder A" => "SSE936",
"SVOL B - Svolder B" => "SSE937",
"SYSR - Systemair" => "SSE43007",
"TEL2 A - Tele2 A" => "SSE1026",
"TEL2 B - Tele2 B" => "SSE1027",
"TLSN - TeliaSonera" => "SSE5095",
"TIEN - Tieto Oyj" => "SSE4025",
"TRAC B - Traction  B" => "SSE4963",
"TRAD - TradeDoubler" => "SSE31884",
"TWW SDB A - Transcom WorldWide SDB A" => "SSE14353",
"TWW SDB B - Transcom WorldWide SDB B" => "SSE14354",
"TRMO - Transmode Holding" => "SSE82457",
"TREL B - Trelleborg B" => "SSE364",
"TAGR - Trigon Agri" => "SSE40543",
"UNIB SDB - Unibet Group" => "SSE36950",
"UFLX B - Uniflex B" => "SSE36986",
"WALL B - Wallenstam B" => "SSE945",
"VBG B - VBG GROUP B" => "SSE942",
"VRG B - Venue Retail Group B" => "SSE946",
"WIHL - Wihlborgs Fastigheter" => "SSE29759",
"VIT B - Vitec Software Group B" => "SSE5177",
"VITR - Vitrolife" => "SSE13469",
"VOLV A - Volvo A" => "SSE365",
"VOLV B - Volvo B" => "SSE366",
"VNIL SDB - Vostok Nafta Investment, SDB" => "SSE41044",
"XANO B - XANO Industri B" => "SSE1074",
"AF B - ÅF B" => "SSE862",
"ORES - Öresund" => "SSE863");

//exit(0);

$sourcescraper = 'aktietips';

scraperwiki::attach($sourcescraper);           

$data = scraperwiki::select(           
    "stock, by, `to`, date, rec
from `swdata` 
where date > '2011-01-01' and date < '2012-05-01' and stock = 'Volvo'
order by date asc"
);

$search_maklare = array();
for($i = 0; $i<count($data); $i++)
{
    $maklare = $data[$i]["by"];
    if (array_key_exists($maklare, $search_maklare) || $maklare == null || $maklare == "")
        continue;

    $stock = $data[$i]["stock"];
    $mrows = getReksFromMaklare($stock, $maklare, $data);
    print_r("<b>" . $stock . " av " . $maklare . "</b><br />");

    $search_maklare[$maklare] = true;
    $kurs1 = -1;
    $rek1 = null;
    $points = 0;
    
    foreach ($mrows as $row)
    {    
        print_r($row["by"] . " (" . $row["date"] . "), rek: " . $row["rec"] . ", riktkurs: " . $row["to"] . "<br />");
    }

    
    //exit(0);
    
    foreach ($mrows as $row)
    {
        if (!is_null($rek1))
        {
            $rek2 = array("stock" => $row["stock"], "date" => $row["date"], "rec" => $row["rec"]);
            $points += getPoints($rek1, $rek2);
        }
    
        $rek1 = array("stock" => $row["stock"], "date" => $row["date"], "rec" => $row["rec"]);
    }
    
    // nuvarande
    
    if ($rek1 == null)
    {
        print_r("avbryter, inga rekar<br />");
        continue;
    }
    $rek_now = array("stock" => $stock, "date" => "2012-04-27");
    
    $points += getPoints($rek1, $rek_now);
    
    print_r("poäng: " . $points . "<br /><hr />");

    if ($i == 4)
    {
    var_dump($search_maklare);
    exit(0);
    }
}

function getPoints($rek1, $rek2)
{
    // tips sparat från föregående loop
    $kurs1 = getKurs($rek1["stock"], $rek1["date"]);
    $kurs2 = getKurs($rek2["stock"], $rek2["date"]);

    $points = 0;
    $p = ($kurs2 - $kurs1) / $kurs1;
    if ($rek1["rec"] > 0 && $kurs2 > $kurs1*1.05) $points = $p;
    if ($rek1["rec"] > 0 && $kurs2*1.05 < $kurs1) $points = $p;
    
    if ($rek1["rec"] < 0 && $kurs2*1.05 < $kurs1) $points = $p;
    if ($rek1["rec"] < 0 && $kurs2 > $kurs1*1.05) $points = $p;

    print_r($rek1["date"] .  ", rek: " . $rek1["rec"] . ", kurs " . $kurs1 . ".<br />" . $rek2["date"] . ", kurs " .  $kurs2 . " => poäng: " . $points . "<br /><br />");

    return $points;
}

function getReksFromMaklare($stock, $maklare, $data)
{
    $arr = array();
    foreach($data as $row)
    {
        if ($row["by"] == $maklare)
            array_push($arr, $row);
    }

    return $arr;
}

function getKurs($stock, $date)
{
    global $stocks;

    $instrument = null;

    if (isset($stocks[$stock]))
        $instrument = $stocks[$stock];
    else
    {
        foreach($stocks as $key => $value)
        {
            if (stripos(strtolower_utf8($key), $stock) !== false) {
                $instrument = $value;
                $stocks[$stock] = $value;
                break;
            }
                //print_r($key . " => " . $value . "<br />");
        }
    }

    if ($instrument == null)
        throw new Exception("Hittade inte instrument");

    return getKursFromNASDAQ($instrument, $date);
}

$cached_instruments = array();
function getKursFromNASDAQ($instrument, $date)
{
    global $cached_instruments;
    $fromdate = "2011-09-01";
    $todate = "2012-04-27";
    $cache_key = $instrument;
    $html = "";

    if (is_null($instrument) || strlen($instrument) < 4)
        throw new Exception("Ogiltigt instrument: " . $instrument);

    if (isset($cached_instruments[$cache_key]))
        $html = $cached_instruments[$cache_key];
    else
    {

        $url = "http://pitea-tidningentest.teknomedia.se/inc/tinymce/utils/nomxs/default.aspx?instrument=" . $instrument . "&fromdate=" . $fromdate . "&todate=" . $todate;
    
        if (!preg_match("/[\d]{4}-\d{2}-\d{2}/", $date, $matches))
            throw new Exception("Date felaktigt format: " . $date);
    
        $html = file_get_contents($url);
        $cached_instruments[$cache_key] = $html;
        print_r($url . "<br />");
    }
//print_r($url . "<br />html from nasdaq: " . $html . "<br /><br />");
    $dom = new simple_html_dom();
    $dom->load($html);

    $kurs = -1;
    foreach($dom->find("tbody tr") as $tr)
    {
        $datetd = $tr->find("td", 0);
        if (!is_null($datetd) && $datetd->plaintext == $date)
        {
            $kurstd = $tr->find("td", 4);
            if (!is_null($kurstd))
            {
                $kurs = $kurstd->plaintext;
                break;
            }
        }
    }
    //print_r("<br />kurs: " . $kurs . "<br />");
    if ($kurs == -1)
        throw new Exception("Hittade inte kurs i resultatet");

    return $kurs;
}




function do_post_request($url, $data, $optional_headers = null)
{
  $params = array('http' => array(
              'method' => 'POST',
              'content' => $data
            ));
  if ($optional_headers !== null) {
    $params['http']['header'] = $optional_headers;
  }
  $ctx = stream_context_create($params);
  $fp = @fopen($url, 'rb', false, $ctx);
  if (!$fp) {
    throw new Exception("Problem with $url, $php_errormsg");
  }
  $response = @stream_get_contents($fp);
  if ($response === false) {
    throw new Exception("Problem reading data from $url, $php_errormsg");
  }
  return $response;
}

function rest_helper($url, $params = null, $verb = 'GET', $format = 'json')
{
  $cparams = array(
    'http' => array(
      'method' => $verb,
      'ignore_errors' => true
    )
  );
  if ($params !== null) {
    $params = http_build_query($params);
    if ($verb == 'POST') {
      $cparams['http']['content'] = $params;
    } else {
      $url .= '?' . $params;
    }
  }

  $context = stream_context_create($cparams);
  $fp = fopen($url, 'rb', false, $context);
  if (!$fp) {
    $res = false;
  } else {
    // If you're trying to troubleshoot problems, try uncommenting the
    // next two lines; it will show you the HTTP response headers across
    // all the redirects:
    // $meta = stream_get_meta_data($fp);
    // var_dump($meta['wrapper_data']);
    $res = stream_get_contents($fp);
  }

  if ($res === false) {
    throw new Exception("$verb $url failed: $php_errormsg");
  }

  switch ($format) {
    case 'json':
      $r = json_decode($res);
      if ($r === null) {
        throw new Exception("failed to decode $res as json");
      }
      return $r;

    case 'xml':
      $r = simplexml_load_string($res);
      if ($r === null) {
        throw new Exception("failed to decode $res as xml");
      }
      return $r;
  }
  return $res;
}

function strtolower_utf8($string){ 
  $convert_to = array( 
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", 
    "v", "w", "x", "y", "z", "à", "á", "â", "ã", "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï", 
    "ð", "ñ", "ò", "ó", "ô", "õ", "ö", "ø", "ù", "ú", "û", "ü", "ý", "а", "б", "в", "г", "д", "е", "ё", "ж", 
    "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", 
    "ь", "э", "ю", "я" 
  ); 
  $convert_from = array( 
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", 
    "V", "W", "X", "Y", "Z", "À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï", 
    "Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "Ø", "Ù", "Ú", "Û", "Ü", "Ý", "А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", 
    "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ъ", 
    "Ь", "Э", "Ю", "Я" 
  ); 

  return str_replace($convert_from, $convert_to, $string); 
}

?>

</div>
  <footer>

  </footer>


</body>
</html>