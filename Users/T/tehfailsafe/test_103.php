<?php
require 'scraperwiki/simple_html_dom.php';
$pages_array = array("Avacyn%20Restored","Dark%20Ascension","Innistrad","Magic%202013","Return%20to%20Ravnica","Gatecrash");

foreach ( $pages_array as $page ){
    $html = scraperWiki::scrape('http://gatherer.wizards.com/Pages/Search/Default.aspx?output=checklist&set=["'.$page.'"]');
    $dom = new simple_html_dom();
    $dom->load($html); 
    getPageList ( $dom);
}

function getPageList ( $dom ){
    foreach( $dom->find('a.nameLink') as $item){
        getCardInfo ( 'http://gatherer.wizards.com/Pages/Card/' . $item->href);
    }
}

function getCardInfo($url){
    $baseURL = 'http://gatherer.wizards.com/Pages/Card/'; 
    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $cardImage = $dom->find('img[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage]', 0)->src;
    $cardImage= str_replace("amp;", "", $cardImage );
    $imgURL = $baseURL . $cardImage;
  
    $name = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow] div[class=value]', 0)->plaintext;
    $name = iconv("UTF-8", "ISO-8859-1//TRANSLIT", $name );

    $mana = "";
    $manaImages = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow] div[class=value] img');
    foreach ( $manaImages  as $manaItem){
        $mana .= substr ( $manaItem->alt, 0, 1);
    }
    $mana = iconv("UTF-8", "ISO-8859-1//TRANSLIT", $mana );

    $cmc = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow] div[class=value]', 0);
    $cmc= iconv("UTF-8", "ISO-8859-1//TRANSLIT", $cmc );

    $type = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow] div[class=value]', 0);
    $type = iconv("UTF-8", "ISO-8859-1//TRANSLIT", $type );

    $text = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow] div[class=value]', 0);
    $text = iconv("UTF-8", "ISO-8859-1//TRANSLIT", $text );

    $flavor = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorRow] div[class=value]', 0);
    $flavor = iconv("UTF-8", "ISO-8859-1//TRANSLIT", $flavor );

    $cardNumber = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow] div[class=value]', 0);
    $cardNumber = iconv("UTF-8", "ISO-8859-1//TRANSLIT", $cardNumber );

    $artist = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistRow] div[class=value]', 0);
    $artist = iconv("UTF-8", "ISO-8859-1//TRANSLIT", $artist  );

    $rarity= $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow] div[class=value]', 0);
    $rarity = iconv("UTF-8", "ISO-8859-1//TRANSLIT", $rarity);

    $set= $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setRow] div[class=value]', 0);
    $set = iconv("UTF-8", "ISO-8859-1//TRANSLIT", $set);

    scraperwiki::save_sqlite(array("card"), array(  
                "Card"=>trim($name), 
                "Image"=>$imgURL, 
                "Mana"=>trim($mana)), 
                "CMC"=>trim($cmc),
                "Type"=>trim($type),
                "Card Text"=>trim($text), 
                "Flavor Text"=>trim($flavor),
                "Artist"=>trim($artist), 
                "Card Number"=>trim($cardNumber),
                "Rarity"=>trim($rarity),
                "Expansion"=>trim($set)
                );            
}



?>

