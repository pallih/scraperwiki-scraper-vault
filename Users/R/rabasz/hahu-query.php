<?php

scraperwiki::sqliteexecute("drop table if exists swdata"); 
scraperwiki::sqlitecommit();

require 'scraperwiki/simple_html_dom.php'; 

//select "swdata2"."id" from `swdata2` left join "swdata1" on "swdata2"."id"="swdata1"."id" where "swdata1"."id" is null

scraperwiki::attach("uj-hasznaltauto-kodok", "src");
$newvalue=scraperwiki::select("* from src.swvariables");

if ($newvalue[0]['value_blob']=="1")
    {
    $query = "swdata2.url from swdata2 left join swdata1 on swdata2.id=swdata1.id where swdata1.id is null";
    }
    else
    {
    $query = "swdata1.url from swdata1 left join swdata2 on swdata1.id=swdata2.id where swdata2.id is null";
    }

$newcars = scraperwiki::select($query);
print $query . "\n";

foreach ($newcars as $carurl=>$url){
    $newurl = $url['url'];
    $kod = substr($newurl, -7);
    
    $html_content = scraperWiki::scrape($newurl);
    $html = str_get_html($html_content);

    $ar = $html->find("span.arsor",0);
    $ar = str_replace("&nbsp;", " ", $ar->innertext);
foreach ($html->find("div.hirdetesboxalso") as $talalat) {
    $prevtd = "...";
    foreach ($talalat->find("td") as $tds) {
        $td = $tds->innertext;
        $td = str_replace("<strong>", "", $td);
        $td = str_replace("</strong>", "", $td);
        if ($prevtd == "Évjárat:") {
            $evjarat = $td;
        } elseif ($prevtd == "Kivitel:") {
            $kivitel = $td;
        } elseif ($prevtd == "Állapot:") {
            $allapot = $td;
        } elseif ($prevtd == "Üzemanyag:") {
            $uzemanyag = $td;
        } elseif ($prevtd == "Sebességváltó fajtája:") {
            $sebvalto = $td;
        } elseif ($prevtd == "Hengerűrtartalom:") {
            $urtartalom = str_replace("&sup3;", "3", $td);
        } elseif ($prevtd == "Henger-elrendezés:") {
            $hengerelr = $td;
        } elseif ($prevtd == "Hajtás:") {
            $hajtas = $td;
        } elseif ($prevtd == "Teljesítmény:") {
            $teljesitmeny = $td;
        } elseif ($prevtd == "Ajtók száma:") {
            $ajtok = $td;
        } elseif ($prevtd == "Klíma fajtája:") {
            $klima = $td;
        } elseif ($prevtd == "Szín:") {
            $szin = $td;
        }
        if ($td == "Évjárat:") {
            $prevtd = "Évjárat:";
        } elseif ($td == "Kivitel:") {
            $prevtd = "Kivitel:";
        } elseif ($td == "Állapot:") {
            $prevtd = "Állapot:";
        } elseif ($td == "Üzemanyag:") {
            $prevtd = "Üzemanyag:";
        } elseif ($td == "Sebességváltó fajtája:") {
            $prevtd = "Sebességváltó fajtája:";
        } elseif ($td == "Hengerűrtartalom:") {
            $prevtd = "Hengerűrtartalom:";
        } elseif ($td == "Henger-elrendezés:") {
            $prevtd = "Henger-elrendezés:";
        } elseif ($td == "Hajtás:") {
            $prevtd = "Hajtás:";
        } elseif ($td == "Teljesítmény:") {
            $prevtd = "Teljesítmény:";
        } elseif ($td == "Ajtók száma:") {
            $prevtd = "Ajtók száma:";
        } elseif ($td == "Klíma fajtája:") {
            $prevtd = "Klíma fajtája:";
        } elseif ($td == "Szín:") {
            $prevtd = "Szín:";
        } else {
            $prevtd = "...";        } 
    }
}

    scraperWiki::save_sqlite(   
            array('id'),
            array(
                'id' => $kod,
                'url' => $newurl,
                'ar' => $ar,
                'evjarat' => $evjarat,
                'kivitel' => $kivitel,
                'allapot' => $allapot,
                'uzemanyag' => $uzemanyag,
                'sebvalto' => $sebvalto,
                'urtartalom' => $urtartalom,
                'hengerelrend' => $hengerelr,
                'hajtas' => $hajtas,
                'teljesitmeny' => $teljesitmeny,
                'ajtok' => $ajtok,
                'klima' => $klima,
                'szin' => $szin
            )
    );

}
?>
