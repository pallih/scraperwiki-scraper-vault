<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.bls.gov/web/empsit/cpseea13.htm");
$html = str_get_html($html_content);

scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `unemployment_data` (`total_employed_in_labor_force` text, `percent_employed_in_labor_force` text, `monthyear` text, `total_unemployed_in_labor_force` text, `age` text, `total_civilian_labor_force` text, `not_in_labor_force` text, `race` text, `sex` text, `percent_unemployed_in_labor_force` text, `civilian_noninstitional_population` text, `percent_of_population_in_labor_force` text)");

scraperwiki::sqliteexecute("DELETE FROM `unemployment_data` WHERE `monthyear` LIKE '% 2011' OR `monthyear` LIKE '% 2012'");

$age = $sex = $race = null;

$monthyear = $html->find("table#cps_eande_m13 thead tr th[2]");
$monthyear = $monthyear[0]->innertext;

$monthyear = new DateTime($monthyear);
$monthyear = $monthyear->format('c');

foreach ($html->find("table#cps_eande_m13 tr") as $el) {
    $row = str_get_html($el);
    $col1 = $row->find("th p");
    if (count($col1) == 0) continue;

    $col1 = $col1[0]->innertext;
    if ($col1 == 'Women' || $col1 == 'Men') {
        $sex = $col1;
    } elseif (preg_match('/years/', $col1)) {
        $age = $col1;
    } else {
        $race = $col1;
    }

    $datavalues = $row->find("td span.datavalue");
    if (count($datavalues) == 0) continue;

    $datavalues = array_map(function($slice) {
        return($slice->innertext);
    }, $datavalues);

    list($population, $total_in_labor_force, $per_of_pop_in_labor, $total_employed, $per_employed, $total_unemployed, $per_unemployed, $not_in_labor_force) = $datavalues;

    $data = array(
        'monthyear' => $monthyear,
        'age' => $age,
        'sex' => $sex,
        'race' => $race,
        'civilian_noninstitional_population' => $population,
        'total_civilian_labor_force' => $total_in_labor_force,
        'percent_of_population_in_labor_force' => $per_of_pop_in_labor,
        'total_employed_in_labor_force' => $total_employed,
        'percent_employed_in_labor_force' => $per_employed,
        'total_unemployed_in_labor_force' => $total_unemployed,
        'percent_unemployed_in_labor_force' => $per_unemployed,
        'not_in_labor_force' => $not_in_labor_force
    );    

    scraperwiki::save_sqlite(array('monthyear', 'age', 'sex', 'race'), $data, "unemployment_data", 2);
}
<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.bls.gov/web/empsit/cpseea13.htm");
$html = str_get_html($html_content);

scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `unemployment_data` (`total_employed_in_labor_force` text, `percent_employed_in_labor_force` text, `monthyear` text, `total_unemployed_in_labor_force` text, `age` text, `total_civilian_labor_force` text, `not_in_labor_force` text, `race` text, `sex` text, `percent_unemployed_in_labor_force` text, `civilian_noninstitional_population` text, `percent_of_population_in_labor_force` text)");

scraperwiki::sqliteexecute("DELETE FROM `unemployment_data` WHERE `monthyear` LIKE '% 2011' OR `monthyear` LIKE '% 2012'");

$age = $sex = $race = null;

$monthyear = $html->find("table#cps_eande_m13 thead tr th[2]");
$monthyear = $monthyear[0]->innertext;

$monthyear = new DateTime($monthyear);
$monthyear = $monthyear->format('c');

foreach ($html->find("table#cps_eande_m13 tr") as $el) {
    $row = str_get_html($el);
    $col1 = $row->find("th p");
    if (count($col1) == 0) continue;

    $col1 = $col1[0]->innertext;
    if ($col1 == 'Women' || $col1 == 'Men') {
        $sex = $col1;
    } elseif (preg_match('/years/', $col1)) {
        $age = $col1;
    } else {
        $race = $col1;
    }

    $datavalues = $row->find("td span.datavalue");
    if (count($datavalues) == 0) continue;

    $datavalues = array_map(function($slice) {
        return($slice->innertext);
    }, $datavalues);

    list($population, $total_in_labor_force, $per_of_pop_in_labor, $total_employed, $per_employed, $total_unemployed, $per_unemployed, $not_in_labor_force) = $datavalues;

    $data = array(
        'monthyear' => $monthyear,
        'age' => $age,
        'sex' => $sex,
        'race' => $race,
        'civilian_noninstitional_population' => $population,
        'total_civilian_labor_force' => $total_in_labor_force,
        'percent_of_population_in_labor_force' => $per_of_pop_in_labor,
        'total_employed_in_labor_force' => $total_employed,
        'percent_employed_in_labor_force' => $per_employed,
        'total_unemployed_in_labor_force' => $total_unemployed,
        'percent_unemployed_in_labor_force' => $per_unemployed,
        'not_in_labor_force' => $not_in_labor_force
    );    

    scraperwiki::save_sqlite(array('monthyear', 'age', 'sex', 'race'), $data, "unemployment_data", 2);
}
