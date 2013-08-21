<?php
######################################
# Basic PHP scraper
######################################

define('LOTRO_API_KEY', 'guumaster/4a87b3ce968590bb3168789187755b4d');
define('LOTRO_BASE_URL', 'http://data.lotro.com/'.LOTRO_API_KEY);

define('LOTRO_SERVICE_GUILDROSTER', LOTRO_BASE_URL."/guildroster/w/<world>/g/<guild>/");
define('LOTRO_SERVICE_CHARACTER', LOTRO_BASE_URL."/item/id/<item_id>/");
define('LOTRO_SERVICE_ITEM', LOTRO_BASE_URL."/charactersheet/w/<world>/c/<char_name>/");

class LOTRO
{
    function getGuildURL($world, $guild)
    {

    }
    
    function getItemURL($item_id)
    {
    
    }

    function getCharacterURL($char_name)
    {

    }
}
phpinfo();
var_dump( $_GET );

$xml  = scraperwiki::scrape("http://data.lotro.com/guumaster/4a87b3ce968590bb3168789187755b4d/charactersheet/w/Riddermark/c/Jessiriel/");

$data = new SimpleXMLElement($xml);
echo $data->character->attributes()->name;
die();

?>
