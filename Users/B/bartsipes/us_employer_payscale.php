<?php
    require 'scraperwiki/simple_html_dom.php';           
    
    #$html = #scraperWiki::scrape("http://www.payscale.com/research/US/Country=United_States/Salary/by_Employer");
    $html = scraperWiki::scrape("http://www.payscale.com/index/US/Employer");
    $dom = new simple_html_dom();
    $dom->load($html);

    #foreach($dom->find("div[id='mainBarChar']>div>table>tbody>tr") as $tr) {
    #    $ths = $tr->find("th>a");
    #    $tds = $tr->find("td[class*='vm']");


    foreach($dom->find("div[class='indexResults'] table tbody tr[class='underlinedItem'] td a") as $a) {
    
    #$as = $dom->find("div[class='indexResults'] table tbody tr[class='underlinedItem'] td a");

    #if (sizeof($as) >= 1) {

    #    $a = $as[0];

        if (!empty($a)) {
            #print_r(" href: " . $a->href);
            $empHtml = scraperWiki::scrape("http://www.payscale.com" . $a->href);
            $empDom = new simple_html_dom();
            $empDom->load($empHtml);

            $record = array();

            $employerName = $empDom->find("input[name='jobtitle']");
            $record['employer_name'] = $employerName[0]->value;

            foreach ($empDom->find("tr.genderRow") as $tr) {
                $tds = $tr->find("td");

                if(sizeof($tds) >= 4) {
                    $fPayRange = $tds[1]->plaintext;
                    $token = strtok($fPayRange, "-");
                    $payArr = array();
                    $i = 0;
                    while ($token != false)
                    {
                        $payArr[$i] = $token;
                        $i = $i + 1;
                        $token = strtok(" ");
                    }
        
                    $record['female_low_range'] = rtrim((string)($payArr[0]));
                    $record['female_high_range'] = ltrim((string)($payArr[1]));

                    $mPayRange = $tds[3]->plaintext;
                    $token = strtok($mPayRange , "-");
                    $payArr = array();
                    $i = 0;
                    while ($token != false)
                    {
                        $payArr[$i] = $token;
                        $i = $i + 1;
                        $token = strtok(" ");
                    }
        
                    $record['male_low_range'] = rtrim((string)($payArr[0]));
                    $record['male_high_range'] = ltrim((string)($payArr[1]));
                }
            }

            $malePer = $empDom->find("div[id='male_percent']");
            if(sizeof($malePer) >= 1) {
                $record['male_percent'] = $malePer[0]->plaintext;
            }

            $femPer= $empDom->find("div[id='female_percent]");
            if(sizeof($femPer) >= 1) {
                $record['female_percent'] = $femPer[0]->plaintext;
            }

            $stress = $empDom->find("table[class='JobStressTable'] tbody tr td div img[class='selected']");
            if(sizeof($stress) >= 1) {
                $record['stress_level'] = $stress[0]->parent()->plaintext;
            }

            $bsDeg = $empDom->find("a[href='/research/US/Degree=Bachelor%27s_Degree']");
            if(sizeof($bsDeg) >= 1) {
                $bsPayRange = $bsDeg[0]->parent()->next_sibling()->plaintext;
                $token = strtok($bsPayRange, "-");
                $payArr = array();
                $i = 0;
                while ($token != false)
                {
                    $payArr[$i] = $token;
                    $i = $i + 1;
                    $token = strtok(" ");
                }
                $record['bachelor_degree_low_range'] = rtrim((string)($payArr[0]));
                $record['bachelor_degree_high_range'] = ltrim((string)($payArr[1]));  
            }

            $asDeg = $empDom->find("a[href='/research/US/Degree=Associate%27s_Degree']");
            if(sizeof($asDeg) >= 1) {
                $asPayRange = $asDeg[0]->parent()->next_sibling()->plaintext;
                $token = strtok($asPayRange, "-");
                $payArr = array();
                $i = 0;
                while ($token != false)
                {
                    $payArr[$i] = $token;
                    $i = $i + 1;
                    $token = strtok(" ");
                }
                $record['associate_degree_low_range'] = rtrim((string)($payArr[0]));
                $record['associate_degree_high_range'] = ltrim((string)($payArr[1])); 
            }

            #print_r(str_replace(" ", "+", $record['employer_name']));
            #$sectorHtml = scraperWiki::scrape("http://www.google.com/finance?q=" . str_replace(" ", "+", $record['employer_name']));
            #$sectorDom = new simple_html_dom();
            #$sectorDom->load($sectorHtml);

            #$sa = $sectorDom->find("a[id='sector']");
            #if (sizeof($sa) >= 1) {
            #    $record['sector'] = $sa[0]->plaintext;
            #}


            #print_r($record);
            scraperwiki::save( array( 'employer_name' ), $record );
        }
    }
?>
<?php
    require 'scraperwiki/simple_html_dom.php';           
    
    #$html = #scraperWiki::scrape("http://www.payscale.com/research/US/Country=United_States/Salary/by_Employer");
    $html = scraperWiki::scrape("http://www.payscale.com/index/US/Employer");
    $dom = new simple_html_dom();
    $dom->load($html);

    #foreach($dom->find("div[id='mainBarChar']>div>table>tbody>tr") as $tr) {
    #    $ths = $tr->find("th>a");
    #    $tds = $tr->find("td[class*='vm']");


    foreach($dom->find("div[class='indexResults'] table tbody tr[class='underlinedItem'] td a") as $a) {
    
    #$as = $dom->find("div[class='indexResults'] table tbody tr[class='underlinedItem'] td a");

    #if (sizeof($as) >= 1) {

    #    $a = $as[0];

        if (!empty($a)) {
            #print_r(" href: " . $a->href);
            $empHtml = scraperWiki::scrape("http://www.payscale.com" . $a->href);
            $empDom = new simple_html_dom();
            $empDom->load($empHtml);

            $record = array();

            $employerName = $empDom->find("input[name='jobtitle']");
            $record['employer_name'] = $employerName[0]->value;

            foreach ($empDom->find("tr.genderRow") as $tr) {
                $tds = $tr->find("td");

                if(sizeof($tds) >= 4) {
                    $fPayRange = $tds[1]->plaintext;
                    $token = strtok($fPayRange, "-");
                    $payArr = array();
                    $i = 0;
                    while ($token != false)
                    {
                        $payArr[$i] = $token;
                        $i = $i + 1;
                        $token = strtok(" ");
                    }
        
                    $record['female_low_range'] = rtrim((string)($payArr[0]));
                    $record['female_high_range'] = ltrim((string)($payArr[1]));

                    $mPayRange = $tds[3]->plaintext;
                    $token = strtok($mPayRange , "-");
                    $payArr = array();
                    $i = 0;
                    while ($token != false)
                    {
                        $payArr[$i] = $token;
                        $i = $i + 1;
                        $token = strtok(" ");
                    }
        
                    $record['male_low_range'] = rtrim((string)($payArr[0]));
                    $record['male_high_range'] = ltrim((string)($payArr[1]));
                }
            }

            $malePer = $empDom->find("div[id='male_percent']");
            if(sizeof($malePer) >= 1) {
                $record['male_percent'] = $malePer[0]->plaintext;
            }

            $femPer= $empDom->find("div[id='female_percent]");
            if(sizeof($femPer) >= 1) {
                $record['female_percent'] = $femPer[0]->plaintext;
            }

            $stress = $empDom->find("table[class='JobStressTable'] tbody tr td div img[class='selected']");
            if(sizeof($stress) >= 1) {
                $record['stress_level'] = $stress[0]->parent()->plaintext;
            }

            $bsDeg = $empDom->find("a[href='/research/US/Degree=Bachelor%27s_Degree']");
            if(sizeof($bsDeg) >= 1) {
                $bsPayRange = $bsDeg[0]->parent()->next_sibling()->plaintext;
                $token = strtok($bsPayRange, "-");
                $payArr = array();
                $i = 0;
                while ($token != false)
                {
                    $payArr[$i] = $token;
                    $i = $i + 1;
                    $token = strtok(" ");
                }
                $record['bachelor_degree_low_range'] = rtrim((string)($payArr[0]));
                $record['bachelor_degree_high_range'] = ltrim((string)($payArr[1]));  
            }

            $asDeg = $empDom->find("a[href='/research/US/Degree=Associate%27s_Degree']");
            if(sizeof($asDeg) >= 1) {
                $asPayRange = $asDeg[0]->parent()->next_sibling()->plaintext;
                $token = strtok($asPayRange, "-");
                $payArr = array();
                $i = 0;
                while ($token != false)
                {
                    $payArr[$i] = $token;
                    $i = $i + 1;
                    $token = strtok(" ");
                }
                $record['associate_degree_low_range'] = rtrim((string)($payArr[0]));
                $record['associate_degree_high_range'] = ltrim((string)($payArr[1])); 
            }

            #print_r(str_replace(" ", "+", $record['employer_name']));
            #$sectorHtml = scraperWiki::scrape("http://www.google.com/finance?q=" . str_replace(" ", "+", $record['employer_name']));
            #$sectorDom = new simple_html_dom();
            #$sectorDom->load($sectorHtml);

            #$sa = $sectorDom->find("a[id='sector']");
            #if (sizeof($sa) >= 1) {
            #    $record['sector'] = $sa[0]->plaintext;
            #}


            #print_r($record);
            scraperwiki::save( array( 'employer_name' ), $record );
        }
    }
?>
