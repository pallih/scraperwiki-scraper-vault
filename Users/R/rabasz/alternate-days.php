<?php

scraperwiki::sqliteexecute("drop table if exists swdata"); 
scraperwiki::sqlitecommit();

$oldnap = scraperwiki::get_var('which-table');

if ($oldnap == 1)
    {
    scraperwiki::save_var('which-table', 2); 
    }
    else
    {
    scraperwiki::save_var('which-table', 1); 
    }

//select "swdata2"."id" from `swdata2` left join "swdata1" on "swdata2"."id"="swdata1"."id" where "swdata1"."id" is null

scraperwiki::attach("uj-hasznaltauto-kodok", "src");
$newvalue=scraperwiki::select("* from src.swvariables");

if ($newvalue[0]['value_blob']=="1")
    {
    $query = "swdata2.url from swdata2 left join swdata1 on swdata2.id=swdata1.id where swdata1.id is null";
    }
    else
    {
    $query = "swdata1.url from swdata1 left join swdata2 on swdata1.id=swdata2.id where swdata2.id is null";
    }

$newcars = scraperwiki::select($query);
print $query . "\n";


foreach ($newcars as $carurl=>$url){
    $newurl = $url['url']; 
     print $newurl . "\n";
 }       

?>
