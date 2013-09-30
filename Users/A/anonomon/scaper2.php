<?php

require 'scraperwiki/simple_html_dom.php';           
//$html_content = scraperwiki::scrape("http://www.photon-database.com/solarmodule_en.aspx");
//$html = str_get_html($html_content);
//$myarr = array();
//foreach ($html->find("select#DropDownList_Hersteller option") as $el) {           
    //echo $el->value . " = " . $el->innertext . "\n";
//    $myarr[] = array("ID"=>$el->value, "NAME"=>$el->innertext);
//}
//scraperwiki::save_sqlite(array("ID"), $myarr);
$data = array();
$i = 0;
//Last offset 300
foreach(scraperwiki::select("* from swdata limit 100 offset 300") as $query)
{
    $html_content = scraperwiki::scrape("http://www.photon-database.com/solarmodule_en.aspx?hersteller=".$query["ID"]."&current=True");
    $html = str_get_html($html_content);
    foreach ($html->find("select#ListBox_Solartypen option") as $el) {
        $data[] = array("ID"=>$query["ID"], "NAME"=>$query["NAME"], "mID"=>$el->value, "mNAME"=>$el->innertext);
    }
}
scraperwiki::save_sqlite(array("mID"), $data, $table_name="models", $verbose=0);

?>
<?php

require 'scraperwiki/simple_html_dom.php';           
//$html_content = scraperwiki::scrape("http://www.photon-database.com/solarmodule_en.aspx");
//$html = str_get_html($html_content);
//$myarr = array();
//foreach ($html->find("select#DropDownList_Hersteller option") as $el) {           
    //echo $el->value . " = " . $el->innertext . "\n";
//    $myarr[] = array("ID"=>$el->value, "NAME"=>$el->innertext);
//}
//scraperwiki::save_sqlite(array("ID"), $myarr);
$data = array();
$i = 0;
//Last offset 300
foreach(scraperwiki::select("* from swdata limit 100 offset 300") as $query)
{
    $html_content = scraperwiki::scrape("http://www.photon-database.com/solarmodule_en.aspx?hersteller=".$query["ID"]."&current=True");
    $html = str_get_html($html_content);
    foreach ($html->find("select#ListBox_Solartypen option") as $el) {
        $data[] = array("ID"=>$query["ID"], "NAME"=>$query["NAME"], "mID"=>$el->value, "mNAME"=>$el->innertext);
    }
}
scraperwiki::save_sqlite(array("mID"), $data, $table_name="models", $verbose=0);

?>
