<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';



$html_content = scraperwiki::scrape("https://sede.madrid.es/portal/site/tramites/menuitem.d3089948cb18b1bb68d8a521ecd08a0c/?vgnextoid=4e24424d52a61110VgnVCM2000000c205a0aRCRD&vgnextchannel=b10737c190180210VgnVCM100000c90da8c0RCRD");

//$html_content = scraperwiki::scrape("https://sede.madrid.es/portal/site/tramites/menuitem.d3089948cb18b1bb68d8a521ecd08a0c/?vgnextoid=2d37c943a3028210VgnVCM2000000c205a0aRCRD&vgnextchannel=385737c190180210VgnVCM100000c90da8c0RCRD");

/*$html_content = scraperwiki::scrape("https://sede.madrid.es/portal/site/tramites/menuitem.d3089948cb18b1bb68d8a521ecd08a0c/?vgnextoid=4e24424d52a61110VgnVCM2000000c205a0aRCRD&vgnextchannel=b10737c190180210VgnVCM100000c90da8c0RCRD");*/

$html_main2 = str_get_html($html_content);

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

                $campo_como[0]->plaintext = "";
                $campo_req[0]->plaintext = "";
                $campo_docu[0]->plaintext = "";
                $campo_info[0]->plaintext = "";
                $campo_pago[0]->plaintext = "";

                for ($i=0; $i<5 && ($titulo_campos[$i] != NULL); $i++)
                {print "si" . "\n";
                    if($titulo_campos[$i]->id == 'req')
                    {
                        if($i==0) {$campo_req = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');}
                        if($i==1) {$campo_req = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');}
                        if($i==2) {$campo_req = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');}
                        if($i==3) {$campo_req = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');}
                        if($i==4) {$campo_req = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');}
print "req" . "\n";
                        //$campo_req = $campo[$i];
                        
                    }//else $campo_req = "NO";
                
                    if ($titulo_campos[$i]->id == 'ins')
                    {
                        if($i==0) $campo_como = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                        if($i==1) $campo_como = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                        if($i==2) $campo_como = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                        if($i==3) $campo_como = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                        if($i==4) $campo_como = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                        //$campos_como = $campo[$i];
print "como" . "\n";                        
                    }//else $campo_como[0]->plaintext = "NO";
                    
                    if ($titulo_campos[$i]->id == 'doc')
                    {
                        if($i==0) $campo_docu = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                        if($i==1) $campo_docu = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                        if($i==2) $campo_docu = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                        if($i==3) $campo_docu = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                        if($i==4) $campo_docu = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                        //$campos_docu = $campo[$i];
print "doc" . "\n";                        
                    }//elseif ($campo_docu[0]->plaintext = "NO");
                
                    if ($titulo_campos[$i]->id == 'mas')
                    {
                        if($i==0) $campo_info = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                        if($i==1) $campo_info = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                        if($i==2) $campo_info = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                        if($i==3) $campo_info = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                        if($i==4) $campo_info = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                       //$campos_info = $campo[$i];
print "info" . "\n";                        
                    }//else $campo_info[0]->plaintext = "NO";
                    
                    if ($titulo_campos[$i]->id == 'dat')
                    {
                        if($i==0) $campo_pago = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                        if($i==1) $campo_pago = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                        if($i==2) $campo_pago = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                        if($i==3) $campo_pago = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                        if($i==4) $campo_pago = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                        //$campos_pago = $campo[$i];
print "pago" . "\n";                        
                    }//else $campo_pago[0]->plaintext = "NO";
                
                }
                
                
                
                //scraperwiki::save(array('Titulo'), $datos);
                
                
                //------- FORMAS DE TRAMITAR ----------------------------
                
                $tramitar_tipo = $html_main2->find('div[class="ficha tramite"] h5');
                $tramitar_text = $html_main2->find('div[class="ficha tramite"] ul[class="tramites"]');
                
                
                for ($i=0; $i<6; $i++)
                {
                    $tramitar_text_new[$i] = "";
                }
                
                for ($i=0; $i<6 && $tramitar_tipo[$i] != NULL; $i++)
                {
                    if ($tramitar_tipo[$i]->plaintext == "Presencial")
                    {
                        $tramitar_text_new[0] = $tramitar_text[$i]->plaintext;
                        
                    }
                
                    if ($tramitar_tipo[$i]->plaintext == "En línea")
                    {
                        $tramitar_text_new[1] = $tramitar_text[$i]->plaintext;
                        
                    }
                    
                    if ($tramitar_tipo[$i]->plaintext == "Correo electrónico")
                    {
                        $tramitar_text_new[2] = $tramitar_text[$i]->plaintext;
                        
                    }
                
                    if ($tramitar_tipo[$i]->plaintext == "Teléfono")
                    {
                        $tramitar_text_new[3] = $tramitar_text[$i]->plaintext;
                        
                    }
                    
                    if ($tramitar_tipo[$i]->plaintext == "Fax")
                    {
                        $tramitar_text_new[4] = $tramitar_text[$i]->plaintext;
                        
                    }
                
                    if ($tramitar_tipo[$i]->plaintext == "Correo postal")
                    {
                        $tramitar_text_new[5] = $tramitar_text[$i]->plaintext;
                        
                    }
                }
                
                    
                //----------- DESCARGAR IMPRESOS -----------------------
                
                $descargar_documento = $html_main2->find('span[class="saveResultAction ftr"] a');

                if ($descargar_documento != NULL)
                {
                    $descargar_documento_dire = $descargar_documento[0]->href;
                    
                    $pad_length = strlen($descargar_documento_dire);
                    $pad_string = "https://sede.madrid.es";
                    
                    $descargar_documento_dire = str_pad  ($descargar_documento_dire, ($pad_length + strlen($pad_string)), $pad_string, STR_PAD_LEFT);
                } else $descargar_documento == "";

$datos = array( 'Titulo' => $nombre_tramite[0]->plaintext, 'Entradilla' => $entradilla_tramite[0]->innertext, 'Requisitos' => $campo_req[0]->plaintext, 'Cómo realizar el trámite' => $campo_como[0]->plaintext, 'Documentación' => $campo_docu[0]->plaintext, 'Más Información' => $campo_info[0]->plaintext, 'Pago' => $campo_pago[0]->plaintext, 'Presencial' => $tramitar_text_new[0], 'En línea' => $tramitar_text_new[1], 'Email' => $tramitar_text_new[2], 'Teléfono' => $tramitar_text_new[3], 'Fax' => $tramitar_text_new[4], 'Correo Postal' => $tramitar_text_new[5], 'Descarga Documentos' => $descargar_documento_dire );
                
                scraperwiki::save(array('Titulo'), $datos);

?>
<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';



$html_content = scraperwiki::scrape("https://sede.madrid.es/portal/site/tramites/menuitem.d3089948cb18b1bb68d8a521ecd08a0c/?vgnextoid=4e24424d52a61110VgnVCM2000000c205a0aRCRD&vgnextchannel=b10737c190180210VgnVCM100000c90da8c0RCRD");

//$html_content = scraperwiki::scrape("https://sede.madrid.es/portal/site/tramites/menuitem.d3089948cb18b1bb68d8a521ecd08a0c/?vgnextoid=2d37c943a3028210VgnVCM2000000c205a0aRCRD&vgnextchannel=385737c190180210VgnVCM100000c90da8c0RCRD");

/*$html_content = scraperwiki::scrape("https://sede.madrid.es/portal/site/tramites/menuitem.d3089948cb18b1bb68d8a521ecd08a0c/?vgnextoid=4e24424d52a61110VgnVCM2000000c205a0aRCRD&vgnextchannel=b10737c190180210VgnVCM100000c90da8c0RCRD");*/

$html_main2 = str_get_html($html_content);

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

                $campo_como[0]->plaintext = "";
                $campo_req[0]->plaintext = "";
                $campo_docu[0]->plaintext = "";
                $campo_info[0]->plaintext = "";
                $campo_pago[0]->plaintext = "";

                for ($i=0; $i<5 && ($titulo_campos[$i] != NULL); $i++)
                {print "si" . "\n";
                    if($titulo_campos[$i]->id == 'req')
                    {
                        if($i==0) {$campo_req = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');}
                        if($i==1) {$campo_req = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');}
                        if($i==2) {$campo_req = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');}
                        if($i==3) {$campo_req = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');}
                        if($i==4) {$campo_req = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');}
print "req" . "\n";
                        //$campo_req = $campo[$i];
                        
                    }//else $campo_req = "NO";
                
                    if ($titulo_campos[$i]->id == 'ins')
                    {
                        if($i==0) $campo_como = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                        if($i==1) $campo_como = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                        if($i==2) $campo_como = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                        if($i==3) $campo_como = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                        if($i==4) $campo_como = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                        //$campos_como = $campo[$i];
print "como" . "\n";                        
                    }//else $campo_como[0]->plaintext = "NO";
                    
                    if ($titulo_campos[$i]->id == 'doc')
                    {
                        if($i==0) $campo_docu = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                        if($i==1) $campo_docu = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                        if($i==2) $campo_docu = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                        if($i==3) $campo_docu = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                        if($i==4) $campo_docu = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                        //$campos_docu = $campo[$i];
print "doc" . "\n";                        
                    }//elseif ($campo_docu[0]->plaintext = "NO");
                
                    if ($titulo_campos[$i]->id == 'mas')
                    {
                        if($i==0) $campo_info = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                        if($i==1) $campo_info = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                        if($i==2) $campo_info = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                        if($i==3) $campo_info = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                        if($i==4) $campo_info = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                       //$campos_info = $campo[$i];
print "info" . "\n";                        
                    }//else $campo_info[0]->plaintext = "NO";
                    
                    if ($titulo_campos[$i]->id == 'dat')
                    {
                        if($i==0) $campo_pago = $html_main2->find('div[id="tabContent_0"] div[class="parrafo"]');
                        if($i==1) $campo_pago = $html_main2->find('div[id="tabContent_1"] div[class="parrafo"]');
                        if($i==2) $campo_pago = $html_main2->find('div[id="tabContent_2"] div[class="parrafo"]');
                        if($i==3) $campo_pago = $html_main2->find('div[id="tabContent_3"] div[class="parrafo"]');
                        if($i==4) $campo_pago = $html_main2->find('div[id="tabContent_4"] div[class="parrafo"]');
                        //$campos_pago = $campo[$i];
print "pago" . "\n";                        
                    }//else $campo_pago[0]->plaintext = "NO";
                
                }
                
                
                
                //scraperwiki::save(array('Titulo'), $datos);
                
                
                //------- FORMAS DE TRAMITAR ----------------------------
                
                $tramitar_tipo = $html_main2->find('div[class="ficha tramite"] h5');
                $tramitar_text = $html_main2->find('div[class="ficha tramite"] ul[class="tramites"]');
                
                
                for ($i=0; $i<6; $i++)
                {
                    $tramitar_text_new[$i] = "";
                }
                
                for ($i=0; $i<6 && $tramitar_tipo[$i] != NULL; $i++)
                {
                    if ($tramitar_tipo[$i]->plaintext == "Presencial")
                    {
                        $tramitar_text_new[0] = $tramitar_text[$i]->plaintext;
                        
                    }
                
                    if ($tramitar_tipo[$i]->plaintext == "En línea")
                    {
                        $tramitar_text_new[1] = $tramitar_text[$i]->plaintext;
                        
                    }
                    
                    if ($tramitar_tipo[$i]->plaintext == "Correo electrónico")
                    {
                        $tramitar_text_new[2] = $tramitar_text[$i]->plaintext;
                        
                    }
                
                    if ($tramitar_tipo[$i]->plaintext == "Teléfono")
                    {
                        $tramitar_text_new[3] = $tramitar_text[$i]->plaintext;
                        
                    }
                    
                    if ($tramitar_tipo[$i]->plaintext == "Fax")
                    {
                        $tramitar_text_new[4] = $tramitar_text[$i]->plaintext;
                        
                    }
                
                    if ($tramitar_tipo[$i]->plaintext == "Correo postal")
                    {
                        $tramitar_text_new[5] = $tramitar_text[$i]->plaintext;
                        
                    }
                }
                
                    
                //----------- DESCARGAR IMPRESOS -----------------------
                
                $descargar_documento = $html_main2->find('span[class="saveResultAction ftr"] a');

                if ($descargar_documento != NULL)
                {
                    $descargar_documento_dire = $descargar_documento[0]->href;
                    
                    $pad_length = strlen($descargar_documento_dire);
                    $pad_string = "https://sede.madrid.es";
                    
                    $descargar_documento_dire = str_pad  ($descargar_documento_dire, ($pad_length + strlen($pad_string)), $pad_string, STR_PAD_LEFT);
                } else $descargar_documento == "";

$datos = array( 'Titulo' => $nombre_tramite[0]->plaintext, 'Entradilla' => $entradilla_tramite[0]->innertext, 'Requisitos' => $campo_req[0]->plaintext, 'Cómo realizar el trámite' => $campo_como[0]->plaintext, 'Documentación' => $campo_docu[0]->plaintext, 'Más Información' => $campo_info[0]->plaintext, 'Pago' => $campo_pago[0]->plaintext, 'Presencial' => $tramitar_text_new[0], 'En línea' => $tramitar_text_new[1], 'Email' => $tramitar_text_new[2], 'Teléfono' => $tramitar_text_new[3], 'Fax' => $tramitar_text_new[4], 'Correo Postal' => $tramitar_text_new[5], 'Descarga Documentos' => $descargar_documento_dire );
                
                scraperwiki::save(array('Titulo'), $datos);

?>
