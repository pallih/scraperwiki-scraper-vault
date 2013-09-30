<?php

 require 'scraperwiki/simple_html_dom.php';     

$url = "http://www.keralapsc.org/notifi.htm";



$html = file_get_html($url);



  foreach($html->find('a[href*="noti"]') as $element) {  

  

   $text_link = $element->plaintext;

  $link_to = $element->href;

  

    if(strlen(trim($text_link)) != '' ){

     $exam_list[] = '<li><a href="http://www.keralapsc.org/' . $link_to .'">'. $text_link . '</a></li>'; }

     }
$limit = count($exam_list);
for($i=0;$i<=$limit;$i++){
echo  $exam_list[$i];

}

?>
<?php

 require 'scraperwiki/simple_html_dom.php';     

$url = "http://www.keralapsc.org/notifi.htm";



$html = file_get_html($url);



  foreach($html->find('a[href*="noti"]') as $element) {  

  

   $text_link = $element->plaintext;

  $link_to = $element->href;

  

    if(strlen(trim($text_link)) != '' ){

     $exam_list[] = '<li><a href="http://www.keralapsc.org/' . $link_to .'">'. $text_link . '</a></li>'; }

     }
$limit = count($exam_list);
for($i=0;$i<=$limit;$i++){
echo  $exam_list[$i];

}

?>
