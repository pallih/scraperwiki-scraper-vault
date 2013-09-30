<?php
require 'simple_html_dom.php'

$dom = new simple_html_dom();

$html;

$teamsArray = array('ducks' , 'flames', 'blackhawks', 'avalanche', 'stars', 'oilers', 'kings', 'wild', 'predators', 'coyotes', 'sharks', 'blues', 'canucks', 'jets', 'bruins', 'sabres', 'hurricanes', 'bluejackets', 'redwings', 'panthers', 'canadiens', 'devils', 'islanders', 'rangers', 'senators', 'flyers', 'penguins', 'lightning', 'mapleleafs', 'capitals', );

for($i=0; $i<30; $i++) {
    $team = $teamsArray[$i];
    print $team;
    $html .= scraperWiki::scrape("http://capgeek.com/" . $team . "/"); 
    $dom->load($html);
    console.log($html);
    foreach($dom->find("table[@id='salarychart'] tr") as $data){
        $name = $data->find("td[@class='player'] a");
        $tds = $data->find('td');
        $salary = $tds[2]->find("span[@class='salary']");
        $cap = $tds[2]->find("span[@class='cap_hit']");
        $record = array(
            'name' => $name, 
            'team' => $team, 
            'salary' => $salary,
            'cap' => $cap
        );
        scraperwiki::save(array('name'), $record);           
    }

    $html = "";
}

?>