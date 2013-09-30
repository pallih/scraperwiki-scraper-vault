<?php

/* scraper by Tomasz Polonczyk http://www.tomot.eu */

require 'scraperwiki/simple_html_dom.php'; 

/* Extract BLOCKS */

scraperwiki::sqliteexecute("create table if not exists data (col1 char(24), col2 int(24), col3 char(24), col4 char(24), col5 char(24), col6 char(24), col7 char(24), col8 char(24), col9 char(24), col10 char(24), col11 char(24), col12 char(24), col13 char(24))"); 

for ($i=1;$i<=2;$i++){

$url = "http://www.gw2db.com/recipes/cook?page=$i";

$html = scraperwiki::scrape($url);

$dom = new simple_html_dom();
$dom->load($html);

foreach ($dom->find('table tr') as $row) {
    
    
    echo $row . "\n";
 // echo $row->find('a',3)->href . $row->find('a',4)->href . $row->find('a',5)->href . $row->find('a',6)->href;

 

    $vals = $row->find('td');
//print_r($vals) ;

//echo test.$vals[4].test;

//    if (!empty($vals)) {

   //     if (preg_match('/[0-9a-fA-F]{64}/', $vals[1]->innertext, $matches )) {




$string = $vals[4]->plaintext; 

preg_match_all('/\d+/', $string, $ing); 



        $data[] = array(
            'col1'       => $vals[0]->plaintext,
         //   '#2'         => $matches[0],
            'col2'         => $vals[1]->plaintext,
            'col3'         => $vals[2]->plaintext,
            'col4'         => $vals[3]->plaintext,
            'col6'         => $ing[0][0],
            'col7'         => str_replace('-',' ',strstr($row->find('a',3)->href, '-')),
            'col8'         => $ing[0][1],
            'col9'         => str_replace('-',' ',strstr($row->find('a',4)->href, '-')),
            'col10'         => $ing[0][2],
            'col11'         => str_replace('-',' ',strstr($row->find('a',5)->href, '-')),
            'col12'         => $ing[0][3],
            'col13'         => str_replace('-',' ',strstr($row->find('a',6)->href, '-')),
         //   'col5'         => $vals[4]->plaintext
          //  
        );
    //    };
//    }
};

scraperwiki::save_sqlite(array('col1'),$data, "data"); 

/* Extract block data */

/* Extract transactions */
}

?>


<?php

/* scraper by Tomasz Polonczyk http://www.tomot.eu */

require 'scraperwiki/simple_html_dom.php'; 

/* Extract BLOCKS */

scraperwiki::sqliteexecute("create table if not exists data (col1 char(24), col2 int(24), col3 char(24), col4 char(24), col5 char(24), col6 char(24), col7 char(24), col8 char(24), col9 char(24), col10 char(24), col11 char(24), col12 char(24), col13 char(24))"); 

for ($i=1;$i<=2;$i++){

$url = "http://www.gw2db.com/recipes/cook?page=$i";

$html = scraperwiki::scrape($url);

$dom = new simple_html_dom();
$dom->load($html);

foreach ($dom->find('table tr') as $row) {
    
    
    echo $row . "\n";
 // echo $row->find('a',3)->href . $row->find('a',4)->href . $row->find('a',5)->href . $row->find('a',6)->href;

 

    $vals = $row->find('td');
//print_r($vals) ;

//echo test.$vals[4].test;

//    if (!empty($vals)) {

   //     if (preg_match('/[0-9a-fA-F]{64}/', $vals[1]->innertext, $matches )) {




$string = $vals[4]->plaintext; 

preg_match_all('/\d+/', $string, $ing); 



        $data[] = array(
            'col1'       => $vals[0]->plaintext,
         //   '#2'         => $matches[0],
            'col2'         => $vals[1]->plaintext,
            'col3'         => $vals[2]->plaintext,
            'col4'         => $vals[3]->plaintext,
            'col6'         => $ing[0][0],
            'col7'         => str_replace('-',' ',strstr($row->find('a',3)->href, '-')),
            'col8'         => $ing[0][1],
            'col9'         => str_replace('-',' ',strstr($row->find('a',4)->href, '-')),
            'col10'         => $ing[0][2],
            'col11'         => str_replace('-',' ',strstr($row->find('a',5)->href, '-')),
            'col12'         => $ing[0][3],
            'col13'         => str_replace('-',' ',strstr($row->find('a',6)->href, '-')),
         //   'col5'         => $vals[4]->plaintext
          //  
        );
    //    };
//    }
};

scraperwiki::save_sqlite(array('col1'),$data, "data"); 

/* Extract block data */

/* Extract transactions */
}

?>


