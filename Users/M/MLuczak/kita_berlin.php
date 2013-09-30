<?php
require 'scraperwiki/simple_html_dom.php';
function checkExistence($in){
    $dom = new simple_html_dom();
    $dom->load($in);
    $title = $dom->getElementByTagName('title')->innertext;
    if(strcmp($title,'Fehler') == 0) return "error";
    try {
        $elem = $dom->getElementById('lblEinrichtung')->first_child()->innertext;
    } catch (Exception $e) {
        var_dump($e);
        return "error";
    }
    $out = $elem;
    return ($out);
}

function parseDetails($name, $id, $in){
    $dom = new simple_html_dom();
    $dom->load($in);
    $data_table = $dom->getElementById('TabelleKitaDetails');
    foreach($data_table->find("tbody tr") as $trs){
        $switch = $trs->childNodes(0)->plaintext;
        switch ($switch) {
            case "Adresse":
                $addr = $trs->childNodes(1)->plaintext;
                break;
            case "Pädagogische Merkmale":
                $concept = $trs->childNodes(1)->plaintext;
                break;
            case "Telefon":
                $tel = $trs->childNodes(1)->plaintext;
                break;
            case "Email":
                $mail = $trs->childNodes(1)->plaintext;
                break;
            case "Internet":
                $web = $trs->childNodes(1)->plaintext;
                break;
            case "Einrichtungsart":
                $type = $trs->childNodes(1)->plaintext;
                break;
            case "Träger":
                $head = $trs->childNodes(1)->plaintext;
                break;
            case "Adresse Träger":
                $head_address = $trs->childNodes(1)->plaintext;
                break;
            case "Trägerart":
                $head_type = $trs->childNodes(1)->plaintext;
                break;
        }
    }
    $record = array('kitaID' => $id, 'kita' => $name, 'address' => $addr, 'telefone' => $tel, 'mail' => $mail, 'web' => $web, 'type' => $type, 'concept' => $concept, 'head' => $head, 'head_address' => $head_address, 'head_type' => $head_type,);
    scraperwiki::save(array('kitaID'), $record);
}

try {
    $latest_data = scraperwiki::sqliteexecute("select kitaID from swdata order by kitaID desc limit 1");
} catch (Exception $e) {
    $latest_data = 0;
}

$next_id = max($latest_data->data[0][0],10056);
for($i=$next_id;$i<=25000;$i++){
    $html = null;
    $url = 'http://www.berlin.de/sen/familie/kindertagesbetreuung/kita_verzeichnis/anwendung/kitaDetails.aspx?ID='.$i;
    while(is_null($html)){
        try {
            $html = scraperwiki::scrape($url);
            $exists = checkExistence($html);
            while(strcmp($exists,"error") == 0){
                print "error -> sleep 5 seconds";
                sleep(5);
                $html = scraperwiki::scrape($url);
                $exists = checkExistence($html);
            }
        } catch (Exception $e) {
            var_dump($e);
            sleep(5);
            $html = null;
        }
    }
    if(strlen($exists)>0){
        var_dump($url);
        parseDetails($exists,$i,$html);
    }
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';
function checkExistence($in){
    $dom = new simple_html_dom();
    $dom->load($in);
    $title = $dom->getElementByTagName('title')->innertext;
    if(strcmp($title,'Fehler') == 0) return "error";
    try {
        $elem = $dom->getElementById('lblEinrichtung')->first_child()->innertext;
    } catch (Exception $e) {
        var_dump($e);
        return "error";
    }
    $out = $elem;
    return ($out);
}

function parseDetails($name, $id, $in){
    $dom = new simple_html_dom();
    $dom->load($in);
    $data_table = $dom->getElementById('TabelleKitaDetails');
    foreach($data_table->find("tbody tr") as $trs){
        $switch = $trs->childNodes(0)->plaintext;
        switch ($switch) {
            case "Adresse":
                $addr = $trs->childNodes(1)->plaintext;
                break;
            case "Pädagogische Merkmale":
                $concept = $trs->childNodes(1)->plaintext;
                break;
            case "Telefon":
                $tel = $trs->childNodes(1)->plaintext;
                break;
            case "Email":
                $mail = $trs->childNodes(1)->plaintext;
                break;
            case "Internet":
                $web = $trs->childNodes(1)->plaintext;
                break;
            case "Einrichtungsart":
                $type = $trs->childNodes(1)->plaintext;
                break;
            case "Träger":
                $head = $trs->childNodes(1)->plaintext;
                break;
            case "Adresse Träger":
                $head_address = $trs->childNodes(1)->plaintext;
                break;
            case "Trägerart":
                $head_type = $trs->childNodes(1)->plaintext;
                break;
        }
    }
    $record = array('kitaID' => $id, 'kita' => $name, 'address' => $addr, 'telefone' => $tel, 'mail' => $mail, 'web' => $web, 'type' => $type, 'concept' => $concept, 'head' => $head, 'head_address' => $head_address, 'head_type' => $head_type,);
    scraperwiki::save(array('kitaID'), $record);
}

try {
    $latest_data = scraperwiki::sqliteexecute("select kitaID from swdata order by kitaID desc limit 1");
} catch (Exception $e) {
    $latest_data = 0;
}

$next_id = max($latest_data->data[0][0],10056);
for($i=$next_id;$i<=25000;$i++){
    $html = null;
    $url = 'http://www.berlin.de/sen/familie/kindertagesbetreuung/kita_verzeichnis/anwendung/kitaDetails.aspx?ID='.$i;
    while(is_null($html)){
        try {
            $html = scraperwiki::scrape($url);
            $exists = checkExistence($html);
            while(strcmp($exists,"error") == 0){
                print "error -> sleep 5 seconds";
                sleep(5);
                $html = scraperwiki::scrape($url);
                $exists = checkExistence($html);
            }
        } catch (Exception $e) {
            var_dump($e);
            sleep(5);
            $html = null;
        }
    }
    if(strlen($exists)>0){
        var_dump($url);
        parseDetails($exists,$i,$html);
    }
}

?>
