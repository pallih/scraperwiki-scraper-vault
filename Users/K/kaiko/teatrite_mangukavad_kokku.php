<?php
$teatrid = array(
      array('id' => 1, "nimi" => 'Tallinna Linnateater', 'url' => 'http://www.linnateater.ee/', 'scraper' => 'wwwlinnateateree_-_mangukava', 'pilet' => 'plevi', "hind" => "null")
    , array('id' => 2, "nimi" => 'Eesti Draamateater',   'url' => 'http://www.draamateater.ee/','scraper' => 'draamateatereeplaylist', 'pilet' => 'pmaailm', "hind" => "null")
    , array('id' => 3, "nimi" => 'Ugala',                'url' => 'http://www.ugala.ee/',       'scraper' => 'ugalaee_-_mangukava', 'pilet' => 'pmaailm', 'hind' => "hind")
);

function q($id, $scraper, $p, $hind = 'hind') {
    scraperwiki::attach($scraper);
    return scraperwiki::select("$id as teater,aeg,tiitel,asukoht,null,link,$hind,valjamuudud,reserveeritud,coalesce(lisainfo,'') as lisainfo,$p from `$scraper`.kava");
}

$kava = array();
foreach($teatrid as $t) $kava = array_merge($kava, q($t['id'], $t['scraper'], $t['pilet'], $t['hind']));

# set ID
foreach($kava as $id => $k) $kava[$id]['id'] = $id+1;
print "Kokku: " . count($kava) . "\n";
#print_r($kava[0]);

# extract piletimaailm and piletilevi for separate tables
$pmaailm = array();
$plevi   = array();
foreach ($kava as $k) {
    $s = 'pmaailm'; if (!empty($k[$s])) { $pmaailm[] = array('etendus' => $k['id'], 'osta_url' => $k[$s]); unset($k[$s]); }
    $s = 'plevi';   if (!empty($k[$s])) { $plevi[]   = array('etendus' => $k['id'], 'osta_url' => $k[$s]); unset($k[$s]); }
}

scraperwiki::save_sqlite(array('id'), $teatrid, 'teatrid');
scraperwiki::save_sqlite(array('id'), $kava,    'kava');
scraperwiki::save_sqlite(array('etendus'), $plevi,   'plevi');
scraperwiki::save_sqlite(array('etendus'), $pmaailm, 'pmaailm');<?php
$teatrid = array(
      array('id' => 1, "nimi" => 'Tallinna Linnateater', 'url' => 'http://www.linnateater.ee/', 'scraper' => 'wwwlinnateateree_-_mangukava', 'pilet' => 'plevi', "hind" => "null")
    , array('id' => 2, "nimi" => 'Eesti Draamateater',   'url' => 'http://www.draamateater.ee/','scraper' => 'draamateatereeplaylist', 'pilet' => 'pmaailm', "hind" => "null")
    , array('id' => 3, "nimi" => 'Ugala',                'url' => 'http://www.ugala.ee/',       'scraper' => 'ugalaee_-_mangukava', 'pilet' => 'pmaailm', 'hind' => "hind")
);

function q($id, $scraper, $p, $hind = 'hind') {
    scraperwiki::attach($scraper);
    return scraperwiki::select("$id as teater,aeg,tiitel,asukoht,null,link,$hind,valjamuudud,reserveeritud,coalesce(lisainfo,'') as lisainfo,$p from `$scraper`.kava");
}

$kava = array();
foreach($teatrid as $t) $kava = array_merge($kava, q($t['id'], $t['scraper'], $t['pilet'], $t['hind']));

# set ID
foreach($kava as $id => $k) $kava[$id]['id'] = $id+1;
print "Kokku: " . count($kava) . "\n";
#print_r($kava[0]);

# extract piletimaailm and piletilevi for separate tables
$pmaailm = array();
$plevi   = array();
foreach ($kava as $k) {
    $s = 'pmaailm'; if (!empty($k[$s])) { $pmaailm[] = array('etendus' => $k['id'], 'osta_url' => $k[$s]); unset($k[$s]); }
    $s = 'plevi';   if (!empty($k[$s])) { $plevi[]   = array('etendus' => $k['id'], 'osta_url' => $k[$s]); unset($k[$s]); }
}

scraperwiki::save_sqlite(array('id'), $teatrid, 'teatrid');
scraperwiki::save_sqlite(array('id'), $kava,    'kava');
scraperwiki::save_sqlite(array('etendus'), $plevi,   'plevi');
scraperwiki::save_sqlite(array('etendus'), $pmaailm, 'pmaailm');