<?php
require 'scraperwiki/simple_html_dom.php';   


for($i = 135000;$i<135100;$i++){
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "http://icsi.examresults.net/MA-Result-Ph1-9.aspx");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POST, true);
$data = array(
    'ddlcourse' => '4',
    'rollno' => $i,
    'submit' => 'B1'
);

curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
$output = curl_exec($ch);
$info = curl_getinfo($ch);
curl_close($ch);

$html = str_get_html($output);
    $name = $html->find('b', 5)->innertext;
    $name = strip_tags($name);
    $name = str_replace('"', "", $name);
    $name = str_replace('  ', "", $name);
    $name = str_replace('&amp;', "", $name);
    $name = str_replace('&nbsp;', "", $name);
    $name = str_replace('&nbsp;&nbsp;', "", $name);
    $name = str_replace(' &nbsp;&nbsp;', "", $name);
    $name = strip_tags($name);

    $number =  $html->find('b', 6)->plaintext;
    $number = trim(str_replace("Roll Number :", "", $number));
    $number = strip_tags($number);
    $number = str_replace('"', "", $number);
    $number = str_replace('  ', "", $number);
    $number = str_replace('&amp;', "", $number);
    $number = str_replace('&nbsp;', "", $number);
    $number = str_replace('&nbsp;&nbsp;', "", $number);
    $number = str_replace(' &nbsp;&nbsp;', "", $number);
    $number = strip_tags($number);
    $number = trim(str_replace(" ", "", $number));


    $res =  $html->find('b', 7)->plaintext;
    $res = trim(str_replace("Result :", "", $res));

    $bee = $html->find('td', 11)->plaintext;
    $bmec = $html->find('td', 13)->plaintext;
    $be = $html->find('td', 15)->plaintext;
    $faa = $html->find('td', 17)->plaintext;
    $total = $html->find('td', 19)->plaintext;

if($number){
$message = scraperwiki::save_sqlite(array("number"), array("number"=>$number, "name"=>$name, "bee"=>$bee, "bmec"=>$bmec, "be"=>$be, "faa"=>$faa, "result"=>$res, "total"=>$total), $table_name="swdata");
}
}
?>