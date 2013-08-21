<?php
function cleanString($var, $strip_tag = ''){
    if ($strip_tag != '') $var = strip_tags($var);
    $var = str_replace('\n', '', $var);
    $var = str_replace('\r', '', $var);
    $var = str_replace('\t', '', $var);
    $var = str_replace('\s', '', $var);
    $var = strtolower($var);
    $var = trim($var);
    return $var;
}

//scraperwiki::sqliteexecute("create table eventi (`url` string, `category` string, `title` string, `sub_title` string, `date_start` string, `date_end` string, `event_in` string, `info_email` string, `info_url` string, `info_number` string, `html_description_block` text)");  

$baseUrl = 'http://www.eventiesagre.it';
$fromPage = 0;
$toPage = 5;

require ('scraperwiki/simple_html_dom.php');

for($ii = $fromPage; $ii <= $toPage; ++$ii){
        
        $urlList = '/pagine/Eventi/sez/mesi/Trentino+Alto+Adige/prov/cit/intit/rilib/864-'.$ii.'-data-DESC-nav.htm';
        $html = file_get_html($baseUrl.$urlList);
        foreach($html->find('tr[class=elenco1 vevent]') as $tr){
        
            $a = $tr->find('a', 0);
            if(!empty($a->href)) $arrLink[] = $a->href;
        
        }
        unset($html, $tr, $a);
        $i = 0;
        foreach ($arrLink as $urlPage){
            
            // url evento
            $records[$i]['url'] = $baseUrl.$urlPage;                                        
        
            $html = file_get_html($baseUrl.$urlPage);
            if (is_object($html)){
                $content = $html->find('div.vevent', 0);
                $category = $content->find('div.category', 0);
                $categoria = str_replace('Eventi', '', $category);
                $categoria = cleanString($categoria, '1');

                // categoria
                $records[$i]['category'] = $categoria;                                          
            
                $block_info = $category->parent();
            
                $h1 = $block_info->find('h1', 0);
                $title = $h1->find('span.titolo', 0);
                $sub_title =  $h1->find('span.testoxxsmall', 0);
            
                // titolo
                $records[$i]['title'] = ($title)? cleanString($title, '1') : 'np';              
                
                // sotto titolo
                $records[$i]['sub_title'] = ($sub_title)? cleanString($sub_title, '1') : 'np';  
            
                $date_start = $block_info->find('span.dtstart', 0);

                // data e ora inizio
                $records[$i]['date_start'] = ($date_start)? cleanString($date_start->outertext,'1') : '';
                $date_end = $block_info->find('span.dtend', 0);
                
                // data e ora fine
                $records[$i]['date_end'] = ($date_end)? cleanString($date_end->outertext, '1') : '';    
            
                $where = $block_info->find('div.locality', 0);
                // dove
                $records[$i]['event_in'] = cleanString($where, '1');
            
                if (preg_match_all("/[a-z0-9]+([_\\.-][a-z0-9]+)*@([a-z0-9]+([\.-][a-z0-9]+)*)+\\.[a-z]{2,}/i", $block_info, $matches)){
                
                    if  ($matches[0][0] != 'segnalazione@eventiesagre.it' && $matches[0][0] != '' ) $info_email = $matches[0][0];
                    else if ($matches[0][0] == 'segnalazione@eventiesagre.it' and $matches[0][1] != '' and $matches[0][1] != 'segnalazione@eventiesagre.it') $info_email = $matches[0][1];
                    else $info_email = '';
                
                // email info contatti
                    $records[$i]['info_email'] = $info_email;                                               
                }
            
                $div_url_img = $block_info->find('img[alt=Sito Web Esterno]', 0);
                if ($div_url_img){
                    $div_url = $div_url_img->parent();
                    $info_url = $div_url->find('a', 0)->href;
                }
                else{
                    $info_url = '';
                }

                // url informazioni
                $records[$i]['info_url'] = $info_url;                                                   
            
                $tr_tel_img = $block_info->find('img[src=/template/originalBlu/images/comuni/info - i.gif]', 0);
            
                if (!empty($tr_tel_img)){
            
                    $tr_tel_fax = str_replace($tr_tel_img, '', $tr_tel_img->parent()->parent());
                    
                    // numeri di telefono o fax informazioni
                    $records[$i]['info_number'] = trim(strip_tags($tr_tel_fax));                        
            
                }
                else $records[$i]['info_number'] = '';
               
                $content_description = $content->find('div.description', 0);
            
                // blocco contenente l'articolo compreso il markup
                $records[$i]['html_description_block'] = $content_description->innertext(); 
                 
                // sul testo possono essere applicati molti altri filtri come per prendere file pdf di informazioni, testo descrittivo, immagini...                            
            
                //foreach ($content_description->find('img') as $image){
            
                //    $description = str_replace($image, '', $content_description);
                //    $records[$i]['image'] .= $baseUrl.$image->src.' ';                                  // immagini presenti nella descrizione
            
                //}
              
            }
            else{
            $records[$i] = '';
            } 
            $i++;
        }
        
        
        
        foreach($records as $record){
        $valori = array();
        $chiavi = array();
        //$chiaviStringa = ""; 
        //$valoriStringa ="";

            if ( !empty($record) )
            foreach($record as $key => $riga){
        
                $chiavi[] = $key;
                $valori[$key] = addslashes($riga);
                //$chiaviStringa .= $key.", "; 
                //$valoriStringa = $key." = '".$riga."', ";
                }

            //print_r($chiavi);
            //print_r($valori);
            //$chiaviStringa = substr($chiaviStringa, 0, -2); 
            //$valoriStringa = substr($valoriStringa, 0, -2);
            
            
            //scraperwiki::sqliteexecute("insert into eventi values (".$chiaviStringa.")", $valori);
            scraperwiki::save_sqlite($chiavi, $valori, 'prova_dati');
            //unset($chiaviStringa, $valoriStringa);
           
            }
    unset($arrLink);
}
?>


















