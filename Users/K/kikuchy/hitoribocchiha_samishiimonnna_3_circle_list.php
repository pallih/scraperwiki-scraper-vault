<?php
$imgpath_prefix = "http://www.sdf-event.info/mform/cutfile";
$html = mb_convert_encoding(scraperWiki::scrape("http://www.sdf-event.info/mform/cutfile/c_list_hs3.php"),
            "UTF-8", "EUC");
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table") as $table){
    $trs = $table->find("tr");
    $tr_title = $trs[0];
    $tr_image = $trs[1];
    $tds = $tr_title->find("td");
    $str_owner = $tds[1]->plaintext;
    $ary_circle = mb_split("/\s\s\s　　/", $tds[0]->plaintext);
    $str_circlename = $ary_circle[0];
    $str_space = $ary_circle[1];
    $dom_a = $tds[0]->find("a", 0);
//print $dom_a->href."\n";
    $str_address = "";
    $str_address = $dom_a->href;
    $str_imgpath = $imgpath_prefix.substr($tr_image->find("td img", 0)->src, 1);
    $record = array(
        "circle_name" => $str_circlename,
        "space_no" => $str_space,
        "owner" => $str_owner,
        "circle_cut" => $str_imgpath,
        "circle_site" => $str_address
    );
    scraperwiki::save(array('circle_name'), $record);
}

?>
<?php
$imgpath_prefix = "http://www.sdf-event.info/mform/cutfile";
$html = mb_convert_encoding(scraperWiki::scrape("http://www.sdf-event.info/mform/cutfile/c_list_hs3.php"),
            "UTF-8", "EUC");
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table") as $table){
    $trs = $table->find("tr");
    $tr_title = $trs[0];
    $tr_image = $trs[1];
    $tds = $tr_title->find("td");
    $str_owner = $tds[1]->plaintext;
    $ary_circle = mb_split("/\s\s\s　　/", $tds[0]->plaintext);
    $str_circlename = $ary_circle[0];
    $str_space = $ary_circle[1];
    $dom_a = $tds[0]->find("a", 0);
//print $dom_a->href."\n";
    $str_address = "";
    $str_address = $dom_a->href;
    $str_imgpath = $imgpath_prefix.substr($tr_image->find("td img", 0)->src, 1);
    $record = array(
        "circle_name" => $str_circlename,
        "space_no" => $str_space,
        "owner" => $str_owner,
        "circle_cut" => $str_imgpath,
        "circle_site" => $str_address
    );
    scraperwiki::save(array('circle_name'), $record);
}

?>
