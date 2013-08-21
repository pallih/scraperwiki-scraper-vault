<?php

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL,"http://www.lcsupply.com");
curl_setopt($ch, CURLOPT_TIMEOUT, 30); //timeout after 30 seconds
curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);
$result=curl_exec ($ch);
curl_close ($ch);
// Search The Results From The Starting Site
if( $result )
{
// I LOOK ONLY FROM TOP domains change this for your usage 
preg_match_all( '/<a href="(http:\/\/www.[^0-9].+?)"/', $result, $output, PREG_SET_ORDER );

foreach( $output as $item )

{
// ALL LINKS DISPLAY HERE 
print_r($item);

// NOW YOU ADD IN YOU DATABASE AND MAKE A LOOP TO ENGINE NEVER STOP 


}

}

?>