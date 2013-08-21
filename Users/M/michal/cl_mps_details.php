<?php

//details of Chilean MPs (diputados)

require 'scraperwiki/simple_html_dom.php';

//update only active MPs:
$date = date("Y-m-d H:i:s");

//read the saved tables
scraperwiki::attach("cl_mps_list", "src");
$rows0 = scraperwiki::select("max(updated_on) as last_updated_on from src.swdata");
if (!empty($rows0)) {
  $last_updated_on = $rows0[0]['last_updated_on'];
  $rows = scraperwiki::select("* from src.swdata where updated_on='{$last_updated_on}'");
  if (!empty($rows)) {

    //for each MP:
    foreach ($rows as $row) {
      $url = 'http://www.camara.cl/camara/diputado_detalle.aspx?prmid='.$row['id'];
      $html = scraperwiki::scrape($url);
      //get dom
      $dom = new simple_html_dom();
      $dom->load($html);

      $div = $dom->find("div[id=ficha]",0);    
      $name_ar = explode("  ",trim($h3 = $div->find("h3",0)->plaintext));
      $name = trim(end($name_ar));
      
      $born_on_es = trim($div->find("div[class=birthDate]",0)->find("p",0)->innertext);
      $profession = trim($div->find("div[class=profession]",0)->find("p",0)->innertext);
      $comunas = trim($div->find("div[class=summary]",0)->find("p",0)->innertext);
      $distrito_ar = explode("  ",trim($div->find("div[class=summary]",0)->find("p[class=distrito]",0)->find("a",0)->innertext));
      $distrito = trim(end($distrito_ar));
      $region_ar = explode("  ",trim($div->find("div[class=summary]",0)->find("p",2)->find("a",0)->innertext));
      $region_rome = trim(current($region_ar));
      $region = trim(end($region_ar));
      $group = trim($div->find("div[class=summary]",2)->find("p",0)->innertext);
      $email = trim($div->find("li[class=email]",0)->plaintext);
      $website_0 = $div->find("div[class=internet]",0)->find("li",0);
      if (!empty($website_0))
        $website = trim($website_0->plaintext);
      else $website = '';
      $mps[] = array(
        'id' => $row['id'],
        'updated_on' => $date,
        'born_on_es' => $born_on_es,
        'profession' => $profession,
        'comunas' => $comunas,
        'distrito' => $distrito,   
        'region_rome' => $region_rome,
        'region' => $region,     
        'group' => $group,
        'email' => $email,
        'website' => $website,
      );
//print_r($mps);die();
    }
    scraperwiki::save_sqlite(array('id'),$mps);
  }
}


?>
<?php

//details of Chilean MPs (diputados)

require 'scraperwiki/simple_html_dom.php';

//update only active MPs:
$date = date("Y-m-d H:i:s");

//read the saved tables
scraperwiki::attach("cl_mps_list", "src");
$rows0 = scraperwiki::select("max(updated_on) as last_updated_on from src.swdata");
if (!empty($rows0)) {
  $last_updated_on = $rows0[0]['last_updated_on'];
  $rows = scraperwiki::select("* from src.swdata where updated_on='{$last_updated_on}'");
  if (!empty($rows)) {

    //for each MP:
    foreach ($rows as $row) {
      $url = 'http://www.camara.cl/camara/diputado_detalle.aspx?prmid='.$row['id'];
      $html = scraperwiki::scrape($url);
      //get dom
      $dom = new simple_html_dom();
      $dom->load($html);

      $div = $dom->find("div[id=ficha]",0);    
      $name_ar = explode("  ",trim($h3 = $div->find("h3",0)->plaintext));
      $name = trim(end($name_ar));
      
      $born_on_es = trim($div->find("div[class=birthDate]",0)->find("p",0)->innertext);
      $profession = trim($div->find("div[class=profession]",0)->find("p",0)->innertext);
      $comunas = trim($div->find("div[class=summary]",0)->find("p",0)->innertext);
      $distrito_ar = explode("  ",trim($div->find("div[class=summary]",0)->find("p[class=distrito]",0)->find("a",0)->innertext));
      $distrito = trim(end($distrito_ar));
      $region_ar = explode("  ",trim($div->find("div[class=summary]",0)->find("p",2)->find("a",0)->innertext));
      $region_rome = trim(current($region_ar));
      $region = trim(end($region_ar));
      $group = trim($div->find("div[class=summary]",2)->find("p",0)->innertext);
      $email = trim($div->find("li[class=email]",0)->plaintext);
      $website_0 = $div->find("div[class=internet]",0)->find("li",0);
      if (!empty($website_0))
        $website = trim($website_0->plaintext);
      else $website = '';
      $mps[] = array(
        'id' => $row['id'],
        'updated_on' => $date,
        'born_on_es' => $born_on_es,
        'profession' => $profession,
        'comunas' => $comunas,
        'distrito' => $distrito,   
        'region_rome' => $region_rome,
        'region' => $region,     
        'group' => $group,
        'email' => $email,
        'website' => $website,
      );
//print_r($mps);die();
    }
    scraperwiki::save_sqlite(array('id'),$mps);
  }
}


?>
