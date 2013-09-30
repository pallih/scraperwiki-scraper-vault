<?php

require_once 'scraperwiki/simple_html_dom.php';  

$last_id = 0;

$last_id_array = scraperwiki::sqliteexecute("select max(id) from swdata");

if ($last_id_array)
    $last_id = $last_id_array->data[0][0];

$last_id++;


for ($q_num = $last_id; $q_num <=$last_id+500; $q_num ++){

    $html = scraperWiki::scrape("http://questions.assemblee-nationale.fr/q13/13-" . $q_num . "QE.htm");
    
    $dom = new simple_html_dom();
        
    $dom->load($html);
    
    foreach ($dom->find(".tdstyle") as $data) {
    
        /*
         *  Scrapes the content of the question
         */
        foreach ($data->find('h2') as $title) {
            if ($title->plaintext == " Texte de la question") {
    
                foreach ($data->find('.contenutexte') as $contenutexte) {
                    $q_texte = $contenutexte->plaintext;
                }
            }
        }
    }
    
    /*
     *  Scrapes the dates
     */
    
    foreach ($dom->find(".tdstyleh4") as $data) {
        $text = $data->innertext;

        $boldText = $data->find("b");

        //If there is an answer
        $boldTextTypes = Array(
            "q_date" => 0,
            "q_page" => 1,
            "a_date" => 2,
            "a_page" => 3
        );
        
           
        $date_q = "";
        $date_a = "";
        list($q_day, $q_month, $q_year) = explode("/", $boldText[$boldTextTypes["q_date"]]->innertext);
        list($a_day, $a_month, $a_year) = explode("/", $boldText[$boldTextTypes["a_date"]]->innertext);

        $date_q = $q_year.  "-" . $q_month . "-" . $q_day;
        $age_q = abs(time() - strtotime($date_q));

        //proceed if the question was asked more than 90 days ago
        if ($age_q > 90){

            //if there is an answer
            if ($a_month && $a_day && $a_year) {

                $date_a = $a_year . "-" . $a_month . "-" . $a_day;
                
                //delai in seconds
                $diff = abs(strtotime($date_a) - strtotime($date_q));
                //converts to days
                $diff = $diff/86400;                    

                switch (true) {
                    case ($diff < 30):
                        $delai = "mois";
                        break;
                    case ($diff < 90):
                        $delai = "trimestre";
                        break;
                    case ($diff < 180):
                        $delai = "semestre";
                        break;
                    case ($diff < 360):
                        $delai = "annee";
                        break;
                    default:
                        $delai = "sup_annee";
                }
            }
            //If there is no answer
            else {
                $delai = "no_answer";
            }
        }
        
        
    }
    
    /*
     *  Stores results
     */
    
    $result = array(
        "id" => $q_num,
        "q_texte" => utf8_encode($q_texte),
        "q_date" => $date_q,
        "a_date" => $date_a,
        "delai" => utf8_encode($delai)
    );
    
    scraperwiki::save_sqlite(array("id"), $result);    
 
}
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';  

$last_id = 0;

$last_id_array = scraperwiki::sqliteexecute("select max(id) from swdata");

if ($last_id_array)
    $last_id = $last_id_array->data[0][0];

$last_id++;


for ($q_num = $last_id; $q_num <=$last_id+500; $q_num ++){

    $html = scraperWiki::scrape("http://questions.assemblee-nationale.fr/q13/13-" . $q_num . "QE.htm");
    
    $dom = new simple_html_dom();
        
    $dom->load($html);
    
    foreach ($dom->find(".tdstyle") as $data) {
    
        /*
         *  Scrapes the content of the question
         */
        foreach ($data->find('h2') as $title) {
            if ($title->plaintext == " Texte de la question") {
    
                foreach ($data->find('.contenutexte') as $contenutexte) {
                    $q_texte = $contenutexte->plaintext;
                }
            }
        }
    }
    
    /*
     *  Scrapes the dates
     */
    
    foreach ($dom->find(".tdstyleh4") as $data) {
        $text = $data->innertext;

        $boldText = $data->find("b");

        //If there is an answer
        $boldTextTypes = Array(
            "q_date" => 0,
            "q_page" => 1,
            "a_date" => 2,
            "a_page" => 3
        );
        
           
        $date_q = "";
        $date_a = "";
        list($q_day, $q_month, $q_year) = explode("/", $boldText[$boldTextTypes["q_date"]]->innertext);
        list($a_day, $a_month, $a_year) = explode("/", $boldText[$boldTextTypes["a_date"]]->innertext);

        $date_q = $q_year.  "-" . $q_month . "-" . $q_day;
        $age_q = abs(time() - strtotime($date_q));

        //proceed if the question was asked more than 90 days ago
        if ($age_q > 90){

            //if there is an answer
            if ($a_month && $a_day && $a_year) {

                $date_a = $a_year . "-" . $a_month . "-" . $a_day;
                
                //delai in seconds
                $diff = abs(strtotime($date_a) - strtotime($date_q));
                //converts to days
                $diff = $diff/86400;                    

                switch (true) {
                    case ($diff < 30):
                        $delai = "mois";
                        break;
                    case ($diff < 90):
                        $delai = "trimestre";
                        break;
                    case ($diff < 180):
                        $delai = "semestre";
                        break;
                    case ($diff < 360):
                        $delai = "annee";
                        break;
                    default:
                        $delai = "sup_annee";
                }
            }
            //If there is no answer
            else {
                $delai = "no_answer";
            }
        }
        
        
    }
    
    /*
     *  Stores results
     */
    
    $result = array(
        "id" => $q_num,
        "q_texte" => utf8_encode($q_texte),
        "q_date" => $date_q,
        "a_date" => $date_a,
        "delai" => utf8_encode($delai)
    );
    
    scraperwiki::save_sqlite(array("id"), $result);    
 
}
?>
