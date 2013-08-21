<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';  

//scraperwiki::sqliteexecute("create table onoreficenze_url (id int, 'text' string, 'url' string)"); 
//scraperwiki::sqliteexecute("delete from onoreficenze_url");
//scraperwiki::sqlitecommit();  
//print_r(scraperwiki::sqliteexecute("desc uri")); 

for ($i=0;$i<=5561;$i++)
{

    $uri="http://www.quirinale.it/elementi/Onorificenze.aspx";
    echo $page=shell_exec("curl -G -d 'pag=$i' -G -d 'daAnno=1946' -G -d 'aAnno=2013' ".$uri);
    scraperwiki::sqliteexecute("insert into onoreficenze_url values (?,?,?)", array($i, $page, $uri."?pag=".$i."&daAnno=1946&aAnno=2013"));
    scraperwiki::sqlitecommit();   
}


?>
