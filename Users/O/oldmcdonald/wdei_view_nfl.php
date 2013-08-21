<?php
# Blank PHP
$sourcescraper = 'wdei_scraper_nfl';

scraperwiki::attach('wdei_scraper_nfl');

$data = scraperwiki::select(           
    "team, \"points/game\", \"yards/game\", \"nextOpponent\" from swdata;"
);

?>
<table border="1px solid black">
<tr>
<?php
foreach($data[0] as $key => $val){
    if($key != 'link'){
        echo '<th>'.$key.'</th>'."\n";
    }
}
echo '</tr>'."\n";
$first = true;
foreach($data as $team){
    echo "<tr>\n";
        foreach($team as $key => $val){
            if($key != 'link'){
                echo '<td>' . $val . '</td>'."\n";
            }
        }
    $first = false;
    echo "</tr>\n";
}
?>
</table>
<?php

?>
