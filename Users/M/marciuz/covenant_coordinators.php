<?php
require 'scraperwiki/simple_html_dom.php';           

for($p=1;$p<6;$p++){

    $html = scraperWiki::scrape("http://www.eumayors.eu/about/covenant-coordinators_en.html?q=&country_search=&signatories=&start=$p");
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find(".spip tr") as $data){

        $record=array('Covenant_Coordinators'=>'', 
                    'Countries'=>'', 
                    'Signatories'=>'', 'Contry_full'=>'', 'Website'=>'','Main_contact'=>'','Position'=>'','Email'=>'');


        $tds = $data->find("td");
    
        if(isset($tds[0]->plaintext)){
    
            $record = array(
                'Covenant_Coordinators' => $tds[0]->plaintext, 
                'Countries' => $tds[1]->plaintext,
                'Signatories' => intval($tds[2]->plaintext)
            );
        
            $link = $tds[0]->find("a");
            $html_dett = scraperWiki::scrape("http://www.eumayors.eu/".$link[0]->href);
            $dom_dett = new simple_html_dom();
            $dom_dett->load($html_dett);
            $data2=$dom_dett->find("#profile_overview");

            if(is_object($data2[0])){
                $tds_dett = $data2[0]->find("td");
            
                   // for($i=0;$i<count($tds_dett);$i++) print $i." -> ".$tds_dett[$i]->plaintext."\n";
                        
                $record['Country_full']= (isset($tds_dett[0]->plaintext)) ? $tds_dett[0]->plaintext : '';
                $record['Website']= (isset($tds_dett[1]->plaintext)) ? $tds_dett[1]->plaintext : '';
                $record['Main_contact']= (isset($tds_dett[2]->plaintext)) ? $tds_dett[2]->plaintext : '';
                $record['Position']= (isset($tds_dett[3]->plaintext)) ? $tds_dett[3]->plaintext : '';
                $record['Email']= (isset($tds_dett[4]->plaintext)) ? $tds_dett[4]->plaintext : '';
            }
    
        
            scraperwiki::save(array('Covenant_Coordinators', 'Countries', 'Signatories', 'Contry_full', 'Website','Main_contact','Position','Email'),$record); 
        
        }
    }

}

