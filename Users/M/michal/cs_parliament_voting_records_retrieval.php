<?php

//Czechoslovakia only
//note: Czechoslovak parliament has IDs between 20551 and 23571 (possibly not continuous)

require 'scraperwiki/simple_html_dom.php';

//get last id
//scraperwiki::save_var('last_id',20532);  //temp
$last_id = scraperwiki::get_var('last_id',20530);

//read the saved tables
scraperwiki::attach("cz_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} and id<23572 order by id");
//$htmls = scraperwiki::select("* from src.swdata where id IN (20532) order by id");//trial

if (!empty($rows)) {
  foreach ($rows as $html) {
    //get dom
    $dom = new simple_html_dom();
    $html2 = scraperwiki::select("* from src.swdata where id={$html['id']}");
    $correct_html2 = str_replace("</td>\n<tr>","</td></tr>\n<tr>",str_replace("</h4></td></tr>","</h4> </td></tr><tr>",str_replace("</h4> </td></tr>","</h4> </td></tr><tr>",str_replace("</table>\n<hr />\n</td></tr>","</table><table>",$html2[0]['html']))));
    $dom->load(str_replace("&nbsp;"," ",$correct_html2));
    //info
    $data = array('id'=>$html['id']);
    $h2s = $dom->find("h2");

    //do not use for Czechoslovak parliament
    //note: Czechoslovak parliament has IDs between 20551 and 23571 (possibly not continous)
    $cs = strpos($h2s[0]->innertext,'shromáždění České a Slovenské Federativní republiky');
    if (!($cs > 0)) {
      scraperwiki::save_var('last_id',$html['id']);
      continue;
    }
      //schuze
    $bigs = $dom->find("big");
    preg_match('/([0-9]{1,}). schůze/',$bigs[0]->plaintext,$matches);
    $schuze = $matches[1];
      //date
    preg_match('/([0-9]{1,}). ([0-9]{1,}). ([0-9]{1,})/',$bigs[0]->plaintext,$matches);
    $date = $matches[3] .'-' . n2($matches[2]) . '-' . n2($matches[1]);
      //time
    preg_match('/([0-9]{1,}:[0-9]{1,})/',$bigs[0]->plaintext,$matches);
    $time = $matches[1];
      //name (if exists)
    $name = $bigs[1]->plaintext;
    //tables
    //there is an error at the source pages - missing <table> tag
    $tables = $dom->find("table");
    $tables2 = $tables[0]->find("table");
    //echo $tables2[0]->outertext;die();
    //first table
    $array = $tables2[0]->find("tr");
    array_shift($array);
    foreach ($array as $row) {
      $tds = $row->find("td");
      $data['needed_' . $tds[0]->innertext] = $tds[1]->innertext;
      $data['present_' . $tds[0]->innertext] = $tds[2]->innertext;
    }

    //save data
    $data['session'] = $schuze;
    $data['date'] = $date;
    $data['time'] = $time;
    $data['name'] = $name;
    scraperwiki::save_sqlite(array('id'),$data,'info');


    //votes
    $data = array();
    $trs = $tables2[1]->find("tr");
    if (!empty($trs)) {
        foreach ($trs as $tr) {
          $h2s = $tr->find('h2');
          if ((isset($h2s[0])) and (strlen($h2s[0]->innertext) > 0)) {
            $chamber = $h2s[0]->innertext;
          } else {
            $h4s = $tr->find('h4');
            if ((isset($h4s[0])) and (strlen($h4s[0]->innertext) > 0)) {
            $club = $h4s[0]->innertext; 
            } 
            else {
            $tds = $tr->find("td");
            for ($k = 0; $k < (count($tds)/2); $k++) {
//echo $tds[2*$k]->innertext;
              $vote = $tds[2*$k]->innertext;
              if (trim($vote) != '') {
                  $tmp = $tds[2*$k+1]->find("a");
                  preg_match('/id=([0-9]{1,})/',$tmp[0]->href,$matches);
                  $mp_id = $matches[1];
                  $name = $tmp[0]->innertext;
//echo '*'.$i.'*'.$name;$i++;
                  $data[] = array(
                    'division_id' => $html['id'],
                    'mp_id' => $mp_id,
                    'vote' => $vote,
                    'club' => $club,
                    'chamber' => $chamber,
                    'name' => $name
                  ); 
               }           
            }
          }
        }
      }
//echo count($data);
//die();
     scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');
    }
   scraperwiki::save_var('last_id',$html['id']);
  }
}

// adds 0s before number
function n2($n) {
  if ($n < 10) return '0'.$n;
  else return $n;
}

?>