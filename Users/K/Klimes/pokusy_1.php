<?php
# Blank PHP
scraperwiki::sqliteexecute("create table Volby ('kandidatka' string, `kandidat` string, 'vek' int, 'navrhujici' string, 'prislusnost' string, 'hlasy' int, 'poradi' int)");           
scraperwiki::sqliteexecute("insert into Volby values (?,?,?,?,?,?,?)", array('CSSD', 'hello', 40, 'CSSD', 'Cssd', 1259, 1));
//scraperwiki::sqliteexecute("insert or replace into ttt values (:xx, :yy)", array("xx"=>10, "yy"=>"again"));


?>
<?php
# Blank PHP
scraperwiki::sqliteexecute("create table Volby ('kandidatka' string, `kandidat` string, 'vek' int, 'navrhujici' string, 'prislusnost' string, 'hlasy' int, 'poradi' int)");           
scraperwiki::sqliteexecute("insert into Volby values (?,?,?,?,?,?,?)", array('CSSD', 'hello', 40, 'CSSD', 'Cssd', 1259, 1));
//scraperwiki::sqliteexecute("insert or replace into ttt values (:xx, :yy)", array("xx"=>10, "yy"=>"again"));


?>
