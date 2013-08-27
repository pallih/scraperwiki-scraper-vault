<?php

define('DEF_BASE_URL', 'http://webservice.recruit.co.jp/shingaku');
define('DEF_SCHOOL_URL', DEF_BASE_URL . '/school/v2/?key=bbf5de40fff8793b&area=01,02,03,04,05,06,07,08,09&format=json&count=%d&start=%d');
define('DEF_CAMPUS_URL', DEF_BASE_URL . '/campus/v2/?key=bbf5de40fff8793b&pref=%s&format=json&count=%d&start=%d');

define('DEF_TABLE_SCHOOL', 'shingaku_school');
define('DEF_TABLE_CAMPUS', 'shingaku_campus');
define('DEF_GET_COUNT', 100);

main();

function main(){
    init();
    updateSchool();
//    updateCampus();

}

function init(){
    mb_internal_encoding('UTF-8');
}

//========================================

function updateSchool(){
    cleaningSchoolTable();
    getSchool();
}

function cleaningSchoolTable(){
    $tableName = DEF_TABLE_SCHOOL;
    scraperwiki::sqliteexecute("drop table if exists $tableName");

    $createTableSQL = <<<_END_SQL_
CREATE TABLE `$tableName` (
    `school_cd` string, 
    `school_name` string,
    `school_name_kana` string,
    `school_category_cd` string,
    `school_category_name` string,
    `title` string,
    `desc` string,
    PRIMARY KEY(
        `school_cd`
    )
)
_END_SQL_;

    scraperwiki::sqliteexecute($createTableSQL);
}


function getSchool(){
    
    $offset = 1;
    $total = null;

    do {
        $response = file_get_contents(sprintf(DEF_SCHOOL_URL, DEF_GET_COUNT, $offset));
        if($response === false) break;;
        $json = json_decode($response);

        if($total === null){
            $total = $json->{'results'}->{'results_available'};
print "total:" . $total . "\n";
        }

        if(!$total){
            break;
        }

        $record = array();
        foreach($json->{'results'}->{'school'} as $school){
            $record[] = array(
                'school_cd' => $school->{'code'},
                'school_name' => $school->{'name'},
                'school_name_kana' => $school->{'kana'},
                'title' => $school->{'title'},
                'desc' => $school->{'desc'},
                'school_category_cd' => $school->{'category'}->{'code'},
                'school_category_name' => $school->{'category'}->{'name'},
            );
        }
        scraperwiki::save_sqlite(array('school_cd'), $record, DEF_TABLE_SCHOOL);
        $offset += DEF_GET_COUNT;
print "offset:" . $offset . "\n";
        sleep(0.5);

    } while ($offset < $total);
}


//=======================================


function updateCampus(){
    cleaningCampusTable();

    $prefList = _getPrefList();
    for($i = 0; $i < 5; $i++){
        $list = array_slice($prefList, $i*10, 10);
        _getCampus(implode(",", $list));
    }

}


function cleaningCampusTable(){

    $tableName = DEF_TABLE_CAMPUS;
    scraperwiki::sqliteexecute("drop table if exists $tableName");

    $createTableSQL = <<<_END_SQL_
CREATE TABLE `$tableName` (
    `campus_cd` string, 
    `campus_name` string,
    `school_cd` string, 
    `school_name` string, 
    `school_category_cd` string, 
    `school_category_name` string, 
    `zip` string,
    `address` string,
    `latitude` blob,
    `longitude` blob,
    PRIMARY KEY(
        `campus_cd`
    )
)
_END_SQL_;

    scraperwiki::sqliteexecute($createTableSQL);

}

function _getPrefList(){
    $prefList = array();
    for($i = 1; $i <= 47; $i++){
        $prefList[] = sprintf('%02d', $i);
    }
    return $prefList;
}


function _getCampus($prefCd){
    
    $offset = 1;
    $total = null;

    do {
        $response = file_get_contents(sprintf(DEF_CAMPUS_URL, $prefCd, DEF_GET_COUNT, $offset));
        if($response === false) break;;
        $json = json_decode($response);

        if($total === null){
            $total = $json->{'results'}->{'results_available'};
print "total:" . $total . "\n";
        }

        if(!$total){
            break;
        }

        $record = array();
        foreach($json->{'results'}->{'campus'} as $campus){
            $record[] = array(
                'campus_cd' => $campus->{'code'},
                'campus_name' => $campus->{'name'},
                'school_cd' => $campus->{'school'}->{'code'},
                'school_name' => $campus->{'school'}->{'name'},
                'school_category_cd' => $campus->{'school'}->{'category'}->{'code'},
                'school_category_name' => $campus->{'school'}->{'category'}->{'name'},
                'zip' => $campus->{'zip'},
                'address' => $campus->{'address'},
                'latitude' => $campus->{'latitude'},
                'longitude' => $campus->{'longitude'},
            );
        }
        scraperwiki::save_sqlite(array('campus_cd'), $record, DEF_TABLE_CAMPUS);
        $offset += DEF_GET_COUNT;
print "offset:" . $offset . "\n";
        sleep(0.5);

    } while ($offset < $total);
}

?>
<?php

define('DEF_BASE_URL', 'http://webservice.recruit.co.jp/shingaku');
define('DEF_SCHOOL_URL', DEF_BASE_URL . '/school/v2/?key=bbf5de40fff8793b&area=01,02,03,04,05,06,07,08,09&format=json&count=%d&start=%d');
define('DEF_CAMPUS_URL', DEF_BASE_URL . '/campus/v2/?key=bbf5de40fff8793b&pref=%s&format=json&count=%d&start=%d');

define('DEF_TABLE_SCHOOL', 'shingaku_school');
define('DEF_TABLE_CAMPUS', 'shingaku_campus');
define('DEF_GET_COUNT', 100);

main();

function main(){
    init();
    updateSchool();
//    updateCampus();

}

function init(){
    mb_internal_encoding('UTF-8');
}

//========================================

function updateSchool(){
    cleaningSchoolTable();
    getSchool();
}

function cleaningSchoolTable(){
    $tableName = DEF_TABLE_SCHOOL;
    scraperwiki::sqliteexecute("drop table if exists $tableName");

    $createTableSQL = <<<_END_SQL_
CREATE TABLE `$tableName` (
    `school_cd` string, 
    `school_name` string,
    `school_name_kana` string,
    `school_category_cd` string,
    `school_category_name` string,
    `title` string,
    `desc` string,
    PRIMARY KEY(
        `school_cd`
    )
)
_END_SQL_;

    scraperwiki::sqliteexecute($createTableSQL);
}


function getSchool(){
    
    $offset = 1;
    $total = null;

    do {
        $response = file_get_contents(sprintf(DEF_SCHOOL_URL, DEF_GET_COUNT, $offset));
        if($response === false) break;;
        $json = json_decode($response);

        if($total === null){
            $total = $json->{'results'}->{'results_available'};
print "total:" . $total . "\n";
        }

        if(!$total){
            break;
        }

        $record = array();
        foreach($json->{'results'}->{'school'} as $school){
            $record[] = array(
                'school_cd' => $school->{'code'},
                'school_name' => $school->{'name'},
                'school_name_kana' => $school->{'kana'},
                'title' => $school->{'title'},
                'desc' => $school->{'desc'},
                'school_category_cd' => $school->{'category'}->{'code'},
                'school_category_name' => $school->{'category'}->{'name'},
            );
        }
        scraperwiki::save_sqlite(array('school_cd'), $record, DEF_TABLE_SCHOOL);
        $offset += DEF_GET_COUNT;
print "offset:" . $offset . "\n";
        sleep(0.5);

    } while ($offset < $total);
}


//=======================================


function updateCampus(){
    cleaningCampusTable();

    $prefList = _getPrefList();
    for($i = 0; $i < 5; $i++){
        $list = array_slice($prefList, $i*10, 10);
        _getCampus(implode(",", $list));
    }

}


function cleaningCampusTable(){

    $tableName = DEF_TABLE_CAMPUS;
    scraperwiki::sqliteexecute("drop table if exists $tableName");

    $createTableSQL = <<<_END_SQL_
CREATE TABLE `$tableName` (
    `campus_cd` string, 
    `campus_name` string,
    `school_cd` string, 
    `school_name` string, 
    `school_category_cd` string, 
    `school_category_name` string, 
    `zip` string,
    `address` string,
    `latitude` blob,
    `longitude` blob,
    PRIMARY KEY(
        `campus_cd`
    )
)
_END_SQL_;

    scraperwiki::sqliteexecute($createTableSQL);

}

function _getPrefList(){
    $prefList = array();
    for($i = 1; $i <= 47; $i++){
        $prefList[] = sprintf('%02d', $i);
    }
    return $prefList;
}


function _getCampus($prefCd){
    
    $offset = 1;
    $total = null;

    do {
        $response = file_get_contents(sprintf(DEF_CAMPUS_URL, $prefCd, DEF_GET_COUNT, $offset));
        if($response === false) break;;
        $json = json_decode($response);

        if($total === null){
            $total = $json->{'results'}->{'results_available'};
print "total:" . $total . "\n";
        }

        if(!$total){
            break;
        }

        $record = array();
        foreach($json->{'results'}->{'campus'} as $campus){
            $record[] = array(
                'campus_cd' => $campus->{'code'},
                'campus_name' => $campus->{'name'},
                'school_cd' => $campus->{'school'}->{'code'},
                'school_name' => $campus->{'school'}->{'name'},
                'school_category_cd' => $campus->{'school'}->{'category'}->{'code'},
                'school_category_name' => $campus->{'school'}->{'category'}->{'name'},
                'zip' => $campus->{'zip'},
                'address' => $campus->{'address'},
                'latitude' => $campus->{'latitude'},
                'longitude' => $campus->{'longitude'},
            );
        }
        scraperwiki::save_sqlite(array('campus_cd'), $record, DEF_TABLE_CAMPUS);
        $offset += DEF_GET_COUNT;
print "offset:" . $offset . "\n";
        sleep(0.5);

    } while ($offset < $total);
}

?>
<?php

define('DEF_BASE_URL', 'http://webservice.recruit.co.jp/shingaku');
define('DEF_SCHOOL_URL', DEF_BASE_URL . '/school/v2/?key=bbf5de40fff8793b&area=01,02,03,04,05,06,07,08,09&format=json&count=%d&start=%d');
define('DEF_CAMPUS_URL', DEF_BASE_URL . '/campus/v2/?key=bbf5de40fff8793b&pref=%s&format=json&count=%d&start=%d');

define('DEF_TABLE_SCHOOL', 'shingaku_school');
define('DEF_TABLE_CAMPUS', 'shingaku_campus');
define('DEF_GET_COUNT', 100);

main();

function main(){
    init();
    updateSchool();
//    updateCampus();

}

function init(){
    mb_internal_encoding('UTF-8');
}

//========================================

function updateSchool(){
    cleaningSchoolTable();
    getSchool();
}

function cleaningSchoolTable(){
    $tableName = DEF_TABLE_SCHOOL;
    scraperwiki::sqliteexecute("drop table if exists $tableName");

    $createTableSQL = <<<_END_SQL_
CREATE TABLE `$tableName` (
    `school_cd` string, 
    `school_name` string,
    `school_name_kana` string,
    `school_category_cd` string,
    `school_category_name` string,
    `title` string,
    `desc` string,
    PRIMARY KEY(
        `school_cd`
    )
)
_END_SQL_;

    scraperwiki::sqliteexecute($createTableSQL);
}


function getSchool(){
    
    $offset = 1;
    $total = null;

    do {
        $response = file_get_contents(sprintf(DEF_SCHOOL_URL, DEF_GET_COUNT, $offset));
        if($response === false) break;;
        $json = json_decode($response);

        if($total === null){
            $total = $json->{'results'}->{'results_available'};
print "total:" . $total . "\n";
        }

        if(!$total){
            break;
        }

        $record = array();
        foreach($json->{'results'}->{'school'} as $school){
            $record[] = array(
                'school_cd' => $school->{'code'},
                'school_name' => $school->{'name'},
                'school_name_kana' => $school->{'kana'},
                'title' => $school->{'title'},
                'desc' => $school->{'desc'},
                'school_category_cd' => $school->{'category'}->{'code'},
                'school_category_name' => $school->{'category'}->{'name'},
            );
        }
        scraperwiki::save_sqlite(array('school_cd'), $record, DEF_TABLE_SCHOOL);
        $offset += DEF_GET_COUNT;
print "offset:" . $offset . "\n";
        sleep(0.5);

    } while ($offset < $total);
}


//=======================================


function updateCampus(){
    cleaningCampusTable();

    $prefList = _getPrefList();
    for($i = 0; $i < 5; $i++){
        $list = array_slice($prefList, $i*10, 10);
        _getCampus(implode(",", $list));
    }

}


function cleaningCampusTable(){

    $tableName = DEF_TABLE_CAMPUS;
    scraperwiki::sqliteexecute("drop table if exists $tableName");

    $createTableSQL = <<<_END_SQL_
CREATE TABLE `$tableName` (
    `campus_cd` string, 
    `campus_name` string,
    `school_cd` string, 
    `school_name` string, 
    `school_category_cd` string, 
    `school_category_name` string, 
    `zip` string,
    `address` string,
    `latitude` blob,
    `longitude` blob,
    PRIMARY KEY(
        `campus_cd`
    )
)
_END_SQL_;

    scraperwiki::sqliteexecute($createTableSQL);

}

function _getPrefList(){
    $prefList = array();
    for($i = 1; $i <= 47; $i++){
        $prefList[] = sprintf('%02d', $i);
    }
    return $prefList;
}


function _getCampus($prefCd){
    
    $offset = 1;
    $total = null;

    do {
        $response = file_get_contents(sprintf(DEF_CAMPUS_URL, $prefCd, DEF_GET_COUNT, $offset));
        if($response === false) break;;
        $json = json_decode($response);

        if($total === null){
            $total = $json->{'results'}->{'results_available'};
print "total:" . $total . "\n";
        }

        if(!$total){
            break;
        }

        $record = array();
        foreach($json->{'results'}->{'campus'} as $campus){
            $record[] = array(
                'campus_cd' => $campus->{'code'},
                'campus_name' => $campus->{'name'},
                'school_cd' => $campus->{'school'}->{'code'},
                'school_name' => $campus->{'school'}->{'name'},
                'school_category_cd' => $campus->{'school'}->{'category'}->{'code'},
                'school_category_name' => $campus->{'school'}->{'category'}->{'name'},
                'zip' => $campus->{'zip'},
                'address' => $campus->{'address'},
                'latitude' => $campus->{'latitude'},
                'longitude' => $campus->{'longitude'},
            );
        }
        scraperwiki::save_sqlite(array('campus_cd'), $record, DEF_TABLE_CAMPUS);
        $offset += DEF_GET_COUNT;
print "offset:" . $offset . "\n";
        sleep(0.5);

    } while ($offset < $total);
}

?>
