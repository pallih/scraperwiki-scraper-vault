<?php

require 'scraperwiki/simple_html_dom.php';          

for( $x = 1; $x <= 198; $x++ ){         
    $html = scraperWiki::scrape("http://natura2000.gdos.gov.pl/datafiles/index/page:${x}/all:0/province_id:1%7C2%7C3%7C4%7C5%7C6%7C7%7C8%7C9%7C10%7C11%7C12%7C13%7C14%7C15%7C16");  
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div[@id='lib-search-results'] tr") as $data){
        $tds = $data->find("td");
        if(count($tds)==7){
            $record = array(
                'data' => $tds[0]->plaintext . "\n",
                'data2' => $tds[2]->plaintext . "\n",
                'data3' => $tds[3] ->plaintext . "\n",
                'data4' => $tds[4] ->plaintext . "\n",
                'data5' => $tds[5] ->plaintext . "\n"
            );
        scraperwiki::save_sqlite(array("data"), $record);
        }
    }
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';          

for( $x = 1; $x <= 198; $x++ ){         
    $html = scraperWiki::scrape("http://natura2000.gdos.gov.pl/datafiles/index/page:${x}/all:0/province_id:1%7C2%7C3%7C4%7C5%7C6%7C7%7C8%7C9%7C10%7C11%7C12%7C13%7C14%7C15%7C16");  
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div[@id='lib-search-results'] tr") as $data){
        $tds = $data->find("td");
        if(count($tds)==7){
            $record = array(
                'data' => $tds[0]->plaintext . "\n",
                'data2' => $tds[2]->plaintext . "\n",
                'data3' => $tds[3] ->plaintext . "\n",
                'data4' => $tds[4] ->plaintext . "\n",
                'data5' => $tds[5] ->plaintext . "\n"
            );
        scraperwiki::save_sqlite(array("data"), $record);
        }
    }
}
?>
