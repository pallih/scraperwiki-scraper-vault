<?php
require 'scraperwiki/simple_html_dom.php';

define('GUILD_ID', '870039153015434974'); // Kings of Numenor on Riddermark server

// thumbs = "http://content.turbine.com/sites/my.lotro.com/themes/default/media/common/class_icon_small/hunter.png"

function &get_page($page_number, &$members )
{
    $guild_id = GUILD_ID;
    $url = "http://my.lotro.com/guild-{$guild_id}/characters/?page={$page_number}";
    $html = scraperwiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $size = count($members);
    $idx = $size;
    $table = $dom->find('table[id=groster_header] tr');
    
    $labels = array('name', 'level', 'race', 'class', 'rank', 'toon_url');
    foreach($table as $row){
        $i=0;
        foreach($row->find('td') as $data) 
        {
            if( $i ==0 ) $idx++;
            $label = $labels[$i++];
            if( $label == 'class') 
            {
                $class = $data->childNodes(0)->getAttribute('title');
                $members[$idx][$label] = strtolower($class);
            }
            else 
            {
//                if( $label == 'name') 
//                {
//                    $members[$idx]['toon_url'] = str_replace(SERVER_PREFIX, "", $data->childNodes(0)->childNodes(0)->getAttribute('href'));
//                }
                $members[$idx][$label] = trim(chop(strtolower($data->plaintext)));
            }
        }
    }
    return $dom;
}

$members = array();

$page_one = get_page(1,$members);

/** PAGER */
$pager = $page_one->find('table.paginate_control td',2);

if( preg_match("/Page: ([0-1]+) of ([0-1]+)/", $pager->innertext, $matches))
{
    $total_pages = $matches[2];
    for( $x=2; $x <= $total_pages;$x++ )
    {
        get_page($x,$members);
    
    }
}

foreach( $members as $data )
{
    scraperwiki::save(array('name'),  $data);
}

$labels = array('name', 'level', 'race', 'class', 'rank');

scraperwiki::save_metadata('data_columns',$labels);
scraperwiki::save_metadata('private_columns','date_scraped');







<?php
require 'scraperwiki/simple_html_dom.php';

define('GUILD_ID', '870039153015434974'); // Kings of Numenor on Riddermark server

// thumbs = "http://content.turbine.com/sites/my.lotro.com/themes/default/media/common/class_icon_small/hunter.png"

function &get_page($page_number, &$members )
{
    $guild_id = GUILD_ID;
    $url = "http://my.lotro.com/guild-{$guild_id}/characters/?page={$page_number}";
    $html = scraperwiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $size = count($members);
    $idx = $size;
    $table = $dom->find('table[id=groster_header] tr');
    
    $labels = array('name', 'level', 'race', 'class', 'rank', 'toon_url');
    foreach($table as $row){
        $i=0;
        foreach($row->find('td') as $data) 
        {
            if( $i ==0 ) $idx++;
            $label = $labels[$i++];
            if( $label == 'class') 
            {
                $class = $data->childNodes(0)->getAttribute('title');
                $members[$idx][$label] = strtolower($class);
            }
            else 
            {
//                if( $label == 'name') 
//                {
//                    $members[$idx]['toon_url'] = str_replace(SERVER_PREFIX, "", $data->childNodes(0)->childNodes(0)->getAttribute('href'));
//                }
                $members[$idx][$label] = trim(chop(strtolower($data->plaintext)));
            }
        }
    }
    return $dom;
}

$members = array();

$page_one = get_page(1,$members);

/** PAGER */
$pager = $page_one->find('table.paginate_control td',2);

if( preg_match("/Page: ([0-1]+) of ([0-1]+)/", $pager->innertext, $matches))
{
    $total_pages = $matches[2];
    for( $x=2; $x <= $total_pages;$x++ )
    {
        get_page($x,$members);
    
    }
}

foreach( $members as $data )
{
    scraperwiki::save(array('name'),  $data);
}

$labels = array('name', 'level', 'race', 'class', 'rank');

scraperwiki::save_metadata('data_columns',$labels);
scraperwiki::save_metadata('private_columns','date_scraped');







