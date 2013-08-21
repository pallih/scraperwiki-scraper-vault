<?php

/**
 * @author        Eko Fedriyanto
 * @contact        echo.firstson@gmail.com
 * @created        21/9/2011 22:57
 * @copyright    2011
 */
// <!-- phpDesigner :: Timestamp [9/21/2011 22:57:00 PM] -->

require_once 'scraperwiki/simple_html_dom.php';

function run_ml($q_num = 0)
{

    $html = scraperWiki::scrape("http://musiklegal.com/search/result/a/" . $q_num);

    $dom = new simple_html_dom();

    $dom->load($html);

    foreach ($dom->find("tr") as $data) {

        $tds = $data->find("td");

        $temp_data = explode('">', str_replace('</<strong>a</strong>>', '', str_replace
            ('<<strong>a</strong> href="http://musiklegal.com/song/detail/', '', $tds[1]->
            plaintext)));

        $record = array('No' => str_replace('.', '', $tds[0]->plaintext), 'Code' => $temp_data[0],
            'Song Title' => $temp_data[1], 'Artist' => $tds[2]->plaintext, 'Album' => $tds[3]->
            plaintext);


        /*
        *  Stores results
        */

        scraperwiki::save_sqlite(array("No"), $record);

        unset($temp_data);

    }

    foreach ($dom->find("a") as $a) {
        if ($a->plaintext == 'Next') {
            $tmp_a = $a->href;
            $tmp_a = str_replace('http://musiklegal.com/search/result/a/', '', $tmp_a);


            if ($tmp_a > 0)
                continue;
        }
    }

    if ((int)$tmp_a != 0) {
        run_ml($tmp_a);
    } else {
        exit();
    }

}


//run_ml(18810);
/*
$last_id_array = scraperwiki::sqliteexecute("select count(*) as C from swdata");

if ($last_id_array)
{
    $tmp_c = (int)$last_id_array->data[0][0];

    $c = $tmp_c - 1; 

} else {

    $c = 0;
}
*/

run_ml(341670);

?>