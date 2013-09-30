<?php
require 'scraperwiki/simple_html_dom.php';    

$html = scraperWiki::scrape("http://www.eumayors.eu/about/signatories_en.html?q=&country_search=&population=&date_of_adhesion=&status=&start=1");   
 
// get the last
$dom = new simple_html_dom();
$dom->load($html);
$AA=$dom->find(".pagination a");
$AA_key=count($AA)-1;

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
                'Signatories' => preg_replace("| +|"," ",$tds[0]->plaintext), 
                'Population' => str_replace("inhabitants","",$tds[1]->plaintext),
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
                $ths = $data2->find("th");
            
                   // for($i=0;$i<count($tds_dett);$i++) print $i." -> ".$tds_dett[$i]->plaintext."\n";
               

               for($ii=0;$ii<=3;$ii++){

                    $k=trim(str_replace(":","",$ths[$ii]->plaintext));
                    if($k!=''){
                        $record[$k]= (isset($tds_dett[$ii]->plaintext)) ? $tds_dett[$ii]->plaintext : '';
                    }
               }
            }
            
       
        
            //print_r($record);
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
$AA_key=count($AA)-1;

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
                'Signatories' => preg_replace("| +|"," ",$tds[0]->plaintext), 
                'Population' => str_replace("inhabitants","",$tds[1]->plaintext),
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
                $ths = $data2->find("th");
            
                   // for($i=0;$i<count($tds_dett);$i++) print $i." -> ".$tds_dett[$i]->plaintext."\n";
               

               for($ii=0;$ii<=3;$ii++){

                    $k=trim(str_replace(":","",$ths[$ii]->plaintext));
                    if($k!=''){
                        $record[$k]= (isset($tds_dett[$ii]->plaintext)) ? $tds_dett[$ii]->plaintext : '';
                    }
               }
            }
            
       
        
            //print_r($record);
            $keys=array_keys($record);
            scraperwiki::save($keys,$record); 
        }
    }
    
    
}
