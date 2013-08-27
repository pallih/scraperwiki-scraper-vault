<?php
// members of the current 10th spanish congress
//there are at least 350

require 'scraperwiki/simple_html_dom.php';

$i = 1;
$continue = true;
while (($i <=350) or ($continue)) {
    $url = "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/DipSustSust?_piref73_1502033_73_1333066_1333066.next_page=/wc/fichaDiputado&idDiputado={$i}&idLegislatura=10&opcion=h";
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    if (strpos($html,'500 Internal Server Error')>0) break;

    $name = str_replace('&nbsp;',' ',$dom->find("div[class=nombre_dip]",0)->plaintext);
    $name_ar = explode(',',$name);
    $prov_ar = explode(' por ',$dom->find('div[class=dip_rojo]',0)->plaintext);
    $province = trim(rtrim(trim($prov_ar[1]),'.'));

    $group_ar = explode(" ( ",$dom->find('div[class=dip_rojo]',1)->plaintext);
    $group = trim($group_ar[0]);
    $group_short_name = trim(rtrim($group_ar[1]),')');

    $data = array(
        'id' => $i,
        'name' => $name,
        'first_name' => trim($name_ar[1]),
        'last_name' => trim($name_ar[0]),
        'province' => $province,
        'group' => $group,
        'group_short_name' => $group_short_name
    );

    //print_r($data);die();
    scraperwiki::save_sqlite(array('id'),$data,'mp');

    $i++;
}
echo 'last i:'.$i;

?>
<?php
// members of the current 10th spanish congress
//there are at least 350

require 'scraperwiki/simple_html_dom.php';

$i = 1;
$continue = true;
while (($i <=350) or ($continue)) {
    $url = "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/DipSustSust?_piref73_1502033_73_1333066_1333066.next_page=/wc/fichaDiputado&idDiputado={$i}&idLegislatura=10&opcion=h";
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    if (strpos($html,'500 Internal Server Error')>0) break;

    $name = str_replace('&nbsp;',' ',$dom->find("div[class=nombre_dip]",0)->plaintext);
    $name_ar = explode(',',$name);
    $prov_ar = explode(' por ',$dom->find('div[class=dip_rojo]',0)->plaintext);
    $province = trim(rtrim(trim($prov_ar[1]),'.'));

    $group_ar = explode(" ( ",$dom->find('div[class=dip_rojo]',1)->plaintext);
    $group = trim($group_ar[0]);
    $group_short_name = trim(rtrim($group_ar[1]),')');

    $data = array(
        'id' => $i,
        'name' => $name,
        'first_name' => trim($name_ar[1]),
        'last_name' => trim($name_ar[0]),
        'province' => $province,
        'group' => $group,
        'group_short_name' => $group_short_name
    );

    //print_r($data);die();
    scraperwiki::save_sqlite(array('id'),$data,'mp');

    $i++;
}
echo 'last i:'.$i;

?>
<?php
// members of the current 10th spanish congress
//there are at least 350

require 'scraperwiki/simple_html_dom.php';

$i = 1;
$continue = true;
while (($i <=350) or ($continue)) {
    $url = "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/DipSustSust?_piref73_1502033_73_1333066_1333066.next_page=/wc/fichaDiputado&idDiputado={$i}&idLegislatura=10&opcion=h";
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    if (strpos($html,'500 Internal Server Error')>0) break;

    $name = str_replace('&nbsp;',' ',$dom->find("div[class=nombre_dip]",0)->plaintext);
    $name_ar = explode(',',$name);
    $prov_ar = explode(' por ',$dom->find('div[class=dip_rojo]',0)->plaintext);
    $province = trim(rtrim(trim($prov_ar[1]),'.'));

    $group_ar = explode(" ( ",$dom->find('div[class=dip_rojo]',1)->plaintext);
    $group = trim($group_ar[0]);
    $group_short_name = trim(rtrim($group_ar[1]),')');

    $data = array(
        'id' => $i,
        'name' => $name,
        'first_name' => trim($name_ar[1]),
        'last_name' => trim($name_ar[0]),
        'province' => $province,
        'group' => $group,
        'group_short_name' => $group_short_name
    );

    //print_r($data);die();
    scraperwiki::save_sqlite(array('id'),$data,'mp');

    $i++;
}
echo 'last i:'.$i;

?>
