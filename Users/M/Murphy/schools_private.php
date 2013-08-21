<?php
//this script will grab all the schools data.
require 'scraperwiki/simple_html_dom.php';      


$rowsperpage = 25;
$schoolid = 13876;

$nameindex;
$authorityindex;
$townindex;
$typeindex;
$phoneindex;
$postcodeindex;
$arraycount;


for($i = 555;$i<2237;$i++){ //2237 pages in total. Set $i to 2 if testing.

    $nameindex = 0;
    $authorityindex = 1;
    $townindex = 2;
    $typeindex = 3;
    $phoneindex = 4;
    $postcodeindex = 5;
    
    $arraycount = 0;

    //$html = scraperWiki::scrape("http://www.edubase.gov.uk/public/quickSearchResult.xhtml?page=".$i);
    $html = scraperWiki::scrape('http://www.edubase.gov.uk/public/quickSearchResult.xhtml;jsessionid=609C43CC7C30E932FCEA8D5D95B99893?page='.$i);
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find("table[class='search_results']") as $data){
        $tds = $data->find("td");

          while($arraycount < $rowsperpage){ 
          
            //grab a postcode and store the longitude and lattitude into an array.
            $postcode = $tds[$postcodeindex]->plaintext;
            $lat_lng = scraperwiki::gb_postcode_to_latlng($postcode);
            

            //create a new array for each record on the page, and store everything into it.            
            ${'record'.$arraycount} = array(
                'name' => $tds[$nameindex]->plaintext, 
                'loacal_authority' => $tds[$authorityindex]->plaintext,
                'town' => $tds[$townindex]->plaintext,
                'type' => $tds[$typeindex]->plaintext,
                'telephone' => $tds[$phoneindex]->plaintext,
                'postcode' => $tds[$postcodeindex]->plaintext,
                'lat' => $lat_lng[0],
                'lng' => $lat_lng[1]
            );
            

           print_r( ${'record'.$arraycount}); //print the array

            //insert all the data into a table.
           scraperwiki::save_sqlite(array("schoolid"),
                array("schoolid"=>$schoolid, 
                        "name"=>${'record'.$arraycount}['name'], 
                        "loacal_authority"=>${'record'.$arraycount}['loacal_authority'], 
                        "town"=>${'record'.$arraycount}['town'], 
                        "type"=>${'record'.$arraycount}['type'], 
                        "telephone"=>${'record'.$arraycount}['telephone'],
                        "postcode"=>${'record'.$arraycount}['postcode'],
                        "lat"=>${'record'.$arraycount}['lat'],
                        "lng"=>${'record'.$arraycount}['lng']
                )
            );

           
           //increment all the vars for the loop.
            $nameindex = $nameindex +6;
            $authorityindex = $authorityindex +6;
            $townindex = $townindex +6;
            $typeindex = $typeindex +6;
            $phoneindex = $phoneindex +6;
            $postcodeindex = $postcodeindex+6;
        
           $arraycount ++;
           $schoolid++;


        }
    }
}


?>
