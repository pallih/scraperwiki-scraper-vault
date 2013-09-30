<?php

ini_set('display_errors', '1');
    ini_set('log_errors', 1);
    ini_set('error_log', dirname(__FILE__) . '/error_log.txt');
    error_reporting(E_ALL);
require 'scraperwiki/simple_html_dom.php';
//$html2 = file_get_html('http://www.bookadda.com/general-search?searchkey=Old+Magazine+Advertisements+1890-1950%3A+Identification+%26+Value+Guide');
$html2 = file_get_html('http://www.bookadda.com/general-search?searchkey=+Old+Magazine+Advertisements+1890-1950%3A+Identification+%26+Value+Guide+');

if(isset($html2))
echo "successful"; else echo "no success"; 
/*$str=$html2->find('div[class=fk-srch-item fk-inf-scroll-item]',0);
//echo $str;
$str1=(string)$str;
echo $str1;
echo gettype($str1);
$id=1;
$record=array(
'id'=>$id,
'html'=>$str1
);
scraperwiki::save(array('id'),$record);*/
?>
<?php

ini_set('display_errors', '1');
    ini_set('log_errors', 1);
    ini_set('error_log', dirname(__FILE__) . '/error_log.txt');
    error_reporting(E_ALL);
require 'scraperwiki/simple_html_dom.php';
//$html2 = file_get_html('http://www.bookadda.com/general-search?searchkey=Old+Magazine+Advertisements+1890-1950%3A+Identification+%26+Value+Guide');
$html2 = file_get_html('http://www.bookadda.com/general-search?searchkey=+Old+Magazine+Advertisements+1890-1950%3A+Identification+%26+Value+Guide+');

if(isset($html2))
echo "successful"; else echo "no success"; 
/*$str=$html2->find('div[class=fk-srch-item fk-inf-scroll-item]',0);
//echo $str;
$str1=(string)$str;
echo $str1;
echo gettype($str1);
$id=1;
$record=array(
'id'=>$id,
'html'=>$str1
);
scraperwiki::save(array('id'),$record);*/
?>
