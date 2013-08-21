<?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


/// -------------------------------- First download the file --------------------------------

$url  = 'http://www.usa.gov/About/developer_resources/allfaqs.xml';
$xml_file_path = '/tmp/allfaqs.xml';
//$xml_file_path = '/Users/philipashlock/Sites/test.dev/scraper/faq-data/allfaqs.xml';


$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$data = curl_exec($ch);

curl_close($ch);

file_put_contents($xml_file_path, $data);
                                          
/// ------------------------------------------------------------------------------------------




$records = get_sources($xml_file_path);


function get_sources($xml_file_path) {
    
    // Specify configuration
    $config = array(
               'indent'         => true,
               'output-xhtml'   => false,
               'output-html'   => true,    
               'show-warnings'    => false,
               'show-body-only' => true,
               'wrap'           => 200);


    $count = 1;




    $XMLReader = new XMLReader;    
    $XMLReader->open($xml_file_path);

    // Move to the first "[item name]" node in the file.
    while ($XMLReader->read() && $XMLReader->name !== "Row");


    // Now that we're at the right depth, hop to the next "[item name]" until the end of tree/file.
    while ($XMLReader->name === "Row") {
    
        if ($count > 1) {
        
            $dom = new simple_html_dom();
            $dom->load($XMLReader->readOuterXML());


            $record = null;

            $record['url']             = $dom->find("Item", 0)->plaintext;
            
            
            $record['faq_id']            = substr($record['url'], strpos($record['url'], '?p_faq_id=') + 10);
            
            $record['question']     = $dom->find("Item", 1)->plaintext;
            $search = array('<BR>', '</LI>', '</P>', '</UL>', '&nbsp;');
            $replace = array(" \n", "</LI> \n", "</P> \n\n", "</UL> \n\n", ' ');
            $record['answer_text']         = strip_tags(str_replace($search, $replace, html_entity_decode($dom->find("Item", 2)->innertext)));                
            $record['answer_html']         = html_entity_decode($dom->find("Item", 2)->innertext);                

            $tidy = new tidy;
            $tidy->parseString($record['answer_html'], $config, 'utf8');
            $tidy->cleanRepair();
            
            $record['answer_html'] = $tidy->value;

            $record['ranking']         = $dom->find("Item", 3)->plaintext;                        
            $record['last_updated'] = $dom->find("Item", 4)->plaintext;                        
            $record['last_updated'] = ($record['last_updated']) ? date(DATE_ATOM, strtotime($record['last_updated'])) : null;

            $record['topic']         = $dom->find("Item", 5)->plaintext;                        
            $record['subtopic']     = $dom->find("Item", 6)->plaintext;
            
            // Set empty strings as null
            array_walk($record, 'check_null');

            scraperwiki::save(array('url'), $record);
            //$records[] = $record;

        }

        // Skip to the next node of interest.
        $XMLReader->next("Row");
        $count++;
    }

     //return $records;
 
}


function check_null(&$value) {
    $value = (empty($value)) ? null : $value;
}





?><?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


/// -------------------------------- First download the file --------------------------------

$url  = 'http://www.usa.gov/About/developer_resources/allfaqs.xml';
$xml_file_path = '/tmp/allfaqs.xml';
//$xml_file_path = '/Users/philipashlock/Sites/test.dev/scraper/faq-data/allfaqs.xml';


$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$data = curl_exec($ch);

curl_close($ch);

file_put_contents($xml_file_path, $data);
                                          
/// ------------------------------------------------------------------------------------------




$records = get_sources($xml_file_path);


function get_sources($xml_file_path) {
    
    // Specify configuration
    $config = array(
               'indent'         => true,
               'output-xhtml'   => false,
               'output-html'   => true,    
               'show-warnings'    => false,
               'show-body-only' => true,
               'wrap'           => 200);


    $count = 1;




    $XMLReader = new XMLReader;    
    $XMLReader->open($xml_file_path);

    // Move to the first "[item name]" node in the file.
    while ($XMLReader->read() && $XMLReader->name !== "Row");


    // Now that we're at the right depth, hop to the next "[item name]" until the end of tree/file.
    while ($XMLReader->name === "Row") {
    
        if ($count > 1) {
        
            $dom = new simple_html_dom();
            $dom->load($XMLReader->readOuterXML());


            $record = null;

            $record['url']             = $dom->find("Item", 0)->plaintext;
            
            
            $record['faq_id']            = substr($record['url'], strpos($record['url'], '?p_faq_id=') + 10);
            
            $record['question']     = $dom->find("Item", 1)->plaintext;
            $search = array('<BR>', '</LI>', '</P>', '</UL>', '&nbsp;');
            $replace = array(" \n", "</LI> \n", "</P> \n\n", "</UL> \n\n", ' ');
            $record['answer_text']         = strip_tags(str_replace($search, $replace, html_entity_decode($dom->find("Item", 2)->innertext)));                
            $record['answer_html']         = html_entity_decode($dom->find("Item", 2)->innertext);                

            $tidy = new tidy;
            $tidy->parseString($record['answer_html'], $config, 'utf8');
            $tidy->cleanRepair();
            
            $record['answer_html'] = $tidy->value;

            $record['ranking']         = $dom->find("Item", 3)->plaintext;                        
            $record['last_updated'] = $dom->find("Item", 4)->plaintext;                        
            $record['last_updated'] = ($record['last_updated']) ? date(DATE_ATOM, strtotime($record['last_updated'])) : null;

            $record['topic']         = $dom->find("Item", 5)->plaintext;                        
            $record['subtopic']     = $dom->find("Item", 6)->plaintext;
            
            // Set empty strings as null
            array_walk($record, 'check_null');

            scraperwiki::save(array('url'), $record);
            //$records[] = $record;

        }

        // Skip to the next node of interest.
        $XMLReader->next("Row");
        $count++;
    }

     //return $records;
 
}


function check_null(&$value) {
    $value = (empty($value)) ? null : $value;
}





?>