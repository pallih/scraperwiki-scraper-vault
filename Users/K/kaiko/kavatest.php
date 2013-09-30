<?php
// paremad URL-id: http://otse.err.ee/saatekavad/tv/:
// ETV: http://otse.err.ee/xml/29-03-2012-etv-2.html
// ETV2: http://otse.err.ee/xml/29-03-2012-etv2-2.html
require 'scraperwiki/simple_html_dom.php';

#$etv_program = fetchETV(1);
#saveTable($etv_program, 'id', 'etv_program');
#$etv_shows = fetchETVShows( array_unique(cutColumn($etv_program, 'show_id')));
#saveTable($etv_shows, 'id', 'etv_shows');

list($kanal2_program, $kanal2_shows) = fetchKanal2Week();
saveTable($kanal2_program, 'id', 'kanal2_program');
saveTable($kanal2_shows,   'id', 'kanal2_shows');

/* destination:
copyWeb(
    'http://kanal2.ee/program/week?date=' . (empty($weekStart) ? date('Y-m-d') : $weekStart),
    'div.saatekava_nadalakava div.dayblock, div.saatekava_nadalakava table.kavatabel tr',
    'span.day, .time, .saade a',
    "SELECT substr(id_1, strlen('saatekava_popup_')) AS show_id FROM _ WHERE ..."
);
problems: 
  - can't do more than one operation on crawled web
  - can't set some variable and fill following fields on top of it (very often date, month or something)
*/

// WORKER FUNCTIONS

function fetchKanal2Week($weekStart = null) {
    $url = 'http://kanal2.ee/program/week?date=' . (empty($weekStart) ? date('Y-m-d') : $weekStart);
    $dom = new simple_html_dom();
    $dom->load(scraperWiki::scrape($url));

    $prog = array();
    $rows = fetchTable($dom,
        'div.saatekava_nadalakava div.dayblock, div.saatekava_nadalakava table.kavatabel tr',
        'span.day, .time, .saade a');
    for ($i = 0; $i < count($rows); $i++) {
        $s = &$rows[$i];
        if (!empty($s['span0'])) {
            $kp = join('-', array_reverse(explode('.', $s['span0'])));
        } else {
            $s['start']   = "$kp $s[td0]:00";
            $s['id']      = strtr("K2$kp$s[td0]", array(':' => '', '-' => ''));
            $s['show_id'] = substr($s['a1_id'], strlen('saatekava_popup_'));
            $prog[] = $s;
        }
    }

    $shows = fetchTable($dom, '.block div[id^="saatekava_popup_content_"]', 'div.title b, div.info; .img img');
    for ($i = 0; $i < count($shows); $i++) {
        $shows[$i]['id'] = substr($shows[$i]['row_id'], strlen('saatekava_popup_content_'));
    }
    return array(
         tableRemap($prog,  'id,show_id,start,title(a1),link(a1_href)')
        ,tableRemap($shows, 'id,title(b0),img(img3_src)')
    );
}

function fetchTV3($dayCount = 10) {
    $url = 'http://www.tv3.ee/index.php?option=com_azpress&channel=tv3&Itemid=610&date='; #2012-03-31
}

function fetchETV($dayCount = 10) {
    // 10 days
    $url = "http://etv.err.ee/index.php?0536614&kuu=";
    $trCSS = '.mid_col_data_out_inner table table tr';
    $tdCSS = 'td[align="right"] b, td[width="100%"] b, td[width="100%"] a; td span.k'; // time, title

    $prog = array();
    for ($day = 0; $day < $dayCount; $day++) {
        $date =  date('Y-m-d', strtotime("today + $day days"));
        $dayList = fetchTable($url . $date, $trCSS, $tdCSS);
        for ($i = 0; $i < count($dayList); $i++) if (!empty($dayList[$i]['b0'])) {
            $s = &$dayList[$i];
            $s['start']   = "$date $s[b0]:00";
            $s['id']      = strtr('ETV' . $date . $s['b0'], array(':' => '', '-' => ''));
            if (!empty($s['a2_href'])) $s['show_id'] = substr($s['a2_href'], 10);
            $prog[] = $s;
        }
    }
    return tableRemap($prog, 'id,show_id,start,title(b1),desc(span3)');
}

function fetchETVShows($showIDList) {
    $url = 'http://etv.err.ee/index.php?';
    if (is_numeric($showIDList)) $showIDList = array($showIDList);
    $shows = array();
    foreach($showIDList as $show_id){
        $r = fetchTable("$url$show_id", 'div.pre_header_area_inner table tr', 'td[align="right"] img');
        if (!empty($r[0])) $shows[] = array('id' => $show_id, 'img' => isset($r[0]['img_src']) ? $r[0]['img0_src'] : null);
    }
    return $shows;
}


// GLOBAL HELPER FUNCTIONS

// src can be simple_html_dom object, url or html
// colCSS may have css selector with semicolon; try this if there some elements may not exists
function fetchTable($src, $rowCSS, $colCSS, $attrList = null) {
    if (is_object($src)) {
        $dom = $src;
    } elseif (is_string($src)) {
        if (is_array(parse_url($src))) {
            $html = scraperWiki::scrape($src);
        } else $html = $src;

        $dom = new simple_html_dom();
        $dom->load($html);
    }
    if (empty($attrList))
        $attrList = explode(' ', 'id src href abbr alt background bgcolor checked style target title type value');
    if (is_string($colCSS))
        $colCSS = explode(';', $colCSS);

    $tr = array();
    $tableColNr = 0;
    $trNodes = array();
    // first search all row nodes
    foreach($dom->find($rowCSS) as $trNr => $trNode) {
        $trNodes[] = $trNode;
        $tr[$trNr] = array();
        foreach($attrList as $attr) if ($trNode->$attr) $tr[$trNr]["row_$attr"] = $trNode->$attr;
    }

    // then walk all column queries and find cells
    for($qNr = 0; $qNr < count($colCSS); $qNr++) {
        $queryColNr = 0;
        for($trNr = 0; $trNr < count($trNodes); $trNr++) {
            $tdNodes = $trNodes[$trNr]->find($colCSS[$qNr]);
            if (count($tdNodes) > $queryColNr) $queryColNr = count($tdNodes);
            for($tdNr = 0; $tdNr < count($tdNodes); $tdNr++) {
                $tdNode = &$tdNodes[$tdNr];
                $prefix = $tdNode->tag . ($tableColNr + $tdNr);
                if ($tdNode->plaintext) $tr[$trNr][$prefix] = $tdNode->plaintext;
                if ($tdNode->innertext) $tr[$trNr][$prefix . '_html'] = $tdNode->innertext;
                foreach($attrList as $attr) if ($tdNode->$attr) $tr[$trNr][$prefix . '_' . $attr] = $tdNode->$attr;
            }
        }
        $tableColNr += $queryColNr;
    }
    return $tr;
}

// scraperwiki dismiss columns where cell content for first row is null :(
function getTableKeys(&$table) {
    $keys = array();
    for ($i = 0; $i < count($table); $i++) $keys = array_unique(array_merge($keys, array_keys($table[$i])));
    return $keys;
}

function saveTable($data, $pkey, $name, $keys = null) {
    if (empty($name)) $name = 'swdata';
    if (is_string($pkey)) $pkey = array($pkey);
    if (empty($keys)) $keys = getTableKeys($data);

    if (!in_array($pkey[0], $keys)) {
        print "Table '$name' have no key '$pkey[0]', adding it";
        for ($i = 0; $i < count($data); $i++) $data[$i][$pkey[0]] = $i + 1;
    }

    scraperwiki::sqliteexecute("drop table if exists $name");
    if ($keys)
    scraperwiki::sqliteexecute("create table $name (" . join(', ', $keys) . ')');
    scraperwiki::save_sqlite($pkey, $data, $name, $keys); 
}

// returns array of one column
function cutColumn($rows, $colname, $addNull = true) {
    $colValues = array();
    for ($i = 0; $i < count($rows); $i++) {
        if (isset($rows[$i][$colname]))
            $colValues[] = $rows[$i][$colname];
        else if ($addNull) $colValues[] = null;
    }
    return $colValues;
}

function tableIndex(&$table, $colname, $unique = true) {
    $idx = array();
    for ($i = 0; $i < count($table); $i++) {
        if ($unique)
            $idx[ $table[$i][$colname] ] = &$table[$i];
        else {
            if (empty($idx[ $table[$i][$colname] ])) 
                $idx[ $table[$i][$colname] ] = array();
            $idx[ $table[$i][$colname] ][] = &$table[$i];
        }
    }
    return $idx;
}

// use like tableRemap($data, 'link(href_1),content(text_1),samenamefield')
function tableRemap($rows, $map) {
    $mapParts = explode(',', $map);
    $map = array();
    foreach($mapParts as $dst) {
        $kv = explode('(', $dst);
        if (count($kv) == 2) {
            list($dst, $src) = $kv;
            $src = substr($src, 0, -1);
        } else $src = $dst;
        $map[] = sprintf('"%s" => isset($el["%s"]) ? $el["%s"] : null', $dst, $src, $src);
    }
    $fn = create_function('$el', 'return array(' . join(', ', $map) . ');');
    return array_map($fn, $rows);
}


?><?php
// paremad URL-id: http://otse.err.ee/saatekavad/tv/:
// ETV: http://otse.err.ee/xml/29-03-2012-etv-2.html
// ETV2: http://otse.err.ee/xml/29-03-2012-etv2-2.html
require 'scraperwiki/simple_html_dom.php';

#$etv_program = fetchETV(1);
#saveTable($etv_program, 'id', 'etv_program');
#$etv_shows = fetchETVShows( array_unique(cutColumn($etv_program, 'show_id')));
#saveTable($etv_shows, 'id', 'etv_shows');

list($kanal2_program, $kanal2_shows) = fetchKanal2Week();
saveTable($kanal2_program, 'id', 'kanal2_program');
saveTable($kanal2_shows,   'id', 'kanal2_shows');

/* destination:
copyWeb(
    'http://kanal2.ee/program/week?date=' . (empty($weekStart) ? date('Y-m-d') : $weekStart),
    'div.saatekava_nadalakava div.dayblock, div.saatekava_nadalakava table.kavatabel tr',
    'span.day, .time, .saade a',
    "SELECT substr(id_1, strlen('saatekava_popup_')) AS show_id FROM _ WHERE ..."
);
problems: 
  - can't do more than one operation on crawled web
  - can't set some variable and fill following fields on top of it (very often date, month or something)
*/

// WORKER FUNCTIONS

function fetchKanal2Week($weekStart = null) {
    $url = 'http://kanal2.ee/program/week?date=' . (empty($weekStart) ? date('Y-m-d') : $weekStart);
    $dom = new simple_html_dom();
    $dom->load(scraperWiki::scrape($url));

    $prog = array();
    $rows = fetchTable($dom,
        'div.saatekava_nadalakava div.dayblock, div.saatekava_nadalakava table.kavatabel tr',
        'span.day, .time, .saade a');
    for ($i = 0; $i < count($rows); $i++) {
        $s = &$rows[$i];
        if (!empty($s['span0'])) {
            $kp = join('-', array_reverse(explode('.', $s['span0'])));
        } else {
            $s['start']   = "$kp $s[td0]:00";
            $s['id']      = strtr("K2$kp$s[td0]", array(':' => '', '-' => ''));
            $s['show_id'] = substr($s['a1_id'], strlen('saatekava_popup_'));
            $prog[] = $s;
        }
    }

    $shows = fetchTable($dom, '.block div[id^="saatekava_popup_content_"]', 'div.title b, div.info; .img img');
    for ($i = 0; $i < count($shows); $i++) {
        $shows[$i]['id'] = substr($shows[$i]['row_id'], strlen('saatekava_popup_content_'));
    }
    return array(
         tableRemap($prog,  'id,show_id,start,title(a1),link(a1_href)')
        ,tableRemap($shows, 'id,title(b0),img(img3_src)')
    );
}

function fetchTV3($dayCount = 10) {
    $url = 'http://www.tv3.ee/index.php?option=com_azpress&channel=tv3&Itemid=610&date='; #2012-03-31
}

function fetchETV($dayCount = 10) {
    // 10 days
    $url = "http://etv.err.ee/index.php?0536614&kuu=";
    $trCSS = '.mid_col_data_out_inner table table tr';
    $tdCSS = 'td[align="right"] b, td[width="100%"] b, td[width="100%"] a; td span.k'; // time, title

    $prog = array();
    for ($day = 0; $day < $dayCount; $day++) {
        $date =  date('Y-m-d', strtotime("today + $day days"));
        $dayList = fetchTable($url . $date, $trCSS, $tdCSS);
        for ($i = 0; $i < count($dayList); $i++) if (!empty($dayList[$i]['b0'])) {
            $s = &$dayList[$i];
            $s['start']   = "$date $s[b0]:00";
            $s['id']      = strtr('ETV' . $date . $s['b0'], array(':' => '', '-' => ''));
            if (!empty($s['a2_href'])) $s['show_id'] = substr($s['a2_href'], 10);
            $prog[] = $s;
        }
    }
    return tableRemap($prog, 'id,show_id,start,title(b1),desc(span3)');
}

function fetchETVShows($showIDList) {
    $url = 'http://etv.err.ee/index.php?';
    if (is_numeric($showIDList)) $showIDList = array($showIDList);
    $shows = array();
    foreach($showIDList as $show_id){
        $r = fetchTable("$url$show_id", 'div.pre_header_area_inner table tr', 'td[align="right"] img');
        if (!empty($r[0])) $shows[] = array('id' => $show_id, 'img' => isset($r[0]['img_src']) ? $r[0]['img0_src'] : null);
    }
    return $shows;
}


// GLOBAL HELPER FUNCTIONS

// src can be simple_html_dom object, url or html
// colCSS may have css selector with semicolon; try this if there some elements may not exists
function fetchTable($src, $rowCSS, $colCSS, $attrList = null) {
    if (is_object($src)) {
        $dom = $src;
    } elseif (is_string($src)) {
        if (is_array(parse_url($src))) {
            $html = scraperWiki::scrape($src);
        } else $html = $src;

        $dom = new simple_html_dom();
        $dom->load($html);
    }
    if (empty($attrList))
        $attrList = explode(' ', 'id src href abbr alt background bgcolor checked style target title type value');
    if (is_string($colCSS))
        $colCSS = explode(';', $colCSS);

    $tr = array();
    $tableColNr = 0;
    $trNodes = array();
    // first search all row nodes
    foreach($dom->find($rowCSS) as $trNr => $trNode) {
        $trNodes[] = $trNode;
        $tr[$trNr] = array();
        foreach($attrList as $attr) if ($trNode->$attr) $tr[$trNr]["row_$attr"] = $trNode->$attr;
    }

    // then walk all column queries and find cells
    for($qNr = 0; $qNr < count($colCSS); $qNr++) {
        $queryColNr = 0;
        for($trNr = 0; $trNr < count($trNodes); $trNr++) {
            $tdNodes = $trNodes[$trNr]->find($colCSS[$qNr]);
            if (count($tdNodes) > $queryColNr) $queryColNr = count($tdNodes);
            for($tdNr = 0; $tdNr < count($tdNodes); $tdNr++) {
                $tdNode = &$tdNodes[$tdNr];
                $prefix = $tdNode->tag . ($tableColNr + $tdNr);
                if ($tdNode->plaintext) $tr[$trNr][$prefix] = $tdNode->plaintext;
                if ($tdNode->innertext) $tr[$trNr][$prefix . '_html'] = $tdNode->innertext;
                foreach($attrList as $attr) if ($tdNode->$attr) $tr[$trNr][$prefix . '_' . $attr] = $tdNode->$attr;
            }
        }
        $tableColNr += $queryColNr;
    }
    return $tr;
}

// scraperwiki dismiss columns where cell content for first row is null :(
function getTableKeys(&$table) {
    $keys = array();
    for ($i = 0; $i < count($table); $i++) $keys = array_unique(array_merge($keys, array_keys($table[$i])));
    return $keys;
}

function saveTable($data, $pkey, $name, $keys = null) {
    if (empty($name)) $name = 'swdata';
    if (is_string($pkey)) $pkey = array($pkey);
    if (empty($keys)) $keys = getTableKeys($data);

    if (!in_array($pkey[0], $keys)) {
        print "Table '$name' have no key '$pkey[0]', adding it";
        for ($i = 0; $i < count($data); $i++) $data[$i][$pkey[0]] = $i + 1;
    }

    scraperwiki::sqliteexecute("drop table if exists $name");
    if ($keys)
    scraperwiki::sqliteexecute("create table $name (" . join(', ', $keys) . ')');
    scraperwiki::save_sqlite($pkey, $data, $name, $keys); 
}

// returns array of one column
function cutColumn($rows, $colname, $addNull = true) {
    $colValues = array();
    for ($i = 0; $i < count($rows); $i++) {
        if (isset($rows[$i][$colname]))
            $colValues[] = $rows[$i][$colname];
        else if ($addNull) $colValues[] = null;
    }
    return $colValues;
}

function tableIndex(&$table, $colname, $unique = true) {
    $idx = array();
    for ($i = 0; $i < count($table); $i++) {
        if ($unique)
            $idx[ $table[$i][$colname] ] = &$table[$i];
        else {
            if (empty($idx[ $table[$i][$colname] ])) 
                $idx[ $table[$i][$colname] ] = array();
            $idx[ $table[$i][$colname] ][] = &$table[$i];
        }
    }
    return $idx;
}

// use like tableRemap($data, 'link(href_1),content(text_1),samenamefield')
function tableRemap($rows, $map) {
    $mapParts = explode(',', $map);
    $map = array();
    foreach($mapParts as $dst) {
        $kv = explode('(', $dst);
        if (count($kv) == 2) {
            list($dst, $src) = $kv;
            $src = substr($src, 0, -1);
        } else $src = $dst;
        $map[] = sprintf('"%s" => isset($el["%s"]) ? $el["%s"] : null', $dst, $src, $src);
    }
    $fn = create_function('$el', 'return array(' . join(', ', $map) . ');');
    return array_map($fn, $rows);
}


?>