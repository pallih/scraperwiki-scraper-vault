<?php
require 'scraperwiki/simple_html_dom.php';
/*
$pages_array = array("Alara%20Reborn","Alliances","Antiquities","Apocalypse","Arabian%20Nights","Archenemy","Avacyn%20Restored","Betrayers%20of%20Kamigawa","Champions%20of%20Kamigawa","Chronicles","Classic%20Sixth%20Edition","Coldsnap","Commander%27s%20Arsenal","Conflux","Dark%20Ascension","Darksteel","Dissension","Eighth%20Edition","Eventide","Exodus","Fallen%20Empires","Fifth%20Dawn","Fifth%20Edition","Fourth%20Edition","Future%20Sight","Gatecrash","Guildpact","Homelands","Ice%20Age","Innistrad","Invasion","Judgment","Legends","Legions","Limited%20Edition%20Alpha","Limited%20Edition%20Beta","Lorwyn","Magic%202010","Magic%202011","Magic%202012","Magic%202013","Magic%3a%20The%20Gathering-Commander","Mercadian%20Masques","Mirage","Mirrodin","Mirrodin%20Besieged","Morningtide","Nemesis","New%20Phyrexia","Ninth%20Edition","Odyssey","Onslaught","Planar%20Chaos","Planeshift","Portal","Portal%20Second%20Age","Portal%20Three%20Kingdoms","Prophecy","Ravnica%3a%20City%20of%20Guilds","Return%20to%20Ravnica","Revised%20Edition","Rise%20of%20the%20Eldrazi","Saviors%20of%20Kamigawa","Scars%20of%20Mirrodin","Scourge","Seventh%20Edition","Shadowmoor","Shards%20of%20Alara","Stronghold","Tempest","Tenth%20Edition","The%20Dark","Time%20Spiral","Torment","Unglued","Unhinged","Unlimited%20Edition","Urza%27s%20Destiny","Urza%27s%20Legacy","Urza%27s%20Saga","Vanguard","Visions","Weatherlight","Worldwake","Zendikar");
*/

$pages_array = array("Seventh%20Edition","Shadowmoor","Shards%20of%20Alara","Stronghold","Tempest","Tenth%20Edition","The%20Dark","Time%20Spiral","Torment","Unglued","Unhinged","Unlimited%20Edition","Urza%27s%20Destiny","Urza%27s%20Legacy","Urza%27s%20Saga","Vanguard","Visions","Weatherlight","Worldwake","Zendikar");


foreach ( $pages_array as $page ){
    $html = scraperWiki::scrape('http://gatherer.wizards.com/Pages/Search/Default.aspx?output=checklist&set=%5b%22'.$page.'%22%5d');
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
  
    $name = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow] div[class=value]', 0);
    if ($name) $name = $name->plaintext;

    $mana = "";
    $manaImages = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow] div[class=value] img');
    foreach ( $manaImages  as $manaItem){
        $mana .= substr ( $manaItem->alt, 0, 1);
    }
    

    $cmc = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow] div[class=value]', 0);
    if ($cmc) $cmc = $cmc->plaintext;

    $type = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow] div[class=value]', 0);
    if ($type) $type = $type->plaintext;

    $text = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow] div[class=value]', 0);
    if ($text) $text = utf8_encode ($text->plaintext);

    $flavor = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorRow] div[class=value]', 0);
    if ($flavor) $flavor = str_replace ('—', '-', $flavor->plaintext);

    $cardNumber = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow] div[class=value]', 0);
    if ($cardNumber) $cardNumber = $cardNumber->plaintext;

    $artist = $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistRow] div[class=value]', 0);
    if ($artist) $artist= $artist->plaintext;

    $rarity= $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow] div[class=value]', 0);
    if ($rarity) $rarity = $rarity->plaintext;

    $set= $dom->find('div[id=ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setRow] div[class=value]', 0);
    if ($set) $set = $set->plaintext;

    scraperwiki::save_sqlite(array("card"), array(  
                "Card"=>trim($name), 
                "Image"=>$imgURL, 
                "Mana"=>trim($mana), 
                "CMC"=>trim($cmc),
                "Type"=>trim($type),
                "Card Text"=>trim($text), 
                "Flavor Text"=>trim($flavor),
                "Artist"=>trim($artist), 
                "Card Number"=>trim($cardNumber),
                "Rarity"=>trim($rarity),
                "Expansion"=>trim($set)
                ));            
}



?>

