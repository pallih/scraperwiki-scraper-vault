<?php


// http://www.basketballliga.at/index.php/abl/termine-und-ergebnisse?season_id=75953
$html = scraperWiki::scrape("http://www.basketballliga.at/index.php/abl/termine-und-ergebnisse?season_id=75953");

// http://zms.datasys.at/meldesystem/spiele/DisplaySpiele.jsp?editTermine=false&referees=true&lvId=12&beglaubigt=false&showBestPlayer=false&time=future
//   http://zms.datasys.at/meldesystem/spiele/DisplaySpiele.jsp?editTermine=false&referees=true&lvId=12&beglaubigt=false&showBestPlayer=false&time=future

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$table = $dom->find("table");

$i = 0;

foreach($table[1]->find("tr") as $row){

    $i++;

    if ($i > 2) {
        $tds = $row->find("td");
        if (sizeof($tds) > 2) { //Datum
            $spielnummer= str_replace(' ', '', trim(strip_tags($tds[1]->plaintext)));
            /* $pos = strrpos($date,' ');
            $month = substr($date,$pos+1);
            $days = str_replace(' ', '', substr($date,0,$pos));*/

            $heim = trim(strip_tags($tds[2]->plaintext));
            $gast = trim(strip_tags($tds[3]->plaintext));
            $date = substr(trim(strip_tags($tds[4]->plaintext)),0,10);
            $time = substr(trim(strip_tags($tds[4]->plaintext)),12);
            $ort = trim(strip_tags($tds[5]->plaintext));
            $score = trim(strip_tags($tds[6]->plaintext));
            $hz = trim(strip_tags($tds[7]->plaintext));
            $sr1= trim(strip_tags($tds[8]->plaintext));
            $sr2= trim(strip_tags($tds[9]->plaintext));
            $sr3= trim(strip_tags($tds[10]->plaintext));


            if ($spielnummer != "Spielnummer") {
                $record = array(
                    'id' => $spielnummer,
                    'date' => $date,
                    'time' => $time,
                    'ort' => $ort,
                    'heim' => $heim,
                    'gast' => $gast,
                    'score' => $score,
                    'hz' => $hz,
                    'sr1' => $sr1,
                    'sr2' => $sr2,
                    'sr3' => $sr3
                );
            }
        }

        if (isset($record)) {
            scraperwiki::save(array('id'), $record);
        }

    } 
}


?>
