<?php
$baseurl="http://www.eventiesagre.it";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$i=0;
$flag=true;
$numeroEvento= 0;
do {
    $html = scraperWiki::scrape("http://www.eventiesagre.it/pagine/Eventi/sez/mesi/Trentino+Alto+Adige/prov/cit/intit/rilib/861-".$i."-data-DESC-nav.htm");        

$dom->load($html);

if ($dom->find("tr.elenco1") != null ){
    foreach($dom->find("tr.elenco1") as $data){
        
        $numeroEvento++;
    
        $tds = $data->find("td");
    
        #tiplogia
        $tipologiaClass = $tds[1]->find("span.category");
        $tipologiaPos = $tds[1]->children(0)->plaintext;
        $tipologiaCheck = false;
        if ($tipologiaClass[0]->plaintext==$tipologiaPos) $tipologiaCheck = true;
    
        #nome evento
        $nomeEventoClass = $tds[1]->find("a.summary");
        $nomeEventoPos = $tds[1]->children(2)->plaintext;
        $nomeEventoCheck = false;
        if ($nomeEventoClass[0]->plaintext==$nomeEventoPos) $nomeEventoCheck = true;
    
        #url evento
        $urlEventoClass = $nomeEventoClass[0]->href;
        $urlEventoPos = $tds[1]->children(2)->href;
        $urlEventoCheck = false;
        if ($urlEventoClass==$urlEventoPos) $urlEventoCheck = true;
    
        #data inizio
        $dataInizioClass = $tds[1]->find("span.dtstart");
        if ($dataInizioClass != null) $dataInizioIso = $dataInizioClass[0]->children(0)->title;
    
        #data fine
        $dataFineClass = $tds[1]->find("span.dtend");
        if ($dataFineClass != null) $dataFineIso = $dataFineClass[0]->children(0)->title;
    
        #luogo
        $luogoClass = $tds[1]->find("span.location");
        $luogoRegione = $luogoClass[0]->children(0)->plaintext;
        if ($luogoClass[0]->children(2)->plaintext=="") {
            $luogoProvincia = $luogoClass[0]->children(1)->plaintext;
            $luogoLocalita="";
        } else {
            $luogoLocalita = $luogoClass[0]->children(1)->plaintext;
            $luogoProvincia = $luogoClass[0]->children(2)->plaintext;
        }
    
        #descrizione
        $descrizioneEventoClass = $tds[1]->find("span.description");
    
        
        $record = array(
            'id' => $numeroEvento,
            'tipologiaPos' => $tipologiaPos,
            'tipologiaClass' => $tipologiaClass[0]->plaintext,
            'tipologiaCheck' => $tipologiaCheck,
            'nomeEventoPos' => $nomeEventoPos,
            'nomeEventoClass' => $nomeEventoClass[0]->plaintext,
            'nomeEventoCheck' => $nomeEventoCheck,
            'urlEventoPos' => $baseurl.$urlEventoPos,
            'urlEventoClass' => $baseurl.$urlEventoClass,
            'urlEventoCheck' => $urlEventoCheck,
            'dataInizioClass' => $dataInizioClass[0]->plaintext,
            'dataInizioIso' => $dataInizioIso,
            'luogoRegione' => $luogoRegione,
            'luogoProvincia' => $luogoProvincia,
            'luogoLocalita' => $luogoLocalita,
            'descrizioneEvento' => $descrizioneEventoClass[0]->plaintext
        );
        #print_r($record);
        scraperwiki::save(array('id'), $record);  
    }
} else $flag=false;
 
    $i++;
} while ($flag);
?>
<?php
$baseurl="http://www.eventiesagre.it";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$i=0;
$flag=true;
$numeroEvento= 0;
do {
    $html = scraperWiki::scrape("http://www.eventiesagre.it/pagine/Eventi/sez/mesi/Trentino+Alto+Adige/prov/cit/intit/rilib/861-".$i."-data-DESC-nav.htm");        

$dom->load($html);

if ($dom->find("tr.elenco1") != null ){
    foreach($dom->find("tr.elenco1") as $data){
        
        $numeroEvento++;
    
        $tds = $data->find("td");
    
        #tiplogia
        $tipologiaClass = $tds[1]->find("span.category");
        $tipologiaPos = $tds[1]->children(0)->plaintext;
        $tipologiaCheck = false;
        if ($tipologiaClass[0]->plaintext==$tipologiaPos) $tipologiaCheck = true;
    
        #nome evento
        $nomeEventoClass = $tds[1]->find("a.summary");
        $nomeEventoPos = $tds[1]->children(2)->plaintext;
        $nomeEventoCheck = false;
        if ($nomeEventoClass[0]->plaintext==$nomeEventoPos) $nomeEventoCheck = true;
    
        #url evento
        $urlEventoClass = $nomeEventoClass[0]->href;
        $urlEventoPos = $tds[1]->children(2)->href;
        $urlEventoCheck = false;
        if ($urlEventoClass==$urlEventoPos) $urlEventoCheck = true;
    
        #data inizio
        $dataInizioClass = $tds[1]->find("span.dtstart");
        if ($dataInizioClass != null) $dataInizioIso = $dataInizioClass[0]->children(0)->title;
    
        #data fine
        $dataFineClass = $tds[1]->find("span.dtend");
        if ($dataFineClass != null) $dataFineIso = $dataFineClass[0]->children(0)->title;
    
        #luogo
        $luogoClass = $tds[1]->find("span.location");
        $luogoRegione = $luogoClass[0]->children(0)->plaintext;
        if ($luogoClass[0]->children(2)->plaintext=="") {
            $luogoProvincia = $luogoClass[0]->children(1)->plaintext;
            $luogoLocalita="";
        } else {
            $luogoLocalita = $luogoClass[0]->children(1)->plaintext;
            $luogoProvincia = $luogoClass[0]->children(2)->plaintext;
        }
    
        #descrizione
        $descrizioneEventoClass = $tds[1]->find("span.description");
    
        
        $record = array(
            'id' => $numeroEvento,
            'tipologiaPos' => $tipologiaPos,
            'tipologiaClass' => $tipologiaClass[0]->plaintext,
            'tipologiaCheck' => $tipologiaCheck,
            'nomeEventoPos' => $nomeEventoPos,
            'nomeEventoClass' => $nomeEventoClass[0]->plaintext,
            'nomeEventoCheck' => $nomeEventoCheck,
            'urlEventoPos' => $baseurl.$urlEventoPos,
            'urlEventoClass' => $baseurl.$urlEventoClass,
            'urlEventoCheck' => $urlEventoCheck,
            'dataInizioClass' => $dataInizioClass[0]->plaintext,
            'dataInizioIso' => $dataInizioIso,
            'luogoRegione' => $luogoRegione,
            'luogoProvincia' => $luogoProvincia,
            'luogoLocalita' => $luogoLocalita,
            'descrizioneEvento' => $descrizioneEventoClass[0]->plaintext
        );
        #print_r($record);
        scraperwiki::save(array('id'), $record);  
    }
} else $flag=false;
 
    $i++;
} while ($flag);
?>
