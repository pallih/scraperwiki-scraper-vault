<?php

    require 'scraperwiki/simple_html_dom.php';           


function scrapPage($page){
    print ("Scraping page ".$page);

    $url="http://www.geipan.fr/index.php?id=202";


    $fields_string = "&no_cache=1&".
        "tx_geipansearch_pi1%5Bsubmit_form%5D=1&".
        "tx_geipansearch_pi1%5Btexte_resume%5D=&".
        "tx_geipansearch_pi1%5Bdate_debut%5D=&".
        "tx_geipansearch_pi1%5Bdate_fin%5D=&".
        "no_cache=1&".
        "tx_geipansearch_pi1%5Bclasse_cas%5D=tous&".
        "tx_geipansearch_pi1%5Bregion%5D=&".
        "page=".$page."&". 
        "order_by=&".
        "sens=";

    $curl = curl_init($url);
      curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
      curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
      curl_setopt($curl, CURLOPT_MAXREDIRS, 10);
      curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
      curl_setopt($curl, CURLOPT_TIMEOUT, 20); 
      curl_setopt($curl,CURLOPT_POST,11);
      curl_setopt($curl,CURLOPT_POSTFIELDS,$fields_string);
      $html = curl_exec($curl);
      print (curl_error($curl)."\n");
//      print($html);

     $dom = new simple_html_dom();
     $dom->load($html);

     $trs = $dom->find("tr");
     foreach ($trs as $tr){
         if (isset($tr->attr['onclick'])){
             $ID = substr($tr->attr['onclick'], strpos($tr->attr['onclick'], "cas=")+4, 13);
             print($ID."\n");
             $tds = $tr->find("td");
             $title = utf8_encode($tds[0]->plaintext);
             $date = $tds[1]->plaintext;
             $departement = utf8_encode($tds[2]->plaintext);
             $classe = $tds[3]->plaintext;
             $maj = $tds[4]->plaintext;
             $city = substr($title, 0, strpos($title, "(")-1);
             $record = array ('ID' => $ID, 'title' => $title, 
                                'date' => $date, 'departement' => $departement, 
                                'classe' => $classe, 'maj' => $maj, 'city' => $city);
             scraperwiki::save(array('ID', 'maj'), $record); 
         }
     }
}

$s = rand(1,6);
$s = 5;
print ("I will only try to update starting from page ". (($s-1)*10)."\n");

for ($i = (($s-1)*10); $i <= 60; $i++) {
    scrapPage($i);
}

?>
