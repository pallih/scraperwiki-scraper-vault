<?php

# Blank PHP
//scraperwiki::sqliteexecute("create table consuntivi (id int, year int, q text, file text)");
//scraperwiki::sqliteexecute("insert into ttt values (?,?)", array(9, 'hello'));
//scraperwiki::sqlitecommit();

print_r(scraperwiki::sqliteexecute("select * from consuntivi")); 




?>
