<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

define("TOON_URL_PATTERN", "http://my.lotro.com/home/character/riddermark/<toon>/");
define('ITEM_URL_PATTERN', "/".preg_quote('http://lorebook.lotro.com/wiki/Special:LotroResource?id=', "/" )."([0-9]+)$/");

// class_banner pattern 
// http://content.turbine.com/sites/playerportal/modules/characterwidget/images/class_banners/lore-master.png

$short_name = 'kon_members-1';
ScraperWiki::attach($short_name, 'src');
$data = ScraperWiki::select("* from swdata");
$i=0;

$names = array();
foreach($data as $member)
{
    $names[] = $member->name;
}
unset($data);
sort($names);

$START = 0;
$END = count($names);
$OFFSET = 0;


for($i=$START;$i<$END+$OFFSET;$i++)
{
    $toon = get_freep_data($names[$i]);
    if( $i == $START) $labels = array_keys($toon);

    scraperwiki::save(array('name'),  $toon);
    echo "{$i}.memory used:".memory_get_usage()."\n";
    unset($toon);
}

scraperwiki::save_metadata('data_columns',$labels);
scraperwiki::save_metadata('private_columns','date_scraped');



function get_freep_data($name)
{
    $url = str_replace("<toon>", $name, TOON_URL_PATTERN);
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    $char = array();
    $char['name'] = $name;

    # MAIN 
    foreach( $dom->find("div.char_equip") as $data)
    {
        $char['origin'] = $data->find('div.char_nat', 0)->plaintext;
        $char['class'] =  $data->find('div.char_class', 0)->plaintext;
        $char['level'] =  $data->find('div.char_level', 0)->plaintext;
        $char['race'] =  $data->find('div.char_race', 0)->plaintext;
        $char['morale'] = $data->find('div.morale', 0)->plaintext;
        $char['power'] = $data->find('div.power', 0)->plaintext;
        $char['armour'] = $data->find('div.armour', 0)->plaintext;
        
        # EQUIPMENT
        $slot = 2;
        foreach( $data->find('a.equipment_icon') as $equip ) 
        {
            $item = $equip->href;
            preg_match(ITEM_URL_PATTERN,$item, $matches);
            $char['slot_'.$slot++] = $matches[1];
        }
    }

    # STATS
    foreach( $dom->find("table.stat_list tr") as $data)
    {
        $stat_name = trim(chop($data->find('th', 0)->plaintext));
        $stat_value = trim(chop($data->find('td', 0)->plaintext)); 
        if( !empty( $stat_value ) )
        {
            $char[$stat_name] = $stat_value;
        }
    }
    $dom->clear(); // simplehtmldom has serious memory leaks, more info: http://simplehtmldom.sourceforge.net/manual_faq.htm#memory_leak
    unset($dom, $html, $matches);
    return $char;

}


<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

define("TOON_URL_PATTERN", "http://my.lotro.com/home/character/riddermark/<toon>/");
define('ITEM_URL_PATTERN', "/".preg_quote('http://lorebook.lotro.com/wiki/Special:LotroResource?id=', "/" )."([0-9]+)$/");

// class_banner pattern 
// http://content.turbine.com/sites/playerportal/modules/characterwidget/images/class_banners/lore-master.png

$short_name = 'kon_members-1';
ScraperWiki::attach($short_name, 'src');
$data = ScraperWiki::select("* from swdata");
$i=0;

$names = array();
foreach($data as $member)
{
    $names[] = $member->name;
}
unset($data);
sort($names);

$START = 0;
$END = count($names);
$OFFSET = 0;


for($i=$START;$i<$END+$OFFSET;$i++)
{
    $toon = get_freep_data($names[$i]);
    if( $i == $START) $labels = array_keys($toon);

    scraperwiki::save(array('name'),  $toon);
    echo "{$i}.memory used:".memory_get_usage()."\n";
    unset($toon);
}

scraperwiki::save_metadata('data_columns',$labels);
scraperwiki::save_metadata('private_columns','date_scraped');



function get_freep_data($name)
{
    $url = str_replace("<toon>", $name, TOON_URL_PATTERN);
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    $char = array();
    $char['name'] = $name;

    # MAIN 
    foreach( $dom->find("div.char_equip") as $data)
    {
        $char['origin'] = $data->find('div.char_nat', 0)->plaintext;
        $char['class'] =  $data->find('div.char_class', 0)->plaintext;
        $char['level'] =  $data->find('div.char_level', 0)->plaintext;
        $char['race'] =  $data->find('div.char_race', 0)->plaintext;
        $char['morale'] = $data->find('div.morale', 0)->plaintext;
        $char['power'] = $data->find('div.power', 0)->plaintext;
        $char['armour'] = $data->find('div.armour', 0)->plaintext;
        
        # EQUIPMENT
        $slot = 2;
        foreach( $data->find('a.equipment_icon') as $equip ) 
        {
            $item = $equip->href;
            preg_match(ITEM_URL_PATTERN,$item, $matches);
            $char['slot_'.$slot++] = $matches[1];
        }
    }

    # STATS
    foreach( $dom->find("table.stat_list tr") as $data)
    {
        $stat_name = trim(chop($data->find('th', 0)->plaintext));
        $stat_value = trim(chop($data->find('td', 0)->plaintext)); 
        if( !empty( $stat_value ) )
        {
            $char[$stat_name] = $stat_value;
        }
    }
    $dom->clear(); // simplehtmldom has serious memory leaks, more info: http://simplehtmldom.sourceforge.net/manual_faq.htm#memory_leak
    unset($dom, $html, $matches);
    return $char;

}


