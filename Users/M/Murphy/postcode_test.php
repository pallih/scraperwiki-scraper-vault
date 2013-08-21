<?php
$postcode = "CF14 2QW";
$lat_lng = scraperwiki::gb_postcode_to_latlng($postcode);
                if ($lat_lng)
                {
                    $values["lat"] = $lat_lng[0]; 
                    $values["lng"] = $lat_lng[1]; 
                }  

print  $values["lat"];
print  $values["lng"];

$nameindex = 0;
$nameindex =+11111111111115;

print $nameindex;
?>
