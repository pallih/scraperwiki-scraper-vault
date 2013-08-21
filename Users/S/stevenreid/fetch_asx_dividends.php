<?php
######################################
# ASX Dividends downloads
# Written by: S3than
# Obtains ASX Dividends from the ASX website for all companies that have issued dividends
######################################

require  'scraperwiki/simple_html_dom.php';
date_default_timezone_set('Australia/Sydney'); 



/*
Data base creation queries

scraperwiki::sqliteexecute('DROP TABLE divdata'); 

scraperwiki::sqliteexecute('CREATE TABLE divdata (date_scraped CHAR(10), ASX_Code CHAR(6), Company_Name VARCHAR(150), Div_Amount_in_cents CHAR(15), Ex_Div_Date CHAR(10), Record_Date CHAR(10), Date_Payable CHAR(10), PERC_Franked CHAR(15), Type CHAR(15), Further_Information VARCHAR(250), UNIQUE(ASX_Code, Ex_Div_Date) ON CONFLICT REPLACE)'); 
*/


$v = 0;
$row = 1;

#The ASX lets you run up to 10 codes at a time this just adds the required breaks in the link in the correct format
function filepr($file) {
    if ($file != null) {
        $file = '+' . $file;
    }
    return $file;
}

# get ASX company list from CSV to an array also adds a counter to the row variable to setup the number of loops for the asx scraper
$handle = fopen("http://www.asx.com.au/asx/research/ASXListedCompanies.csv", 'r');
$file= array();
while(($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
    
    $row++;
    if (isset($data[1])) {
        array_push($file, $data[1]);
    }
}
fclose($handle);
$file = array_slice($file, 3);

sort($file);

#Link details
$partial = 'http://www.asx.com.au/asx/markets/dividends.do?by=asxCodes&asxCodes=';
$end = '&view=all';

#Pass the row variable through to the function to limit the number of iterations
#The ASX lets you run up to 10 codes at a time the intial row variable is the number of codes return the number of rows / 10 to limit the number of iterations 
$row = ($row / 10);
$row++;
$row = round(($row) + 0.5);

for ($j = 0; $j < $row; $j++) {
    # Create the link
    $link = $partial . $file[$v] . filepr($file[$v + 1]) . filepr($file[$v + 2])
            . filepr($file[$v + 3]) . filepr($file[$v + 4]) . filepr($file[$v + 5])
            . filepr($file[$v + 6]) . filepr($file[$v + 7]) . filepr($file[$v + 8])
            . filepr($file[$v + 9]) . $end;

    #add 10 to v so that the next group of 10 codes is used for the next link request
    $v = $v + 10;
    
    $html = scraperwiki::scrape($link);

    # Use the PHP Simple HTML DOM Parser to extract <tr> tags
    $dom = new simple_html_dom();
    $dom->load($html);

    #Output each row for the different companies
    foreach($dom->find('tr') as $data){
        #ensure the right section of the ASX web page is used, if no results are returned from the ASX website this will skip that section
        if(count($data->children)== 9)
        {
            # Removes the headings from each page as the headings are set below 
            if (($data->children[0]->plaintext) != 'Code'){
                # ASX adds * to codes that have announcements listed from today date, this removes as not needed at this time
                $str = $data->children[0]->plaintext;
                $tidyAsxcode = str_split($str, 4);

                $ex_div_date = explode('/',$data->children[3]->plaintext);
                $ex_div_date = $ex_div_date[2] . '-' . $ex_div_date[1] . '-' . $ex_div_date[0];

                $record_date = explode('/',$data->children[4]->plaintext);
                $record_date = $record_date[2] . '-' . $record_date[1] . '-' . $record_date[0];
                
                $date_payable = explode('/',$data->children[5]->plaintext);
                $date_payable = $date_payable[2] . '-' . $date_payable[1] . '-' . $date_payable[0];

                scraperwiki::save_sqlite(
                                array('ASX_Code','Ex_Div_Date'), 
                                array(
                                        'date_scraped'        => date('Y-m-d'),
                                        'ASX_Code'            => trim($tidyAsxcode[5]),
                                        'Company_Name'        => trim($data->children[1]->plaintext),
                                        'Div_Amount_in_cents' => trim($data->children[2]->plaintext),
                                        'Ex_Div_Date'         => trim($ex_div_date),
                                        'Record_Date'         => trim($record_date),
                                        'Date_Payable'        => trim($date_payable),
                                        'PERC_Franked'        => trim($data->children[6]->plaintext),
                                        'Type'                => trim($data->children[7]->plaintext),
                                        'Further_Information' => trim($data->children[8]->plaintext)
                                ),
                                'divdata'
                            );
            }
        }    
    }
}