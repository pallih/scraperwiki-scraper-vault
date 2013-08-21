<?php
require 'scraperwiki/simple_html_dom.php';

//print_r(scraperwiki::show_tables()); 

$url = "http://www.itu.int/oth/T0202.aspx?parent=T0202";

$html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);


//$documents = array();

//scraperwiki::sqliteexecute("drop table if exists 'swdata'"); 
//scraperwiki::sqliteexecute("create table 'swdata' ('prefix' string PRIMARY KEY ASC, 'code' string, 'name' string)");  

foreach ($html->find("option[value*=T0202]") as $el) {

    echo($el."\n");
    $id = $el->value;
    


    preg_match("/(.*)\((.*)\)/",$el->innertext,$matches);

    $prefix = preg_replace( '/\s+/', '', $matches[1] );
    $location_name =  $matches[2];

    scraperwiki::sqliteexecute("insert or replace into 'swdata' values (?,?,?)", array($prefix,'id','location_name'));
    scraperwiki::sqlitecommit();

    print $prefix ;
}




?>
