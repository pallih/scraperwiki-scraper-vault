<?php
require 'scraperwiki/simple_html_dom.php';

$members=array();

function get_list($url,$type,$base) {
    $members2=array();
    $html = scraperWiki::scrape($url);                
    $dom = new simple_html_dom();
    $dom->load($html);
    $tables = $dom->find("table");
    $rows=$tables[9]->find("tr");
    foreach ($rows as $row) {
        print $row->plaintext;
        $columns=$row->find("td");
        $link=$row->find("a");
        //print $link->plaintext;
        $check=0;
        if(count($link)>0) {
            while($link[$check]->plaintext=='') {
                $check++;
            }
            if (substr($link[$check]->href,0,1)=='/') {
                $toscrape='http://www.info.gov.za'.$link[$check]->href;
            }
            else {
                $toscrape=$base.$link[$check]->href;
            }
            $html2 = scraperWiki::scrape($toscrape);
            $dom2 = new simple_html_dom();
            $dom2->load($html2);
            $name1=$dom2->find("h4");
        }
        
        if (count($name1)>0) {
            $name2 = explode(',',$name1[0]->plaintext);
            $name=$name2[0];
        }
        else {
            //print 'http://www.info.gov.za/leaders/ministers/'.$link[0]->href;
            $name = $columns[0]->plaintext;
        }
        //print $name;
        //$name = explode(',',$name1[0]->plaintext);
    
        $member=array();
        $member['name']=str_replace("\n",'',$name);
        $member['portfolio']=str_replace("\n",'',$columns[1]->plaintext);
        $member['type']=$type;
        $members2[]=$member;
    }
    return $members2;
}

$get=get_list('http://www.info.gov.za/leaders/ministers/index.html','Minister','http://www.info.gov.za/leaders/ministers/');
$members=array_merge($members,$get);
$get=get_list('http://www.info.gov.za/leaders/depmin/index.html','Deputy Minister','http://www.info.gov.za/leaders/depmin/');
$members=array_merge($members,$get);

function get_individual($url,$portfolio) {
    
    $member=array();
    $html2 = scraperWiki::scrape($url);
    $dom2 = new simple_html_dom();
    $dom2->load($html2);
    $name1=$dom2->find("h4");
    if (count($name1)>0) {
        $name2 = explode(',',$name1[0]->plaintext);
        $member['name']=$name2[0];
    }
    $member['portfolio']=$portfolio;
    return $member;
}

$members[]=get_individual('http://www.info.gov.za/leaders/president/index.htm','President');
$members[]=get_individual('http://www.info.gov.za/leaders/deppres/index.html','Deputy President');

scraperwiki::sqliteexecute("drop table if exists swdata"); 
scraperwiki::save(array(), $members);
?>
<?php
require 'scraperwiki/simple_html_dom.php';

$members=array();

function get_list($url,$type,$base) {
    $members2=array();
    $html = scraperWiki::scrape($url);                
    $dom = new simple_html_dom();
    $dom->load($html);
    $tables = $dom->find("table");
    $rows=$tables[9]->find("tr");
    foreach ($rows as $row) {
        print $row->plaintext;
        $columns=$row->find("td");
        $link=$row->find("a");
        //print $link->plaintext;
        $check=0;
        if(count($link)>0) {
            while($link[$check]->plaintext=='') {
                $check++;
            }
            if (substr($link[$check]->href,0,1)=='/') {
                $toscrape='http://www.info.gov.za'.$link[$check]->href;
            }
            else {
                $toscrape=$base.$link[$check]->href;
            }
            $html2 = scraperWiki::scrape($toscrape);
            $dom2 = new simple_html_dom();
            $dom2->load($html2);
            $name1=$dom2->find("h4");
        }
        
        if (count($name1)>0) {
            $name2 = explode(',',$name1[0]->plaintext);
            $name=$name2[0];
        }
        else {
            //print 'http://www.info.gov.za/leaders/ministers/'.$link[0]->href;
            $name = $columns[0]->plaintext;
        }
        //print $name;
        //$name = explode(',',$name1[0]->plaintext);
    
        $member=array();
        $member['name']=str_replace("\n",'',$name);
        $member['portfolio']=str_replace("\n",'',$columns[1]->plaintext);
        $member['type']=$type;
        $members2[]=$member;
    }
    return $members2;
}

$get=get_list('http://www.info.gov.za/leaders/ministers/index.html','Minister','http://www.info.gov.za/leaders/ministers/');
$members=array_merge($members,$get);
$get=get_list('http://www.info.gov.za/leaders/depmin/index.html','Deputy Minister','http://www.info.gov.za/leaders/depmin/');
$members=array_merge($members,$get);

function get_individual($url,$portfolio) {
    
    $member=array();
    $html2 = scraperWiki::scrape($url);
    $dom2 = new simple_html_dom();
    $dom2->load($html2);
    $name1=$dom2->find("h4");
    if (count($name1)>0) {
        $name2 = explode(',',$name1[0]->plaintext);
        $member['name']=$name2[0];
    }
    $member['portfolio']=$portfolio;
    return $member;
}

$members[]=get_individual('http://www.info.gov.za/leaders/president/index.htm','President');
$members[]=get_individual('http://www.info.gov.za/leaders/deppres/index.html','Deputy President');

scraperwiki::sqliteexecute("drop table if exists swdata"); 
scraperwiki::save(array(), $members);
?>
