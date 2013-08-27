<?php

require 'scraperwiki/simple_html_dom.php';

//get last id
//scraperwiki::save_var('last_id',1281);  //temp
$last_id = scraperwiki::get_var('last_id',1281);

//read the saved tables
scraperwiki::attach("cl_parliament_voting_records_downloader", "src");
$ids = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");

//different votes:
$votes = array('for','against','abstain','art5','paired');

if (!empty($ids)) {
  foreach ($ids as $id) {
    $data = array();
    $row = scraperwiki::select("* from src.swdata where id={$id['id']}");
    //info
    $dom = new simple_html_dom();
    $dom->load('<html><body>'.$row[0]['info'].'</body></html>');
    $data_info = array();
    $data_info['name'] = trim($dom->find('h2',0)->plaintext);
    $ps = $dom->find('p');
    if (count($ps) > 0) {
      foreach($ps as $p) {
        $label = rtrim($p->find('strong',0)->plaintext,':');
        $value = trim(str_replace($label.':','',$p->plaintext));
        if ($label == 'Fecha') {
          $time_ar = explode(' ',$value);
          $data_info['date'] = $time_ar[4].'-'.month($time_ar[2]).'-'.$time_ar[0];
          $data_info['time'] = $time_ar[5];    
        } else if ($label == 'Resultado') {
          $tds = $dom->find('td');
          $data_info['for'] = trim($tds[0]->plaintext);
          $data_info['against'] = trim($tds[1]->plaintext);
          $data_info['abstain'] = trim($tds[2]->plaintext);
          $data_info['dispensed'] = trim($tds[3]->plaintext);
        } else if ($label == 'Trámite') {
          $val_ar = explode("  ",$value);
          $new_value = '';
          if (count($val_ar) > 0) {
            foreach ($val_ar as $v) {
              if(strlen($v) > 0)
                $new_value .= trim($v) . ' ';
//echo '*'.$v.'*';
            }
          }
          $data_info[$label] = trim($new_value);
        } else {
          $data_info[$label] = $value;
        }

      }
    }
    $data_info['id'] = $id['id'];
    scraperwiki::save_sqlite(array('id'),$data_info,'info');
//print_r($data_info);die();

    //votes
    foreach ($votes as $vote) {
      $dom = new simple_html_dom();
      $dom->load('<html><body>'.$row[0][$vote].'</body></html>');
      
      $tds = $dom->find('td');
      if (count($tds) > 0) {
        foreach ($tds as $td) {
          if (trim($td->plaintext) != '') {
            preg_match('/prmID=([0-9]{1,})/',$td->find('a',0)->href,$matches);
            $data[] = array(
              'name' => trim($td->find('a',0)->plaintext), //because of pareos, see e.g. http://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=7144
              'mp_id' => $matches[1],
              'division_id' => $id['id'],
              'vote' => $vote
            );
            if (count($td->find('a')) > 1) {  //because of pareos, see e.g. http://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=7144
              $data[] = array(
              'name' => trim($td->find('a',1)->plaintext), 
              'mp_id' => $matches[1],
              'division_id' => $id['id'],
              'vote' => $vote . '_2',  //mark as 'paired_2'
            );
            }

          }
        }
      }
    } 
    scraperwiki::save_sqlite(array('mp_id','division_id'),$data,'vote');
    scraperwiki::save_var('last_id',$id['id']);
  }
}
scraperwiki::save_var('last_id',0);

//months
function month($text) {
  $ar = array(
    'Ene' => '01',
    'Feb' => '02',
    'Mar' => '03',
    'Abr' => '04',
    'May' => '05',
    'Jun' => '06',
    'Jul' => '07',
    'Ago' => '08',
    'Sep' => '09',
    'Set' => '09',
    'Oct' => '10',
    'Nov' => '11',
    'Dic' => '12',
  );
  return $ar[rtrim($text,'.')];
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

//get last id
//scraperwiki::save_var('last_id',1281);  //temp
$last_id = scraperwiki::get_var('last_id',1281);

//read the saved tables
scraperwiki::attach("cl_parliament_voting_records_downloader", "src");
$ids = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");

//different votes:
$votes = array('for','against','abstain','art5','paired');

if (!empty($ids)) {
  foreach ($ids as $id) {
    $data = array();
    $row = scraperwiki::select("* from src.swdata where id={$id['id']}");
    //info
    $dom = new simple_html_dom();
    $dom->load('<html><body>'.$row[0]['info'].'</body></html>');
    $data_info = array();
    $data_info['name'] = trim($dom->find('h2',0)->plaintext);
    $ps = $dom->find('p');
    if (count($ps) > 0) {
      foreach($ps as $p) {
        $label = rtrim($p->find('strong',0)->plaintext,':');
        $value = trim(str_replace($label.':','',$p->plaintext));
        if ($label == 'Fecha') {
          $time_ar = explode(' ',$value);
          $data_info['date'] = $time_ar[4].'-'.month($time_ar[2]).'-'.$time_ar[0];
          $data_info['time'] = $time_ar[5];    
        } else if ($label == 'Resultado') {
          $tds = $dom->find('td');
          $data_info['for'] = trim($tds[0]->plaintext);
          $data_info['against'] = trim($tds[1]->plaintext);
          $data_info['abstain'] = trim($tds[2]->plaintext);
          $data_info['dispensed'] = trim($tds[3]->plaintext);
        } else if ($label == 'Trámite') {
          $val_ar = explode("  ",$value);
          $new_value = '';
          if (count($val_ar) > 0) {
            foreach ($val_ar as $v) {
              if(strlen($v) > 0)
                $new_value .= trim($v) . ' ';
//echo '*'.$v.'*';
            }
          }
          $data_info[$label] = trim($new_value);
        } else {
          $data_info[$label] = $value;
        }

      }
    }
    $data_info['id'] = $id['id'];
    scraperwiki::save_sqlite(array('id'),$data_info,'info');
//print_r($data_info);die();

    //votes
    foreach ($votes as $vote) {
      $dom = new simple_html_dom();
      $dom->load('<html><body>'.$row[0][$vote].'</body></html>');
      
      $tds = $dom->find('td');
      if (count($tds) > 0) {
        foreach ($tds as $td) {
          if (trim($td->plaintext) != '') {
            preg_match('/prmID=([0-9]{1,})/',$td->find('a',0)->href,$matches);
            $data[] = array(
              'name' => trim($td->find('a',0)->plaintext), //because of pareos, see e.g. http://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=7144
              'mp_id' => $matches[1],
              'division_id' => $id['id'],
              'vote' => $vote
            );
            if (count($td->find('a')) > 1) {  //because of pareos, see e.g. http://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=7144
              $data[] = array(
              'name' => trim($td->find('a',1)->plaintext), 
              'mp_id' => $matches[1],
              'division_id' => $id['id'],
              'vote' => $vote . '_2',  //mark as 'paired_2'
            );
            }

          }
        }
      }
    } 
    scraperwiki::save_sqlite(array('mp_id','division_id'),$data,'vote');
    scraperwiki::save_var('last_id',$id['id']);
  }
}
scraperwiki::save_var('last_id',0);

//months
function month($text) {
  $ar = array(
    'Ene' => '01',
    'Feb' => '02',
    'Mar' => '03',
    'Abr' => '04',
    'May' => '05',
    'Jun' => '06',
    'Jul' => '07',
    'Ago' => '08',
    'Sep' => '09',
    'Set' => '09',
    'Oct' => '10',
    'Nov' => '11',
    'Dic' => '12',
  );
  return $ar[rtrim($text,'.')];
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

//get last id
//scraperwiki::save_var('last_id',1281);  //temp
$last_id = scraperwiki::get_var('last_id',1281);

//read the saved tables
scraperwiki::attach("cl_parliament_voting_records_downloader", "src");
$ids = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");

//different votes:
$votes = array('for','against','abstain','art5','paired');

if (!empty($ids)) {
  foreach ($ids as $id) {
    $data = array();
    $row = scraperwiki::select("* from src.swdata where id={$id['id']}");
    //info
    $dom = new simple_html_dom();
    $dom->load('<html><body>'.$row[0]['info'].'</body></html>');
    $data_info = array();
    $data_info['name'] = trim($dom->find('h2',0)->plaintext);
    $ps = $dom->find('p');
    if (count($ps) > 0) {
      foreach($ps as $p) {
        $label = rtrim($p->find('strong',0)->plaintext,':');
        $value = trim(str_replace($label.':','',$p->plaintext));
        if ($label == 'Fecha') {
          $time_ar = explode(' ',$value);
          $data_info['date'] = $time_ar[4].'-'.month($time_ar[2]).'-'.$time_ar[0];
          $data_info['time'] = $time_ar[5];    
        } else if ($label == 'Resultado') {
          $tds = $dom->find('td');
          $data_info['for'] = trim($tds[0]->plaintext);
          $data_info['against'] = trim($tds[1]->plaintext);
          $data_info['abstain'] = trim($tds[2]->plaintext);
          $data_info['dispensed'] = trim($tds[3]->plaintext);
        } else if ($label == 'Trámite') {
          $val_ar = explode("  ",$value);
          $new_value = '';
          if (count($val_ar) > 0) {
            foreach ($val_ar as $v) {
              if(strlen($v) > 0)
                $new_value .= trim($v) . ' ';
//echo '*'.$v.'*';
            }
          }
          $data_info[$label] = trim($new_value);
        } else {
          $data_info[$label] = $value;
        }

      }
    }
    $data_info['id'] = $id['id'];
    scraperwiki::save_sqlite(array('id'),$data_info,'info');
//print_r($data_info);die();

    //votes
    foreach ($votes as $vote) {
      $dom = new simple_html_dom();
      $dom->load('<html><body>'.$row[0][$vote].'</body></html>');
      
      $tds = $dom->find('td');
      if (count($tds) > 0) {
        foreach ($tds as $td) {
          if (trim($td->plaintext) != '') {
            preg_match('/prmID=([0-9]{1,})/',$td->find('a',0)->href,$matches);
            $data[] = array(
              'name' => trim($td->find('a',0)->plaintext), //because of pareos, see e.g. http://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=7144
              'mp_id' => $matches[1],
              'division_id' => $id['id'],
              'vote' => $vote
            );
            if (count($td->find('a')) > 1) {  //because of pareos, see e.g. http://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=7144
              $data[] = array(
              'name' => trim($td->find('a',1)->plaintext), 
              'mp_id' => $matches[1],
              'division_id' => $id['id'],
              'vote' => $vote . '_2',  //mark as 'paired_2'
            );
            }

          }
        }
      }
    } 
    scraperwiki::save_sqlite(array('mp_id','division_id'),$data,'vote');
    scraperwiki::save_var('last_id',$id['id']);
  }
}
scraperwiki::save_var('last_id',0);

//months
function month($text) {
  $ar = array(
    'Ene' => '01',
    'Feb' => '02',
    'Mar' => '03',
    'Abr' => '04',
    'May' => '05',
    'Jun' => '06',
    'Jul' => '07',
    'Ago' => '08',
    'Sep' => '09',
    'Set' => '09',
    'Oct' => '10',
    'Nov' => '11',
    'Dic' => '12',
  );
  return $ar[rtrim($text,'.')];
}

?>
