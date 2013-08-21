<?php
    $sourcescraper = 'test_php_2';
    $limit = 20;
    $offset = 0;

    scraperwiki::attach($sourcescraper);
    $keys = scraperwiki::sqliteexecute('select * from `'.$sourcescraper.'`.swdata limit ?', array($limit))->keys;
    sort($keys);

    print('<h2>Some data from scraper: '.$sourcescraper.'  ('.sizeof($keys).' columns)</h2>');
    print('<table border="1" style="border-collapse:collapse;">');

    # column headings
    print('<tr>');
    foreach ($keys as $key) {
        print('<th>'.$key.'</th>');
    }
    print('</tr>');

    # rows
    $rows = scraperwiki::select('* from `'.$sourcescraper.'`.swdata limit ? offset ?', array($limit, $offset));
    foreach($rows as $row) {
    print('<tr>');
        foreach ($keys as $key) {
            print('<td>'.$row[$key].'</td>');
        }
    print('</tr>');
    }
?>