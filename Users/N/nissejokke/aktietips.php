<?php

require 'scraperwiki/simple_html_dom.php';  
setlocale(LC_ALL, 'sv_SE.utf8');

parseAktietips();


function parseAktietips()
{
    
    for($i = 1; $i<30; $i++){
        
        parseAktietipsOnPage($i);

    }
}

function parseAktietipsOnPage($page)
{
    $html = scraperWiki::scrape("http://www.di.se/borssidor/alla-aktietips/?page=" . $page);           
    $dom = new simple_html_dom();
    $dom->load($html);

    print_r("parsar sida "  . $page . "\n");

    $foundlinks = array();
    $i = 0;
    $stock;
    foreach($dom->find("#analysis-list-wrap table tr") as $tr){
        //if ($i++>10)
        //    continue;
        try {

            $links = $tr->find("a");
            
            $href = $links[1]->href;
            $stock = getPlaintext($links[0]);
            $class = $links[0]->class;
            $rub = getPlaintext($links[1]);

            if (stripos($class, "diff-positive") > 0)
                $rek = 1;
            else if (stripos($class, "diff-negative") > 0)
                $rek = -1;
            else if (stripos($class, "diff-null") > 0)
                continue;
            else
                $rek = 0;

            $tds = $tr->find("td");
            $hus = getPlaintext($tds[1]);
            $date = getPlaintext($tds[2]);
            $text = "";
            $args = explode("&#39;", $href);

            $obj = array("stock" => $stock, "by" => $hus, "rec" => $rek, "headline" => $rub, "text" => $text, "date" => $date);
            
            
            //print_r($obj);
            //break;
  
           scraperwiki::save(array('stock', 'by', 'date'), $obj);
        }
        catch(Exception $e)
        {
            print("Error: " . $e->getMessage() . "\n");
        }
        
    }
}

function getAktietip($stock, $rub, $url)
{
    global $analyshus;
    global $companys;

    print_r($stock . " => " . $rub . " => " . $url);

    if (substr($url, 0, 5) != "http:")
        $url= "http://di.se" . $url;

    $html = scraperWiki::scrape($url);           
    $dom = new simple_html_dom();
    $dom->load($html);

    $arr = array();
    $hus = null;
    $rek = -100;

    // bolag
    foreach($dom->find("dl") as $dl)
    {
        $dt = getPlaintext($dl->find("dt", 0));
        $dd_el = $dl->find("dd", 0);
        $dd = getPlaintext($dd_el);

        switch($dt)
        {
            case "Analys av:": $hus = $dd; break;
            case "Rek:": 

                    if (stripos($dd_el->innertext, "sell") > 0)
                        $rek = -1;
                    else if (stripos($dd_el->innertext, "buy") > 0)
                        $rek = 1;
                    else if (stripos($dd_el->innertext, "keep") > 0)
                        $rek = 0;

                break;
        }

        
    }

    $rub = getPlaintext($dom->find("p strong", 0));
    $text = getPlaintext($dom->find("p", 1));
    $date = getPlaintext($dom->find("span.data", 0));

    if (stripos($rub, "starkt") > -1)
        $rek = $rek * 2;

    $rc = getRiktkursAndCurrency($text, $rub);

    $obj = array("stock" => $stock, "by" => $hus, "rec" => $rek, "headline" => $rub, "text" => $text, "date" => $date);
    $obj = array_merge($obj, $rc);

    return $obj;
}

// gamla

function getNews()
{
    $html = scraperWiki::scrape("http://di.se/Bors--Marknad/Borstips/");           
    $dom = new simple_html_dom();
    $dom->load($html);

    $foundlinks = array();$i = 0;
    foreach($dom->find(".table-article-list a") as $link){
        //if ($i++<60)
        //    continue;
        try {

            
            $url = $link->href;

            //print_r(getPlaintext($link) . " " . $url . "\n");

            $objs = getRec($url);

            foreach($objs as $obj)
            {
                //print_r($obj);
                if (is_null($obj["stock"]))
                    throw new Exception("Stock saknas " . $url);
                if (is_null($obj["by"]))
                    throw new Exception("By saknas " . $url);
                if (is_null($obj["date"]))
                    throw new Exception("Date saknas " . $url);
//print_r (json_encode($obj) . "\n");
                scraperwiki::save(array('stock', 'by', 'date'), $obj);
            }
        }
        catch(Exception $e)
        {
            print("Error: " . $e->getMessage() . "\n");
        }
        
    }
}


function getRec($newsurl, $debug=false)
{
    global $analyshus;
    global $companys;

    if (substr($newsurl, 0, 5) != "http:")
        $newsurl = "http://di.se" . $newsurl;

    $html = scraperWiki::scrape($newsurl);           
    $dom = new simple_html_dom();
    $dom->load($html);

    $arr = array();

    // bolag
    $rub_el = $dom->find("h1", 0);
    if (is_null($rub_el))
        throw new Exception("Hittade inte rubrikelementet " . $newsurl);
    $rub = preg_replace("/[\n\r]/", "", getPlaintext($rub_el));
    $i = 0;
    if (preg_match("/([\wåäöÅÄÖ& ]+)\s*:\s*(.+)/i", $rub, $matches)) {
        $stock = strtolower_utf8(trim($matches[1]));
        $hus = trim($matches[2]);
        array_push($arr, 
            array("stock" => $stock, 
                    "rek" => "", 
                    "to" => -1, 
                    "by" => "",
                    "rub" => $rub, 
                    "url" => $newsurl,
                    "text" => "",
                    "date" => "",
                    "currency" => ""));


        foreach($analyshus as $key => $value)
        {
            if (stripos($hus, $key) > -1)
            {
                $arr[0]["by"] = $value;
                break;
            }

        }

        //print_r($arr[0]["by"] . ", l:" . count(trim($arr[0]["by"])));
        if (strlen($arr[0]["by"]) == 0)
            throw new Exception("'$hus' är inte en mäklare, rub: " . $rub . " " . $newsurl);

    }
    else
        throw new Exception("Ingen matchande rubrik hittades: " . $newsurl . " " . getPlaintext($dom->find("#articleBody", 0)));

    if ($arr[0]["by"] == "")
        throw new Exception("Hittade inte mäklare: " . $rub);

    // kolla om bolaget finns
    // först kollas om nyckeln finns i arrayen, sen om ej fanns så söks arrayen igenom och om strängen finns i början av nyckel
    $stockname = null;

    if (array_key_exists(strtolower($stock), $companys))
        $stockname = $companys[strtolower($stock)];

    if (is_null($stockname))    
        $stockname = getitem_array_in_string($companys, strtolower($stock));

    if (is_null($stockname))
        $stockname = getitem_array_in_string($companys, str_replace(" ", "", strtolower($stock)));

    if (is_null($stockname))
        throw new Exception("$stock är inte en aktie " . $newsurl);

    $arr[0]["stock"] = $stockname;

    // datum
    $datebox = $dom->find("#phArticle .date", 0);
    if (!is_null($datebox))
    {
        $arr[0]["date"] = trim(str_replace("Uppdaterad ", "", getPlaintext($datebox)));
    }

    if ($arr[0]["date"] == "")
        throw new Exception("Inget datum " . $newsurl);

    // riktkurs
    $to = -1;
    $intro = $dom->find("#articleIntro", 0);
    $arttext = $dom->find("#articleBody", 0);
    $text = "";
    if (!is_null($intro) && strlen(getPlaintext($intro)) > 0)
        $text = getPlaintext($intro) . utf8_encode(". ");
    if (!is_null($arttext))
        $text = ($text . getPlaintext($arttext));

    array_merge($arr[0], getRiktkursAndCurrency($text));

    
    //$text = iconv("UTF-8","UTF-8//IGNORE",$text);
    $arr[0]["text"] = preg_replace("/[\n\r]/", "", $text); //preg_replace('/[^(\x20-\xFF)]*/','', $text);
    $rek = "";

    // rekommendation
    $rekindex = iarray_in_string(array("rekommendation", "höjer", "sänker"), $text);
    if ($rekindex > -1)
    {
        $words = explode(" ", strtolower(preg_replace("/[!\.,]/", "", substr($text, $rekindex))));
        $starkt = false;
        for($i=0; $i<count($words); $i++)
        {    
            switch ($words[$i])
            {
                case "starkt":
                    $starkt = true;
                case "köp":
                case "övervikt":
                case "öka":
                case "köprekommendation":
                case "outperform":
                    $rek = "+"; break;
                case "buy":
                    $rek = "+";
                    if ($i>0 && strtolower($words[$i-1]) == "conviction")
                        $rek = "++";
                    break;
                case "perform":
                    if ($i>0 && strtolower($words[$i-1]) == "sector")
                        $rek = "-";
                case "minska":
                case "undervikt":
                case "sälj":
                case "säljrekommendation":
                case "underperform":
                    $rek = "-"; break;
                case "neutral":
                case "jämvikt":
                case "behåll":
                case "behållrekommendation":
                    $rek = "0"; break;
            }
            
            //print $words[$i] . " => " . $rek;
            if (strlen($rek) > 0)
            {
                    if ($rek != "0" && $starkt)
                    $rek = $rek . $rek;
                // else nått konstigt om else inträffar här
                break;
            }
        }

        if (strlen($rek) > 0)
            $arr[0]["rek"] = $rek;
    }
    
    if ($rek == "")
    {        
        if (stripos($text, "köprekommendation") > -1)
            $rek = "+";
        if (iarray_in_string(array("säljrekommendation", "säljlista"), $text) > -1)
            $rek = "-";
        if (stripos($text, "behållrekommendation") > -1)
            $rek = "0";       

        if (strlen($rek) > 0)
            $arr[0]["rek"] = $rek;
    }

    if ($debug)
        print_r($arr[0]);

    return $arr;
}

function getRiktkursAndCurrency($text, $rub = "")
{
    $reg = array("/(till|är|anges|på|fortsatt) ([\d,:.]+)(\s\w+)?/i", "/(riktkursen|riktkurs|om) ([\d,:.]+)(\s\w+)?/i");
    $arr = array();

    // parsa antal månaders sikt
    if (preg_match("/([\d]+) månaders?/i", $text, $matches, PREG_OFFSET_CAPTURE)) {
        $sikt = intval($matches[1][0]);
        if ($sikt > 0)
        {
            $arr["months"] = $sikt;

            // rensa så inte antalet månader antas som riktkurs
            $newtext = substr($text, 0, $matches[0][1]) . substr($text, $matches[0][1] + strlen($matches[0][0]));
            $text = $newtext;
        }
    }

    $texter = array($rub, $text);

    foreach ($texter as $te)
    {
        foreach($reg as $r)
        {

            if (preg_match($r, $te, $matches, PREG_OFFSET_CAPTURE)) {
                $to = floatval(preg_replace("/[,:]/", ".", $matches[2][0]));
                $arr["to"] = $to;
        
                // valuta
                if (count($matches) == 4)
                {
                    $index = $matches[3][1];
                    $currency = array("euro", "eur", "sek", "kronor", "kr", "dollar", "pund", "brittiska pund", "kanadensiska dollar", "schweizerfranc");
                    foreach($currency as $c)
                    {
                        if (strtolower(trim(substr($te, $index, strlen($c)+1))) == $c)
                        {
                            $arr["currency"] = $c;
                            break;
                        }
                    }       
                }
    
                break;
            }
        }

        if (isset($arr["to"]))
            break;
    }

    return $arr;
}

function getAnalyshus()
{

return array("abg securities" => "ABG",
"abg sundal collier" => "ABG",
"abg" => "ABG",
"abn amro" => "ABN AMRO",
"affärsvärlden" => "Affärsvärlden",
"aktiespararen" => "Aktiespararen",
"alfred berg" => "Alfred Berg",
"aragon" => "Aragon",
"aros" => "Aros",
"avanza" => "Avanza",
"avanza analys" => "Avanza",
"baird" => "Baird",
"baird equity research" => "Baird",
"boa" => "Bank of America",
"bank of america" => "Bank of America",
"bank of america merill lynch" => "Bank of America",
"bank of america merill lynch" => "Bank of America",
"bank of america merill lynch" => "Bank of America",
"bank of america merrill lynch" => "Bank of America",
"bank of america merrill lynch" => "Bank of America",
"bank of america merill lynch" => "Bank of America",
"bank of america merrill lynch" => "Bank of America",
"barclays" => "Barclays",
"barclays capital" => "Barclays",
"bear sterns" => "Bear Sterns",
"berenberg" => "Berenberg",
"berenberg bank" => "Berenberg Bank",
"bernstein" => "Bernstein",
"biotech sweden" => "Biotech Sweden",
"bnp paribas" => "BNP Paribas",
"börsinsikt" => "Börsinsikt",
"börsveckan" => "Börsveckan",
"canaccord" => "Canaccord",
"canaccord genuity" => "Canaccord Genuity",
"carnegie" => "Carnegie",
"cazenove" => "Cazenove",
"cheuverux" => "Cheuverux",
"cheuvreux" => "Cheuvreux",
"cibc" => "CIBC",
"citi" => "Citigroup",
"citigroup" => "Citigroup",
"collins stewart" => "Collins Stewart",
"commerzbank" => "Commerzbank",
"credit agricole croup" => "Credit Agricole Croup",
"credit suiss" => "Credit Suisse",
"credit suisse" => "Credit Suisse",
"dagens industri" => "Dagens Industri",
"di" => "Dagens Industri",
"daiwa institute of research" => "Daiwa Institute of Research",
"danske" => "Danske Bank",
"danske bank" => "Danske Bank",
"danske markets" => "Danske Markets",
"deutsche bank" => "Deutsche Bank",
"dnb" => "DNB",
"dnb markets" => "DNB",
"dnb nor" => "DNB Nor",
"dnb nor markets" => "DnB Nor",
"dresdner kleinwort wasserstein" => "Dresdner Kleinwort Wasserstein",
"dundee" => "Dundee",
"ekonomi24" => "ekonomi24",
"enskilda securities" => "Enskilda Securities",
"eq" => "EQ Bank",
"eq bank" => "EQ Bank",
"erik penser" => "Erik Penser Bank",
"erik penser bank" => "Erik Penser Bank",
"erik pensers bank" => "Erik Penser Bank",
"evli" => "Evli",
"exane" => "Exane",
"exane bnp" => "Exane BNP",
"exane bnp paribas" => "Exane BNP Paribas",
"finans & vision" => "Finans & Vision",
"finanstidningen" => "Finanstidningen",
"fischer partners" => "Fischer Partners",
"glitnir" => "Glitnir",
"goldman" => "Goldman Sachs",
"goldman sachs" => "Goldman Sachs",
"h&q private banking" => "H&Q Private Banking",
"hagströmer & qviberg" => "Hagströmer & Qviberg",
"handelsbanken" => "Handelsbanken",
"helvea" => "Helvea",
"hq bank" => "HQ Bank",
"hq.se" => "HQ.SE",
"hsbc" => "HSBC",
"human securities" => "Human Securities",
"ing" => "ING",
"ing barrings" => "ING",
"ing financial markets" => "ING",
"jefferies" => "Jefferies",
"josephthal" => "Josephthal",
"jp morgan" => "JP Morgan",
"julius bär" => "Julius Bär",
"jyske bank" => "Jyske Bank",
"kaupthing" => "Kaupthing",
"kaupthing bank" => "Kaupthing",
"kbw" => "KBW",
"keybanc" => "Keybanc",
"lehman brothers" => "Lehman Brothers",
"liberium" => "Liberium",
"macquarie" => "Macquarie",
"macquarie equities research" => "Macquarie",
"macquarie research" => "Macquarie",
"macquire" => "Macquire",
"main first" => "Main First",
"main first bank" => "Main First",
"mandatum" => "Mandatum",
"matteus" => "Matteus",
"merrill lynch" => "Merrill Lynch",
"morgan stanley" => "Morgan Stanley",
"natixis" => "Natixis",
"naxitis" => "Naxitis",
"nomura" => "Nomura",
"nomura equity research" => "Nomura",
"nordbanken" => "Nordbanken",
"nordbanken aktier" => "Nordbanken",
"nordea" => "Nordea",
"nordea equity research" => "Nordea",
"nordea markets" => "Nordea",
"nordiska" => "Nordiska",
"oddo" => "Oddo",
"oddo securities" => "Oddo",
"opstock" => "Opstock",
"pareto" => "Pareto Öhman",
"pareto Öhman" => "Pareto Öhman",
"piper jaffray" => "Piper Jaffray",
"placera.nu" => "Placera.nu",
"placeringsguiden" => "Placeringsguiden",
"pojhola" => "Pohjola",
"pohjola" => "Pohjola",
"pohjola bank" => "Pohjola",
"privata affärer" => "Privata Affärer",
"prudential" => "Prudential",
"rbc" => "RBC",
"rbc capital markets" => "RBC",
"redburn" => "Redburn",
"redeye" => "Redeye",
"remium" => "Remium",
"remium securities" => "Remium Securities",
"robertson stephens" => "Robertson Stephens",
"rbs"  => "Royal Bank of Scotland",
"rbos"  => "Royal Bank of Scotland",
"royal bank of scotland" => "Royal Bank of Scotland",
"salomon smith barney" => "Salomon Smith Barney",
"sands brothers" => "Sands Brothers",
"sanford bernstein" => "Sanford Bernstein",
"seb" => "SEB",
"seb enskilda" => "SEB Enskilda",
"skandiabanken" => "Skandiabanken",
"shb" => "Handelsbanken",
"societe generale" => "Societe Generale",
"societe generale" => "Societe Generale",
"standard & poor" => "Standard & Poor",
"standard & poors" => "Standard & Poor",
"s&p equity research" => "Standard & Poor",
"s&p" => "Standard & Poor",
"stockpicker" => "Stockpicker",
"swedbank" => "Swedbank",
"swedbank" => "Swedbank",
"swedbank equity research" => "Swedbank",
"swedbank first securities" => "Swedbank",
"swedbank markets" => "Swedbank",
"sydbank" => "Sydbank",
"td securities" => "TD Securities",
"td newcrest" => "TD Newcrest",
"terra markets" => "Terra Markets",
"transcom" => "Transcom",
"trends" => "Trends",
"ubs" => "UBS",
"ubs warburg" => "UBS",
"underperform" => "Underperform",
"unicredit" => "Unicredit",
"us bancorp" => "US Bancorp",
"veckans affärer" => "Veckans Affärer",
"wells fargo" => "Wells Fargo",
"west lb" => "West LB",
"westlb" => "WestLB",
"westlb panmure" => "WestLB Panmure",
"williams de broe" => "Williams de Broe",
"wit soundview" => "Wit Soundview",
"ålandsbanken" => "Ålandsbanken",
"öhman" => "Öhman");
}

function getAllCompanys()
{
    /*
    $html = scraperWiki::scrape("http://di.se/Stockwatch/StockwatchCompanies/");           
    $dom = new simple_html_dom();
    $dom->load($html);

    $arr = array();
    foreach($dom->find(".alphabet-index ul li a") as $link){

        $stock = strtolower(getPlaintext($link));
        $arr[$stock] = "";
        print_r("\"" . $stock . "\" => \"" . getPlaintext($link) . "\",\n");
    }

    return $arr;
    */
    $companys = array("2e group" => "2E Group",
"3l system" => "3L System",
"5050 poker holding ab" => "5050 Poker Holding AB",
"a-com" => "A-Com",
"aarhuskarlshamn" => "AarhusKarlshamn",
"abb" => "ABB",
"acando" => "Acando",
"acap invest" => "ACAP Invest",
"accelerator nordic" => "Accelerator Nordic",
"active biotech" => "Active Biotech",
"addnode" => "AddNode",
"addtech" => "Addtech",
"addvise" => "Addvise",
"aerocrine b" => "Aerocrine B",
"africa oil" => "Africa Oil",
"agellis group" => "Agellis Group",
"aik fotboll" => "AIK Fotboll",
"alfa laval" => "Alfa Laval",
"allenex" => "Allenex",
"alliance oil" => "Alliance Oil",
"allokton" => "Allokton",
"alltele" => "AllTele",
"alpcot" => "Alpcot Agro",
"amhult" => "Amhult",
"anoto group" => "Anoto Group",
"aqeri" => "Aqeri",
"aqua terrena" => "Aqua Terrena",
"arcam" => "Arcam",
"archelon mineral" => "Archelon Mineral",
"arctic" => "Arctic",
"arctic gold" => "Arctic Gold",
"arise windpower" => "Arise Windpower",
"arocell" => "AroCell",
"aros quality group" => "Aros Quality Group",
"artimplant" => "Artimplant",
"aspiro" => "Aspiro",
"assa abloy" => "Assa Abloy",
"astrazeneca" => "AstraZeneca",
"atlas copco" => "Atlas Copco",
"atrium ljungberg" => "Atrium Ljungberg",
"autoliv" => "Autoliv",
"avalon enterprise" => "Avalon Enterprise",
"avanza" => "Avanza",
"avega" => "Avega",
"avensia innovation" => "Avensia Innovation",
"avtech sweden b" => "Avtech Sweden B",
"axfood" => "Axfood",
"axichem" => "Axichem",
"axis" => "Axis",
"axlon group" => "Axlon Group",
"b&b tools" => "B&B Tools",
"bahnhof" => "Bahnhof",
"be group" => "BE Group",
"beijer alma" => "Beijer Alma",
"beijer electronics" => "Beijer Electronics",
"beowulf mining" => "Beowulf Mining",
"bergs timber" => "Bergs Timber",
"betsson" => "Betsson",
"betting promotion sweden b" => "Betting Promotion Sweden B",
"bilia" => "Bilia",
"billerud" => "Billerud",
"biogaia" => "BioGaia",
"bioinvent" => "BioInvent",
"biolight" => "Biolight",
"biolin scientific" => "Biolin Scientific",
"biophausia" => "BioPhausia",
"biotage" => "Biotage",
"björn borg" => "Björn Borg",
"black earth farming" => "Black Earth Farming",
"blackpearl resources sdb" => "BlackPearl Resources SDB",
"boliden" => "Boliden",
"bong" => "Bong",
"borevind" => "Borevind",
"botnia exploration" => "Botnia Exploration",
"boule diagnostics ab" => "Boule Diagnostics AB",
"bredband2" => "Bredband2",
"bringwell" => "Bringwell",
"brinova" => "Brinova",
"brio" => "Brio",
"bts group" => "BTS Group",
"bure equity" => "Bure Equity",
"byggmax" => "Byggmax",
"c-rad" => "C-Rad",
"c2sat holding" => "C2SAT holding",
"caperio holding" => "Caperio Holding",
"capilon" => "Capilon",
"cardo" => "Cardo",
"castellum" => "Castellum",
"catech" => "Catech",
"catella" => "Catella",
"catena" => "Catena",
"cavotec sa" => "Cavotec SA",
"cdon group ab" => "CDON Group AB",
"cellavision" => "CellaVision",
"central asia gold" => "Central Asia Gold",
"cherryföretagen" => "Cherryföretagen",
"chrontech pharma" => "ChronTech Pharma",
"cision" => "Cision",
"clas ohlson" => "Clas Ohlson",
"clean oil technology" => "Clean Oil Technology",
"clinical laserthermia" => "Clinical Laserthermia",
"cloetta" => "Cloetta",
"coastal contacts" => "Coastal Contacts",
"commodity quest" => "Commodity Quest",
"concentric ab" => "Concentric AB",
"concordia maritime" => "Concordia Maritime",
"confidence international ab" => "Confidence International AB",
"connecta ab" => "Connecta AB",
"conpharm" => "Conpharm",
"consilium" => "Consilium",
"corem property group ab" => "Corem Property Group AB",
"covial device ab" => "Covial Device AB",
"creades a" => "Creades A",
"crown energy ab" => "Crown Energy AB",
"cryptzone" => "Cryptzone",
"ctt systems" => "CTT Systems",
"cybaero" => "CybAero",
"cybercom" => "Cybercom",
"dacke" => "Dacke",
"dagon" => "Dagon",
"dannemora mineral" => "Dannemora Mineral",
"dedicare ab" => "Dedicare AB",
"deltaco" => "Deltaco",
"dgc one" => "DGC One",
"diadrom holding" => "Diadrom Holding",
"diamyd medical" => "Diamyd Medical",
"dibs payment services" => "DIBS Payment Services",
"dignitana" => "Dignitana",
"din bostad sverige" => "Din Bostad Sverige",
"diös fastigheter" => "Diös Fastigheter",
"done management & systems" => "Done Management & Systems",
"doro" => "Doro",
"drillcon" => "Drillcon",
"duni" => "Duni",
"duroc" => "Duroc",
"east capital explorer" => "East Capital Explorer",
"elanders" => "Elanders",
"electra gruppen" => "Electra Gruppen",
"electrolux" => "Electrolux",
"elekta" => "Elekta",
"elektronikgruppen" => "ElektronikGruppen",
"ellen" => "Ellen",
"elos" => "Elos",
"elverket vallentuna" => "Elverket Vallentuna",
"empire" => "Empire",
"endomines" => "Endomines",
"enea" => "Enea",
"energyo solutions russia" => "EnergyO Solutions Russia",
"eniro" => "Eniro",
"enjoy group" => "Enjoy Group",
"enquest" => "Enquest",
"entraction holding" => "Entraction Holding",
"enzymatica" => "Enzymatica",
"eolus vind" => "Eolus Vind",
"epicept" => "Epicept",
"episurf medical ab" => "Episurf Medical AB",
"ericsson" => "Ericsson",
"esoteric golf technology" => "Esoteric Golf Technology",
"etrion" => "Etrion",
"eurocine vaccines" => "Eurocine Vaccines",
"eurocon consulting" => "Eurocon Consulting",
"ework scandinavia" => "eWork Scandinavia",
"exini diagnostics ab" => "Exini Diagnostics AB",
"fabege" => "Fabege",
"factum electronics hold." => "Factum Electronics Hold.",
"fagerhult" => "Fagerhult",
"fast partner" => "Fast Partner",
"fastighets balder b" => "Fastighets Balder B",
"feelgood" => "Feelgood",
"fenix outdoor" => "Fenix Outdoor",
"fingerprint" => "Fingerprint",
"finnvedenbulten ab" => "FinnvedenBulten AB",
"firefly" => "Firefly",
"forestlight studio" => "Forestlight Studio",
"formpipe software" => "Formpipe Software",
"fortnox" => "Fortnox",
"fortnox international ab" => "Fortnox International AB",
"free2move holding" => "Free2move Holding",
"g&l beijer" => "G&L Beijer",
"g5 entertainment" => "G5 Entertainment",
"generic sweden" => "Generic Sweden",
"genovis" => "Genovis",
"getinge" => "Getinge",
"getupdated internet marketing" => "Getupdated Internet Marketing",
"geveko" => "Geveko",
"ginger oil" => "Ginger Oil",
"global health partner" => "Global Health Partner",
"glycorex" => "Glycorex",
"götenehus group ab" => "Götenehus Group AB",
"guideline" => "Guideline",
"gunnebo" => "Gunnebo",
"hakon invest" => "Hakon Invest",
"haldex" => "Haldex",
"hansa medical" => "Hansa Medical",
"havsfrun" => "Havsfrun",
"hcs holding" => "HCS Holding",
"heba" => "Heba",
"hedson technologies" => "Hedson Technologies",
"hemtex" => "Hemtex",
"hennes & mauritz" => "Hennes & Mauritz",
"h&m" => "Hennes & Mauritz",
"hm" => "Hennes & Mauritz",
"hexagon" => "Hexagon",
"hexatronic scandinavia" => "Hexatronic Scandinavia",
"hexpol" => "Hexpol",
"hifab group" => "Hifab Group",
"hiq" => "HiQ",
"hl display" => "HL Display",
"hms networks" => "HMS Networks",
"höganäs" => "Höganäs",
"holmen" => "Holmen",
"hq ab" => "HQ AB",
"hufvudstaden" => "Hufvudstaden",
"human care" => "Human Care",
"husqvarna" => "Husqvarna",
"hydropulsor" => "Hydropulsor",
"hyresfastighetsfonden mgmt swe ab" => "Hyresfastighetsfonden Mgmt Swe AB",
"i.a.r systems group" => "I.a.r Systems Group",
"ibs" => "IBS",
"idl biotech" => "IDL Biotech",
"ifs" => "IFS",
"image systems" => "Image Systems",
"impact coatings" => "Impact Coatings",
"industrivärden" => "Industrivärden",
"indutrade" => "Indutrade",
"insight energy" => "Insight Energy",
"insplanet" => "Insplanet",
"int. gold exploration" => "Int. Gold Exploration",
"intellecta" => "Intellecta",
"intrum justitia" => "Intrum Justitia",
"investor" => "Investor",
"invisio communications" => "Invisio Communications",
"isconova" => "Isconova",
"itab shop concept" => "ITAB Shop Concept",
"jays ab" => "Jays AB",
"jeeves" => "Jeeves",
"jlt mobile computers" => "JLT Mobile Computers",
"jm" => "JM",
"josab international" => "Josab International",
"kabe" => "Kabe",
"kancera" => "Kancera",
"kapp-ahl" => "Kapp-Ahl",
"karo bio" => "Karo Bio",
"karolinska development" => "Karolinska Development",
"keynote media group" => "Keynote Media Group",
"kilsta metall" => "Kilsta Metall",
"kinnevik" => "Kinnevik",
"klövern ab" => "Klövern AB",
"knowit" => "KnowIT",
"kopparberg mineral" => "Kopparberg Mineral",
"kopparbergs bryggeri" => "Kopparbergs Bryggeri",
"kopy goldfields ab" => "Kopy Goldfields AB",
"kungsleden" => "Kungsleden",
"labs2 group" => "Labs2 Group",
"lagercrantz" => "Lagercrantz",
"lammhult" => "Lammhult",
"lappland goldminers" => "Lappland Goldminers",
"latour" => "Latour",
"lawson software" => "Lawson software",
"lbi international" => "LBI International",
"lc-tec holding" => "LC-TEC Holding",
"leox holding" => "Leox Holding",
"lifeassays" => "LifeAssays",
"lightlab" => "Lightlab",
"lindab" => "Lindab",
"loomis" => "Loomis",
"lovisagruvan" => "Lovisagruvan",
"lucara diamond corp." => "Lucara Diamond Corp.",
"lundbergs" => "Lundbergs",
"lundin mining" => "Lundin Mining",
"lundin petroleum" => "Lundin Petroleum",
"luxonen" => "Luxonen",
"mackmyra svensk whisky ab" => "Mackmyra Svensk Whisky AB",
"malmbergs elekt." => "Malmbergs Elekt.",
"meda" => "Meda",
"medcap" => "Medcap",
"medcore" => "MedCore",
"mediaprovider scandinavia" => "Mediaprovider Scandinavia",
"medirox" => "MediRox",
"medivir" => "Medivir",
"megacon" => "Megacon",
"mekonomen" => "Mekonomen",
"melker schörling" => "Melker Schörling",
"metro" => "Metro",
"metromark hospitality group" => "Metromark Hospitality Group",
"micro systemation" => "Micro Systemation",
"micronic mydata" => "Micronic Mydata",
"midsona ab" => "Midsona AB",
"midway" => "Midway",
"millicom" => "Millicom",
"mineral invest international mii" => "Mineral Invest International MII",
"moberg derma ab" => "Moberg Derma AB",
"modern times group" => "Modern Times Group",
"mtg" => "Modern Times Group",
"modul 1 data" => "Modul 1 Data",
"morphic" => "Morphic",
"mq" => "MQ",
"mq holding" => "MQ",
"msc konsult" => "MSC Konsult",
"multiq" => "MultiQ",
"munters" => "Munters",
"mvv holding" => "MVV Holding",
"naxs nordic access buyout fund" => "NAXS Nordic Access Buyout Fund",
"ncc" => "NCC",
"nederman holding" => "Nederman Holding",
"net entertainment" => "NET Entertainment",
"net insight" => "Net Insight",
"netjobs group" => "NetJobs Group",
"netonnet" => "Netonnet",
"neurovive pharmaceutical" => "NeuroVive Pharmaceutical",
"new nordic healthbrands" => "New Nordic Healthbrands",
"new wave group" => "New Wave Group",
"nfo drives" => "NFO Drives",
"ngs group" => "NGS Group",
"nibe" => "NIBE",
"niscayah group" => "Niscayah Group",
"nischer" => "Nischer",
"nobia" => "Nobia",
"nokia" => "Nokia",
"nolato" => "Nolato",
"nordea" => "Nordea",
"nordic mines" => "Nordic Mines",
"nordnet" => "Nordnet",
"note" => "Note",
"novacast" => "NovaCast",
"novestra" => "Novestra",
"novotek" => "Novotek",
"nsp holding" => "NSP Holding",
"oasmia pharmaceutical" => "Oasmia Pharmaceutical",
"obducat" => "Obducat",
"odd molly international" => "Odd Molly International",
"oem" => "OEM",
"old mutual" => "Old Mutual",
"online brands nordic ab" => "Online Brands Nordic AB",
"opcon" => "Opcon",
"opus prodox" => "OPUS Prodox",
"orasolv" => "Orasolv",
"orc software" => "Orc Software",
"orexo" => "Orexo",
"oriflame" => "Oriflame",
"ortivus" => "Ortivus",
"oxigene" => "Oxigene",
"pa resources" => "PA Resources",
"pallas group" => "Pallas Group",
"panalarm" => "Panalarm",
"panaxia security" => "Panaxia Security",
"paradox entertainment" => "Paradox Entertainment",
"partnertech" => "PartnerTech",
"paynova" => "Paynova",
"peab" => "Peab",
"petrogrand ab" => "Petrogrand AB",
"pfizer" => "Pfizer",
"phonera" => "Phonera",
"pilum" => "Pilum",
"pledpharma" => "PledPharma",
"polyplank" => "Polyplank",
"poolia" => "Poolia",
"precio systemutveckling" => "Precio Systemutveckling",
"precise biometrics" => "Precise Biometrics",
"precomp solutions" => "Precomp Solutions",
"prevas" => "Prevas",
"pricer" => "Pricer",
"proact it group" => "ProAct IT Group",
"probi" => "Probi",
"proffice" => "Proffice",
"profilgruppen" => "ProfilGruppen",
"psi group" => "PSI Group",
"pv enterprise sweden" => "PV Enterprise Sweden",
"q-med" => "Q-Med",
"rasta group" => "Rasta group",
"ratos" => "Ratos",
"raysearch laboratories" => "RaySearch Laboratories",
"readsoft" => "Readsoft",
"redbet holding" => "Redbet Holding",
"rederi transatlantic b" => "Rederi Transatlantic B",
"rejlerkoncernen" => "Rejlerkoncernen",
"resurs cnc" => "Resurs CNC",
"rezidor hotel group" => "Rezidor Hotel Group",
"rnb retail and brands" => "RNB Retail and Brands",
"rnb" => "RNB Retail and Brands",
"rörvik timber ab" => "Rörvik Timber AB",
"rottneros" => "Rottneros",
"ruric" => "Ruric",
"rusforest" => "Rusforest",
"saab" => "Saab",
"sagax" => "Sagax",
"sagax pref" => "Sagax pref",
"säki" => "SäkI",
"sandvik" => "Sandvik",
"sas" => "SAS",
"sca" => "SCA",
"scandbook holding" => "Scandbook Holding",
"scandinavian clinical nutrition" => "Scandinavian Clinical Nutrition",
"scandinavian healthy brands" => "Scandinavian Healthy Brands",
"scania" => "Scania",
"seamless" => "Seamless",
"seanet maritime communications" => "SeaNet Maritime Communications",
"seb" => "SEB",
"seco tools" => "Seco Tools",
"sectra" => "Sectra",
"securitas" => "Securitas",
"selena oil & gas" => "Selena Oil & Gas",
"semafo inc" => "SEMAFO Inc",
"semcon" => "Semcon",
"sensodetect" => "SensoDetect",
"sensys traffic" => "Sensys Traffic",
"servage" => "Servage",
"shamaran petroleum corp." => "Shamaran Petroleum Corp.",
"shb" => "SHB",
"shelton petroleum ab" => "Shelton Petroleum AB",
"si holding ab" => "SI Holding AB",
"sigma" => "Sigma",
"sintercast" => "SinterCast",
"sjr in scandinavia ab" => "SJR in Scandinavia AB",
"skanditek" => "Skanditek",
"skåne-möllan" => "Skåne-möllan",
"skanska" => "Skanska",
"skånska energi ab" => "Skånska Energi AB",
"skf" => "SKF",
"skistar" => "SkiStar",
"smarteq" => "Smarteq",
"softronic" => "Softronic",
"sotkamo silver" => "Sotkamo Silver",
"srab shipping ab" => "SRAB Shipping AB",
"ssab" => "SSAB",
"starbreeze" => "Starbreeze",
"stille" => "Stille",
"stjärnafyrkant" => "StjärnaFyrkant",
"stora enso" => "Stora Enso",
"studsvik ab" => "Studsvik AB",
"stureguld ab" => "Stureguld AB",
"svedbergs" => "Svedbergs",
"svenska capital oil" => "Svenska Capital Oil",
"sveriges bostadsrättscentrum ab" => "Sveriges Bostadsrättscentrum AB",
"svolder" => "Svolder",
"sweco" => "Sweco",
"swedbank" => "Swedbank",
"swedish bar systems holding" => "Swedish Bar Systems Holding",
"swedish match" => "Swedish Match",
"swedish orphan biovitrum" => "Swedish Orphan Biovitrum",
"swedol" => "Swedol",
"switchcore ab" => "SwitchCore AB",
"systemair" => "Systemair",
"tagmaster" => "TagMaster",
"taurus energy" => "Taurus Energy",
"tele2" => "Tele2",
"telia sonera" => "Telia Sonera",
"termoregulator holding" => "Termoregulator Holding",
"tethys oil" => "Tethys Oil",
"tieto" => "Tieto",
"tilgin" => "Tilgin",
"tractechnology" => "TracTechnology",
"traction" => "Traction",
"tradedoubler" => "TradeDoubler",
"transcom worldwide" => "Transcom WorldWide",
"translink holding" => "TransLink Holding",
"transmode holding ab" => "Transmode Holding AB",
"travelpartner" => "Travelpartner",
"trelleborg" => "Trelleborg",
"tretti" => "Tretti",
"tricorona" => "Tricorona",
"trigon agri a/s" => "Trigon Agri A/S",
"trustbuddy international" => "TrustBuddy International",
"trygga hem skandinavien" => "Trygga Hem Skandinavien",
"unibet group" => "Unibet Group",
"uniflex" => "Uniflex",
"unlimited travel group" => "Unlimited Travel Group",
"vbg" => "VBG",
"venue retail group" => "Venue Retail Group",
"victoria park" => "Victoria Park",
"vindico security" => "Vindico Security",
"vinovo" => "Vinovo",
"vitec software group" => "Vitec Software Group",
"vitrolife" => "Vitrolife",
"vkg energy services" => "VKG Energy Services",
"volvo" => "Volvo",
"vostok nafta investment ltd sdb" => "Vostok Nafta Investment Ltd SDB",
"wallenstam" => "Wallenstam",
"wesc" => "WeSC",
"west international" => "West International",
"wihlborgs" => "Wihlborgs",
"wise group" => "Wise Group",
"world class seagull international" => "World Class Seagull International",
"xano" => "Xano",
"xcounter ab" => "Xcounter AB",
"yield" => "Yield",
"zetadisplay" => "ZetaDisplay",
"åf" => "ÅF",
"öresund" => "Öresund"
);
    return $companys;
}

function getPlaintext($el)
{
    if (is_null($el))
        return "";
    $value = trim(html_entity_decode($el->plaintext, ENT_QUOTES, 'UTF-8'));
    $value = mb_check_encoding($value, 'UTF-8') ? $value : utf8_encode($value);
    return $value;
}

function iarray_in_string($arr, $str)
{
    $index;
    foreach($arr as $item)
    {
        if (($index = stripos($str, $item)) > -1)
            return $index;
    }
    return -1;
}

// söker array arr där str == eller börjar på
function getitem_array_in_string($arr, $str)
{
    foreach($arr as $item)
    {
        if (stripos($str, $item) == 0)
            return $item;
    }
    return null;
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
