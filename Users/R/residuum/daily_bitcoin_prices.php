<?php
$new_values = scraperwiki::scrape('http://bitcoincharts.com/t/weighted_prices.json');
$json = json_decode($new_values, TRUE);
$data = array("DATE" => time(), "EUR" => $json["EUR"]["24h"], "USD" => $json["USD"]["24h"]);
$result = scraperwiki::save_sqlite(array("DATE"), $data);
scraperwiki::sqlitecommit();
?>
<?php
$new_values = scraperwiki::scrape('http://bitcoincharts.com/t/weighted_prices.json');
$json = json_decode($new_values, TRUE);
$data = array("DATE" => time(), "EUR" => $json["EUR"]["24h"], "USD" => $json["USD"]["24h"]);
$result = scraperwiki::save_sqlite(array("DATE"), $data);
scraperwiki::sqlitecommit();
?>
