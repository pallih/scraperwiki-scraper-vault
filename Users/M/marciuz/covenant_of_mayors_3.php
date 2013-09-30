<?php
require 'scraperwiki/simple_html_dom.php';    

$html = scraperWiki::scrape("http://www.eumayors.eu/about/signatories_en.html?q=&country_search=&population=&date_of_adhesion=&status=&start=1");   
 
// get the last
$dom = new simple_html_dom();
$dom->load($html);
$AA=$dom->find(".pagination a");
$AA_key=count($AA)-2;

echo $MAX=$AA[$AA_key]->plaintext;


  

for($p=1;$p<=$MAX;$p++){

    $html = scraperWiki::scrape("http://www.eumayors.eu/about/signatories_en.html?q=&country_search=&population=&date_of_adhesion=&status=&start=$p"); 
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find(".spip tr") as $data){

        
        $tds = $data->find("td");
        
    
        if(isset($tds[0]->plaintext)){

            $img= $tds[3]->find('img', 0 )->getAttribute('alt');

    
            $record = array(
                'Signatories' => preg_replace("| +|"," ",$tds[0]->plaintext), 
                'Population' => str_replace("inhabitants","",$tds[1]->plaintext),
                'Adhesion' => str_replace("&nbsp;"," ",$tds[2]->plaintext),
                'Status'=> $img
            );

                    
            print_r($record);
            $keys=array_keys($record);
            scraperwiki::save($keys,$record); 
        }
    }
    
    
}
<?php
require 'scraperwiki/simple_html_dom.php';    

$html = scraperWiki::scrape("http://www.eumayors.eu/about/signatories_en.html?q=&country_search=&population=&date_of_adhesion=&status=&start=1");   
 
// get the last
$dom = new simple_html_dom();
$dom->load($html);
$AA=$dom->find(".pagination a");
$AA_key=count($AA)-2;

echo $MAX=$AA[$AA_key]->plaintext;


  

for($p=1;$p<=$MAX;$p++){

    $html = scraperWiki::scrape("http://www.eumayors.eu/about/signatories_en.html?q=&country_search=&population=&date_of_adhesion=&status=&start=$p"); 
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find(".spip tr") as $data){

        
        $tds = $data->find("td");
        
    
        if(isset($tds[0]->plaintext)){

            $img= $tds[3]->find('img', 0 )->getAttribute('alt');

    
            $record = array(
                'Signatories' => preg_replace("| +|"," ",$tds[0]->plaintext), 
                'Population' => str_replace("inhabitants","",$tds[1]->plaintext),
                'Adhesion' => str_replace("&nbsp;"," ",$tds[2]->plaintext),
                'Status'=> $img
            );

                    
            print_r($record);
            $keys=array_keys($record);
            scraperwiki::save($keys,$record); 
        }
    }
    
    
}
