<?php
require  'scraperwiki/simple_html_dom.php';


###### Find out how many pages of coucillors there are, hardcoded for now but could parse one of these URLs for pages
$pages = array('http://www.edinburgh.gov.uk/directory/22/councillors_register_of_interests_and_expenses?page=1',
    'http://www.edinburgh.gov.uk/directory/22/councillors_register_of_interests_and_expenses?page=2');

/*
def pdftoxml(pdfdata):
    """converts pdf file to xml file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmpxml = xmlin.name # "temph.xml"
    cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    #xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata

*/

###### On each page, get a list of councillors
$CouncillorsURLs = array();
foreach ($pages as $page) {
    $html = scraperwiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('ul') as $data) {
        if (in_array(substr($data->class,0,9),array('info_left','info_righ'))) {
            foreach($data->find('a') as $data2) {
                 $CouncillorsURLs[] = $data2->href;
            }
        }
    }
}

###### Now get counciller pages


$councillorExpenses = array(
        'Expense claims 2009/10'=>array(),
        'Expense Claims 2010/11 Quarters 1-3'=>array()
    );


##foreach(array($CouncillorsURLs[0]) as $url) {   ### temp only load 1 for now!
foreach($CouncillorsURLs as $url) { 
    sleep(5);
    $html = scraperwiki::scrape('http://www.edinburgh.gov.uk'.$url);
    $dom = new simple_html_dom();
    $dom->load($html);
    $foundData = array();
    foreach($dom->find('table') as $data) {
        if ($data->class == 'directoryRecord') {
            foreach($data->find('tr') as $dataRow) {                
                $headerText = array_shift($dataRow->find('th'))->plaintext;
                $dataCell = array_shift($dataRow->find('td'));
                if (in_array($headerText,array_keys($councillorExpenses))) {
                    $aLink = array_shift($dataCell->find('a'));
                    $councillorExpenses[$headerText][$foundData['Name']] = $aLink->href;
                } else {
                    $foundData[$headerText] = $dataCell->innertext;
                }                
            }
        }
    }
    $mainData = array(
            'Name'=>$foundData['Name'],
            'Party'=>$foundData['Political group'],
            'RelatedUndertakings'=>$foundData['Related undertakings'],
            'Remuneration'=>$foundData['Remuneration'],
            'ElectionExpenses'=>$foundData['Election expenses'],
        );
    scraperwiki::save_sqlite(array('Name'),$mainData,'councillors');

    if (isset($foundData['Shares and securities'])) {
        $d = explode("<br />",$foundData['Shares and securities']);
        foreach($d as $v) {
            if (trim($v)) {
                scraperwiki::save_sqlite(array('Name','In'), 
                    array('Name'=>$foundData['Name'],'In'=>trim($v)),
                    'councillorsSharesAndSecurities');
            }
        }
    }

    if (isset($foundData['Non-financial interests'])) {
        $d = explode("<br />",$foundData['Non-financial interests']);
        foreach($d as $v) {
            if (trim($v)) {
                scraperwiki::save_sqlite(array('Name','Interest'),
                    array('Name'=>$foundData['Name'],'Interest'=>trim($v)),
                    'councillorsNonFinancialInterests');
            }
        }
    }


    if (isset($foundData['Houses, land and buildings'])) {
        $d = explode("<br />",$foundData['Houses, land and buildings']);
        foreach($d as $v) {
            if (trim($v)) {
                scraperwiki::save_sqlite(array('Name','Where'),
                    array('Name'=>$foundData['Name'],'Where'=>trim($v)),
                    'councillorsHousesLandBuildings');
            }
        }
    }

     if (isset($foundData['Gifts and hospitality'])) {
         $d = explode("<br />",$foundData['Gifts and hospitality']);
         foreach($d as $v) {
             if (trim($v)) {
                $bitsOfLine = explode(" ",trim($v),2);
                $giftsDataToSave = array('Name'=>$foundData['Name'],'Date'=>$bitsOfLine[0],'What'=>'','Amount'=>'','Who'=>'','RawString'=>'');
                $bits = explode(",",$bitsOfLine[1],3);
                if (count($bits) == 3 && is_numeric(trim(substr($bits[1],8)))) {
                    $giftsDataToSave['What'] = trim($bits[0]);
                    $giftsDataToSave['Amount'] = floatVal(substr($bits[1],8));
                    $giftsDataToSave['Who'] = trim($bits[2]);
                    scraperwiki::save_sqlite(array_keys($giftsDataToSave),$giftsDataToSave,'councillorsGiftsHospitality');
                } else {
                    $matches = array();
                    preg_match_all('/\&pound\;(\d+)/', $bitsOfLine[1], $matches);
                    if (count($matches) > 0 && count($matches[1]) > 0) {
                        $giftsDataToSave['RawString'] = trim($v);
                        $allAmounts = array();
                        foreach($matches[1] as $match) {
                            $allAmounts[] = floatval($match);
                        }
                        $giftsDataToSave['Amount'] = max($allAmounts);
                        scraperwiki::save_sqlite(array_keys($giftsDataToSave),$giftsDataToSave,'councillorsGiftsHospitality');
                    } else {
                        scraperwiki::save_sqlite(array('Name','CantParse'),
                             array('Name'=>$foundData['Name'],'CantParse'=>trim($v)),
                             'councillorsGiftsHospitalityCantParse');
                    }
                }                
             }
         }
     }

}


###### Now get councillor expenses

function getAmountFromLine($line) {
    $matches = array();
    preg_match('/\£(\d+\.+\d+)/', $line, $matches);
    return $matches[1];
}

function getAmountFromBoldLine($line) {
    $matches = array();
    preg_match('/\<b\>(\d+\.+\d+)/', $line, $matches);
    return $matches[1];
}

foreach($councillorExpenses as $councillorExpenseKey=>$councillorExpensesURLs) {
    foreach($councillorExpensesURLs as $councillorName=>$url) {
        sleep(2);
        ###print " Key $councillorExpenseKey  Coun $councillorName  $url \n";

        $dataToSave = array('Name'=>$councillorName,"Expenses"=>$councillorExpenseKey);

        $html = scraperwiki::scrape($url);
        $dom = new simple_html_dom();
        $dom->load($html);

        foreach($dom->find('h2') as $data) {
             if ($data->class == 'downloadNow') {
                $pdfLink = array_shift($data->find('a'))->href;
                $pdfData = scraperwiki::scrape($pdfLink);
                $tmpfname = tempnam("/tmp", "FOO");                
                $handle = fopen($tmpfname, "wb");
                fwrite($handle, $pdfData);
                fclose($handle);

                $tmphtmlfname = tempnam("/tmp", "FOO"); 
                $execOutput = array();
                exec('/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "'.$tmpfname.'" "'.$tmphtmlfname.'"', $execOutput);
                $pdfDataAshtml = file_get_contents($tmphtmlfname.".xml");

                $pdfDataAshtmlLines = explode("\n",$pdfDataAshtml);
                for ($i = 1; $i <= count($pdfDataAshtmlLines); $i++) {
                    if ($pdfDataAshtmlLines[$i] && strpos($pdfDataAshtmlLines[$i],'Sub Total</text>') > 1) {
                        $dataToSave['Subsistence'] = getAmountFromLine($pdfDataAshtmlLines[$i+5]);
                        $dataToSave['OtherTravel'] = getAmountFromLine($pdfDataAshtmlLines[$i+6]);
                        $dataToSave['OtherExpenses'] = getAmountFromLine($pdfDataAshtmlLines[$i+7]);                        
                    } 
                    if ($pdfDataAshtmlLines[$i] && strpos($pdfDataAshtmlLines[$i],'Cash Value of Mileage Claim</text>') > 1) {
                        $dataToSave['MileageClaims'] = getAmountFromLine($pdfDataAshtmlLines[$i+1]);
                    } 
                    if ($pdfDataAshtmlLines[$i] && strpos($pdfDataAshtmlLines[$i],'Total Claimed</b></text>') > 1) {
                         $dataToSave['PhoneComputer'] = getAmountFromBoldLine($pdfDataAshtmlLines[$i+2]);
                    } 
                }
            }
        }
        scraperwiki::save_sqlite(array('Name','Expenses'),$dataToSave,'councillorsExpenses');

    }
}
?>
<?php
require  'scraperwiki/simple_html_dom.php';


###### Find out how many pages of coucillors there are, hardcoded for now but could parse one of these URLs for pages
$pages = array('http://www.edinburgh.gov.uk/directory/22/councillors_register_of_interests_and_expenses?page=1',
    'http://www.edinburgh.gov.uk/directory/22/councillors_register_of_interests_and_expenses?page=2');

/*
def pdftoxml(pdfdata):
    """converts pdf file to xml file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmpxml = xmlin.name # "temph.xml"
    cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    #xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata

*/

###### On each page, get a list of councillors
$CouncillorsURLs = array();
foreach ($pages as $page) {
    $html = scraperwiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('ul') as $data) {
        if (in_array(substr($data->class,0,9),array('info_left','info_righ'))) {
            foreach($data->find('a') as $data2) {
                 $CouncillorsURLs[] = $data2->href;
            }
        }
    }
}

###### Now get counciller pages


$councillorExpenses = array(
        'Expense claims 2009/10'=>array(),
        'Expense Claims 2010/11 Quarters 1-3'=>array()
    );


##foreach(array($CouncillorsURLs[0]) as $url) {   ### temp only load 1 for now!
foreach($CouncillorsURLs as $url) { 
    sleep(5);
    $html = scraperwiki::scrape('http://www.edinburgh.gov.uk'.$url);
    $dom = new simple_html_dom();
    $dom->load($html);
    $foundData = array();
    foreach($dom->find('table') as $data) {
        if ($data->class == 'directoryRecord') {
            foreach($data->find('tr') as $dataRow) {                
                $headerText = array_shift($dataRow->find('th'))->plaintext;
                $dataCell = array_shift($dataRow->find('td'));
                if (in_array($headerText,array_keys($councillorExpenses))) {
                    $aLink = array_shift($dataCell->find('a'));
                    $councillorExpenses[$headerText][$foundData['Name']] = $aLink->href;
                } else {
                    $foundData[$headerText] = $dataCell->innertext;
                }                
            }
        }
    }
    $mainData = array(
            'Name'=>$foundData['Name'],
            'Party'=>$foundData['Political group'],
            'RelatedUndertakings'=>$foundData['Related undertakings'],
            'Remuneration'=>$foundData['Remuneration'],
            'ElectionExpenses'=>$foundData['Election expenses'],
        );
    scraperwiki::save_sqlite(array('Name'),$mainData,'councillors');

    if (isset($foundData['Shares and securities'])) {
        $d = explode("<br />",$foundData['Shares and securities']);
        foreach($d as $v) {
            if (trim($v)) {
                scraperwiki::save_sqlite(array('Name','In'), 
                    array('Name'=>$foundData['Name'],'In'=>trim($v)),
                    'councillorsSharesAndSecurities');
            }
        }
    }

    if (isset($foundData['Non-financial interests'])) {
        $d = explode("<br />",$foundData['Non-financial interests']);
        foreach($d as $v) {
            if (trim($v)) {
                scraperwiki::save_sqlite(array('Name','Interest'),
                    array('Name'=>$foundData['Name'],'Interest'=>trim($v)),
                    'councillorsNonFinancialInterests');
            }
        }
    }


    if (isset($foundData['Houses, land and buildings'])) {
        $d = explode("<br />",$foundData['Houses, land and buildings']);
        foreach($d as $v) {
            if (trim($v)) {
                scraperwiki::save_sqlite(array('Name','Where'),
                    array('Name'=>$foundData['Name'],'Where'=>trim($v)),
                    'councillorsHousesLandBuildings');
            }
        }
    }

     if (isset($foundData['Gifts and hospitality'])) {
         $d = explode("<br />",$foundData['Gifts and hospitality']);
         foreach($d as $v) {
             if (trim($v)) {
                $bitsOfLine = explode(" ",trim($v),2);
                $giftsDataToSave = array('Name'=>$foundData['Name'],'Date'=>$bitsOfLine[0],'What'=>'','Amount'=>'','Who'=>'','RawString'=>'');
                $bits = explode(",",$bitsOfLine[1],3);
                if (count($bits) == 3 && is_numeric(trim(substr($bits[1],8)))) {
                    $giftsDataToSave['What'] = trim($bits[0]);
                    $giftsDataToSave['Amount'] = floatVal(substr($bits[1],8));
                    $giftsDataToSave['Who'] = trim($bits[2]);
                    scraperwiki::save_sqlite(array_keys($giftsDataToSave),$giftsDataToSave,'councillorsGiftsHospitality');
                } else {
                    $matches = array();
                    preg_match_all('/\&pound\;(\d+)/', $bitsOfLine[1], $matches);
                    if (count($matches) > 0 && count($matches[1]) > 0) {
                        $giftsDataToSave['RawString'] = trim($v);
                        $allAmounts = array();
                        foreach($matches[1] as $match) {
                            $allAmounts[] = floatval($match);
                        }
                        $giftsDataToSave['Amount'] = max($allAmounts);
                        scraperwiki::save_sqlite(array_keys($giftsDataToSave),$giftsDataToSave,'councillorsGiftsHospitality');
                    } else {
                        scraperwiki::save_sqlite(array('Name','CantParse'),
                             array('Name'=>$foundData['Name'],'CantParse'=>trim($v)),
                             'councillorsGiftsHospitalityCantParse');
                    }
                }                
             }
         }
     }

}


###### Now get councillor expenses

function getAmountFromLine($line) {
    $matches = array();
    preg_match('/\£(\d+\.+\d+)/', $line, $matches);
    return $matches[1];
}

function getAmountFromBoldLine($line) {
    $matches = array();
    preg_match('/\<b\>(\d+\.+\d+)/', $line, $matches);
    return $matches[1];
}

foreach($councillorExpenses as $councillorExpenseKey=>$councillorExpensesURLs) {
    foreach($councillorExpensesURLs as $councillorName=>$url) {
        sleep(2);
        ###print " Key $councillorExpenseKey  Coun $councillorName  $url \n";

        $dataToSave = array('Name'=>$councillorName,"Expenses"=>$councillorExpenseKey);

        $html = scraperwiki::scrape($url);
        $dom = new simple_html_dom();
        $dom->load($html);

        foreach($dom->find('h2') as $data) {
             if ($data->class == 'downloadNow') {
                $pdfLink = array_shift($data->find('a'))->href;
                $pdfData = scraperwiki::scrape($pdfLink);
                $tmpfname = tempnam("/tmp", "FOO");                
                $handle = fopen($tmpfname, "wb");
                fwrite($handle, $pdfData);
                fclose($handle);

                $tmphtmlfname = tempnam("/tmp", "FOO"); 
                $execOutput = array();
                exec('/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "'.$tmpfname.'" "'.$tmphtmlfname.'"', $execOutput);
                $pdfDataAshtml = file_get_contents($tmphtmlfname.".xml");

                $pdfDataAshtmlLines = explode("\n",$pdfDataAshtml);
                for ($i = 1; $i <= count($pdfDataAshtmlLines); $i++) {
                    if ($pdfDataAshtmlLines[$i] && strpos($pdfDataAshtmlLines[$i],'Sub Total</text>') > 1) {
                        $dataToSave['Subsistence'] = getAmountFromLine($pdfDataAshtmlLines[$i+5]);
                        $dataToSave['OtherTravel'] = getAmountFromLine($pdfDataAshtmlLines[$i+6]);
                        $dataToSave['OtherExpenses'] = getAmountFromLine($pdfDataAshtmlLines[$i+7]);                        
                    } 
                    if ($pdfDataAshtmlLines[$i] && strpos($pdfDataAshtmlLines[$i],'Cash Value of Mileage Claim</text>') > 1) {
                        $dataToSave['MileageClaims'] = getAmountFromLine($pdfDataAshtmlLines[$i+1]);
                    } 
                    if ($pdfDataAshtmlLines[$i] && strpos($pdfDataAshtmlLines[$i],'Total Claimed</b></text>') > 1) {
                         $dataToSave['PhoneComputer'] = getAmountFromBoldLine($pdfDataAshtmlLines[$i+2]);
                    } 
                }
            }
        }
        scraperwiki::save_sqlite(array('Name','Expenses'),$dataToSave,'councillorsExpenses');

    }
}
?>
