<?php
print_r(scraperwiki::sqliteexecute("select * from swdata where ok = 1 limit 5")); 
exit();
require 'scraperwiki/simple_html_dom.php';
for($i=100;$i<105;$i++){
$html_content = scraperwiki::scrape("http://vietphrase.com/go/99tvshows.com/xx/forumdisplay.php?fid=10&filter=0&orderby=views&page=$i");
$html = str_get_html($html_content);
$data = array();
foreach($html->find('div.maintable table.tableborder a') as $a)
{
    if(preg_match('#viewthread#',$a->href,$m) && strlen($a->plaintext) >7) {
      //  echo $a->href ." | ".$a->plaintext ."<br />";
    
        scraperwiki::save_sqlite(array('url'),array('title'=>$a->plaintext,'url'=> $a->href,'ok'=>0)); 
    }
}
$html->clear();
unset($html);
}
?>
<?php
print_r(scraperwiki::sqliteexecute("select * from swdata where ok = 1 limit 5")); 
exit();
require 'scraperwiki/simple_html_dom.php';
for($i=100;$i<105;$i++){
$html_content = scraperwiki::scrape("http://vietphrase.com/go/99tvshows.com/xx/forumdisplay.php?fid=10&filter=0&orderby=views&page=$i");
$html = str_get_html($html_content);
$data = array();
foreach($html->find('div.maintable table.tableborder a') as $a)
{
    if(preg_match('#viewthread#',$a->href,$m) && strlen($a->plaintext) >7) {
      //  echo $a->href ." | ".$a->plaintext ."<br />";
    
        scraperwiki::save_sqlite(array('url'),array('title'=>$a->plaintext,'url'=> $a->href,'ok'=>0)); 
    }
}
$html->clear();
unset($html);
}
?>
