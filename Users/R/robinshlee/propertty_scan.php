<?php
require 'scraperwiki/simple_html_dom.php';

$domain="www.iproperty.com.my";
#modes: [S,R,N]-[Sale,Rent,New]
$mode = "t=S";
#types: [AR,A,E,T,B,R,AC,S,H,C,AI,F,I,AA,G]-[All Res,Apt,Condo,Terrace,Bungalow,Res Land,All Comm,Shop,Hotel,Comm Land,All Ind,Factory,Ind Land,All Agri,Agri]
$type = "gpt=E";
#states: [KL,JO,KE,KT,MA,NS,OT,PA,PE,PK,PL,PJ,SA,SW,SE,TR]
$state = "st=SE";
$minp = "mp=100000";
$maxp = "xp=400000";

$url = "http://".$domain."/property/searchresult.aspx?";
$url = $url."&".$mode;
$url = $url."&".$type;
$url = $url."&".$state;
$url = $url."&ct=";
$url = $url."&k=";
$url = $url."&pt=";
$url = $url."&".$minp;
$url = $url."&".$maxp;
$url = $url."&mbr=&xbr=&mbu=&xbu=&lo=&wp=&wv=&wa=&ht=&au=&sby=&ns=1";
#print $url."\n";

$html = str_get_html(scraperWiki::scrape($url));
#print $html."\n";
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('//*[@id="box-525w-container"]/div[?]/div/div[3]/a[2]') as $data) {
#    print $data;
    $link = $data->href;
#    print $link;
#    print "\n";
    $url = "http://".$domain.$link;
    $page = str_get_html(scraperWiki::scrape($url));

    $dom2 = new simple_html_dom();
    $dom2->load($page);

#    $property = $dom2->find('//*[@id="contentarea"]/h6');
#    var_dump($property[0]);
#    print "\n";

    $record = array(
        'propname' => $link
        );
#    scraperwiki::save(array('name'), $record);

    $found = false;
    foreach($dom2->find('//*[@id="contentarea"]/div[4]/ul') as $table) {
#        print $table;
        $found = true;
        $rows = $table->find("li");
        for ($i = 0; $i < count($rows); $i++) {
            $items = $rows[$i]->find("span");
#            $rec = array(
#                    $items[0]->plaintext => $items[1]->plaintext
#                );
#            print json_encode($record);
#            print "\n";
#            array_merge($record, $rec);
            $column = preg_replace('/[^A-Za-z0-9]/', '', strtolower($items[0]->plaintext));
            $record[$column] = trim($items[1]->plaintext);            
        }
    }

    if (!$found) {
        foreach($dom2->find('//*[@id="contentarea"]/div[5]/ul') as $table) {
#            print $table;
            $found = true;
            $rows = $table->find("li");
            for ($i = 0; $i < count($rows); $i++) {
                $items = $rows[$i]->find("span");
#                $rec = array(
#                        $items[0]->plaintext => $items[1]->plaintext
#                    );
#                print json_encode($record)
#                print "\n";
#                array_merge($record, $rec);
                $column = preg_replace('/[^A-Za-z0-9]/', '', strtolower($items[0]->plaintext));
                $record[$column] = trim($items[1]->plaintext);            
            }
        }
    }
#    print json_encode($record);
#    print "\n";
#    break;
    scraperwiki::save(array('propname'), $record);
}
?><?php
require 'scraperwiki/simple_html_dom.php';

$domain="www.iproperty.com.my";
#modes: [S,R,N]-[Sale,Rent,New]
$mode = "t=S";
#types: [AR,A,E,T,B,R,AC,S,H,C,AI,F,I,AA,G]-[All Res,Apt,Condo,Terrace,Bungalow,Res Land,All Comm,Shop,Hotel,Comm Land,All Ind,Factory,Ind Land,All Agri,Agri]
$type = "gpt=E";
#states: [KL,JO,KE,KT,MA,NS,OT,PA,PE,PK,PL,PJ,SA,SW,SE,TR]
$state = "st=SE";
$minp = "mp=100000";
$maxp = "xp=400000";

$url = "http://".$domain."/property/searchresult.aspx?";
$url = $url."&".$mode;
$url = $url."&".$type;
$url = $url."&".$state;
$url = $url."&ct=";
$url = $url."&k=";
$url = $url."&pt=";
$url = $url."&".$minp;
$url = $url."&".$maxp;
$url = $url."&mbr=&xbr=&mbu=&xbu=&lo=&wp=&wv=&wa=&ht=&au=&sby=&ns=1";
#print $url."\n";

$html = str_get_html(scraperWiki::scrape($url));
#print $html."\n";
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('//*[@id="box-525w-container"]/div[?]/div/div[3]/a[2]') as $data) {
#    print $data;
    $link = $data->href;
#    print $link;
#    print "\n";
    $url = "http://".$domain.$link;
    $page = str_get_html(scraperWiki::scrape($url));

    $dom2 = new simple_html_dom();
    $dom2->load($page);

#    $property = $dom2->find('//*[@id="contentarea"]/h6');
#    var_dump($property[0]);
#    print "\n";

    $record = array(
        'propname' => $link
        );
#    scraperwiki::save(array('name'), $record);

    $found = false;
    foreach($dom2->find('//*[@id="contentarea"]/div[4]/ul') as $table) {
#        print $table;
        $found = true;
        $rows = $table->find("li");
        for ($i = 0; $i < count($rows); $i++) {
            $items = $rows[$i]->find("span");
#            $rec = array(
#                    $items[0]->plaintext => $items[1]->plaintext
#                );
#            print json_encode($record);
#            print "\n";
#            array_merge($record, $rec);
            $column = preg_replace('/[^A-Za-z0-9]/', '', strtolower($items[0]->plaintext));
            $record[$column] = trim($items[1]->plaintext);            
        }
    }

    if (!$found) {
        foreach($dom2->find('//*[@id="contentarea"]/div[5]/ul') as $table) {
#            print $table;
            $found = true;
            $rows = $table->find("li");
            for ($i = 0; $i < count($rows); $i++) {
                $items = $rows[$i]->find("span");
#                $rec = array(
#                        $items[0]->plaintext => $items[1]->plaintext
#                    );
#                print json_encode($record)
#                print "\n";
#                array_merge($record, $rec);
                $column = preg_replace('/[^A-Za-z0-9]/', '', strtolower($items[0]->plaintext));
                $record[$column] = trim($items[1]->plaintext);            
            }
        }
    }
#    print json_encode($record);
#    print "\n";
#    break;
    scraperwiki::save(array('propname'), $record);
}
?>