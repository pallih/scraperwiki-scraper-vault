<?php



require 'scraperwiki/simple_html_dom.php'; 

/* Extract BLOCKS */

scraperwiki::sqliteexecute("create table if not exists blocks (number int, hash char(64), time string, transactions int, total_btc decimal, size_kb decimal)"); 

$url = "http://blockexplorer.com/";

$html = scraperwiki::scrape($url);

$dom = new simple_html_dom();
$dom->load($html);

foreach ($dom->find('table.txtable tr') as $row) {

    echo $row->plaintext . "\n";

    $vals = $row->find('td');

    if (!empty($vals)) {

      //  if (preg_match('/[0-9a-fA-F]{64}/', $vals[1]->innertext, $matches )) {

        $data[] = array(
            'number'       => $vals[0]->plaintext,
            'hash'         => $matches[0],
            'time'         => $vals[2]->plaintext,
            'transactions' => $vals[3]->plaintext,
            'total_btc'    => $vals[4]->plaintext,
            'size_kb'      => $vals[5]->plaintext
        );
     //   };
    }
};

scraperwiki::save_sqlite(array('number'),$data, "blocks");

/* Extract block data */

/* Extract transactions */

?>