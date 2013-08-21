<?php
require 'scraperwiki/simple_html_dom.php';    

$html = scraperWiki::scrape("http://www.eumayors.eu/about/signatories_en.html?q=&country_search=&population=&date_of_adhesion=&status=&start=1");   
 
// get the last
$dom = new simple_html_dom();
$dom->load($html);
$AA=$dom->find(".pagination a");
$AA_key=count($AA)-2;

$MAX=$AA[$AA_key]->plaintext;


  

for($p=1;$p<$MAX;$p++){

    $html = scraperWiki::scrape("http://www.eumayors.eu/about/signatories_en.html?q=&country_search=&population=&date_of_adhesion=&status=&start=$p"); 
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find(".spip tr") as $data){

        
        $tds = $data->find("td");
    
        if(isset($tds[0]->plaintext)){

            $img= $tds[3]->find('img', 0 )->getAttribute('alt');

    
            $record = array(
                'Signatories' => $tds[0]->plaintext, 
                'Population' => str_replace(" inhabitants","",$tds[1]->plaintext),
                'Adhesion' => str_replace("&nbsp;"," ",$tds[2]->plaintext),
                'Status'=> $img
            );

            

           
        
            $link = $tds[0]->find("a");

         
            $html_dett = scraperWiki::scrape("http://www.eumayors.eu/".$link[0]->href);
            $dom_dett = new simple_html_dom();
            $dom_dett->load($html_dett);
            $data2=$dom_dett->find("#profile_overview table",0);

            if(is_object($data2)){
                $tds_dett = $data2->find("td");
            
                   // for($i=0;$i<count($tds_dett);$i++) print $i." -> ".$tds_dett[$i]->plaintext."\n";
                        
                $record['Population']= (isset($tds_dett[0]->plaintext)) ? $tds_dett[0]->plaintext : '';
                $record['Area']= (isset($tds_dett[1]->plaintext)) ? $tds_dett[1]->plaintext : '';
                $record['Country']= (isset($tds_dett[2]->plaintext)) ? $tds_dett[2]->plaintext : '';
                $record['Website']= (isset($tds_dett[3]->plaintext)) ? $tds_dett[3]->plaintext : '';
            }
            
       
        
            print_r($record);
            scraperwiki::save(array('Signatories', 'Population', 'Adhesion', 'Status','Population','Area','Country','Website'),$record); 
        }
    }
    
    
}
