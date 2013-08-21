<?php
$sourcescraper = 'german-landkreise';
scraperwiki::attach($sourcescraper);           


$grouped_by_state = scraperwiki::select("state, COUNT(*) AS num FROM swdata GROUP BY state");
$all_by_population = scraperwiki::select("name, inhabitants FROM swdata ORDER BY inhabitants DESC");
$all_by_area = scraperwiki::select("name, CAST(area AS NUMERIC) AS area FROM swdata ORDER BY area DESC");
$all_by_density = scraperwiki::select("name, inhab_density FROM swdata ORDER BY inhab_density DESC");

echo '<h2>Landkreise nach Bundesland</h2>';
echo '<table>';
foreach ($grouped_by_state AS $item) {
    echo '<tr><td>'.$item['state'].'</td><td>'.$item['num'].'</td></tr>'."\n";
}
echo '</table>';

echo '<h2>Landkreise nach Einwohnerzahl</h2>';
echo '<table>';
foreach ($all_by_population AS $item) {
    echo '<tr><td>'.$item['name'].'</td><td>'.$item['inhabitants'].'</td></tr>'."\n";
}
echo '</table>';

echo '<h2>Landkreise nach Fläche (km<sup>2</sup>)</h2>';
echo '<table>';
foreach ($all_by_area AS $item) {
    echo '<tr><td>'.$item['name'].'</td><td>'.$item['area'].'</td></tr>'."\n";
}
echo '</table>';

echo '<h2>Landkreise nach Bevölkerungsdichte (Einwohner/km<sup>2</sup>)</h2>';
echo '<table>';
foreach ($all_by_density AS $item) {
    echo '<tr><td>'.$item['name'].'</td><td>'.$item['inhab_density'].'</td></tr>'."\n";
}
echo '</table>';


?>
