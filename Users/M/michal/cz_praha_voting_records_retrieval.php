<?php

//retrieves data from https://scraperwiki.com/scrapers/cz_praha_voting_records_downloader/

//temp
scraperwiki::save_var('last_id',0);

require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("cz_praha_voting_records_downloader", "src");

$last_id = scraperwiki::get_var('last_id',0);
$rows = scraperwiki::select("id from src.division where CAST(id as INTEGER)>{$last_id} order by CAST(id as integer)");

foreach ($rows as $row) {
  $r = scraperwiki::select("* from src.division where CAST(id as INTEGER)={$row['id']}");
//print_r($r);
  $r = $r[0];
  $html = '<html><body>' . $r['html'] . '</body></html>';
  $dom = new simple_html_dom();
  $dom->load($html);
  
  $info = array(
    'id' => $r['id'],
    'decision_number' => $r['decision_number'],
    'date' => $r['date'],
    'document_number' => $r['document_number'],
    'name' => $r['name'],
    'passed' => $r['passed'],
    'link' => $r['link'],
  );
  $part = get_first_string($html,'</h2>','<div>');
  $info['for'] = (trim(get_first_string($part,'pro:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'pro:</span>','<br'));
  $info['against'] = (trim(get_first_string($part,'proti:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'proti:</span>','<br'));
  $info['abstain'] = (trim(get_first_string($part,'zdržel se:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'zdržel se:</span>','<br'));
  $info['number_representatives'] = (trim(get_first_string($part,'Počet zastupitelů:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'Počet zastupitelů:</span>','<br'));
  $info['present'] = (trim(get_first_string($part,'přítomno:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'přítomno:</span>','<br'));

  $trs = $dom->find("table[class=data-grid]",0)->find("tr");
    array_shift($trs);
    $data = array();
    foreach ($trs as $tr) {
        $tds = $tr->find("td");
        $mp_id = get_first_string($tds[0]->find("a",0)->href . "&","memberId=","&");
        $data[] = array(
            'division_id' => $info['id'],
            'mp_id' => $mp_id,
            'vote' => trim($tds[1]->plaintext),
            'mp_name' => $tds[0]->plaintext,
        );
    }
    //one division done
    scraperwiki::save_sqlite(array('id'),$info,'division');
    scraperwiki::save_sqlite(array('division_id','mp_id'),$data,'mp_vote');
    scraperwiki::save_var('last_id',$info['id']);
}

/**

* finds substrings between opening and closing markers

* @return result array of the substrings

*/

function returnSubstrings($text, $openingMarker, $closingMarker) {

$openingMarkerLength = strlen($openingMarker);

$closingMarkerLength = strlen($closingMarker);

$result = array();

$position = 0;

while (($position = strpos($text, $openingMarker, $position)) !== false) {

$position += $openingMarkerLength;

if (($closingMarkerPosition = strpos($text, $closingMarker, $position)) !== false) {

$result[] = substr($text, $position, $closingMarkerPosition - $position);

$position = $closingMarkerPosition + $closingMarkerLength;

}

}

return $result;

}


/**

* finds 1st substring between opening and closing markers

* @return result 1st substring

*/

function get_first_string ($text,$openingMarker, $closingMarker) {

$out_ar = returnSubstrings($text, $openingMarker, $closingMarker);

$out = $out_ar[0];

return($out);

}

?>
<?php

//retrieves data from https://scraperwiki.com/scrapers/cz_praha_voting_records_downloader/

//temp
scraperwiki::save_var('last_id',0);

require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("cz_praha_voting_records_downloader", "src");

$last_id = scraperwiki::get_var('last_id',0);
$rows = scraperwiki::select("id from src.division where CAST(id as INTEGER)>{$last_id} order by CAST(id as integer)");

foreach ($rows as $row) {
  $r = scraperwiki::select("* from src.division where CAST(id as INTEGER)={$row['id']}");
//print_r($r);
  $r = $r[0];
  $html = '<html><body>' . $r['html'] . '</body></html>';
  $dom = new simple_html_dom();
  $dom->load($html);
  
  $info = array(
    'id' => $r['id'],
    'decision_number' => $r['decision_number'],
    'date' => $r['date'],
    'document_number' => $r['document_number'],
    'name' => $r['name'],
    'passed' => $r['passed'],
    'link' => $r['link'],
  );
  $part = get_first_string($html,'</h2>','<div>');
  $info['for'] = (trim(get_first_string($part,'pro:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'pro:</span>','<br'));
  $info['against'] = (trim(get_first_string($part,'proti:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'proti:</span>','<br'));
  $info['abstain'] = (trim(get_first_string($part,'zdržel se:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'zdržel se:</span>','<br'));
  $info['number_representatives'] = (trim(get_first_string($part,'Počet zastupitelů:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'Počet zastupitelů:</span>','<br'));
  $info['present'] = (trim(get_first_string($part,'přítomno:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'přítomno:</span>','<br'));

  $trs = $dom->find("table[class=data-grid]",0)->find("tr");
    array_shift($trs);
    $data = array();
    foreach ($trs as $tr) {
        $tds = $tr->find("td");
        $mp_id = get_first_string($tds[0]->find("a",0)->href . "&","memberId=","&");
        $data[] = array(
            'division_id' => $info['id'],
            'mp_id' => $mp_id,
            'vote' => trim($tds[1]->plaintext),
            'mp_name' => $tds[0]->plaintext,
        );
    }
    //one division done
    scraperwiki::save_sqlite(array('id'),$info,'division');
    scraperwiki::save_sqlite(array('division_id','mp_id'),$data,'mp_vote');
    scraperwiki::save_var('last_id',$info['id']);
}

/**

* finds substrings between opening and closing markers

* @return result array of the substrings

*/

function returnSubstrings($text, $openingMarker, $closingMarker) {

$openingMarkerLength = strlen($openingMarker);

$closingMarkerLength = strlen($closingMarker);

$result = array();

$position = 0;

while (($position = strpos($text, $openingMarker, $position)) !== false) {

$position += $openingMarkerLength;

if (($closingMarkerPosition = strpos($text, $closingMarker, $position)) !== false) {

$result[] = substr($text, $position, $closingMarkerPosition - $position);

$position = $closingMarkerPosition + $closingMarkerLength;

}

}

return $result;

}


/**

* finds 1st substring between opening and closing markers

* @return result 1st substring

*/

function get_first_string ($text,$openingMarker, $closingMarker) {

$out_ar = returnSubstrings($text, $openingMarker, $closingMarker);

$out = $out_ar[0];

return($out);

}

?>
<?php

//retrieves data from https://scraperwiki.com/scrapers/cz_praha_voting_records_downloader/

//temp
scraperwiki::save_var('last_id',0);

require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("cz_praha_voting_records_downloader", "src");

$last_id = scraperwiki::get_var('last_id',0);
$rows = scraperwiki::select("id from src.division where CAST(id as INTEGER)>{$last_id} order by CAST(id as integer)");

foreach ($rows as $row) {
  $r = scraperwiki::select("* from src.division where CAST(id as INTEGER)={$row['id']}");
//print_r($r);
  $r = $r[0];
  $html = '<html><body>' . $r['html'] . '</body></html>';
  $dom = new simple_html_dom();
  $dom->load($html);
  
  $info = array(
    'id' => $r['id'],
    'decision_number' => $r['decision_number'],
    'date' => $r['date'],
    'document_number' => $r['document_number'],
    'name' => $r['name'],
    'passed' => $r['passed'],
    'link' => $r['link'],
  );
  $part = get_first_string($html,'</h2>','<div>');
  $info['for'] = (trim(get_first_string($part,'pro:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'pro:</span>','<br'));
  $info['against'] = (trim(get_first_string($part,'proti:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'proti:</span>','<br'));
  $info['abstain'] = (trim(get_first_string($part,'zdržel se:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'zdržel se:</span>','<br'));
  $info['number_representatives'] = (trim(get_first_string($part,'Počet zastupitelů:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'Počet zastupitelů:</span>','<br'));
  $info['present'] = (trim(get_first_string($part,'přítomno:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'přítomno:</span>','<br'));

  $trs = $dom->find("table[class=data-grid]",0)->find("tr");
    array_shift($trs);
    $data = array();
    foreach ($trs as $tr) {
        $tds = $tr->find("td");
        $mp_id = get_first_string($tds[0]->find("a",0)->href . "&","memberId=","&");
        $data[] = array(
            'division_id' => $info['id'],
            'mp_id' => $mp_id,
            'vote' => trim($tds[1]->plaintext),
            'mp_name' => $tds[0]->plaintext,
        );
    }
    //one division done
    scraperwiki::save_sqlite(array('id'),$info,'division');
    scraperwiki::save_sqlite(array('division_id','mp_id'),$data,'mp_vote');
    scraperwiki::save_var('last_id',$info['id']);
}

/**

* finds substrings between opening and closing markers

* @return result array of the substrings

*/

function returnSubstrings($text, $openingMarker, $closingMarker) {

$openingMarkerLength = strlen($openingMarker);

$closingMarkerLength = strlen($closingMarker);

$result = array();

$position = 0;

while (($position = strpos($text, $openingMarker, $position)) !== false) {

$position += $openingMarkerLength;

if (($closingMarkerPosition = strpos($text, $closingMarker, $position)) !== false) {

$result[] = substr($text, $position, $closingMarkerPosition - $position);

$position = $closingMarkerPosition + $closingMarkerLength;

}

}

return $result;

}


/**

* finds 1st substring between opening and closing markers

* @return result 1st substring

*/

function get_first_string ($text,$openingMarker, $closingMarker) {

$out_ar = returnSubstrings($text, $openingMarker, $closingMarker);

$out = $out_ar[0];

return($out);

}

?>
<?php

//retrieves data from https://scraperwiki.com/scrapers/cz_praha_voting_records_downloader/

//temp
scraperwiki::save_var('last_id',0);

require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("cz_praha_voting_records_downloader", "src");

$last_id = scraperwiki::get_var('last_id',0);
$rows = scraperwiki::select("id from src.division where CAST(id as INTEGER)>{$last_id} order by CAST(id as integer)");

foreach ($rows as $row) {
  $r = scraperwiki::select("* from src.division where CAST(id as INTEGER)={$row['id']}");
//print_r($r);
  $r = $r[0];
  $html = '<html><body>' . $r['html'] . '</body></html>';
  $dom = new simple_html_dom();
  $dom->load($html);
  
  $info = array(
    'id' => $r['id'],
    'decision_number' => $r['decision_number'],
    'date' => $r['date'],
    'document_number' => $r['document_number'],
    'name' => $r['name'],
    'passed' => $r['passed'],
    'link' => $r['link'],
  );
  $part = get_first_string($html,'</h2>','<div>');
  $info['for'] = (trim(get_first_string($part,'pro:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'pro:</span>','<br'));
  $info['against'] = (trim(get_first_string($part,'proti:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'proti:</span>','<br'));
  $info['abstain'] = (trim(get_first_string($part,'zdržel se:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'zdržel se:</span>','<br'));
  $info['number_representatives'] = (trim(get_first_string($part,'Počet zastupitelů:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'Počet zastupitelů:</span>','<br'));
  $info['present'] = (trim(get_first_string($part,'přítomno:</span>','<br')) == '') ? 0 : trim(get_first_string($part,'přítomno:</span>','<br'));

  $trs = $dom->find("table[class=data-grid]",0)->find("tr");
    array_shift($trs);
    $data = array();
    foreach ($trs as $tr) {
        $tds = $tr->find("td");
        $mp_id = get_first_string($tds[0]->find("a",0)->href . "&","memberId=","&");
        $data[] = array(
            'division_id' => $info['id'],
            'mp_id' => $mp_id,
            'vote' => trim($tds[1]->plaintext),
            'mp_name' => $tds[0]->plaintext,
        );
    }
    //one division done
    scraperwiki::save_sqlite(array('id'),$info,'division');
    scraperwiki::save_sqlite(array('division_id','mp_id'),$data,'mp_vote');
    scraperwiki::save_var('last_id',$info['id']);
}

/**

* finds substrings between opening and closing markers

* @return result array of the substrings

*/

function returnSubstrings($text, $openingMarker, $closingMarker) {

$openingMarkerLength = strlen($openingMarker);

$closingMarkerLength = strlen($closingMarker);

$result = array();

$position = 0;

while (($position = strpos($text, $openingMarker, $position)) !== false) {

$position += $openingMarkerLength;

if (($closingMarkerPosition = strpos($text, $closingMarker, $position)) !== false) {

$result[] = substr($text, $position, $closingMarkerPosition - $position);

$position = $closingMarkerPosition + $closingMarkerLength;

}

}

return $result;

}


/**

* finds 1st substring between opening and closing markers

* @return result 1st substring

*/

function get_first_string ($text,$openingMarker, $closingMarker) {

$out_ar = returnSubstrings($text, $openingMarker, $closingMarker);

$out = $out_ar[0];

return($out);

}

?>
