<?php
######################################
# Scraper Scuole Italiane (Susanna Martinelli)
######################################

require  'scraperwiki/simple_html_dom.php';





$prov_marche = array("ANCONA","ASCOLI PICENO","MACERATA","PESARO");
$prov_calabria = array("CATANZARO","COSENZA","CROTONE","REGGIO CALABRIA","VIBO VALENTIA");
$prov_toscana = array("AREZZO","FIRENZE","GROSSETO","LIVORNO","LUCCA","MASSA","PISA","PISTOIA","PRATO","SIENA");
$prov_veneto = array("BELLUNO","PADOVA","ROVIGO","TREVISO","VENEZIA","VERONA","VICENZA");
$prov_lombardia = array("BERGAMO","BRESCIA","COMO","CREMONA","LECCO","LODI","MANTOVA","MILANO","PAVIA","SONDRIO","VARESE");
$prov_sardegna = array("CAGLIARI","NUORO","ORISTANO","SASSARI");
$prov_sicilia = array("AGRIGENTO","CALTANISSETTA","CATANIA","ENNA","MESSINA","PALERMO","RAGUSA", "SIRACUSA","TRAPANI");
$prov_puglia = array("BARI","BRINDISI","FOGGIA","LECCE","TARANTO");
$prov_friuliv = array("GORIZIA","PORDENONDE","TRIESTE","UDINE");
$prov_liguria = array("GENOVA","IMPERIA","LA SPEZIA","SAVONA");
$prov_emilia_paranoica = array("BOLOGNA","FERRARA","FORLI'","MODENA","PARMA","PIACENZA","RAVENNA","REGGIO EMILIA","RIMINI");
$prov_campania = array("AVELLINO","BENEVENTO","CASERTA","NAPOLI","SALERNO");
$prov_piemonte = array("ALESSANDRIA","ASTI","BIELLA","CUNEO","NOVARA","TORINO","VERBANO-CUSIO-OSSOLA","VERCELLI");
$prov_lazio = array("FROSINONE","LATINA","RIETI","ROMA","VITERBO");
$prov_abruzzo = array("CHIETI","L'AQUILA","PESCARA","TERAMO");
$prov_molise = array("CAMPOBASSO", "ISERNIA");
$prov_umbria = array("PERUGIA","TERNI");
$prov_trentino = array("TRENTO");
$prov_basilicata = array("MATERA","POTENZA");

$regioni = array( "TOSCANA" => $prov_toscana,
                  "CALABRIA"=> $prov_calabria,
                  "VENETO" => $prov_veneto,
                  "MARCHE" => $prov_marche,
                  "LOMBARDIA" => $prov_lombardia,
                  "SARDEGNA" => $prov_sardegna,
                  "SICILIA" => $prov_sicilia,
                  "PUGLIA" => $prov_puglia,
                  "FRIULI-VENEZIA " => $prov_friuliv,
                  "LIGURIA" => $prov_liguria,
                  "EMILIA ROMAGNA"=>$prov_emilia_paranoica,
                  "CAMPANIA" => $prov_campania,
                  "PIEMONTE" => $prov_piemonte,
                  "LAZIO" => $prov_lazio,
                  "ABRUZZO" => $prov_abruzzo,
                  "MOLISE" => $prov_molise,
                  "UMBRIA" => $prov_umbria,
                  "TRENTINO-ALTO A" => $prov_trentino,
                  "BASILICATA" => $prov_basilicata);

$tipologie=array("CENTRO TERRITORIALE PERMANENTE",
                 "CIRCOLO DIDATTICO",
                 "CORSO SERALE",
                 "ISTITUTO COMPRENSIVO",
                 "ISTITUTO DI ISTRUZIONE SUPERIORE",
                 "SCUOLA DELL'INFANZIA",
                 "SCUOLA PRIMARIA",
                 "SCUOLA SECONDARIA DI I GRADO",
                 "SCUOLA SECONDARIA DI II GRADO");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
  $main_url="http://www.trampi.istruzione.it/ricScu/cerca.do?";
    $last_tipo="";
    $last_provincia="";
    $last_regione="";
    # se non funziona va cambiato in 'scuole_italiane'
    $rows = scraperwiki::getData("scuole_italiane_p4",1,0);
    if (isset($rows)) {
        $last_record = $rows[0];
        #print_r($last_record);
        $last_tipo=$last_record->tipologia;
        $last_tipo = strtoupper(trim($last_tipo));
     
        $last_provincia=$last_record->provincia;
        $last_provincia = strtoupper(trim($last_provincia));
   
        
        $last_regione = $last_record->regione;
        $last_regione = strtoupper(trim($last_regione));
    
         print ("Ultimo record trovato: tipo: ".$last_tipo." regione: ".$last_regione." provincia: ".$last_provincia."\n");
        $found_tipo=false;
        $found_prov=false;
        $found_regione=false;
    } else {
        $found_tipo=true;
        $found_prov=true;
        $found_regione=true;
    }
    #$dom ->clear();
    #unset($dom);
    foreach(array_keys($regioni) as $regione){  
        if (strcmp($regione,$last_regione)==0 || $found_regione){ 
            #echo "regione:".$regione." last_regione: ".$last_regione.strcmp($regione,$last_regione)."\n";
            $found_regione = true;
            foreach($tipologie as $tipo){
                   #echo "tipo:".$tipo." last_tipo: ".$last_tipo.strcmp($tipo,$last_tipo)."\n";
                   if (strcmp($tipo,$last_tipo)==0 || $found_tipo){
                   $found_tipo=true;
                   $provincie = $regioni[$regione];
                foreach($provincie as $prov){
                           # echo "prov:".$prov." last_provincia: ".$last_provincia."\n";
                            if(strcmp($prov,$last_provincia)==0 || $found_prov){
                            $found_prov=true;
                            $url=$main_url."regione=".urlencode($regione)."&provincia=".urlencode($prov)."&comune=&tipologia=".urlencode($tipo)."&denominazione=&codicemecc=&order=DES_NOM";
                                $html = scraperwiki::scrape($url);
                                try {
                                    print $url."\n";
                                    create_dataset2($html);
                                }catch(Exception $e){
                                    echo "Eccezione: ".$e."\n";
                                }
                            }
                
                    }
                }
            }
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
