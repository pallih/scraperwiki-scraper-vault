<?php

require 'scraperwiki/simple_html_dom.php';

$html_content = scraperwiki::scrape("http://www.bodytalk.gr/?page_id=74&shop=8");
$html = str_get_html($html_content);
$dbData = array('id'=>'','big_image'=>'','small_image'=>'','location'=>'','address'=>'','tel'=>'','fax'=>'','mail'=>'','ll'=>'','lat'=>'','lon'=>'');
$i=0;
foreach ($html->find("#shops_right_rep") as $el) {
$dbData['id'] = $i++;
$bigImg = $el->find('#shops_right_rep_img a');
$bigImgSrc = $bigImg[0]->href;
$dbData['big_image'] = $bigImgSrc;

$smallImage = $bigImg[0]->find('img');
$smallImageSrc = $smallImage[0]->src;
$dbData['small_image'] = $smallImageSrc;

$location = $el->find('#shops_right_rep_title');
$locationSrc = $location[0]->innertext;
$dbData['location'] = $locationSrc;

$txt = $el->find('#real_text');

preg_match("/(.*)st./i",$txt[0]->plaintext,$address);
$address = isset($address[1])?trim($address[1]):'';
$address = explode('|',$address);
if(count($address)==1){$address = $address[0];}
else { $address = trim($address[1]);}
$dbData['address'] = $address;


preg_match("/tel\.([:0-9\s-]*)/i",$txt[0]->plaintext,$tel);
$tel = preg_replace('/[:\s-]/','',$tel[1]);
$dbData['tel'] = $tel;

preg_match("/fax\.([:0-9\s-]*)/i",$txt[0]->plaintext,$fax);
$fax =isset($fax[1])?preg_replace('/[:\s-]/','',$fax[1]):'';
$dbData['fax'] = $fax;

preg_match("/[^\s\|]*@[^\s]*/i",$txt[0]->plaintext,$mail);
$mail =isset($mail[0])?preg_replace('/[:\s-]/','',$mail[0]):'';
$dbData['mail'] = $mail;

$map = $el->find('#shops_right_rep_map a');
if(isset($map[0])){
$mapHref = $map[0]->href;

$map_html_content = scraperwiki::scrape("http://www.bodytalk.gr/".$mapHref);
$map_html = str_get_html($map_html_content);

$mapIframe = $map_html->find('iframe');
$mapSrc = $mapIframe[0]->src."\n";

preg_match("/ll=([^\&]*)&/",$mapSrc,$ll );
$dbData['ll'] = $ll[1];
$ll = explode(',',$ll[1]);
$dbData['lat'] = $ll[0];
$dbData['lon'] = $ll[1];
}

$message = scraperwiki::save_sqlite(array("id"),$dbData);

}

?>


<?php

require 'scraperwiki/simple_html_dom.php';

$html_content = scraperwiki::scrape("http://www.bodytalk.gr/?page_id=74&shop=8");
$html = str_get_html($html_content);
$dbData = array('id'=>'','big_image'=>'','small_image'=>'','location'=>'','address'=>'','tel'=>'','fax'=>'','mail'=>'','ll'=>'','lat'=>'','lon'=>'');
$i=0;
foreach ($html->find("#shops_right_rep") as $el) {
$dbData['id'] = $i++;
$bigImg = $el->find('#shops_right_rep_img a');
$bigImgSrc = $bigImg[0]->href;
$dbData['big_image'] = $bigImgSrc;

$smallImage = $bigImg[0]->find('img');
$smallImageSrc = $smallImage[0]->src;
$dbData['small_image'] = $smallImageSrc;

$location = $el->find('#shops_right_rep_title');
$locationSrc = $location[0]->innertext;
$dbData['location'] = $locationSrc;

$txt = $el->find('#real_text');

preg_match("/(.*)st./i",$txt[0]->plaintext,$address);
$address = isset($address[1])?trim($address[1]):'';
$address = explode('|',$address);
if(count($address)==1){$address = $address[0];}
else { $address = trim($address[1]);}
$dbData['address'] = $address;


preg_match("/tel\.([:0-9\s-]*)/i",$txt[0]->plaintext,$tel);
$tel = preg_replace('/[:\s-]/','',$tel[1]);
$dbData['tel'] = $tel;

preg_match("/fax\.([:0-9\s-]*)/i",$txt[0]->plaintext,$fax);
$fax =isset($fax[1])?preg_replace('/[:\s-]/','',$fax[1]):'';
$dbData['fax'] = $fax;

preg_match("/[^\s\|]*@[^\s]*/i",$txt[0]->plaintext,$mail);
$mail =isset($mail[0])?preg_replace('/[:\s-]/','',$mail[0]):'';
$dbData['mail'] = $mail;

$map = $el->find('#shops_right_rep_map a');
if(isset($map[0])){
$mapHref = $map[0]->href;

$map_html_content = scraperwiki::scrape("http://www.bodytalk.gr/".$mapHref);
$map_html = str_get_html($map_html_content);

$mapIframe = $map_html->find('iframe');
$mapSrc = $mapIframe[0]->src."\n";

preg_match("/ll=([^\&]*)&/",$mapSrc,$ll );
$dbData['ll'] = $ll[1];
$ll = explode(',',$ll[1]);
$dbData['lat'] = $ll[0];
$dbData['lon'] = $ll[1];
}

$message = scraperwiki::save_sqlite(array("id"),$dbData);

}

?>


