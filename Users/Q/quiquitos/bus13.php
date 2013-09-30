<?php
    require 'scraperwiki/simple_html_dom.php';           
    
    $html = scraperWiki::scrape("http://www.payscale.com/research/US/Country=United_States/Salary/by_Employer");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div[id='mainBarChar']>div>table>tbody>tr") as $tr) {
        $ths = $tr->find("th>a");
        $tds = $tr->find("td[class*='vm']");
        if (sizeof($ths) == 1 && sizeof($tds) == 1) { 
            $record = array();
            $record['employer_name'] = $ths[0]->plaintext;
            $payRange = $tds[0]->plaintext;
            $token = strtok($payRange, "-");
            $payArr = array();
            $i = 0;
            while ($token != false)
            {
                #print_r("  i is " . $i);
                #print_r("  token is: " . $token . " ");
                $payArr[$i] = $token;
                $i = $i + 1;
                $token = strtok(" ");
            }
            #foreach($payArr as $p) {
            #    print_r(" element is " . $p . " ");
            #}
            #print_r(" 0 element is " . $payArr[0]);
            #print_r(" 1 element is " . $payArr[1]);
            $record['low_range'] = rtrim((string)($payArr[0]));
            $record['high_range'] = ltrim((string)($payArr[1]));
            #print_r($record);
            scraperwiki::save( array( 'employer_name' ), $record );
        }
    }
?>
<?php
    require 'scraperwiki/simple_html_dom.php';           
    
    $html = scraperWiki::scrape("http://www.payscale.com/research/US/Country=United_States/Salary/by_Employer");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div[id='mainBarChar']>div>table>tbody>tr") as $tr) {
        $ths = $tr->find("th>a");
        $tds = $tr->find("td[class*='vm']");
        if (sizeof($ths) == 1 && sizeof($tds) == 1) { 
            $record = array();
            $record['employer_name'] = $ths[0]->plaintext;
            $payRange = $tds[0]->plaintext;
            $token = strtok($payRange, "-");
            $payArr = array();
            $i = 0;
            while ($token != false)
            {
                #print_r("  i is " . $i);
                #print_r("  token is: " . $token . " ");
                $payArr[$i] = $token;
                $i = $i + 1;
                $token = strtok(" ");
            }
            #foreach($payArr as $p) {
            #    print_r(" element is " . $p . " ");
            #}
            #print_r(" 0 element is " . $payArr[0]);
            #print_r(" 1 element is " . $payArr[1]);
            $record['low_range'] = rtrim((string)($payArr[0]));
            $record['high_range'] = ltrim((string)($payArr[1]));
            #print_r($record);
            scraperwiki::save( array( 'employer_name' ), $record );
        }
    }
?>
