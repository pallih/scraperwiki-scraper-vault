<?php
require 'scraperwiki/simple_html_dom.php';
function gazelangs($url,$lang){    
    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    $michi = "strong";
    $michi = $michi." hope";
    foreach($dom->find("ul[@class='trans_sent']") as $data){
        $tds = $data->find("li");
            $record = array(
                'user_input' => $tds[0]->plaintext, 
                'babelfish_output' => $tds[1]->plaintext, 
                'timestamp_scrape' => date("Y-m-d H:i:s"),
                'page' => $url,
                'language' => $lang
            );
            // print json_encode($record) . "\n";
            scraperwiki::save(array('user_input','babelfish_output','timestamp_scrape','page','language'), $record);
    }
}
gazelangs("http://en.babelfish.com/dutch-translator/","Dutch");
gazelangs("http://en.babelfish.com/spanish-translator/","Spanish");
gazelangs("http://en.babelfish.com/french-translator/","French");
gazelangs("http://en.babelfish.com/greek-translator/","Greek");
gazelangs("http://en.babelfish.com/hindi-translator/","Hindi");
gazelangs("http://en.babelfish.com/italian-translator/","Italian");
gazelangs("http://en.babelfish.com/japanese-translator/","Japanese");
gazelangs("http://en.babelfish.com/portuguese-translator/","Portuguese");
gazelangs("http://en.babelfish.com/ukrainian-translator/","Ukrainian");
gazelangs("http://en.babelfish.com/arabic-translator/","Arabic");
gazelangs("http://en.babelfish.com/chinese-translator/","Chinese");
gazelangs("http://en.babelfish.com/danish-translator/","Danish");

?>
