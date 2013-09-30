 <?php
$page = "http://skeedr.com/rjw.html";
$people = array();
$person = array();
$i = 0;

$search_html = scraperWiki::scrape($page);

require 'scraperwiki/simple_html_dom.php';
$search_dom = new simple_html_dom();
$search_dom->load($search_html); 

foreach($search_dom->find('div[class=card-top clear]') as $item){
    foreach($item->find("h2") as $namelink){
        $person['name'] =  $namelink->plaintext;
print_r($namelink->plaintext."\r\n");
    }
    foreach($item->find("dl") as $dl){
        $person['phone'] = $dl->children(1)->plaintext;
        $person['email'] = $dl->children(3)->plaintext;
        print_r($dl->children(1)->plaintext."\r\n");
        print_r($dl->children(3)->plaintext."\r\n");
    }
    $people[$i] = $person;
    $i++;
//print_r($item->plaintext."\r\n");
}

foreach($people as $wanted){
     scraperwiki::save_sqlite(array("name"), $wanted); 
}
?> <?php
$page = "http://skeedr.com/rjw.html";
$people = array();
$person = array();
$i = 0;

$search_html = scraperWiki::scrape($page);

require 'scraperwiki/simple_html_dom.php';
$search_dom = new simple_html_dom();
$search_dom->load($search_html); 

foreach($search_dom->find('div[class=card-top clear]') as $item){
    foreach($item->find("h2") as $namelink){
        $person['name'] =  $namelink->plaintext;
print_r($namelink->plaintext."\r\n");
    }
    foreach($item->find("dl") as $dl){
        $person['phone'] = $dl->children(1)->plaintext;
        $person['email'] = $dl->children(3)->plaintext;
        print_r($dl->children(1)->plaintext."\r\n");
        print_r($dl->children(3)->plaintext."\r\n");
    }
    $people[$i] = $person;
    $i++;
//print_r($item->plaintext."\r\n");
}

foreach($people as $wanted){
     scraperwiki::save_sqlite(array("name"), $wanted); 
}
?>