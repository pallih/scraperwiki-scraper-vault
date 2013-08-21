<?php
require  'scraperwiki/simple_html_dom.php';

$inis = ini_get_all();

print_r($inis);

$url="http://www.trampi.istruzione.it/ricScu/cerca.do?regione=PIEMONTE&provincia=TORINO&comune=TORINO&tipologia=&denominazione=&codicemecc=&order=DES_NOM";
$url2="http://www.trampi.istruzione.it/ricScu/cerca.do?regione=CALABRIA&provincia=COSENZA&comune=&tipologia=&denominazione=&codicemecc=&order=DES_NOM";
$url3="http://www.trampi.istruzione.it/ricScu/cerca.do?regione=LOMBARDIA&provincia=PAVIA&comune=&tipologia=&denominazione=&codicemecc=&order=DES_NOM";
$url4="http://www.trampi.istruzione.it/ricScu/cerca.do?regione=CAMPANIA&provincia=AVELLINO&comune=&tipologia=ISTITUTO%20DI%20ISTRUZIONE%20SUPERIORE&denominazione=&codicemecc=&order=DES_NOM";
$url4="http://www.trampi.istruzione.it/ricScu/cerca.do?regione=VENETO&provincia=VICENZA&comune=&tipologia=CORSO%20SERALE&denominazione=&codicemecc=&order=DES_NOM";
$url5="http://www.trampi.istruzione.it/ricScu/cerca.do?regione=LOMBARDIA&provincia=BRESCIA&comune=&tipologia=ISTITUTO%20COMPRENSIVO&denominazione=&codicemecc=&order=DES_NOM";
$html = scraperwiki::scrape($url5);
$i=0;
$dom = new simple_html_dom();
$dom->set_callback('my_callback');
#$dom->load($html);
$res="";
scraperwiki::save(array('allow_call_time_pass_reference'), $inis);
#function my_callback($d){
    foreach($dom->find('table',2)->children() as $data)
    {  
        if ($data != null)  $res = trim($data->plaintext);
    
        if ( ($i>0) && (strlen($res)>0) ){
            # Store data in the datastore
            
            #print $res;
            $res = str_replace('&#39;',"'",$res);
            #splitto i risultati in un array
            $array_result = split('&nbsp;',$res);
       
            #print_r($res);
            #echo $denom;
               
            # Mi salvo il codiceMPI 
            $codMPI=trim($array_result[1]);
            $url_MPI="http://www.trampi.istruzione.it/ricScu/dettaglio.do?cod=".$codMPI;
            print $url_MPI."\n";
            $html = scraperwiki::scrape($url_MPI);
            $dom_mpi = new simple_html_dom();
            $dom_mpi->load($html);
            $tel="";
            $fax="";
            $email="";
            $web="";
            $indS="";
            foreach($dom_mpi->find('table[cellspacing=1] tr') as $data_mpi){
               $res=$data_mpi->plaintext."\n";
               $values = split(':',$res);
               #print_r($values);
               if(strlen($values[0])>0){
                    
                    if(stripos($values[0], 'tel')!==false){
                         $tel=trim($values[1]);
                         print "tel:".$tel."\t";
                    }
                    if(stripos($values[0], 'fax')!==false){
                         $fax=trim($values[1]);
                        print "fax:".$fax."\t";
                    }
                    if(stripos($values[0], 'e-mail')!==false) {
                        $email=trim($values[1]);
                        print "email:".$email."\t";
                    }
                    if(stripos($values[0], 'web')!==false){
                        if(strlen($values[2])>0) $web=trim($values[1].":".$values[2]);
                        print "web:".$web."\t";
                    }
                    if(stripos($values[0], 'studio')!==false){
                        $indS = str_replace('</td>','',$values[1]);
                        $indS = str_replace('</tr>','',$indS);
                        $indS = str_replace(array("\r","\t","\n"),'',$indS);
                        
                        $indS=trim($indS);
                        print "ind studio:".$indS."\n";
                    }
               }
               unset($values);
            }
            $dom_mpi->clear();
            unset($dom_mpi);
     
           $dataset = array 
                    (
                        'denominazione' => trim(html_entity_decode($array_result[0])),
                        'codiceMPI' => trim($array_result[1]),
                        'tipologia' => trim(html_entity_decode($array_result[2])), 
                        'tipologiaIIgrado' => trim(html_entity_decode($array_result[3])), 
                        'descrizione' => trim(html_entity_decode($array_result[4])),
                        'indirizzo' => trim(html_entity_decode($array_result[5])),
                        'località' => trim(html_entity_decode($array_result[6])),
                        'cap' =>trim($array_result[7]),
                        'comune' => trim(html_entity_decode($array_result[8])),
                        'provincia' => trim(html_entity_decode($array_result[9])),
                        'regione' => trim(html_entity_decode($array_result[10])),
                        'codIstitutoComprensivo' => trim(html_entity_decode($array_result[11])),
                        'telefono' => $tel,
                        'fax' => $fax,
                        'email' => $email,
                        'web' => $web,
                        'IndirizziStudio' =>trim(html_entity_decode($indS))
            );
           
          
           #print_r($dataset);
           #scraperwiki::save(array('data'), array('data' => $data->plaintext));
           if (strlen($dataset['denominazione']) > 1){
            scraperwiki::save(array('denominazione','codiceMPI'), $dataset);
          }
           unset($dataset);
           unset($res);
           unset($tel);
           unset($fax);
           unset($email);
           unset($web);
           unset($indS);
        }
           $i=$i+1;
    }
              #dealloco il dom sennò schianta
              $dom->clear();
              unset($dom);
   #}       
        
?>
