<?php

# Blank PHP

//scraperwiki::sqliteexecute("DROP TABLE last_update");
scraperwiki::sqliteexecute(
    "CREATE TABLE IF NOT EXISTS ll (
        id INTEGER PRIMARY KEY ASC,
        HITs_available int,
        jobs int
    )"
);
scraperwiki::sqliteexecute(
    "CREATE TABLE IF NOT EXISTS ll (
        id INTEGER PRIMARY KEY ASC,
        HITs_available int,
        jobs int
    )"
);
//scraperwiki::sqliteexecute('update ll set jobs = 100 AND (set jobs = 200)');
scraperwiki::sqliteexecute('INSERT INTO ll (jobs) VALUES (100), (200), (300)');
scraperwiki::sqlitecommit();
//


$res = scraperwiki::select('* FROM ll');

print_r($res[0]);
//print_r(scraperwiki::show_tables());  
//print_r(scraperwiki::table_info($name="last_update")); 

?>
<?php

# Blank PHP

//scraperwiki::sqliteexecute("DROP TABLE last_update");
scraperwiki::sqliteexecute(
    "CREATE TABLE IF NOT EXISTS ll (
        id INTEGER PRIMARY KEY ASC,
        HITs_available int,
        jobs int
    )"
);
scraperwiki::sqliteexecute(
    "CREATE TABLE IF NOT EXISTS ll (
        id INTEGER PRIMARY KEY ASC,
        HITs_available int,
        jobs int
    )"
);
//scraperwiki::sqliteexecute('update ll set jobs = 100 AND (set jobs = 200)');
scraperwiki::sqliteexecute('INSERT INTO ll (jobs) VALUES (100), (200), (300)');
scraperwiki::sqlitecommit();
//


$res = scraperwiki::select('* FROM ll');

print_r($res[0]);
//print_r(scraperwiki::show_tables());  
//print_r(scraperwiki::table_info($name="last_update")); 

?>
