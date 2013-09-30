<?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.onemotoring.com.sg/1m/coe/coeDetail.html"); 

$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find('table.table_standard_type2', 0); 

$entry = 0;
foreach ($table->find('tr') as $row)
{
    $element = $row->find('td');
    if ($element)
    {
        $record_first_half[$entry] = array(
            'category'    => $element[0]->plaintext,
            'description' => $element[1]->plaintext,
            'quota'       => $element[2]->plaintext,
            'qp'          => $element[3]->plaintext,
            'pqp'         => $element[4]->plaintext
            );

        $entry++;
    }
}

$entry =0;
$table = $dom->find('table.table_standard_type2', 1); 
foreach ($table->find('tr') as $row)
{
    $element = $row->find('td');
    if ($element)
    {
        $record_second_half[$entry] = array(
            'category'     => $element[0]->plaintext,
            'received'     => $element[2]->plaintext,
            'successful'   => $element[3]->plaintext,
            'unsuccessful' => $element[4]->plaintext,
            'unused'       => $element[5]->plaintext
            );

        $entry++;
    }
}

for (;$entry >0; $entry--)
{
    $full_record = array_merge($record_first_half[$entry-1], $record_second_half[$entry-1]);
    scraperwiki::save(array('category'), $full_record);
}
?>
<?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.onemotoring.com.sg/1m/coe/coeDetail.html"); 

$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find('table.table_standard_type2', 0); 

$entry = 0;
foreach ($table->find('tr') as $row)
{
    $element = $row->find('td');
    if ($element)
    {
        $record_first_half[$entry] = array(
            'category'    => $element[0]->plaintext,
            'description' => $element[1]->plaintext,
            'quota'       => $element[2]->plaintext,
            'qp'          => $element[3]->plaintext,
            'pqp'         => $element[4]->plaintext
            );

        $entry++;
    }
}

$entry =0;
$table = $dom->find('table.table_standard_type2', 1); 
foreach ($table->find('tr') as $row)
{
    $element = $row->find('td');
    if ($element)
    {
        $record_second_half[$entry] = array(
            'category'     => $element[0]->plaintext,
            'received'     => $element[2]->plaintext,
            'successful'   => $element[3]->plaintext,
            'unsuccessful' => $element[4]->plaintext,
            'unused'       => $element[5]->plaintext
            );

        $entry++;
    }
}

for (;$entry >0; $entry--)
{
    $full_record = array_merge($record_first_half[$entry-1], $record_second_half[$entry-1]);
    scraperwiki::save(array('category'), $full_record);
}
?>
