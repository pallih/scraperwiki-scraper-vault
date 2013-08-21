<?php
/**
The MIT License (MIT)

Copyright (c) 2013 ibnuyahya@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

/**
Preparing table structure
=========================
scraperwiki::sqliteexecute("drop table if exists publicgold"); 
scraperwiki::sqliteexecute('CREATE TABLE `publicgold` (`last_update` DATETIME,`item` TEXT,`sell` NUMERIC,`buy` NUMERIC)');
*/

    require 'scraperwiki/simple_html_dom.php';  
    $html = scraperWiki::scrape('http://publicgold.com.my/v1/');         
    $dom = new simple_html_dom();
    $dom->load($html);
  
    $trs = $dom->find('table',1)->find('tr');

    $last_update = trim($trs[0]->find('td',0)->plaintext);
    $last_update = str_replace('(Last updated ','',$last_update);
    $last_update = str_replace(')','',$last_update);
    $last_update = trim(str_replace('_',' ',$last_update));

    //gold bars
    $gold_bars = array();
    $gold_bars[] = array_merge(array('last_update'=>$last_update),get_data(3));
    $gold_bars[] = array_merge(array('last_update'=>$last_update),get_data(4));
    $gold_bars[] = array_merge(array('last_update'=>$last_update),get_data(5));
    $gold_bars[] = array_merge(array('last_update'=>$last_update),get_data(6));
    $gold_bars[] = array_merge(array('last_update'=>$last_update),get_data(7));
    $gold_bars[] = array_merge(array('last_update'=>$last_update),get_data(8));
    scraperwiki::save_sqlite(array('last_update', 'item'), $gold_bars,$table_name="publicgold");
    
    //dinars
    $dinars = array();
    $dinars[] = array_merge(array('last_update'=>$last_update),get_data(10));
    $dinars[] = array_merge(array('last_update'=>$last_update),get_data(11));
    $dinars[] = array_merge(array('last_update'=>$last_update),get_data(12));
    $dinars[] = array_merge(array('last_update'=>$last_update),get_data(13));
    scraperwiki::save_sqlite(array('last_update', 'item'), $dinars,$table_name="publicgold");
    

    function get_data($tr=0)
    {
        global $trs;
        return array(
            'item' => (string)$trs[$tr]->find('td',0)->plaintext,
            'sell' => preg_replace('/[^0-9.]/s', '',(string)$trs[$tr]->find('td',1)->plaintext),
            'buy' => preg_replace('/[^0-9.]/s', '',(string)$trs[$tr]->find('td',2)->plaintext),
    
        );
    }

?>
