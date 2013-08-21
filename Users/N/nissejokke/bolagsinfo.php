<?php

require 'scraperwiki/simple_html_dom.php';  
setlocale(LC_ALL, 'sv_SE.utf8');
//$html = scraperWiki::scrape("http://di.se/Stockwatch/StockwatchReports/?ParentSeqNo=515");           


//print $html . "\n";
// http://di.se/Borslistor/Sv-Large-Cap/

startLargeCompaniesScrape();

//print(xroot(9.7/1.56, 10));

function xroot($value, $base)
{
    return pow($value, 1.0/$base);
}

function scrapeLargestOwner($id)
{    
    $html = scraperWiki::scrape("http://di.se/Stockwatch/StockwatchOverview/?ParentSeqNo=" . $id);
    $dom = new simple_html_dom();
    $dom->load($html);
print $dom->find(".content table", 4)->innertext;
exit(0);
    foreach($dom->find(".content table", 4) as $link){

        $id = substr($link->href, strrpos($link->href, "=") + 1);
        $url = "http://di.se/Stockwatch/StockwatchReports/?ParentSeqNo=" . $id;

        print("scraping " . $link->plaintext . " (" . $url . ")\n");

        try {
            scrapeStock($url);
        }
        catch(Exception $e)
        {
            print("Error: " . $e->getMessage() . "\n");
        }

        exit(0);
    }
}

function startAllCompaniesScrape()
{
    $html = scraperWiki::scrape("http://di.se/Stockwatch/StockwatchCompanies/");           
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find(".alphabet-index ul li a") as $link){

        $id = substr($link->href, strrpos($link->href, "=") + 1);
        $url = "http://di.se/Stockwatch/StockwatchReports/?ParentSeqNo=" . $id;

        print("scraping " . $link->plaintext . " (" . $url . ")\n");

        try {
            scrapeStock($url);
        }
        catch(Exception $e)
        {
            print("Error: " . $e->getMessage() . "\n");
        }

        exit(0);
    }
}

function startLargeCompaniesScrape()
{
    $html = scraperWiki::scrape("http://di.se/Borslistor/Sv-Large-Cap/");           
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find(".table-stocklist a") as $link){

        $id = intval(substr($link->href, strrpos($link->href, "=") + 1));
        if ($id < 1)
            continue;

        $url = "http://di.se/Stockwatch/StockwatchReports/?ParentSeqNo=" . $id;
        scrapeLargestOwner($id);
        print("scraping " . $link->plaintext . " (" . $url . ")\n");
        
        try {
            scrapeStock($url);
        }
        catch(Exception $e)
        {
            print("Error: " . $e->getMessage() . "\n");
        }
        

    }
}


function scrapeStock($url)
{
    $html = scraperWiki::scrape($url);                    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $header = $dom->find(".stock-report-header h2", 0);
    if (is_null($header))
        throw new Exception("no header");

    $company = trim($header->plaintext);
    
    $trindex = 0;
    $years = array();
    $yrs = $dom->find("table#tblRep12 tr", 2)->find("td");
    
    if (count($yrs) <= 1)
        throw new Exception("no data, skipping");

    $firstyear = intval("20" . substr(getString($yrs[1]), 0, 2));
    
    if ($firstyear < 2000)
        throw new Exception("Invalid years");

    // Resultaträkning och balansräkning

    $records = array();

    $trindex = 0;
    foreach($dom->find("table#tblRep12 tr") as $trs){
        if ($trindex++ < 3)
            continue;
    
        $field = getString($trs->find("td", 0));
    
        $skip = false;
        switch($field)
        {
            case "Resultaträkning":
            case "Balansräkning":
            case "Rapportperiod":
            case "Datum för rapportperioden":
                $skip = true; break;
        }
    
        if ($skip)
            continue;
    
        $field = formatField($field);

        $tdindex = 0;
        foreach($trs->find("td") as $tds)
        {
            if ($tdindex++ == 0)
                continue;
    
            $value = getFloat($tds);

            $year = $firstyear - $tdindex + 2;
    
            if (!array_key_exists(strval($year), $records))
                $records[strval($year)] = array('bolag' => $company, 'ar' => $year);

            $records[strval($year)][$field] = $value;
    
        }

    }

    
    
    // Nyckeltal

    $trindex = 0;
    $tbls = $dom->find("table.stock-report");
    $nyckeltal = $tbls[count($tbls)-1];
    
    foreach($nyckeltal->find("tr") as $trs){
        if ($trindex++ < 2)
            continue;
    
        $field = getString($trs->find("td", 0));
    
        $skip = false;
        switch($field)
        {
            case "ÖVRIGA":
            case "AVKASTNINGS- OCH MARGINALMÅTT":
                $skip = true; break;
        }
    
        if ($skip)
            continue;
    
        $field = formatField($field);

        $tdindex = 0;
        foreach($trs->find("td") as $tds)
        {
            if ($tdindex++ == 0)
                continue;
    
            $value = getFloat($tds);  

            $year = $firstyear - $tdindex + 2;
    
            if (!array_key_exists(strval($year), $records))
                $records[strval($year)] = array('bolag' => $company, 'ar' => $year);

            $records[strval($year)][$field] = $value;
        }
    
    }

    foreach($records as $record)
    {
        scraperwiki::save(array('bolag', 'ar'), $record);
    }
}

function formatField($field)
{
    $f = strtolower($field);
    $change = array('å','ä','ö','Å','Ä','Ö');
    $to = array('a', 'a', 'o', 'a','a','o');
    $f = str_replace($change, $to, $f); 
    //$f = mb_strtolower($field , mb_detect_encoding($field));

    $f = preg_replace("/[^a-z0-9_ ]/", "", $f);

    $f = str_replace(" ", "_", $f);
    if (endsWith($f, "_"))
        $f = substr($f, 0, strlen($f)-1);
    $f = str_replace("__", "_", $f);
    return $f;
}

function getString($el)
{
    if (is_null($el))
        return "";
    return trim(str_replace(":", "", html_entity_decode($el->plaintext, ENT_QUOTES, 'UTF-8')));
}

function getFloat($el)
{
    return floatval(str_replace(" ", "", getString($el)));
}

function startsWith($haystack, $needle)
{
    $length = strlen($needle);
    return (substr($haystack, 0, $length) === $needle);
}

function endsWith($haystack, $needle)
{
    $length = strlen($needle);
    if ($length == 0) {
        return true;
    }

    $start  = $length * -1; //negative
    return (substr($haystack, $start) === $needle);
}

?>
