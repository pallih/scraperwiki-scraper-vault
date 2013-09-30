<?php
$skipExisting = TRUE;

require 'scraperwiki/simple_html_dom.php';
scraperwiki::attach("reality_path_jmvs", "paths");            
$paths = scraperwiki::select("* from paths.swdata order by date desc");
$i=0;
scraperwiki::save_sqlite(array('path'),array('path'=>'nic'),'real_data');
foreach ($paths as $row)
{
    if ($skipExisting)
    {
        if(count(scraperwiki::select("
            path 
            FROM real_data 
            WHERE 
                (path = ?)
                OR 
                (path = ?) 
            LIMIT 1
        ",array($row['path'],"DEL: ".$row['path']))) > 0)
        {
            print ("Skipping ".$row['path']."\n");
            continue;
        }
    }

    $i++;
    $path = $row['path'];
    $found = FALSE;
    print ("http://www.sreality.cz$path\n");
    $html = scraperWiki::scrape("http://www.sreality.cz$path");
    $dom = new simple_html_dom();
    $dom->load($html);

    $datastr = "";
    foreach($dom->find("div[@id='infoColumn']") as $data) {
        $datastr = (string) $data;
        $found = TRUE;
    }

    $img = "";
    foreach($dom->find("div[@id='photoGallery'] img[@id='middlePhoto']") as $data) {
        $img = $data->getAttribute('src');
    }

    if ($found)
    {
        scraperwiki::save_sqlite(array('path'), array(
            'path' => $path,
            'data' => $datastr,
            'img' => $img,
            'lid2' => $i,
            'date' => date("Y-m-d H:i:s"),
        ),'real_data');
    } else {
        scraperwiki::save_sqlite(array('path'), array(
            'path' => "DEL: ".$path,
            'date' => date("Y-m-d H:i:s"),
            'del' => true
        ),'real_data');        
    }

}
<?php
$skipExisting = TRUE;

require 'scraperwiki/simple_html_dom.php';
scraperwiki::attach("reality_path_jmvs", "paths");            
$paths = scraperwiki::select("* from paths.swdata order by date desc");
$i=0;
scraperwiki::save_sqlite(array('path'),array('path'=>'nic'),'real_data');
foreach ($paths as $row)
{
    if ($skipExisting)
    {
        if(count(scraperwiki::select("
            path 
            FROM real_data 
            WHERE 
                (path = ?)
                OR 
                (path = ?) 
            LIMIT 1
        ",array($row['path'],"DEL: ".$row['path']))) > 0)
        {
            print ("Skipping ".$row['path']."\n");
            continue;
        }
    }

    $i++;
    $path = $row['path'];
    $found = FALSE;
    print ("http://www.sreality.cz$path\n");
    $html = scraperWiki::scrape("http://www.sreality.cz$path");
    $dom = new simple_html_dom();
    $dom->load($html);

    $datastr = "";
    foreach($dom->find("div[@id='infoColumn']") as $data) {
        $datastr = (string) $data;
        $found = TRUE;
    }

    $img = "";
    foreach($dom->find("div[@id='photoGallery'] img[@id='middlePhoto']") as $data) {
        $img = $data->getAttribute('src');
    }

    if ($found)
    {
        scraperwiki::save_sqlite(array('path'), array(
            'path' => $path,
            'data' => $datastr,
            'img' => $img,
            'lid2' => $i,
            'date' => date("Y-m-d H:i:s"),
        ),'real_data');
    } else {
        scraperwiki::save_sqlite(array('path'), array(
            'path' => "DEL: ".$path,
            'date' => date("Y-m-d H:i:s"),
            'del' => true
        ),'real_data');        
    }

}
