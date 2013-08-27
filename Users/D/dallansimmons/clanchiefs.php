<?php

require 'scraperwiki/simple_html_dom.php';

$clans = array();

//Clan scrape src
$html = scraperWiki::scrape('http://www.clanchiefs.org/p/chiefs.html'); 

//Load src
$dom = new simple_html_dom();
$dom->load($html);

//Snatch up dem purdy clan ids
$options = $dom->find('option');

array_shift($options);

foreach($options as $option) {
    $clan = array();
    $clan['clan'] = $option->plaintext;
    $clan['id'] = $option->value;
    array_push($clans , $clan);
}

scraperwiki::save(array('clan'), $clans);

/*
//Now the fun part, post on their server and get clan chief information

//set post variable
$url = 'http://www.clanchiefs.org/p/chiefs.html';
$id_field = urlencode('intClanID=1');
print $id_field;

//open connection
$ch = curl_init();

//set cURL info
curl_setopt($ch,CURLOPT_URL,$url);
curl_setopt($ch,CURLOPT_POST,count(1));
curl_setopt($ch,CURLOPT_POSTFIELDS,$id_field);

//execute post
$result = curl_exec($ch);

//close connection
curl_close($ch);

print $result;
*/

?>

<?php

require 'scraperwiki/simple_html_dom.php';

$clans = array();

//Clan scrape src
$html = scraperWiki::scrape('http://www.clanchiefs.org/p/chiefs.html'); 

//Load src
$dom = new simple_html_dom();
$dom->load($html);

//Snatch up dem purdy clan ids
$options = $dom->find('option');

array_shift($options);

foreach($options as $option) {
    $clan = array();
    $clan['clan'] = $option->plaintext;
    $clan['id'] = $option->value;
    array_push($clans , $clan);
}

scraperwiki::save(array('clan'), $clans);

/*
//Now the fun part, post on their server and get clan chief information

//set post variable
$url = 'http://www.clanchiefs.org/p/chiefs.html';
$id_field = urlencode('intClanID=1');
print $id_field;

//open connection
$ch = curl_init();

//set cURL info
curl_setopt($ch,CURLOPT_URL,$url);
curl_setopt($ch,CURLOPT_POST,count(1));
curl_setopt($ch,CURLOPT_POSTFIELDS,$id_field);

//execute post
$result = curl_exec($ch);

//close connection
curl_close($ch);

print $result;
*/

?>

