<?php
require('scraperwiki/simple_html_dom.php');
$html = scraperWiki::scrape('http://www.oireachtas.ie/members-hist/default.asp?housetype=1&HouseNum=23&disp=mem');
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('ul[id=memberslist] li') as $li) {
    list($name,$constituency,$party) = preg_split('/\r\n/',$li->plaintext,-1,PREG_SPLIT_NO_EMPTY);
    
    $party = substr($party,strpos($party,':')+1);
    $party = substr($party,0,strpos($party,'('));
    
    $member = array('name'=>trim($name),'constituency'=>trim($constituency),'party'=>trim($party));
    scraperwiki::save_sqlite(array('name'),$member);
}
?>
<?php
require('scraperwiki/simple_html_dom.php');
$html = scraperWiki::scrape('http://www.oireachtas.ie/members-hist/default.asp?housetype=1&HouseNum=23&disp=mem');
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('ul[id=memberslist] li') as $li) {
    list($name,$constituency,$party) = preg_split('/\r\n/',$li->plaintext,-1,PREG_SPLIT_NO_EMPTY);
    
    $party = substr($party,strpos($party,':')+1);
    $party = substr($party,0,strpos($party,'('));
    
    $member = array('name'=>trim($name),'constituency'=>trim($constituency),'party'=>trim($party));
    scraperwiki::save_sqlite(array('name'),$member);
}
?>
<?php
require('scraperwiki/simple_html_dom.php');
$html = scraperWiki::scrape('http://www.oireachtas.ie/members-hist/default.asp?housetype=1&HouseNum=23&disp=mem');
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('ul[id=memberslist] li') as $li) {
    list($name,$constituency,$party) = preg_split('/\r\n/',$li->plaintext,-1,PREG_SPLIT_NO_EMPTY);
    
    $party = substr($party,strpos($party,':')+1);
    $party = substr($party,0,strpos($party,'('));
    
    $member = array('name'=>trim($name),'constituency'=>trim($constituency),'party'=>trim($party));
    scraperwiki::save_sqlite(array('name'),$member);
}
?>
