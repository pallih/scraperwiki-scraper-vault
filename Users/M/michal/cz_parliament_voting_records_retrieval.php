<?php

//2012-05-30: they changed a lot at psp.cz websites!! The scraper has been changed starting 55900 !
//it is kept for Czechoslovakia (cs_parliament_voting_records_retrieval)

require 'scraperwiki/simple_html_dom.php';

//corrections:
/*scraperwiki::save_var('last_id',55899); //55150
scraperwiki::sqliteexecute("delete from info where id>55899");
scraperwiki::sqliteexecute("delete from vote where division_id>55899");
scraperwiki::sqlitecommit();
die();*/

//get last id
$last_id = scraperwiki::get_var('last_id',0);
echo $last_id;

//read the saved tables
scraperwiki::attach("cz_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");
//$htmls = scraperwiki::select("* from src.swdata where id IN (53693,53449,54166,54228,53601) order by id");//trial

if (!empty($rows)) {
  foreach ($rows as $html) {
    //get dom
    $dom = new simple_html_dom();
    $html2 = scraperwiki::select("* from src.swdata where id={$html['id']}");
    $dom->load(str_replace("&nbsp;"," ",$html2[0]['html']));
    //info
    $data = array('id'=>$html['id']);
    $h2s = $dom->find("h2");

    //do not use for Czechoslovak parliament
    //note: Czechoslovak parliament has IDs between 20551 and 23571 (possibly not continuous)
    $cs = strpos($h2s[0]->innertext,'shromáždění České a Slovenské Federativní republiky');
    if ($cs > 0) {
      scraperwiki::save_var('last_id',$html['id']);
      continue;
    }

    $h1 = $dom->find("h1",0);

      //schuze
    preg_match('/([0-9]{1,}). schůze/',$h1->innertext,$matches);
    $schuze = $matches[1];
      //link
    if (is_object($h1))
      $as = $h1->find("a");
    if (isset($as[0]))
      $link = $as[0]->href;
     else
      $link = '';
      //hlasovani
    preg_match('/([0-9a-zA-Z]{1,}). hlasování/',$h1->innertext,$matches);
    $hlasovani = $matches[1];
      //date
    preg_match('/([0-9]{1,}). ([0-9]{1,}). ([0-9]{1,})/',$h1->innertext,$matches);
    $date = $matches[3] .'-' . n2($matches[2]) . '-' . n2($matches[1]);
      //time
    preg_match('/([0-9]{1,}:[0-9]{1,})/',$h1->innertext,$matches);
    $time = $matches[1];
      //name (if exists)
    $tmp = strpos($h1->innertext,"<br />");
    if ($tmp > 0) {
      $name = trim(substr($h1->innertext,$tmp+strlen('<br />')));
      if (strlen($name) > 0)
        $data['name'] = $name;
      else $data['name'] = '';
    } else $data['name'] = '';
      //passed
    if (strpos($dom->innertext,"NÁVRH BYL ZAMÍTNUT") > 0) $data['passed'] = 'n';
    if (strpos($dom->innertext,"NÁVRH BYL PŘIJAT") > 0) $data['passed'] = 'y';

    //55708, 55714: another table added! workaround:
    //if ((strpos($tables[0]->innertext,'vznesena námitka') > 0) or (strpos($tables[0]->innertext, 'proti průběhu nebo výsledku hlasování'))) $table_i = 1;
    //else $table_i = 0;

    $p = $dom->find("p[class=counts]",0);
    $strongs = $p->find("strong");
    //preg_match('/PŘÍTOMNO=([0-9]{1,})/',$tables[$table_i]->innertext,$matches);
    $present = $strongs[0]->innertext;
    //preg_match('/JE TŘEBA=([0-9]{1,})/',$tables[$table_i]->innertext,$matches);
    $needed = $strongs[1]->innertext;

    //save data
    $data['session'] = $schuze;
    $data['link'] = $link;
    $data['division'] = $hlasovani;
    $data['date'] = $date;
    $data['time'] = $time;
    $data['present'] = $present;
    $data['needed'] = $needed;
//print_r($data);die();
    scraperwiki::save_sqlite(array('id'),$data,'info');

    //votes
        //**problem mezi 51685-51734, nenajde to druhou tabulku, nevim proc; 53066-53085, 

    //uls
    $data = array();
    $uls = $dom->find("ul[class=results]");
    foreach ($uls as $key=>$ul) {
      $club_ar = explode("(<span",$h2s[$key+1]->innertext);
      $club = strip_tags(trim($club_ar[0]));
      $lis = $ul->find("li");
      foreach ($lis as $li) {
        $tmp = $li->find("a",0);
        preg_match('/id=([0-9]{1,})/',$tmp->href,$matches);
        $mp_id = $matches[1];
        $vote = $li->find('span',0)->innertext;
        $name = $tmp->innertext;
        $data[] = array(
                    'division_id' => $html['id'],
                    'mp_id' => $mp_id,
                    'vote' => $vote,
                    'club' => $club,
                    'name' => $name
        );
      }
    }
//print_r($data);die();
    scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');

    //$tables = $dom->find("table");

    //if (isset ($tables[1])) {
       /* $data = array();
        $trs = $tables[$table_i+1]->find("tr");
        if (!empty($trs)) {
            foreach ($trs as $tr) {
              $h3s = $tr->find('h3');
              if ((isset($h3s[0])) and (strlen($h3s[0]->innertext) > 0)) {
                $club_ar = explode('(<b>',$h3s[0]->innertext);
                $club = $club_ar[0];
              } else {
                $tds = $tr->find("td");
                for ($k = 0; $k < (count($tds)/2); $k++) {
                  $vote = $tds[2*$k]->innertext;
                  $tmp = $tds[2*$k+1]->find("a");
                  preg_match('/id=([0-9]{1,})/',$tmp[0]->href,$matches);
                  $mp_id = $matches[1];
                  $name = $tmp[0]->innertext;
                  $data[] = array(
                    'division_id' => $html['id'],
                    'mp_id' => $mp_id,
                    'vote' => $vote,
                    'club' => $club,
                    'name' => $name
                  );            
                }
            }
          }
//print_r($data);die();
         scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');
        }*/
   //}// 


   scraperwiki::save_var('last_id',$html['id']);
  }
}

// adds 0s before number
function n2($n) {
  if ($n < 10) return '0'.$n;
  else return $n;
}

?><?php

//2012-05-30: they changed a lot at psp.cz websites!! The scraper has been changed starting 55900 !
//it is kept for Czechoslovakia (cs_parliament_voting_records_retrieval)

require 'scraperwiki/simple_html_dom.php';

//corrections:
/*scraperwiki::save_var('last_id',55899); //55150
scraperwiki::sqliteexecute("delete from info where id>55899");
scraperwiki::sqliteexecute("delete from vote where division_id>55899");
scraperwiki::sqlitecommit();
die();*/

//get last id
$last_id = scraperwiki::get_var('last_id',0);
echo $last_id;

//read the saved tables
scraperwiki::attach("cz_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");
//$htmls = scraperwiki::select("* from src.swdata where id IN (53693,53449,54166,54228,53601) order by id");//trial

if (!empty($rows)) {
  foreach ($rows as $html) {
    //get dom
    $dom = new simple_html_dom();
    $html2 = scraperwiki::select("* from src.swdata where id={$html['id']}");
    $dom->load(str_replace("&nbsp;"," ",$html2[0]['html']));
    //info
    $data = array('id'=>$html['id']);
    $h2s = $dom->find("h2");

    //do not use for Czechoslovak parliament
    //note: Czechoslovak parliament has IDs between 20551 and 23571 (possibly not continuous)
    $cs = strpos($h2s[0]->innertext,'shromáždění České a Slovenské Federativní republiky');
    if ($cs > 0) {
      scraperwiki::save_var('last_id',$html['id']);
      continue;
    }

    $h1 = $dom->find("h1",0);

      //schuze
    preg_match('/([0-9]{1,}). schůze/',$h1->innertext,$matches);
    $schuze = $matches[1];
      //link
    if (is_object($h1))
      $as = $h1->find("a");
    if (isset($as[0]))
      $link = $as[0]->href;
     else
      $link = '';
      //hlasovani
    preg_match('/([0-9a-zA-Z]{1,}). hlasování/',$h1->innertext,$matches);
    $hlasovani = $matches[1];
      //date
    preg_match('/([0-9]{1,}). ([0-9]{1,}). ([0-9]{1,})/',$h1->innertext,$matches);
    $date = $matches[3] .'-' . n2($matches[2]) . '-' . n2($matches[1]);
      //time
    preg_match('/([0-9]{1,}:[0-9]{1,})/',$h1->innertext,$matches);
    $time = $matches[1];
      //name (if exists)
    $tmp = strpos($h1->innertext,"<br />");
    if ($tmp > 0) {
      $name = trim(substr($h1->innertext,$tmp+strlen('<br />')));
      if (strlen($name) > 0)
        $data['name'] = $name;
      else $data['name'] = '';
    } else $data['name'] = '';
      //passed
    if (strpos($dom->innertext,"NÁVRH BYL ZAMÍTNUT") > 0) $data['passed'] = 'n';
    if (strpos($dom->innertext,"NÁVRH BYL PŘIJAT") > 0) $data['passed'] = 'y';

    //55708, 55714: another table added! workaround:
    //if ((strpos($tables[0]->innertext,'vznesena námitka') > 0) or (strpos($tables[0]->innertext, 'proti průběhu nebo výsledku hlasování'))) $table_i = 1;
    //else $table_i = 0;

    $p = $dom->find("p[class=counts]",0);
    $strongs = $p->find("strong");
    //preg_match('/PŘÍTOMNO=([0-9]{1,})/',$tables[$table_i]->innertext,$matches);
    $present = $strongs[0]->innertext;
    //preg_match('/JE TŘEBA=([0-9]{1,})/',$tables[$table_i]->innertext,$matches);
    $needed = $strongs[1]->innertext;

    //save data
    $data['session'] = $schuze;
    $data['link'] = $link;
    $data['division'] = $hlasovani;
    $data['date'] = $date;
    $data['time'] = $time;
    $data['present'] = $present;
    $data['needed'] = $needed;
//print_r($data);die();
    scraperwiki::save_sqlite(array('id'),$data,'info');

    //votes
        //**problem mezi 51685-51734, nenajde to druhou tabulku, nevim proc; 53066-53085, 

    //uls
    $data = array();
    $uls = $dom->find("ul[class=results]");
    foreach ($uls as $key=>$ul) {
      $club_ar = explode("(<span",$h2s[$key+1]->innertext);
      $club = strip_tags(trim($club_ar[0]));
      $lis = $ul->find("li");
      foreach ($lis as $li) {
        $tmp = $li->find("a",0);
        preg_match('/id=([0-9]{1,})/',$tmp->href,$matches);
        $mp_id = $matches[1];
        $vote = $li->find('span',0)->innertext;
        $name = $tmp->innertext;
        $data[] = array(
                    'division_id' => $html['id'],
                    'mp_id' => $mp_id,
                    'vote' => $vote,
                    'club' => $club,
                    'name' => $name
        );
      }
    }
//print_r($data);die();
    scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');

    //$tables = $dom->find("table");

    //if (isset ($tables[1])) {
       /* $data = array();
        $trs = $tables[$table_i+1]->find("tr");
        if (!empty($trs)) {
            foreach ($trs as $tr) {
              $h3s = $tr->find('h3');
              if ((isset($h3s[0])) and (strlen($h3s[0]->innertext) > 0)) {
                $club_ar = explode('(<b>',$h3s[0]->innertext);
                $club = $club_ar[0];
              } else {
                $tds = $tr->find("td");
                for ($k = 0; $k < (count($tds)/2); $k++) {
                  $vote = $tds[2*$k]->innertext;
                  $tmp = $tds[2*$k+1]->find("a");
                  preg_match('/id=([0-9]{1,})/',$tmp[0]->href,$matches);
                  $mp_id = $matches[1];
                  $name = $tmp[0]->innertext;
                  $data[] = array(
                    'division_id' => $html['id'],
                    'mp_id' => $mp_id,
                    'vote' => $vote,
                    'club' => $club,
                    'name' => $name
                  );            
                }
            }
          }
//print_r($data);die();
         scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');
        }*/
   //}// 


   scraperwiki::save_var('last_id',$html['id']);
  }
}

// adds 0s before number
function n2($n) {
  if ($n < 10) return '0'.$n;
  else return $n;
}

?><?php

//2012-05-30: they changed a lot at psp.cz websites!! The scraper has been changed starting 55900 !
//it is kept for Czechoslovakia (cs_parliament_voting_records_retrieval)

require 'scraperwiki/simple_html_dom.php';

//corrections:
/*scraperwiki::save_var('last_id',55899); //55150
scraperwiki::sqliteexecute("delete from info where id>55899");
scraperwiki::sqliteexecute("delete from vote where division_id>55899");
scraperwiki::sqlitecommit();
die();*/

//get last id
$last_id = scraperwiki::get_var('last_id',0);
echo $last_id;

//read the saved tables
scraperwiki::attach("cz_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");
//$htmls = scraperwiki::select("* from src.swdata where id IN (53693,53449,54166,54228,53601) order by id");//trial

if (!empty($rows)) {
  foreach ($rows as $html) {
    //get dom
    $dom = new simple_html_dom();
    $html2 = scraperwiki::select("* from src.swdata where id={$html['id']}");
    $dom->load(str_replace("&nbsp;"," ",$html2[0]['html']));
    //info
    $data = array('id'=>$html['id']);
    $h2s = $dom->find("h2");

    //do not use for Czechoslovak parliament
    //note: Czechoslovak parliament has IDs between 20551 and 23571 (possibly not continuous)
    $cs = strpos($h2s[0]->innertext,'shromáždění České a Slovenské Federativní republiky');
    if ($cs > 0) {
      scraperwiki::save_var('last_id',$html['id']);
      continue;
    }

    $h1 = $dom->find("h1",0);

      //schuze
    preg_match('/([0-9]{1,}). schůze/',$h1->innertext,$matches);
    $schuze = $matches[1];
      //link
    if (is_object($h1))
      $as = $h1->find("a");
    if (isset($as[0]))
      $link = $as[0]->href;
     else
      $link = '';
      //hlasovani
    preg_match('/([0-9a-zA-Z]{1,}). hlasování/',$h1->innertext,$matches);
    $hlasovani = $matches[1];
      //date
    preg_match('/([0-9]{1,}). ([0-9]{1,}). ([0-9]{1,})/',$h1->innertext,$matches);
    $date = $matches[3] .'-' . n2($matches[2]) . '-' . n2($matches[1]);
      //time
    preg_match('/([0-9]{1,}:[0-9]{1,})/',$h1->innertext,$matches);
    $time = $matches[1];
      //name (if exists)
    $tmp = strpos($h1->innertext,"<br />");
    if ($tmp > 0) {
      $name = trim(substr($h1->innertext,$tmp+strlen('<br />')));
      if (strlen($name) > 0)
        $data['name'] = $name;
      else $data['name'] = '';
    } else $data['name'] = '';
      //passed
    if (strpos($dom->innertext,"NÁVRH BYL ZAMÍTNUT") > 0) $data['passed'] = 'n';
    if (strpos($dom->innertext,"NÁVRH BYL PŘIJAT") > 0) $data['passed'] = 'y';

    //55708, 55714: another table added! workaround:
    //if ((strpos($tables[0]->innertext,'vznesena námitka') > 0) or (strpos($tables[0]->innertext, 'proti průběhu nebo výsledku hlasování'))) $table_i = 1;
    //else $table_i = 0;

    $p = $dom->find("p[class=counts]",0);
    $strongs = $p->find("strong");
    //preg_match('/PŘÍTOMNO=([0-9]{1,})/',$tables[$table_i]->innertext,$matches);
    $present = $strongs[0]->innertext;
    //preg_match('/JE TŘEBA=([0-9]{1,})/',$tables[$table_i]->innertext,$matches);
    $needed = $strongs[1]->innertext;

    //save data
    $data['session'] = $schuze;
    $data['link'] = $link;
    $data['division'] = $hlasovani;
    $data['date'] = $date;
    $data['time'] = $time;
    $data['present'] = $present;
    $data['needed'] = $needed;
//print_r($data);die();
    scraperwiki::save_sqlite(array('id'),$data,'info');

    //votes
        //**problem mezi 51685-51734, nenajde to druhou tabulku, nevim proc; 53066-53085, 

    //uls
    $data = array();
    $uls = $dom->find("ul[class=results]");
    foreach ($uls as $key=>$ul) {
      $club_ar = explode("(<span",$h2s[$key+1]->innertext);
      $club = strip_tags(trim($club_ar[0]));
      $lis = $ul->find("li");
      foreach ($lis as $li) {
        $tmp = $li->find("a",0);
        preg_match('/id=([0-9]{1,})/',$tmp->href,$matches);
        $mp_id = $matches[1];
        $vote = $li->find('span',0)->innertext;
        $name = $tmp->innertext;
        $data[] = array(
                    'division_id' => $html['id'],
                    'mp_id' => $mp_id,
                    'vote' => $vote,
                    'club' => $club,
                    'name' => $name
        );
      }
    }
//print_r($data);die();
    scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');

    //$tables = $dom->find("table");

    //if (isset ($tables[1])) {
       /* $data = array();
        $trs = $tables[$table_i+1]->find("tr");
        if (!empty($trs)) {
            foreach ($trs as $tr) {
              $h3s = $tr->find('h3');
              if ((isset($h3s[0])) and (strlen($h3s[0]->innertext) > 0)) {
                $club_ar = explode('(<b>',$h3s[0]->innertext);
                $club = $club_ar[0];
              } else {
                $tds = $tr->find("td");
                for ($k = 0; $k < (count($tds)/2); $k++) {
                  $vote = $tds[2*$k]->innertext;
                  $tmp = $tds[2*$k+1]->find("a");
                  preg_match('/id=([0-9]{1,})/',$tmp[0]->href,$matches);
                  $mp_id = $matches[1];
                  $name = $tmp[0]->innertext;
                  $data[] = array(
                    'division_id' => $html['id'],
                    'mp_id' => $mp_id,
                    'vote' => $vote,
                    'club' => $club,
                    'name' => $name
                  );            
                }
            }
          }
//print_r($data);die();
         scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');
        }*/
   //}// 


   scraperwiki::save_var('last_id',$html['id']);
  }
}

// adds 0s before number
function n2($n) {
  if ($n < 10) return '0'.$n;
  else return $n;
}

?><?php

//2012-05-30: they changed a lot at psp.cz websites!! The scraper has been changed starting 55900 !
//it is kept for Czechoslovakia (cs_parliament_voting_records_retrieval)

require 'scraperwiki/simple_html_dom.php';

//corrections:
/*scraperwiki::save_var('last_id',55899); //55150
scraperwiki::sqliteexecute("delete from info where id>55899");
scraperwiki::sqliteexecute("delete from vote where division_id>55899");
scraperwiki::sqlitecommit();
die();*/

//get last id
$last_id = scraperwiki::get_var('last_id',0);
echo $last_id;

//read the saved tables
scraperwiki::attach("cz_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");
//$htmls = scraperwiki::select("* from src.swdata where id IN (53693,53449,54166,54228,53601) order by id");//trial

if (!empty($rows)) {
  foreach ($rows as $html) {
    //get dom
    $dom = new simple_html_dom();
    $html2 = scraperwiki::select("* from src.swdata where id={$html['id']}");
    $dom->load(str_replace("&nbsp;"," ",$html2[0]['html']));
    //info
    $data = array('id'=>$html['id']);
    $h2s = $dom->find("h2");

    //do not use for Czechoslovak parliament
    //note: Czechoslovak parliament has IDs between 20551 and 23571 (possibly not continuous)
    $cs = strpos($h2s[0]->innertext,'shromáždění České a Slovenské Federativní republiky');
    if ($cs > 0) {
      scraperwiki::save_var('last_id',$html['id']);
      continue;
    }

    $h1 = $dom->find("h1",0);

      //schuze
    preg_match('/([0-9]{1,}). schůze/',$h1->innertext,$matches);
    $schuze = $matches[1];
      //link
    if (is_object($h1))
      $as = $h1->find("a");
    if (isset($as[0]))
      $link = $as[0]->href;
     else
      $link = '';
      //hlasovani
    preg_match('/([0-9a-zA-Z]{1,}). hlasování/',$h1->innertext,$matches);
    $hlasovani = $matches[1];
      //date
    preg_match('/([0-9]{1,}). ([0-9]{1,}). ([0-9]{1,})/',$h1->innertext,$matches);
    $date = $matches[3] .'-' . n2($matches[2]) . '-' . n2($matches[1]);
      //time
    preg_match('/([0-9]{1,}:[0-9]{1,})/',$h1->innertext,$matches);
    $time = $matches[1];
      //name (if exists)
    $tmp = strpos($h1->innertext,"<br />");
    if ($tmp > 0) {
      $name = trim(substr($h1->innertext,$tmp+strlen('<br />')));
      if (strlen($name) > 0)
        $data['name'] = $name;
      else $data['name'] = '';
    } else $data['name'] = '';
      //passed
    if (strpos($dom->innertext,"NÁVRH BYL ZAMÍTNUT") > 0) $data['passed'] = 'n';
    if (strpos($dom->innertext,"NÁVRH BYL PŘIJAT") > 0) $data['passed'] = 'y';

    //55708, 55714: another table added! workaround:
    //if ((strpos($tables[0]->innertext,'vznesena námitka') > 0) or (strpos($tables[0]->innertext, 'proti průběhu nebo výsledku hlasování'))) $table_i = 1;
    //else $table_i = 0;

    $p = $dom->find("p[class=counts]",0);
    $strongs = $p->find("strong");
    //preg_match('/PŘÍTOMNO=([0-9]{1,})/',$tables[$table_i]->innertext,$matches);
    $present = $strongs[0]->innertext;
    //preg_match('/JE TŘEBA=([0-9]{1,})/',$tables[$table_i]->innertext,$matches);
    $needed = $strongs[1]->innertext;

    //save data
    $data['session'] = $schuze;
    $data['link'] = $link;
    $data['division'] = $hlasovani;
    $data['date'] = $date;
    $data['time'] = $time;
    $data['present'] = $present;
    $data['needed'] = $needed;
//print_r($data);die();
    scraperwiki::save_sqlite(array('id'),$data,'info');

    //votes
        //**problem mezi 51685-51734, nenajde to druhou tabulku, nevim proc; 53066-53085, 

    //uls
    $data = array();
    $uls = $dom->find("ul[class=results]");
    foreach ($uls as $key=>$ul) {
      $club_ar = explode("(<span",$h2s[$key+1]->innertext);
      $club = strip_tags(trim($club_ar[0]));
      $lis = $ul->find("li");
      foreach ($lis as $li) {
        $tmp = $li->find("a",0);
        preg_match('/id=([0-9]{1,})/',$tmp->href,$matches);
        $mp_id = $matches[1];
        $vote = $li->find('span',0)->innertext;
        $name = $tmp->innertext;
        $data[] = array(
                    'division_id' => $html['id'],
                    'mp_id' => $mp_id,
                    'vote' => $vote,
                    'club' => $club,
                    'name' => $name
        );
      }
    }
//print_r($data);die();
    scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');

    //$tables = $dom->find("table");

    //if (isset ($tables[1])) {
       /* $data = array();
        $trs = $tables[$table_i+1]->find("tr");
        if (!empty($trs)) {
            foreach ($trs as $tr) {
              $h3s = $tr->find('h3');
              if ((isset($h3s[0])) and (strlen($h3s[0]->innertext) > 0)) {
                $club_ar = explode('(<b>',$h3s[0]->innertext);
                $club = $club_ar[0];
              } else {
                $tds = $tr->find("td");
                for ($k = 0; $k < (count($tds)/2); $k++) {
                  $vote = $tds[2*$k]->innertext;
                  $tmp = $tds[2*$k+1]->find("a");
                  preg_match('/id=([0-9]{1,})/',$tmp[0]->href,$matches);
                  $mp_id = $matches[1];
                  $name = $tmp[0]->innertext;
                  $data[] = array(
                    'division_id' => $html['id'],
                    'mp_id' => $mp_id,
                    'vote' => $vote,
                    'club' => $club,
                    'name' => $name
                  );            
                }
            }
          }
//print_r($data);die();
         scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');
        }*/
   //}// 


   scraperwiki::save_var('last_id',$html['id']);
  }
}

// adds 0s before number
function n2($n) {
  if ($n < 10) return '0'.$n;
  else return $n;
}

?>