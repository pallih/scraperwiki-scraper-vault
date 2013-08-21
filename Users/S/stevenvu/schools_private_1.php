<?php
//this script will grab all the schools data.
require 'scraperwiki/simple_html_dom.php';

//Quick and dirty edit to include more columns.


$rowsperpage = 25;
$schoolid = 13876;

$nameindex;
$authorityindex;
$townindex;
$typeindex;
$urnindex;
$establishmentindex;
$laindex;
$ukprnindex;
$phoneindex;
$postcodeindex;
$arraycount;


for($i = 1;$i<2241;$i++){ //2237 pages in total. Set $i to 2 if testing.
    $nameindex = 0;
    $authorityindex = 1;
    $townindex = 2;
    $statusindex = 3;
    $typeindex = 4;
    $urnindex = 5;
    $establishmentindex = 6;
    $laindex = 7;
    $ukprnindex = 8;
    $phoneindex = 9;
    $postcodeindex = 10;
    
    $arraycount = 0;

    //$html = scraperWiki::scrape("http://www.edubase.gov.uk/public/quickSearchResult.xhtml?page=".$i);
    $html = scraperWiki::scrape('http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml;jsessionid=1DF1D2D491E2C6D958DE7BE23CFAC566?page='.$i);
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find("table[class='search_results']") as $data){
        $tds = $data->find("td");

          while($arraycount < $rowsperpage){ 
          
            

            //create a new array for each record on the page, and store everything into it.            
            ${'record'.$arraycount} = array(
                'name' => $tds[$nameindex]->plaintext, 
                'loacal_authority' => $tds[$authorityindex]->plaintext,
                'town' => $tds[$townindex]->plaintext,
                'status' => $tds[$statusindex]->plaintext,
                'type' => $tds[$typeindex]->plaintext,
                'urn' => $tds[$urnindex]->plaintext,
                'establishment' => $tds[$establishmentindex]->plaintext,
                'la' => $tds[$laindex]->plaintext,
                'prn' => $tds[$ukprnindex]->plaintext,
                'telephone' => $tds[$phoneindex]->plaintext,
                'postcode' => $tds[$postcodeindex]->plaintext,
            );
            

           print_r( ${'record'.$arraycount}); //print the array

            //insert all the data into a table.
           scraperwiki::save_sqlite(array("schoolid"),
                array("schoolid"=>$schoolid, 
                        "name"=>${'record'.$arraycount}['name'], 
                        "loacal_authority"=>${'record'.$arraycount}['loacal_authority'], 
                        "town"=>${'record'.$arraycount}['town'], 
                        "status"=>${'record'.$arraycount}['status'], 
                        "type"=>${'record'.$arraycount}['type'],
                        "urn"=>${'record'.$arraycount}['urn'],
                        "establishment"=>${'record'.$arraycount}['establishment'],
                        "la"=>${'record'.$arraycount}['la'],
                        "prn"=>${'record'.$arraycount}['prn'],
                        "telephone"=>${'record'.$arraycount}['telephone'],
                        "postcode"=>${'record'.$arraycount}['postcode'],
                )
            );

           
           //increment all the vars for the loop.
            $nameindex = $nameindex +11;
            $authorityindex = $authorityindex +11;
            $townindex = $townindex +11;
            $statusindex = $statusindex +11;
            $typeindex = $typeindex +11;
            $establishmentindex = $establishmentindex +11;
            $laindex = $typeindex +11;
            $ukprnindex    = $typeindex +11;    
            $phoneindex = $phoneindex +11;
            $postcodeindex = $postcodeindex+11;
        
           $arraycount ++;
           $schoolid++;


        }
    }
}


?>
