<?php

# Blank PHP

$html_content = scraperwiki::scrape("https://sede.madrid.es/portal/site/tramites/menuitem.c22ce77143639022396bb9f7ecd08a0c/?vgnextoid=aae537c190180210VgnVCM100000c90da8c0RCRD");

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html_content);


    //foreach ($dom->find('div[class="panelSubs"] ul[class="listContents"] li a') as $dire)
    foreach ($dom->find('div[class="panelSubs"]') as $dire_main)
    {
        $j=0;
        $grupo = $dire_main->find('div[class="destHeadA"]');
        
        foreach ($dom->find('ul[class="listContents"] li a') as $dire)
        {




            if ($dire->plaintext != "Ver todos los trámites")
            {
                $sub_titulo_main = $dire->plaintext;
                
                $dire_main = $dire->href;
            
                $pad_length = strlen($dire_main);
                $pad_string = "https://sede.madrid.es";
        
                $dire_main = str_pad  ($dire_main, ($pad_length + strlen($pad_string)), $pad_string, STR_PAD_LEFT);
        
                $html_dire_main = scraperwiki::scrape($dire_main);
                $html_main = str_get_html($html_dire_main);
    
                //print $sub_titulo_main . "\n";
                //print $dire_main . "\n";
    
                foreach ($html_main->find('div[class="itemTitle"] a') as $dire2)
                {
                    //$sub_titulo_main2 = $dire2->plaintext;
                    
                    $dire_main2 = $dire2->href;
                    
                    $pad_length = strlen($dire_main2);
                    $pad_string = "https://sede.madrid.es";
            
                    $dire_main2 = str_pad  ($dire_main2, ($pad_length + strlen($pad_string)), $pad_string, STR_PAD_LEFT);
            
                    $html_dire_main2 = scraperwiki::scrape($dire_main2);
                    $html_main2 = str_get_html($html_dire_main2);
    
                    //--------- TITULO ----------------------------------------
    
                    $nombre_tramite = $html_main2->find('h3[class="detailTitle"]');
                    //print $titulo . "\n";
                    
                    
                    //--------- ENTRADILLA ------------------------------------
                    
                    $entradilla_tramite = $html_main2->find('div[class="entradilla"] div[class="parrafo"]');
                    
                    
                    
                    
                    //---------- CAMPOS COMUNES ------------------------------
                    
                    $titulo_campos = $html_main2->find('div[class="tabContent"] h4 a');
    
                    //print $titulo_campos[0]->plaintext . "\n";
                    
                    /*$campo[0] = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                    $campo[1] = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                    $campo[2] = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                    $campo[3] = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                    $campo[4] = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');*/
    
                    /*for ($i=0; $i<5; $i++)
                    {
                        $tramitar_text_new[$i] = "NO";
                    }*/
    
                    $campo_como[0]->innertext = " ";
                    $campo_req[0]->innertext = " ";
                    $campo_docu[0]->innertext = " ";
                    $campo_info[0]->innertext = " ";
                    $campo_pago[0]->innertext = " ";
    
                    for ($i=0; $i<5 && ($titulo_campos[$i] != NULL); $i++)
                    {//print "si" . "\n";
                        if($titulo_campos[$i]->id == 'req') 
                        {
                            if($i==0) {$campo_req = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');}
                            if($i==1) {$campo_req = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');}
                            if($i==2) {$campo_req = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');}
                            if($i==3) {$campo_req = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');}
                            if($i==4) {$campo_req = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');}
                            
                        }
                    
                        if ($titulo_campos[$i]->id == 'ins')
                        {
                            if($i==0) $campo_como = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                            if($i==1) $campo_como = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                            if($i==2) $campo_como = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                            if($i==3) $campo_como = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                            if($i==4) $campo_como = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                            
                           
                        }
                        
                        if ($titulo_campos[$i]->id == 'doc')
                        {
                            if($i==0) $campo_docu = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                            if($i==1) $campo_docu = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                            if($i==2) $campo_docu = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                            if($i==3) $campo_docu = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                            if($i==4) $campo_docu = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                         
                        }
                    
                        if ($titulo_campos[$i]->id == 'mas')
                        {
                            if($i==0) $campo_info = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                            if($i==1) $campo_info = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                            if($i==2) $campo_info = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                            if($i==3) $campo_info = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                            if($i==4) $campo_info = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                      
                
                        }
                        
                        if ($titulo_campos[$i]->id == 'dat')
                        {
                            if($i==0) $campo_pago = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                            if($i==1) $campo_pago = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                            if($i==2) $campo_pago = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                            if($i==3) $campo_pago = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                            if($i==4) $campo_pago = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                            
                        }
                    
                    }
                    
                    
                    
                    //scraperwiki::save(array('Titulo'), $datos);
                    
                    
                    //------- FORMAS DE TRAMITAR ----------------------------
                    
                    $tramitar_tipo = $html_main2->find('div[class="ficha tramite"] h5');
                    $tramitar_text = $html_main2->find('div[class="ficha tramite"] ul[class="tramites"]');
                    
                    
                    for ($i=0; $i<6; $i++)
                    {
                        $tramitar_text_new[$i] = " ";
                    }
                    
                    for ($i=0; $i<6 && $tramitar_tipo[$i] != NULL; $i++)
                    {
                        if ($tramitar_tipo[$i]->plaintext == "Presencial")
                        {
                            $tramitar_text_new[0] = $tramitar_text[$i]->innertext;
                            
                        }
                    
                        if ($tramitar_tipo[$i]->plaintext == "En línea")
                        {
                            $tramitar_text_new[1] = $tramitar_text[$i]->innertext;
                            
                        }
                        
                        if ($tramitar_tipo[$i]->plaintext == "Correo electrónico")
                        {
                            $tramitar_text_new[2] = $tramitar_text[$i]->innertext;
                            
                        }
                    
                        if ($tramitar_tipo[$i]->plaintext == "Teléfono")
                        {
                            $tramitar_text_new[3] = $tramitar_text[$i]->innertext;
                            
                        }
                        
                        if ($tramitar_tipo[$i]->plaintext == "Fax")
                        {
                            $tramitar_text_new[4] = $tramitar_text[$i]->innertext;
                            
                        }
                    
                        if ($tramitar_tipo[$i]->plaintext == "Correo postal")
                        {
                            $tramitar_text_new[5] = $tramitar_text[$i]->innertext;
                            
                        }
                    }
                    
                        
                    //----------- DESCARGAR IMPRESOS -----------------------
                    
                    $descargar_documento = $html_main2->find('span[class="saveResultAction ftr"] a');
    
                    if ($descargar_documento != NULL)
                    {
                        $descargar_documento_dire = $descargar_documento[0]->href;
                        
                        $pad_length = strlen($descargar_documento_dire);
                        $pad_string = "https://sede.madrid.es";
                        
                        $descargar_documento_dire = str_pad($descargar_documento_dire, ($pad_length + strlen($pad_string)), $pad_string, STR_PAD_LEFT);
                    } else $descargar_documento_dire = " ";
                    
                    //$datos = array( 'Tema' => $sub_titulo_main, 'Subtema' => $sub_titulo_main2, 'Titulo' => $nombre_tramite[0]->plaintext, 'Entradilla' => $entradilla_tramite[0]->innertext, 'Requisitos' => $campo0[0]->innertext, 'Cómo realizar el trámite' => $campo1[0]->innertext, 'Documentación' => $campo2[0]->innertext, 'Más Información' => $campo3[0]->innertext, 'Pago' => $campo4[0]->innertext, 'Presencial' => $tramitar_text_new[0], 'En línea' => $tramitar_text_new[1], 'Email' => $tramitar_text_new[2], 'Teléfono' => $tramitar_text_new[3], 'Fax' => $tramitar_text_new[4], 'Correo Postal' => $tramitar_text_new[5], 'Descarga Documentos' => $descargar_documento_dire );
    
    $datos = array( 'Grupo' => $grupo[$j]->plaintext, 'Tema' => $sub_titulo_main, 'Titulo' => $nombre_tramite[0]->plaintext, 'Entradilla' => $entradilla_tramite[0]->innertext, 'Requisitos' => $campo_req[0]->innertext, 'Cómo realizar el trámite' => $campo_como[0]->innertext, 'Documentación' => $campo_docu[0]->innertext, 'Más Información' => $campo_info[0]->innertext, 'Pago' => $campo_pago[0]->innertext, 'Presencial' => $tramitar_text_new[0], 'En línea' => $tramitar_text_new[1], 'Email' => $tramitar_text_new[2], 'Teléfono' => $tramitar_text_new[3], 'Fax' => $tramitar_text_new[4], 'Correo Postal' => $tramitar_text_new[5], 'Descarga Documentos' => $descargar_documento_dire );
                    
                    //scraperwiki::save(array('Titulo'), $datos);
                    scraperwiki::save(array('Grupo','Tema','Titulo'), $datos);
                    
                                
               }
                    
     }else $j++;
                        
   }                     
                        
}

    



?>
