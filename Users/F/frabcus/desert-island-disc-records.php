<?php

require  'scraperwiki/simple_html_dom.php';

function do_day($rec) {
    
    $html = scraperwiki::scrape($rec['url']);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $cell = $dom->find('a[name=discs]');
    
    $lines = $cell[0]->parent->find('text');
    print $lines[10] . "\n";
    print count($lines) . "\n";

    # loop by number, as null lines stop a foreach
    $n = 0;
    for ($line_no = 0; $line_no < count($lines); $line_no++) {
        $line = $lines[$line_no];
        if (strlen($line) == 3) { # the DOM object crashes on this row, so ignore
            continue;
        }
        #if (preg_match("#^" . $n . "#", $line, $matches)) {
            print $line_no . " " . strlen($line) . "\n";
            $n = $n + 1;
            print $line . "\n";
        #}
    }

    #scraperwiki::save(array('data'), array('data' => $data->plaintext));
};

$rec = array('guest' => 'Anne Scott-James', 'url' => 'http://www.bbc.co.uk/radio4/factual/desertislanddiscs_20041010.shtml', 'date' => '2004-10-10');
do_day($rec);

print "Finished\n";
?>