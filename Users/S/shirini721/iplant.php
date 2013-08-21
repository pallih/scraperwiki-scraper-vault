<?php
 $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://auth.iplantcollaborative.org/idp/Authn/UserPassword'); //login URL
    curl_setopt ($ch, CURLOPT_POST, 1);
    $postData='j_username=zashktorab&j_password=Omg909072!!';
    curl_setopt ($ch, CURLOPT_POSTFIELDS, $postData);
    curl_setopt ($ch, CURLOPT_COOKIEJAR, 'cookie.txt');
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    $store = curl_exec ($ch);
    return $ch;

$html_content = scraperWiki::scrape("https://my-plant.org/users/all");

require 'scraperwiki/simple_html_dom.php';

$html = str_get_html($html_content);
foreach ($html->find("div.reduce") as $el) {
   print $el . "\n";

 $record = array(
        'user' => $el->plaintext
 
    );
 scraperwiki::save(array('user'), $record); 
}


?>
