<?php

//note: strangely, there were problems with simple_html_dom.php, when running second! html file (first went ok) for terms>=50 (49 ok)
//    therefore I have redone it in the 'old' way using returnSubstrings() function

//require 'scraperwiki/simple_html_dom.php';


//temp
//scraperwiki::sqliteexecute("delete from vote where term>=50");
//scraperwiki::sqlitecommit();die();

//get last id
//scraperwiki::save_var('last_term',52);  //temp
//scraperwiki::save_var('last_mp_id',0);  //temp
$last_mp_id = scraperwiki::get_var('last_mp_id',0);
$last_term = scraperwiki::get_var('last_term',0);

//read the saved tables
scraperwiki::attach("br_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("term,mp_id from src.swdata where term>{$last_term} or (term={$last_term} and mp_id>{$last_mp_id}) order by term,mp_id");

if (count($rows) > 0) {
  foreach ($rows as $row) {
    $html = scraperwiki::select("* from src.swdata where mp_id={$row['mp_id']} and term={$row['term']}");

    if ($html[0]['html'] == '') continue;

    //$dom = new simple_html_dom();  //simple_html_dom.php
    //$dom->load($html[0]['html']);  //simple_html_dom.php

    //mp
    $data_mp = array(
      'mp_id' => $html[0]['mp_id'],
      'term' => $html[0]['term'],
    );

    //$as = $dom->find('h3',0)->find('a');  //simple_html_dom.php
    $as0 = get_first_string($html[0]['html'],'<h3','</h3>');
    $as = returnSubstrings($as0,'<a','/a>');
    
    if (count($as) > 0) {
      //preg_match('/id=([0-9]{1,})/',$as[0]->href,$matches);  //simple_html_dom.php
      preg_match('/id=([0-9]{1,})/',$as[0],$matches);
      $data_mp['mp_unique_id'] = $matches[1];
      //$tmp = explode ('-',$as[0]->plaintext);  //simple_html_dom.php
      $tmp = explode ('-',get_first_string($as[0],'">','<'));
      $tmp2 = explode('/',trim(end($tmp)));
      $data_mp['state'] = $tmp2[1];
      $data_mp['party'] = $tmp2[0];
      array_pop($tmp);
      $data_mp['name'] = trim(implode('-',$tmp));
    }
    scraperwiki::save_sqlite(array('term','mp_id'),$data_mp,'mp');

    //votes
    $data = array();
    //$trs0 = $dom->find('table[class=tabela-1]',0);  //simple_html_dom.php
    $trs0 = get_first_string($html[0]['html'],'<table class="tabela-1"','<!--Fim Código-->');
    $trs = returnSubstrings($trs0,'<tr','</tr>');
    if (count($trs) > 0) {
      array_shift($trs); //first row is the header
      foreach ($trs as $tr) {
        //$tds = $tr->find('td');  //simple_html_dom.php;
        $tds = returnSubstrings($tr,'<td','</td>');

        //if ($tr->class == 'even') { //session  //simple_html_dom.php
        if (strpos($tr,'even') > 0) { //session
          //$da = explode('/',trim($tds[0]->plaintext));  //simple_html_dom.php
          $da = explode('/',trim(strip_tags('<td'.$tds[0])));
          $date = $da[2].'-'.$da[1].'-'.$da[0];
          //$session = trim($tds[1]->plaintext);  //simple_html_dom.php
          $session = trim(strip_tags('<td'.$tds[1]));
          //$presence = str_replace('&nbsp;','',trim($tds[2]->plaintext));  //simple_html_dom.php
          $presence = str_replace('&nbsp;','',trim(strip_tags('<td'.$tds[2])));
        } else { //vote
          $d = array(
            'date' => $date,
            'session' => $session,
            'presence' => $presence,
            //'name' => trim($tds[1]->plaintext),  //simple_html_dom.php
            'name' => trim((strip_tags('<td'.$tds[1]))),
            //'vote' => trim($tds[3]->plaintext),  //simple_html_dom.php
            'vote' => trim((strip_tags('<td'.$tds[3]))),
            'mp_id' => $html[0]['mp_id'],
            'term' => $html[0]['term'],
          );
          $data[] = $d;
        }
        
      }
      scraperwiki::save_sqlite(array('term','mp_id','date','name'),$data,'vote');
    }
    scraperwiki::save_var('last_term', $html[0]['term']);
    scraperwiki::save_var('last_mp_id',$html[0]['mp_id']);
  }
}
scraperwiki::save_var('last_term', 0);
scraperwiki::save_var('last_mp_id', 0);


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

//note: strangely, there were problems with simple_html_dom.php, when running second! html file (first went ok) for terms>=50 (49 ok)
//    therefore I have redone it in the 'old' way using returnSubstrings() function

//require 'scraperwiki/simple_html_dom.php';


//temp
//scraperwiki::sqliteexecute("delete from vote where term>=50");
//scraperwiki::sqlitecommit();die();

//get last id
//scraperwiki::save_var('last_term',52);  //temp
//scraperwiki::save_var('last_mp_id',0);  //temp
$last_mp_id = scraperwiki::get_var('last_mp_id',0);
$last_term = scraperwiki::get_var('last_term',0);

//read the saved tables
scraperwiki::attach("br_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("term,mp_id from src.swdata where term>{$last_term} or (term={$last_term} and mp_id>{$last_mp_id}) order by term,mp_id");

if (count($rows) > 0) {
  foreach ($rows as $row) {
    $html = scraperwiki::select("* from src.swdata where mp_id={$row['mp_id']} and term={$row['term']}");

    if ($html[0]['html'] == '') continue;

    //$dom = new simple_html_dom();  //simple_html_dom.php
    //$dom->load($html[0]['html']);  //simple_html_dom.php

    //mp
    $data_mp = array(
      'mp_id' => $html[0]['mp_id'],
      'term' => $html[0]['term'],
    );

    //$as = $dom->find('h3',0)->find('a');  //simple_html_dom.php
    $as0 = get_first_string($html[0]['html'],'<h3','</h3>');
    $as = returnSubstrings($as0,'<a','/a>');
    
    if (count($as) > 0) {
      //preg_match('/id=([0-9]{1,})/',$as[0]->href,$matches);  //simple_html_dom.php
      preg_match('/id=([0-9]{1,})/',$as[0],$matches);
      $data_mp['mp_unique_id'] = $matches[1];
      //$tmp = explode ('-',$as[0]->plaintext);  //simple_html_dom.php
      $tmp = explode ('-',get_first_string($as[0],'">','<'));
      $tmp2 = explode('/',trim(end($tmp)));
      $data_mp['state'] = $tmp2[1];
      $data_mp['party'] = $tmp2[0];
      array_pop($tmp);
      $data_mp['name'] = trim(implode('-',$tmp));
    }
    scraperwiki::save_sqlite(array('term','mp_id'),$data_mp,'mp');

    //votes
    $data = array();
    //$trs0 = $dom->find('table[class=tabela-1]',0);  //simple_html_dom.php
    $trs0 = get_first_string($html[0]['html'],'<table class="tabela-1"','<!--Fim Código-->');
    $trs = returnSubstrings($trs0,'<tr','</tr>');
    if (count($trs) > 0) {
      array_shift($trs); //first row is the header
      foreach ($trs as $tr) {
        //$tds = $tr->find('td');  //simple_html_dom.php;
        $tds = returnSubstrings($tr,'<td','</td>');

        //if ($tr->class == 'even') { //session  //simple_html_dom.php
        if (strpos($tr,'even') > 0) { //session
          //$da = explode('/',trim($tds[0]->plaintext));  //simple_html_dom.php
          $da = explode('/',trim(strip_tags('<td'.$tds[0])));
          $date = $da[2].'-'.$da[1].'-'.$da[0];
          //$session = trim($tds[1]->plaintext);  //simple_html_dom.php
          $session = trim(strip_tags('<td'.$tds[1]));
          //$presence = str_replace('&nbsp;','',trim($tds[2]->plaintext));  //simple_html_dom.php
          $presence = str_replace('&nbsp;','',trim(strip_tags('<td'.$tds[2])));
        } else { //vote
          $d = array(
            'date' => $date,
            'session' => $session,
            'presence' => $presence,
            //'name' => trim($tds[1]->plaintext),  //simple_html_dom.php
            'name' => trim((strip_tags('<td'.$tds[1]))),
            //'vote' => trim($tds[3]->plaintext),  //simple_html_dom.php
            'vote' => trim((strip_tags('<td'.$tds[3]))),
            'mp_id' => $html[0]['mp_id'],
            'term' => $html[0]['term'],
          );
          $data[] = $d;
        }
        
      }
      scraperwiki::save_sqlite(array('term','mp_id','date','name'),$data,'vote');
    }
    scraperwiki::save_var('last_term', $html[0]['term']);
    scraperwiki::save_var('last_mp_id',$html[0]['mp_id']);
  }
}
scraperwiki::save_var('last_term', 0);
scraperwiki::save_var('last_mp_id', 0);


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
