<?php
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://jobs.pwc.de/html/searchresult.php");
$html = str_get_html($html_content);

foreach ($html->find("table.table_content tr") as $el) {
    print $el . "\n";
    $tds = $el->find("td");
    if(count($tds) > 0){
        //$date = date_create_from_format('d.m.Y', $tds[0]->plaintext);
        $url = "http://jobs.pwc.de" . $tds[1]->first_child()->href;
        $key = md5($tds[0]->plaintext.$tds[1]->plaintext) . "\n";
        //print $url . "\n";
        $record = array(
            'id'        => $key,
            'published' => $tds[0]->plaintext,
            'title'     => $tds[1]->plaintext,
            'level'     => $tds[2]->plaintext,
            'location'  => $tds[3]->plaintext,
            'url'       => $url
        );
        scraperwiki::save(array('id'), $record);
    }
    //$el->__destruct();
}
?>
<?php
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://jobs.pwc.de/html/searchresult.php");
$html = str_get_html($html_content);

foreach ($html->find("table.table_content tr") as $el) {
    print $el . "\n";
    $tds = $el->find("td");
    if(count($tds) > 0){
        //$date = date_create_from_format('d.m.Y', $tds[0]->plaintext);
        $url = "http://jobs.pwc.de" . $tds[1]->first_child()->href;
        $key = md5($tds[0]->plaintext.$tds[1]->plaintext) . "\n";
        //print $url . "\n";
        $record = array(
            'id'        => $key,
            'published' => $tds[0]->plaintext,
            'title'     => $tds[1]->plaintext,
            'level'     => $tds[2]->plaintext,
            'location'  => $tds[3]->plaintext,
            'url'       => $url
        );
        scraperwiki::save(array('id'), $record);
    }
    //$el->__destruct();
}
?>
