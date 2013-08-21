<?php

require 'scraperwiki/simple_html_dom.php';
function decode_ip($input){
$input = str_replace(array('fgh', 'vbn', 'rty',), array('2','3', '8'), $input);
        preg_match("/\d+/", $input, $matches);
$input = $matches[0];
return ($input >> 24) . '.' . (($input >> 16) & 0xff) . '.' . (($input >> 8) & 0xff) . '.' . ($input & 0xff);
}
function grab($url) {
$html = scraperWiki::scrape($url);           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("#tbl_proxy_list tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==7){
        $input = decode_ip((string) $tds[0]);
        $record = array(
            'ip' => $input
        );
        scraperwiki::save(array('ip'), $record); 
    }

}
}

grab("http://www.proxynova.com/proxy-server-list/country-us/");
grab("http://www.proxynova.com/proxy-server-list/country-cn/");
grab("http://www.proxynova.com/proxy-server-list/country-br/");
grab("http://www.proxynova.com/proxy-server-list/country-id/");
grab("http://www.proxynova.com/proxy-server-list/country-ve/");
grab("http://www.proxynova.com/proxy-server-list/country-th/");
grab("http://www.proxynova.com/proxy-server-list/country-ae/");
grab("http://www.proxynova.com/proxy-server-list/country-eg/");
grab("http://www.proxynova.com/proxy-server-list/country-pe/");
grab("http://www.proxynova.com/proxy-server-list/country-ru/");
grab("http://www.proxynova.com/proxy-server-list/country-in/");
grab("http://www.proxynova.com/proxy-server-list/country-tw/");
grab("http://www.proxynova.com/proxy-server-list/country-de/");
grab("http://www.proxynova.com/proxy-server-list/country-ua/");
grab("http://www.proxynova.com/proxy-server-list/country-ar/");
grab("http://www.proxynova.com/proxy-server-list/country-za/");
grab("http://www.proxynova.com/proxy-server-list/country-co/");
grab("http://www.proxynova.com/proxy-server-list/country-fr/");
grab("http://www.proxynova.com/proxy-server-list/country-gb/");
grab("http://www.proxynova.com/proxy-server-list/country-ir/");
grab("http://www.proxynova.com/proxy-server-list/country-ca/");
grab("http://www.proxynova.com/proxy-server-list/country-sy/");
grab("http://www.proxynova.com/proxy-server-list/country-pl/");
grab("http://www.proxynova.com/proxy-server-list/country-hk/");
grab("http://www.proxynova.com/proxy-server-list/country-nl/");
grab("http://www.proxynova.com/proxy-server-list/country-cz/");
grab("http://www.proxynova.com/proxy-server-list/country-it/");
grab("http://www.proxynova.com/proxy-server-list/country-jp/");
?>
