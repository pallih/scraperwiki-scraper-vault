<?php
######################################
# Scraper Scuole Italiane (Susanna Martinelli)
######################################

require  'scraperwiki/simple_html_dom.php';



$regioni = array("UMBRIA",
                 "ABRUZZO",
                 "BASILICATA",
                 "TRENTINO-ALTO%20A",
                 "MOLISE");



$tipologie=array("CENTRO%20TERRITORIALE%20PERMANENTE",
                 "CIRCOLO%20DIDATTICO",
                 "CORSO%20SERALE",
                 "ISTITUTO%20COMPRENSIVO",
                 "ISTITUTO%20DI%20ISTRUZIONE%20SUPERIORE",
                 "SCUOLA%20DELL'INFANZIA",
                 "SCUOLA%20PRIMARIA",
                 "SCUOLA%20SECONDARIA%20DI%20I%20GRADO",
                 "SCUOLA%20SECONDARIA%20DI%20II%20GRADO");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$main_url="http://www.trampi.istruzione.it/ricScu/cerca.do?";   
 
   
      
      #$dom ->clear();
      #unset($dom);
foreach($regioni as $regione){
      foreach($tipologie as $tipo){
      #foreach($prov_lazio as $prov){
                  $url=$main_url."regione=".$regione."&provincia=&comune=&tipologia=".$tipo."&denominazione=&codicemecc=&order=DES_NOM";
                      print $url."\n";
                      $html = scraperwiki::scrape($url);
                      try {
                          create_dataset2($html);
                      }catch(Exception $e){
                          echo "Eccezione: ".$e."\n";
                      }
      
      #}
  }
    
}
  
  
  function create_dataset2($html){
      $i=0;
      $dom = new simple_html_dom();
      $dom->load($html);
      usleep(200);
      #controllo se esiste veramente prima di entrare
      $table = $dom->find('table',2);
      if (isset($table)) {
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
                  #print $url_MPI."\n";
                  $html = scraperwiki::scrape($url_MPI);
                  $dom_mpi = new simple_html_dom();
                  $dom_mpi->load($html);
                  $tel="";
                  $fax="";
                  $email="";
                  $web="";
                  $indS="";
                  $tr= $dom_mpi->find('table[cellspacing=1] tr');
                  if (isset($tr)){
                      foreach($dom_mpi->find('table[cellspacing=1] tr') as $data_mpi){
                         $res=$data_mpi->plaintext."\n";
                         $values = split(':',$res);
                         #print_r($values);
                          
                         if(strlen($values[0])>0){
                            if(stripos($values[0], 'tel')!==false){
                                   $tel=trim($values[1]);
                                   #print "tel:".$tel."\t";
                              }else if(stripos($values[0], 'fax')!==false){
                                       $fax=trim($values[1]);
                                      #print "fax:".$fax."\t";
                                  } else if(stripos($values[0], 'e-mail')!==false) {
                                          $email=trim($values[1]);
                                         }else if( (stripos($values[0], 'web')!==false)){
                                                   while (list($key, $value) = each($values)) {
                                                            if($key=2) {
                                                                      $web=$values[1].":".$value;
                                                             }
          
                                                              
                                                   }
                                                   } else if(stripos($values[0], 'studio')!==false){
                                                              $indS = str_replace('</td>','',$values[1]);
                                                              $indS = str_replace('</tr>','',$indS);
                                                              $indS = str_replace(array("\r","\t","\n"),'',$indS);
                                                              $indS=trim($indS);
                                                              #print "ind studio:".$indS."\n";
                                                     }
                         #echo $web."\n";
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
      }
  }
      
  
  
      
  
  ?>