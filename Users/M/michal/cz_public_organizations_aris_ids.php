<?php

require 'scraperwiki/simple_html_dom.php'; 
//read the saved tables
scraperwiki::attach("cz_public_organizations_aris_basics", "src");
$dris = scraperwiki::select("* from src.dri order by value");
$periods = scraperwiki::select("* from src.period order by value");
$forms = scraperwiki::select("* from src.form order by value");
$chapters = scraperwiki::select("* from src.chapter order by value");
$regions = scraperwiki::select("* from src.region order by value");
//$periods = array('0' => array('value' => '12/2010'));  //temp
//$forms = array('0' => array('value' => 50)); //temp
//scraperwiki::save_var('last_c',4); //temp

/*$d = scraperwiki::save_var('last_d',0);
$p = scraperwiki::save_var('last_p',0);
$f = scraperwiki::save_var('last_f',0);
$c = scraperwiki::save_var('last_c',0);
$r = scraperwiki::save_var('last_r',0);*/ //first run only

$d = scraperwiki::get_var('last_d',0);
$p = scraperwiki::get_var('last_p',0);
$f = scraperwiki::get_var('last_f',0);
$c = scraperwiki::get_var('last_c',0);
$r = scraperwiki::get_var('last_r',0);

foreach ((array) $dris as $dkey => $dri) {
 scraperwiki::save_var('last_d',$dkey); 
 if ($dkey < $d) continue;

  foreach ((array) $periods as $pkey => $period) {
   scraperwiki::save_var('last_p',$pkey); 
   if ($pkey < $p) continue;
    $period_encoded = urlencode($period['value']);

    foreach ((array) $forms as $fkey => $form) {
     scraperwiki::save_var('last_f',$fkey); 
     if ($fkey < $f) continue;

      switch ($dri['label']) {
        case 'Místně řízené organizace':
          foreach((array) $regions as  $rkey => $region) {
            scraperwiki::save_var('last_r',$rkey); 
            if ($rkey < $r) continue;
              $url = "http://wwwinfo.mfcr.cz/cgi-bin/aris/iarisorg/organizace.pl?dri={$dri['value']}&obdobi={$period_encoded}&prijmy=0&vydaje=0&pevne=0&vykaz={$form['value']}&vykaznam={$form['value']}&zko={$region['value']}&zkonam={$region['value']}";
              $data = retrieve($url);
              save($data,$dri,$period,$form,'region',$region);
          }
          scraperwiki::save_var('last_r',0);
          $r = 0;
          break;

        default:
          foreach ((array) $chapters as $ckey=>$chapter) {
            scraperwiki::save_var('last_c',$ckey);
            if ($ckey < $c) continue;
              $url = "http://wwwinfo.mfcr.cz/cgi-bin/aris/iarisorg/organizace.pl?dri={$dri['value']}&obdobi={$period_encoded}&prijmy=0&vydaje=0&pevne=0&vykaz={$form['value']}&vykaznam={$form['value']}&kapitola={$chapter['value']}&kapitolanam={$chapter['value']}";
              $data = retrieve($url);
//echo $url; print_r($data);
              save($data,$dri,$period,$form,'chapter',$chapter);
//echo '*'; 
          }
          scraperwiki::save_var('last_c',0);
          $c = 0;
      }
    }
    scraperwiki::save_var('last_f',0);
    $f = 0;
  }
  scraperwiki::save_var('last_p',0);
  $p = 0;
}
scraperwiki::save_var('last_d',0);
$d = 0;



function save($data,$dri,$period,$form,$type,$type_value) {
 foreach ((array) $data as $da) {
  $d = array (
    'org_id' => $da['value'],
    'dri' => $dri['value'],
    'period' => $period['value'],
    'form' => $form['value'],
  );
  $o = array(
    'id' => $da['value'],
    'name' => $da['label'],
  );
  switch ($type) {
    case 'chapter':
      $o['chapter'] = $type_value['value'];
      $d['chapter'] = $type_value['value'];
      break;
    case 'region':
      $o['region'] = $type_value['value'];
      $d['region'] = $type_value['value'];
      break;
  }
  scraperwiki::save_sqlite(array('org_id','period','form'), $d, "form");
  scraperwiki::save_sqlite(array('id'), $o, "organization");
 }
}

function retrieve($url) {
  $html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
  if (strpos($html,'<b>Došlo k chybě</b>')) { //error
    echo $url;
    die();
  }
  if (strpos($html,'žádné výkazy!') > 0) { //no form for given combinations
    return array();
  } else {
    //get dom
    $dom = new simple_html_dom();
    $dom->load($html);
    $orgs_obj = $dom->find('select[name=icoNam]',0)->find('option');
    foreach ((array) $orgs_obj as $org) {
      $data[] = array('value' => $org->value, 'label' => trim($org->innertext));
    }
    return $data;
  }
}

?>
<?php

require 'scraperwiki/simple_html_dom.php'; 
//read the saved tables
scraperwiki::attach("cz_public_organizations_aris_basics", "src");
$dris = scraperwiki::select("* from src.dri order by value");
$periods = scraperwiki::select("* from src.period order by value");
$forms = scraperwiki::select("* from src.form order by value");
$chapters = scraperwiki::select("* from src.chapter order by value");
$regions = scraperwiki::select("* from src.region order by value");
//$periods = array('0' => array('value' => '12/2010'));  //temp
//$forms = array('0' => array('value' => 50)); //temp
//scraperwiki::save_var('last_c',4); //temp

/*$d = scraperwiki::save_var('last_d',0);
$p = scraperwiki::save_var('last_p',0);
$f = scraperwiki::save_var('last_f',0);
$c = scraperwiki::save_var('last_c',0);
$r = scraperwiki::save_var('last_r',0);*/ //first run only

$d = scraperwiki::get_var('last_d',0);
$p = scraperwiki::get_var('last_p',0);
$f = scraperwiki::get_var('last_f',0);
$c = scraperwiki::get_var('last_c',0);
$r = scraperwiki::get_var('last_r',0);

foreach ((array) $dris as $dkey => $dri) {
 scraperwiki::save_var('last_d',$dkey); 
 if ($dkey < $d) continue;

  foreach ((array) $periods as $pkey => $period) {
   scraperwiki::save_var('last_p',$pkey); 
   if ($pkey < $p) continue;
    $period_encoded = urlencode($period['value']);

    foreach ((array) $forms as $fkey => $form) {
     scraperwiki::save_var('last_f',$fkey); 
     if ($fkey < $f) continue;

      switch ($dri['label']) {
        case 'Místně řízené organizace':
          foreach((array) $regions as  $rkey => $region) {
            scraperwiki::save_var('last_r',$rkey); 
            if ($rkey < $r) continue;
              $url = "http://wwwinfo.mfcr.cz/cgi-bin/aris/iarisorg/organizace.pl?dri={$dri['value']}&obdobi={$period_encoded}&prijmy=0&vydaje=0&pevne=0&vykaz={$form['value']}&vykaznam={$form['value']}&zko={$region['value']}&zkonam={$region['value']}";
              $data = retrieve($url);
              save($data,$dri,$period,$form,'region',$region);
          }
          scraperwiki::save_var('last_r',0);
          $r = 0;
          break;

        default:
          foreach ((array) $chapters as $ckey=>$chapter) {
            scraperwiki::save_var('last_c',$ckey);
            if ($ckey < $c) continue;
              $url = "http://wwwinfo.mfcr.cz/cgi-bin/aris/iarisorg/organizace.pl?dri={$dri['value']}&obdobi={$period_encoded}&prijmy=0&vydaje=0&pevne=0&vykaz={$form['value']}&vykaznam={$form['value']}&kapitola={$chapter['value']}&kapitolanam={$chapter['value']}";
              $data = retrieve($url);
//echo $url; print_r($data);
              save($data,$dri,$period,$form,'chapter',$chapter);
//echo '*'; 
          }
          scraperwiki::save_var('last_c',0);
          $c = 0;
      }
    }
    scraperwiki::save_var('last_f',0);
    $f = 0;
  }
  scraperwiki::save_var('last_p',0);
  $p = 0;
}
scraperwiki::save_var('last_d',0);
$d = 0;



function save($data,$dri,$period,$form,$type,$type_value) {
 foreach ((array) $data as $da) {
  $d = array (
    'org_id' => $da['value'],
    'dri' => $dri['value'],
    'period' => $period['value'],
    'form' => $form['value'],
  );
  $o = array(
    'id' => $da['value'],
    'name' => $da['label'],
  );
  switch ($type) {
    case 'chapter':
      $o['chapter'] = $type_value['value'];
      $d['chapter'] = $type_value['value'];
      break;
    case 'region':
      $o['region'] = $type_value['value'];
      $d['region'] = $type_value['value'];
      break;
  }
  scraperwiki::save_sqlite(array('org_id','period','form'), $d, "form");
  scraperwiki::save_sqlite(array('id'), $o, "organization");
 }
}

function retrieve($url) {
  $html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
  if (strpos($html,'<b>Došlo k chybě</b>')) { //error
    echo $url;
    die();
  }
  if (strpos($html,'žádné výkazy!') > 0) { //no form for given combinations
    return array();
  } else {
    //get dom
    $dom = new simple_html_dom();
    $dom->load($html);
    $orgs_obj = $dom->find('select[name=icoNam]',0)->find('option');
    foreach ((array) $orgs_obj as $org) {
      $data[] = array('value' => $org->value, 'label' => trim($org->innertext));
    }
    return $data;
  }
}

?>
