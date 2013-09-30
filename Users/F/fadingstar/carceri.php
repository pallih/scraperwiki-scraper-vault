<?php
/*
** Scraper di indirizzi e recapiti di tutte le strutture penitenziarie italiane 
** (comprese strutture minorili)
*/

require 'scraperwiki/simple_html_dom.php';

//print_r(scraperwiki::show_tables());
#scraperwiki::sqliteexecute("drop table if exists strutture_penitenziarie_italiane"); 
//print_r(scraperwiki::show_tables());


/*
 * Crawler & Parser
*/
$base_urls = Array( 'http://www.giustizia.it/giustizia/it/mg_4.wp?selectedNode=3_6&facetNode_1=3_6&letter=No&frame11_item=',  // strutture penitenziarie, ospedali e uffici
                    'http://www.giustizia.it/giustizia/it/mg_4.wp?facetNode_1=3_5&selectedNode=3_5_5&letter=No&frame11_item='); // minorili

$num_pages = Array(32,2);

$url_end = '&zl=-1';

for ($j = 0; $j <= 1; $j++) {

    for ($i = 1; $i <= $num_pages[$j]; $i++) {
    
        $num = strval($i);
    
        $url = $base_urls[$j] . $num . $url_end;
        print $url . "\n";
    
        $carceri = scraperWiki::scrape($url);     
        $carceri_dom = new simple_html_dom();
        $carceri_dom->load($carceri);
    
        $html = str_get_html($carceri);
    
        foreach ($html->find("div.resultGeoBody li") as $el) { 
        
            $citta = $aka = $cap = $nome_carcere = $telefono = $fax = $citta = $nome_carcere = $cf = $festa = $mail = $indirizzo = '';
    
            // Nome istituto penitenziario
            $nome_carcere = $el -> find ("strong", 0) -> innertext ;
            #print $nome_carcere."\n";
    
            // <span class="stronger">92100</span> - CAP
            $cap = $el -> find ("span.stronger", 0) -> innertext ;
            #print $cap ."\n";
    
            // <span class="stronger">AGRIGENTO</span> - Citta
            $citta = $el -> find ("span.stronger", 1) -> innertext ;
            #print $citta."\n";
    
            // indirizzo, tel, fax, mail, ecc...
            $righe = $el -> plaintext;
            $righe = explode( "\n", $righe );
    
           
            if( preg_match("/[a-z]+/i", $righe[1]) != 0 ) {
                $indirizzo =  $righe[1];
            }
    
            
            foreach ($righe as $r) {
    
                #print $r."\n";
                
                if (strstr($r, 'telefoni:&nbsp;')) {
                    $tel = explode(";",$r);
                    #print $tel[1]."\n";
                    if( $telefono == '' &&  preg_match("/[0-9]+/i", $tel[1]) != 0 ) {
                        $telefono = $tel[1];
                    }
                    
                }
    
                if (strstr($r, 'e-mail:&nbsp;')) {
                    $email = explode(";",$r);
                    #print $email[1]."\n";
                    if( $mail == '' &&  preg_match("/@+/i", $email[1]) != 0 ) {
                        $mail = $email[1];
                    }
                }
    
                if (strstr($r, 'fax:&nbsp;')) {
                    $fax_n = explode(";",$r);
                    #print $fax[1]."\n";
                    if( $fax == '' &&  preg_match("/[0-9]+/i", $fax_n[1]) != 0 ) {
                        $fax = $fax_n[1];
                    }
                }
    
                if (strstr($r, 'C.F.:&nbsp;')) {
                    $cf_n = explode(";",$r);
                    #print $cf_n[1]."\n";
                    if( $cf == '' &&  preg_match("/[0-9]+/i", $cf_n[1]) != 0 ) {
                        $cf = $cf_n[1];
                    }
                }
    
                if (strstr($r, 'Festivit')){
                    $festa_n = explode(":",$r);
                    #print $festa_n[1]."\n";
                    if( $festa == '' &&  preg_match("/[a-z0-9]+/i", $festa_n[1]) != 0 ) {
                        $festa = $festa_n[1];
                    }
                }
            }
    
     
        
            /*
            * SQLite storage di un singolo carcere
            */
    
            $record = array("nome" => trim($nome_carcere),
                            "citta" => trim($citta),
                            "cap" => trim($cap),
                            "indirizzo" => trim($indirizzo),
                            "telefono" => trim($telefono),
                            "fax" => trim($fax),         
                            "cf" => trim($cf),     
                            "aka" => trim($aka),    
                            "festivita" => trim($festa),   
                            //"info" => trim("O"),        // TODO
                            //"web" => trim("O"),         // TODO
                            "email" => trim($mail));
            
            scraperwiki::save_sqlite(array("nome", "indirizzo"), $record, $table_name="strutture_penitenziarie_italiane");
            
        }
    
    }
}

/*
 * Per facilitare l'incrocio con la tabella di Ristretti mappiamo
 * i nomi delle carceri per come sono conosciuti comunemente o risolvere casi di ambiguità. 
 * In fase di incrocio, sarà data priorità massima a questi corrispettivi (espliciti)
*/
$dictionary_aka = array("Genova Marassi"=>"Casa circondariale di GENOVA",
                        "Genova Pontedecimo"=>"Casa circondariale femminile di GENOVA",
                        "Genova"=>"Casa circondariale di GENOVA",           // ?

                        "Gorgona (LI)"=>"Casa di reclusione di GORGONA",

                        "Firenze Solliccianino" => "Casa circondariale - Casa di reclusione di FIRENZE",
                        "Firenze Sollicciano" => "Casa circondariale - Casa di reclusione di FIRENZE",

                        "Brucoli (SR)" => "Casa circondariale di SIRACUSA",

                        "Bollate (MI)" => "Seconda Casa di reclusione di MILANO", 
                        "Milano Opera"=>"Casa circondariale - Casa di reclusione di MILANO",
                        "Opera (Mi)"=>"Casa circondariale - Casa di reclusione di MILANO",
                        "Milano San Vittore"=>"Casa circondariale di MILANO",
                        "San Vittore (Mi)"=>"Casa circondariale di MILANO",

                        "Napoli"=>"Casa circondariale  di NAPOLI",          // ?
                        "Napoli Poggioreale"=>"Casa circondariale  di NAPOLI",
                        "Napoli Secondigliano"=>"Centro penitenziario NAPOLI SECONDIGLIANO",
                        "Poggioreale (Na)"=>"Casa circondariale  di NAPOLI",

                        "Santa Maria C.V. (Ce)"=>"Casa circondariale di SANTA MARIA CAPUA VETERE",
                        "S.M. Capua Vetere (CE)"=>"Casa circondariale di SANTA MARIA CAPUA VETERE",

                        "Opg Aversa (CE)"=>"Ospedale psichiatrico giudiziario di AVERSA",
                        "Opg Barcellona P.G. (ME)" => "Ospedale psichiatrico giudiziario di BARCELLONA POZZO DI GOTTO",
                        "Opg Castiglione (MN)" => "Ospedale psichiatrico giudiziario di CASTIGLIONE DELLE STIVIERE",
                        "Opg Montelupo (FI)" => "Ospedale psichiatrico giudiziario di MONTELUPO FIORENTINO",
                        "Opg Reggio Emilia" => "Ospedale psichiatrico giudiziario di REGGIO NELL&#39;EMILIA",
                        "Opg Napoli" => "Ospedale psichiatrico giudiziario di NAPOLI",
                        "Viterbo (Osp. Belcolle)"=>"Unit√† ospedaliera di medicina protetta  - Casa circondariale VITERBO",

                        "Massa Carrara"=>"Casa circondariale - Casa di reclusione di MASSA",
                        "Mamone (CA)"=>"Casa di reclusione della frazione di Mamone ONANI",

                        "Roma Rebibbia" => "Casa circondariale di ROMA - &quot;Terza casa&quot;",
                        "Rebibbia (Ro)" => "Casa circondariale di ROMA - &quot;Terza casa&quot;",
                        "Roma Regina Coeli" => "Casa circondariale di ROMA",

                        "Ipm Casal Del Marmo (RM)"=>"Istituto Penale Minorenni di ROMA",
                        "Firenze Ipm"=>"Istituto Penale Minorenni di FIRENZE",

                        "Is Arenas (CA)"=>"Casa di reclusione di Arbus &quot;Is Arenas&quot;",

                        "Padova C. Circ."=>"Casa circondariale di PADOVA",
                        "Padova C. Circondariale"=>"Casa circondariale di PADOVA",
                        "Padova Reclusione"=>"Casa di reclusione di PADOVA",

                        "Pagliarelli (PA)"=>"Casa circondariale di PALERMO - Pagliarelli",
                        "Palermo Pagliarelli"=>"Casa circondariale di PALERMO - Pagliarelli",
                        "Palermo Ucciardone"=>"Casa circondariale di PALERMO - Ucciardone",
                        "Parma C.C."=>"Casa di reclusione di PARMA",

                        "Venezia S.M. Maggiore"=>"Casa circondariale di VENEZIA",
                        "Venezia Giudecca"=>"Casa circondariale di VENEZIA",
                        "Venezia"=>"Casa circondariale di VENEZIA");


print_r(scraperwiki::show_tables()); 


?><?php
/*
** Scraper di indirizzi e recapiti di tutte le strutture penitenziarie italiane 
** (comprese strutture minorili)
*/

require 'scraperwiki/simple_html_dom.php';

//print_r(scraperwiki::show_tables());
#scraperwiki::sqliteexecute("drop table if exists strutture_penitenziarie_italiane"); 
//print_r(scraperwiki::show_tables());


/*
 * Crawler & Parser
*/
$base_urls = Array( 'http://www.giustizia.it/giustizia/it/mg_4.wp?selectedNode=3_6&facetNode_1=3_6&letter=No&frame11_item=',  // strutture penitenziarie, ospedali e uffici
                    'http://www.giustizia.it/giustizia/it/mg_4.wp?facetNode_1=3_5&selectedNode=3_5_5&letter=No&frame11_item='); // minorili

$num_pages = Array(32,2);

$url_end = '&zl=-1';

for ($j = 0; $j <= 1; $j++) {

    for ($i = 1; $i <= $num_pages[$j]; $i++) {
    
        $num = strval($i);
    
        $url = $base_urls[$j] . $num . $url_end;
        print $url . "\n";
    
        $carceri = scraperWiki::scrape($url);     
        $carceri_dom = new simple_html_dom();
        $carceri_dom->load($carceri);
    
        $html = str_get_html($carceri);
    
        foreach ($html->find("div.resultGeoBody li") as $el) { 
        
            $citta = $aka = $cap = $nome_carcere = $telefono = $fax = $citta = $nome_carcere = $cf = $festa = $mail = $indirizzo = '';
    
            // Nome istituto penitenziario
            $nome_carcere = $el -> find ("strong", 0) -> innertext ;
            #print $nome_carcere."\n";
    
            // <span class="stronger">92100</span> - CAP
            $cap = $el -> find ("span.stronger", 0) -> innertext ;
            #print $cap ."\n";
    
            // <span class="stronger">AGRIGENTO</span> - Citta
            $citta = $el -> find ("span.stronger", 1) -> innertext ;
            #print $citta."\n";
    
            // indirizzo, tel, fax, mail, ecc...
            $righe = $el -> plaintext;
            $righe = explode( "\n", $righe );
    
           
            if( preg_match("/[a-z]+/i", $righe[1]) != 0 ) {
                $indirizzo =  $righe[1];
            }
    
            
            foreach ($righe as $r) {
    
                #print $r."\n";
                
                if (strstr($r, 'telefoni:&nbsp;')) {
                    $tel = explode(";",$r);
                    #print $tel[1]."\n";
                    if( $telefono == '' &&  preg_match("/[0-9]+/i", $tel[1]) != 0 ) {
                        $telefono = $tel[1];
                    }
                    
                }
    
                if (strstr($r, 'e-mail:&nbsp;')) {
                    $email = explode(";",$r);
                    #print $email[1]."\n";
                    if( $mail == '' &&  preg_match("/@+/i", $email[1]) != 0 ) {
                        $mail = $email[1];
                    }
                }
    
                if (strstr($r, 'fax:&nbsp;')) {
                    $fax_n = explode(";",$r);
                    #print $fax[1]."\n";
                    if( $fax == '' &&  preg_match("/[0-9]+/i", $fax_n[1]) != 0 ) {
                        $fax = $fax_n[1];
                    }
                }
    
                if (strstr($r, 'C.F.:&nbsp;')) {
                    $cf_n = explode(";",$r);
                    #print $cf_n[1]."\n";
                    if( $cf == '' &&  preg_match("/[0-9]+/i", $cf_n[1]) != 0 ) {
                        $cf = $cf_n[1];
                    }
                }
    
                if (strstr($r, 'Festivit')){
                    $festa_n = explode(":",$r);
                    #print $festa_n[1]."\n";
                    if( $festa == '' &&  preg_match("/[a-z0-9]+/i", $festa_n[1]) != 0 ) {
                        $festa = $festa_n[1];
                    }
                }
            }
    
     
        
            /*
            * SQLite storage di un singolo carcere
            */
    
            $record = array("nome" => trim($nome_carcere),
                            "citta" => trim($citta),
                            "cap" => trim($cap),
                            "indirizzo" => trim($indirizzo),
                            "telefono" => trim($telefono),
                            "fax" => trim($fax),         
                            "cf" => trim($cf),     
                            "aka" => trim($aka),    
                            "festivita" => trim($festa),   
                            //"info" => trim("O"),        // TODO
                            //"web" => trim("O"),         // TODO
                            "email" => trim($mail));
            
            scraperwiki::save_sqlite(array("nome", "indirizzo"), $record, $table_name="strutture_penitenziarie_italiane");
            
        }
    
    }
}

/*
 * Per facilitare l'incrocio con la tabella di Ristretti mappiamo
 * i nomi delle carceri per come sono conosciuti comunemente o risolvere casi di ambiguità. 
 * In fase di incrocio, sarà data priorità massima a questi corrispettivi (espliciti)
*/
$dictionary_aka = array("Genova Marassi"=>"Casa circondariale di GENOVA",
                        "Genova Pontedecimo"=>"Casa circondariale femminile di GENOVA",
                        "Genova"=>"Casa circondariale di GENOVA",           // ?

                        "Gorgona (LI)"=>"Casa di reclusione di GORGONA",

                        "Firenze Solliccianino" => "Casa circondariale - Casa di reclusione di FIRENZE",
                        "Firenze Sollicciano" => "Casa circondariale - Casa di reclusione di FIRENZE",

                        "Brucoli (SR)" => "Casa circondariale di SIRACUSA",

                        "Bollate (MI)" => "Seconda Casa di reclusione di MILANO", 
                        "Milano Opera"=>"Casa circondariale - Casa di reclusione di MILANO",
                        "Opera (Mi)"=>"Casa circondariale - Casa di reclusione di MILANO",
                        "Milano San Vittore"=>"Casa circondariale di MILANO",
                        "San Vittore (Mi)"=>"Casa circondariale di MILANO",

                        "Napoli"=>"Casa circondariale  di NAPOLI",          // ?
                        "Napoli Poggioreale"=>"Casa circondariale  di NAPOLI",
                        "Napoli Secondigliano"=>"Centro penitenziario NAPOLI SECONDIGLIANO",
                        "Poggioreale (Na)"=>"Casa circondariale  di NAPOLI",

                        "Santa Maria C.V. (Ce)"=>"Casa circondariale di SANTA MARIA CAPUA VETERE",
                        "S.M. Capua Vetere (CE)"=>"Casa circondariale di SANTA MARIA CAPUA VETERE",

                        "Opg Aversa (CE)"=>"Ospedale psichiatrico giudiziario di AVERSA",
                        "Opg Barcellona P.G. (ME)" => "Ospedale psichiatrico giudiziario di BARCELLONA POZZO DI GOTTO",
                        "Opg Castiglione (MN)" => "Ospedale psichiatrico giudiziario di CASTIGLIONE DELLE STIVIERE",
                        "Opg Montelupo (FI)" => "Ospedale psichiatrico giudiziario di MONTELUPO FIORENTINO",
                        "Opg Reggio Emilia" => "Ospedale psichiatrico giudiziario di REGGIO NELL&#39;EMILIA",
                        "Opg Napoli" => "Ospedale psichiatrico giudiziario di NAPOLI",
                        "Viterbo (Osp. Belcolle)"=>"Unit√† ospedaliera di medicina protetta  - Casa circondariale VITERBO",

                        "Massa Carrara"=>"Casa circondariale - Casa di reclusione di MASSA",
                        "Mamone (CA)"=>"Casa di reclusione della frazione di Mamone ONANI",

                        "Roma Rebibbia" => "Casa circondariale di ROMA - &quot;Terza casa&quot;",
                        "Rebibbia (Ro)" => "Casa circondariale di ROMA - &quot;Terza casa&quot;",
                        "Roma Regina Coeli" => "Casa circondariale di ROMA",

                        "Ipm Casal Del Marmo (RM)"=>"Istituto Penale Minorenni di ROMA",
                        "Firenze Ipm"=>"Istituto Penale Minorenni di FIRENZE",

                        "Is Arenas (CA)"=>"Casa di reclusione di Arbus &quot;Is Arenas&quot;",

                        "Padova C. Circ."=>"Casa circondariale di PADOVA",
                        "Padova C. Circondariale"=>"Casa circondariale di PADOVA",
                        "Padova Reclusione"=>"Casa di reclusione di PADOVA",

                        "Pagliarelli (PA)"=>"Casa circondariale di PALERMO - Pagliarelli",
                        "Palermo Pagliarelli"=>"Casa circondariale di PALERMO - Pagliarelli",
                        "Palermo Ucciardone"=>"Casa circondariale di PALERMO - Ucciardone",
                        "Parma C.C."=>"Casa di reclusione di PARMA",

                        "Venezia S.M. Maggiore"=>"Casa circondariale di VENEZIA",
                        "Venezia Giudecca"=>"Casa circondariale di VENEZIA",
                        "Venezia"=>"Casa circondariale di VENEZIA");


print_r(scraperwiki::show_tables()); 


?><?php
/*
** Scraper di indirizzi e recapiti di tutte le strutture penitenziarie italiane 
** (comprese strutture minorili)
*/

require 'scraperwiki/simple_html_dom.php';

//print_r(scraperwiki::show_tables());
#scraperwiki::sqliteexecute("drop table if exists strutture_penitenziarie_italiane"); 
//print_r(scraperwiki::show_tables());


/*
 * Crawler & Parser
*/
$base_urls = Array( 'http://www.giustizia.it/giustizia/it/mg_4.wp?selectedNode=3_6&facetNode_1=3_6&letter=No&frame11_item=',  // strutture penitenziarie, ospedali e uffici
                    'http://www.giustizia.it/giustizia/it/mg_4.wp?facetNode_1=3_5&selectedNode=3_5_5&letter=No&frame11_item='); // minorili

$num_pages = Array(32,2);

$url_end = '&zl=-1';

for ($j = 0; $j <= 1; $j++) {

    for ($i = 1; $i <= $num_pages[$j]; $i++) {
    
        $num = strval($i);
    
        $url = $base_urls[$j] . $num . $url_end;
        print $url . "\n";
    
        $carceri = scraperWiki::scrape($url);     
        $carceri_dom = new simple_html_dom();
        $carceri_dom->load($carceri);
    
        $html = str_get_html($carceri);
    
        foreach ($html->find("div.resultGeoBody li") as $el) { 
        
            $citta = $aka = $cap = $nome_carcere = $telefono = $fax = $citta = $nome_carcere = $cf = $festa = $mail = $indirizzo = '';
    
            // Nome istituto penitenziario
            $nome_carcere = $el -> find ("strong", 0) -> innertext ;
            #print $nome_carcere."\n";
    
            // <span class="stronger">92100</span> - CAP
            $cap = $el -> find ("span.stronger", 0) -> innertext ;
            #print $cap ."\n";
    
            // <span class="stronger">AGRIGENTO</span> - Citta
            $citta = $el -> find ("span.stronger", 1) -> innertext ;
            #print $citta."\n";
    
            // indirizzo, tel, fax, mail, ecc...
            $righe = $el -> plaintext;
            $righe = explode( "\n", $righe );
    
           
            if( preg_match("/[a-z]+/i", $righe[1]) != 0 ) {
                $indirizzo =  $righe[1];
            }
    
            
            foreach ($righe as $r) {
    
                #print $r."\n";
                
                if (strstr($r, 'telefoni:&nbsp;')) {
                    $tel = explode(";",$r);
                    #print $tel[1]."\n";
                    if( $telefono == '' &&  preg_match("/[0-9]+/i", $tel[1]) != 0 ) {
                        $telefono = $tel[1];
                    }
                    
                }
    
                if (strstr($r, 'e-mail:&nbsp;')) {
                    $email = explode(";",$r);
                    #print $email[1]."\n";
                    if( $mail == '' &&  preg_match("/@+/i", $email[1]) != 0 ) {
                        $mail = $email[1];
                    }
                }
    
                if (strstr($r, 'fax:&nbsp;')) {
                    $fax_n = explode(";",$r);
                    #print $fax[1]."\n";
                    if( $fax == '' &&  preg_match("/[0-9]+/i", $fax_n[1]) != 0 ) {
                        $fax = $fax_n[1];
                    }
                }
    
                if (strstr($r, 'C.F.:&nbsp;')) {
                    $cf_n = explode(";",$r);
                    #print $cf_n[1]."\n";
                    if( $cf == '' &&  preg_match("/[0-9]+/i", $cf_n[1]) != 0 ) {
                        $cf = $cf_n[1];
                    }
                }
    
                if (strstr($r, 'Festivit')){
                    $festa_n = explode(":",$r);
                    #print $festa_n[1]."\n";
                    if( $festa == '' &&  preg_match("/[a-z0-9]+/i", $festa_n[1]) != 0 ) {
                        $festa = $festa_n[1];
                    }
                }
            }
    
     
        
            /*
            * SQLite storage di un singolo carcere
            */
    
            $record = array("nome" => trim($nome_carcere),
                            "citta" => trim($citta),
                            "cap" => trim($cap),
                            "indirizzo" => trim($indirizzo),
                            "telefono" => trim($telefono),
                            "fax" => trim($fax),         
                            "cf" => trim($cf),     
                            "aka" => trim($aka),    
                            "festivita" => trim($festa),   
                            //"info" => trim("O"),        // TODO
                            //"web" => trim("O"),         // TODO
                            "email" => trim($mail));
            
            scraperwiki::save_sqlite(array("nome", "indirizzo"), $record, $table_name="strutture_penitenziarie_italiane");
            
        }
    
    }
}

/*
 * Per facilitare l'incrocio con la tabella di Ristretti mappiamo
 * i nomi delle carceri per come sono conosciuti comunemente o risolvere casi di ambiguità. 
 * In fase di incrocio, sarà data priorità massima a questi corrispettivi (espliciti)
*/
$dictionary_aka = array("Genova Marassi"=>"Casa circondariale di GENOVA",
                        "Genova Pontedecimo"=>"Casa circondariale femminile di GENOVA",
                        "Genova"=>"Casa circondariale di GENOVA",           // ?

                        "Gorgona (LI)"=>"Casa di reclusione di GORGONA",

                        "Firenze Solliccianino" => "Casa circondariale - Casa di reclusione di FIRENZE",
                        "Firenze Sollicciano" => "Casa circondariale - Casa di reclusione di FIRENZE",

                        "Brucoli (SR)" => "Casa circondariale di SIRACUSA",

                        "Bollate (MI)" => "Seconda Casa di reclusione di MILANO", 
                        "Milano Opera"=>"Casa circondariale - Casa di reclusione di MILANO",
                        "Opera (Mi)"=>"Casa circondariale - Casa di reclusione di MILANO",
                        "Milano San Vittore"=>"Casa circondariale di MILANO",
                        "San Vittore (Mi)"=>"Casa circondariale di MILANO",

                        "Napoli"=>"Casa circondariale  di NAPOLI",          // ?
                        "Napoli Poggioreale"=>"Casa circondariale  di NAPOLI",
                        "Napoli Secondigliano"=>"Centro penitenziario NAPOLI SECONDIGLIANO",
                        "Poggioreale (Na)"=>"Casa circondariale  di NAPOLI",

                        "Santa Maria C.V. (Ce)"=>"Casa circondariale di SANTA MARIA CAPUA VETERE",
                        "S.M. Capua Vetere (CE)"=>"Casa circondariale di SANTA MARIA CAPUA VETERE",

                        "Opg Aversa (CE)"=>"Ospedale psichiatrico giudiziario di AVERSA",
                        "Opg Barcellona P.G. (ME)" => "Ospedale psichiatrico giudiziario di BARCELLONA POZZO DI GOTTO",
                        "Opg Castiglione (MN)" => "Ospedale psichiatrico giudiziario di CASTIGLIONE DELLE STIVIERE",
                        "Opg Montelupo (FI)" => "Ospedale psichiatrico giudiziario di MONTELUPO FIORENTINO",
                        "Opg Reggio Emilia" => "Ospedale psichiatrico giudiziario di REGGIO NELL&#39;EMILIA",
                        "Opg Napoli" => "Ospedale psichiatrico giudiziario di NAPOLI",
                        "Viterbo (Osp. Belcolle)"=>"Unit√† ospedaliera di medicina protetta  - Casa circondariale VITERBO",

                        "Massa Carrara"=>"Casa circondariale - Casa di reclusione di MASSA",
                        "Mamone (CA)"=>"Casa di reclusione della frazione di Mamone ONANI",

                        "Roma Rebibbia" => "Casa circondariale di ROMA - &quot;Terza casa&quot;",
                        "Rebibbia (Ro)" => "Casa circondariale di ROMA - &quot;Terza casa&quot;",
                        "Roma Regina Coeli" => "Casa circondariale di ROMA",

                        "Ipm Casal Del Marmo (RM)"=>"Istituto Penale Minorenni di ROMA",
                        "Firenze Ipm"=>"Istituto Penale Minorenni di FIRENZE",

                        "Is Arenas (CA)"=>"Casa di reclusione di Arbus &quot;Is Arenas&quot;",

                        "Padova C. Circ."=>"Casa circondariale di PADOVA",
                        "Padova C. Circondariale"=>"Casa circondariale di PADOVA",
                        "Padova Reclusione"=>"Casa di reclusione di PADOVA",

                        "Pagliarelli (PA)"=>"Casa circondariale di PALERMO - Pagliarelli",
                        "Palermo Pagliarelli"=>"Casa circondariale di PALERMO - Pagliarelli",
                        "Palermo Ucciardone"=>"Casa circondariale di PALERMO - Ucciardone",
                        "Parma C.C."=>"Casa di reclusione di PARMA",

                        "Venezia S.M. Maggiore"=>"Casa circondariale di VENEZIA",
                        "Venezia Giudecca"=>"Casa circondariale di VENEZIA",
                        "Venezia"=>"Casa circondariale di VENEZIA");


print_r(scraperwiki::show_tables()); 


?><?php
/*
** Scraper di indirizzi e recapiti di tutte le strutture penitenziarie italiane 
** (comprese strutture minorili)
*/

require 'scraperwiki/simple_html_dom.php';

//print_r(scraperwiki::show_tables());
#scraperwiki::sqliteexecute("drop table if exists strutture_penitenziarie_italiane"); 
//print_r(scraperwiki::show_tables());


/*
 * Crawler & Parser
*/
$base_urls = Array( 'http://www.giustizia.it/giustizia/it/mg_4.wp?selectedNode=3_6&facetNode_1=3_6&letter=No&frame11_item=',  // strutture penitenziarie, ospedali e uffici
                    'http://www.giustizia.it/giustizia/it/mg_4.wp?facetNode_1=3_5&selectedNode=3_5_5&letter=No&frame11_item='); // minorili

$num_pages = Array(32,2);

$url_end = '&zl=-1';

for ($j = 0; $j <= 1; $j++) {

    for ($i = 1; $i <= $num_pages[$j]; $i++) {
    
        $num = strval($i);
    
        $url = $base_urls[$j] . $num . $url_end;
        print $url . "\n";
    
        $carceri = scraperWiki::scrape($url);     
        $carceri_dom = new simple_html_dom();
        $carceri_dom->load($carceri);
    
        $html = str_get_html($carceri);
    
        foreach ($html->find("div.resultGeoBody li") as $el) { 
        
            $citta = $aka = $cap = $nome_carcere = $telefono = $fax = $citta = $nome_carcere = $cf = $festa = $mail = $indirizzo = '';
    
            // Nome istituto penitenziario
            $nome_carcere = $el -> find ("strong", 0) -> innertext ;
            #print $nome_carcere."\n";
    
            // <span class="stronger">92100</span> - CAP
            $cap = $el -> find ("span.stronger", 0) -> innertext ;
            #print $cap ."\n";
    
            // <span class="stronger">AGRIGENTO</span> - Citta
            $citta = $el -> find ("span.stronger", 1) -> innertext ;
            #print $citta."\n";
    
            // indirizzo, tel, fax, mail, ecc...
            $righe = $el -> plaintext;
            $righe = explode( "\n", $righe );
    
           
            if( preg_match("/[a-z]+/i", $righe[1]) != 0 ) {
                $indirizzo =  $righe[1];
            }
    
            
            foreach ($righe as $r) {
    
                #print $r."\n";
                
                if (strstr($r, 'telefoni:&nbsp;')) {
                    $tel = explode(";",$r);
                    #print $tel[1]."\n";
                    if( $telefono == '' &&  preg_match("/[0-9]+/i", $tel[1]) != 0 ) {
                        $telefono = $tel[1];
                    }
                    
                }
    
                if (strstr($r, 'e-mail:&nbsp;')) {
                    $email = explode(";",$r);
                    #print $email[1]."\n";
                    if( $mail == '' &&  preg_match("/@+/i", $email[1]) != 0 ) {
                        $mail = $email[1];
                    }
                }
    
                if (strstr($r, 'fax:&nbsp;')) {
                    $fax_n = explode(";",$r);
                    #print $fax[1]."\n";
                    if( $fax == '' &&  preg_match("/[0-9]+/i", $fax_n[1]) != 0 ) {
                        $fax = $fax_n[1];
                    }
                }
    
                if (strstr($r, 'C.F.:&nbsp;')) {
                    $cf_n = explode(";",$r);
                    #print $cf_n[1]."\n";
                    if( $cf == '' &&  preg_match("/[0-9]+/i", $cf_n[1]) != 0 ) {
                        $cf = $cf_n[1];
                    }
                }
    
                if (strstr($r, 'Festivit')){
                    $festa_n = explode(":",$r);
                    #print $festa_n[1]."\n";
                    if( $festa == '' &&  preg_match("/[a-z0-9]+/i", $festa_n[1]) != 0 ) {
                        $festa = $festa_n[1];
                    }
                }
            }
    
     
        
            /*
            * SQLite storage di un singolo carcere
            */
    
            $record = array("nome" => trim($nome_carcere),
                            "citta" => trim($citta),
                            "cap" => trim($cap),
                            "indirizzo" => trim($indirizzo),
                            "telefono" => trim($telefono),
                            "fax" => trim($fax),         
                            "cf" => trim($cf),     
                            "aka" => trim($aka),    
                            "festivita" => trim($festa),   
                            //"info" => trim("O"),        // TODO
                            //"web" => trim("O"),         // TODO
                            "email" => trim($mail));
            
            scraperwiki::save_sqlite(array("nome", "indirizzo"), $record, $table_name="strutture_penitenziarie_italiane");
            
        }
    
    }
}

/*
 * Per facilitare l'incrocio con la tabella di Ristretti mappiamo
 * i nomi delle carceri per come sono conosciuti comunemente o risolvere casi di ambiguità. 
 * In fase di incrocio, sarà data priorità massima a questi corrispettivi (espliciti)
*/
$dictionary_aka = array("Genova Marassi"=>"Casa circondariale di GENOVA",
                        "Genova Pontedecimo"=>"Casa circondariale femminile di GENOVA",
                        "Genova"=>"Casa circondariale di GENOVA",           // ?

                        "Gorgona (LI)"=>"Casa di reclusione di GORGONA",

                        "Firenze Solliccianino" => "Casa circondariale - Casa di reclusione di FIRENZE",
                        "Firenze Sollicciano" => "Casa circondariale - Casa di reclusione di FIRENZE",

                        "Brucoli (SR)" => "Casa circondariale di SIRACUSA",

                        "Bollate (MI)" => "Seconda Casa di reclusione di MILANO", 
                        "Milano Opera"=>"Casa circondariale - Casa di reclusione di MILANO",
                        "Opera (Mi)"=>"Casa circondariale - Casa di reclusione di MILANO",
                        "Milano San Vittore"=>"Casa circondariale di MILANO",
                        "San Vittore (Mi)"=>"Casa circondariale di MILANO",

                        "Napoli"=>"Casa circondariale  di NAPOLI",          // ?
                        "Napoli Poggioreale"=>"Casa circondariale  di NAPOLI",
                        "Napoli Secondigliano"=>"Centro penitenziario NAPOLI SECONDIGLIANO",
                        "Poggioreale (Na)"=>"Casa circondariale  di NAPOLI",

                        "Santa Maria C.V. (Ce)"=>"Casa circondariale di SANTA MARIA CAPUA VETERE",
                        "S.M. Capua Vetere (CE)"=>"Casa circondariale di SANTA MARIA CAPUA VETERE",

                        "Opg Aversa (CE)"=>"Ospedale psichiatrico giudiziario di AVERSA",
                        "Opg Barcellona P.G. (ME)" => "Ospedale psichiatrico giudiziario di BARCELLONA POZZO DI GOTTO",
                        "Opg Castiglione (MN)" => "Ospedale psichiatrico giudiziario di CASTIGLIONE DELLE STIVIERE",
                        "Opg Montelupo (FI)" => "Ospedale psichiatrico giudiziario di MONTELUPO FIORENTINO",
                        "Opg Reggio Emilia" => "Ospedale psichiatrico giudiziario di REGGIO NELL&#39;EMILIA",
                        "Opg Napoli" => "Ospedale psichiatrico giudiziario di NAPOLI",
                        "Viterbo (Osp. Belcolle)"=>"Unit√† ospedaliera di medicina protetta  - Casa circondariale VITERBO",

                        "Massa Carrara"=>"Casa circondariale - Casa di reclusione di MASSA",
                        "Mamone (CA)"=>"Casa di reclusione della frazione di Mamone ONANI",

                        "Roma Rebibbia" => "Casa circondariale di ROMA - &quot;Terza casa&quot;",
                        "Rebibbia (Ro)" => "Casa circondariale di ROMA - &quot;Terza casa&quot;",
                        "Roma Regina Coeli" => "Casa circondariale di ROMA",

                        "Ipm Casal Del Marmo (RM)"=>"Istituto Penale Minorenni di ROMA",
                        "Firenze Ipm"=>"Istituto Penale Minorenni di FIRENZE",

                        "Is Arenas (CA)"=>"Casa di reclusione di Arbus &quot;Is Arenas&quot;",

                        "Padova C. Circ."=>"Casa circondariale di PADOVA",
                        "Padova C. Circondariale"=>"Casa circondariale di PADOVA",
                        "Padova Reclusione"=>"Casa di reclusione di PADOVA",

                        "Pagliarelli (PA)"=>"Casa circondariale di PALERMO - Pagliarelli",
                        "Palermo Pagliarelli"=>"Casa circondariale di PALERMO - Pagliarelli",
                        "Palermo Ucciardone"=>"Casa circondariale di PALERMO - Ucciardone",
                        "Parma C.C."=>"Casa di reclusione di PARMA",

                        "Venezia S.M. Maggiore"=>"Casa circondariale di VENEZIA",
                        "Venezia Giudecca"=>"Casa circondariale di VENEZIA",
                        "Venezia"=>"Casa circondariale di VENEZIA");


print_r(scraperwiki::show_tables()); 


?>