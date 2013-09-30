<?php

$tableName = DEF_TABLE_SCHOOL;
scraperwiki::sqliteexecute("drop table if exists test");

$createTableSQL = <<<_END_SQL_
CREATE TABLE `test` (
    `id` string, 
    `latitude_string` string,
    `longitude_string` string,
    `latitude_real` real,
    `longitude_real` real,
    `latitude` blob,
    `longitude` blob,
    PRIMARY KEY(
        `id`
    )
)
_END_SQL_;

scraperwiki::sqliteexecute($createTableSQL);

$record = array(
    array(
        id => '1', 
        'latitude_string' => '37.0436550874401',
        'longitude_string' => '136.94928386031',
        'latitude_real' => '37.0436550874401',
        'longitude_real' => '136.94928386031',
        'latitude' => '37.0436550874401',
        'longitude' => '136.94928386031',
    ),
);

scraperwiki::save_sqlite(array('id'), $record, 'test');

?>
<?php

$tableName = DEF_TABLE_SCHOOL;
scraperwiki::sqliteexecute("drop table if exists test");

$createTableSQL = <<<_END_SQL_
CREATE TABLE `test` (
    `id` string, 
    `latitude_string` string,
    `longitude_string` string,
    `latitude_real` real,
    `longitude_real` real,
    `latitude` blob,
    `longitude` blob,
    PRIMARY KEY(
        `id`
    )
)
_END_SQL_;

scraperwiki::sqliteexecute($createTableSQL);

$record = array(
    array(
        id => '1', 
        'latitude_string' => '37.0436550874401',
        'longitude_string' => '136.94928386031',
        'latitude_real' => '37.0436550874401',
        'longitude_real' => '136.94928386031',
        'latitude' => '37.0436550874401',
        'longitude' => '136.94928386031',
    ),
);

scraperwiki::save_sqlite(array('id'), $record, 'test');

?>
<?php

$tableName = DEF_TABLE_SCHOOL;
scraperwiki::sqliteexecute("drop table if exists test");

$createTableSQL = <<<_END_SQL_
CREATE TABLE `test` (
    `id` string, 
    `latitude_string` string,
    `longitude_string` string,
    `latitude_real` real,
    `longitude_real` real,
    `latitude` blob,
    `longitude` blob,
    PRIMARY KEY(
        `id`
    )
)
_END_SQL_;

scraperwiki::sqliteexecute($createTableSQL);

$record = array(
    array(
        id => '1', 
        'latitude_string' => '37.0436550874401',
        'longitude_string' => '136.94928386031',
        'latitude_real' => '37.0436550874401',
        'longitude_real' => '136.94928386031',
        'latitude' => '37.0436550874401',
        'longitude' => '136.94928386031',
    ),
);

scraperwiki::save_sqlite(array('id'), $record, 'test');

?>
<?php

$tableName = DEF_TABLE_SCHOOL;
scraperwiki::sqliteexecute("drop table if exists test");

$createTableSQL = <<<_END_SQL_
CREATE TABLE `test` (
    `id` string, 
    `latitude_string` string,
    `longitude_string` string,
    `latitude_real` real,
    `longitude_real` real,
    `latitude` blob,
    `longitude` blob,
    PRIMARY KEY(
        `id`
    )
)
_END_SQL_;

scraperwiki::sqliteexecute($createTableSQL);

$record = array(
    array(
        id => '1', 
        'latitude_string' => '37.0436550874401',
        'longitude_string' => '136.94928386031',
        'latitude_real' => '37.0436550874401',
        'longitude_real' => '136.94928386031',
        'latitude' => '37.0436550874401',
        'longitude' => '136.94928386031',
    ),
);

scraperwiki::save_sqlite(array('id'), $record, 'test');

?>
