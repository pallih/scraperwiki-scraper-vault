<?php
require 'scraperwiki/simple_html_dom.php';           

# Now using the schedule direct off the IGF site - ignoring codes.

print "hello - step 1\n";

require_once('scraperwiki/excel_reader2.php');           
$url = "http://www.intgovforum.org/cms/2011/Agenda/IGF6-Schedule_25_Sept.xls";
file_put_contents("/tmp/spreadsheet.xls", scraperWiki::scrape($url));
$book = new Spreadsheet_Excel_Reader("/tmp/spreadsheet.xls",false);

for($n = 1; $n < 200; $n++) {

    print "step 2 - $n\n";

    if($book->val($n, 1) == "Code" && !is_int($book->val($n+1,4))) {
        $theme = $book->val($n+1,3);
    } elseif($book->val($n,1) == "Code" && $book->val($n-1,3) == "Open Fora Hosts") {
        $theme = "Open Forum";
    }
   
    if(is_int($book->val($n,4))) {
        unset($code, $proposal,$title,$wsroom,$confroom,$day,$time,$start,$end,$organisation,$description,$link,$background_paper);
        $code = $book->val($n,1);
        $proposal = $book->val($n,2);
        $title = $book->val($n,3);
        $day = $book->val($n,4);
        $time = $book->val($n,5);
        $wsroom = $book->val($n,6);
        $organisation = $book->val($n,7);

        $time = explode("-",$time);
        $start = "2011-09-".(26 + $day) ." " . trim($time[0]);
        $end = "2011-09-".(26 + $day) ." " . trim($time[1]);

        $proposal = str_replace(array("Feeder"," ","-","Main Session"),"",$proposal);


        //We should also be able to scrape session details from the IGF site for Workshops with a proposal number:
        if($proposal) {
            $html = scraperWiki::scrape("http://www.intgovforum.org/cms/component/chronocontact/?chronoformname=Workshops2011View&wspid=".str_replace(array("Feeder"," ","-"),"",$proposal));
            $dom = new simple_html_dom();
            $dom->load($html);
            foreach($dom->find("#ChronoContact_Workshops2011View .cf_text") as $data){
                $link = "http://www.intgovforum.org/cms/component/chronocontact/?chronoformname=Workshops2011View&wspid=".str_replace(array("Feeder"," ","-"),"",$proposal);
                if(strstr($data->plaintext,"Concise Description")) {
                    $description = str_replace("<b>Concise Description:</b>","",$data->plaintext);
                    echo $description;
                }
                if(strstr($data->plaintext,"Concise Description")) {
                    $background_paper = $data->find("a",0)->href;
                }
            }
        } else {
            if($theme == "Open Forum") { $code = "OF"; }
            if($proposal == "Main Session") {
                $proposal = $code;
            } else {
                $proposal = ($code ? $code : "A") . (1 + $code_count[$code]++) ;
            }
        }

        
        $message = scraperwiki::save_sqlite(array("proposal_id"), array("code"=>$code, "theme"=>$theme,"proposal_id"=>$proposal, "title"=>$title, "start"=>$start, "end"=>$end,"wsroom"=>$wsroom,"organiser"=>$organisation, "description"=>$description,"link"=>$link,"backgroundpaper"=>$background_paper));
        print_r($message); 

    }

}

?>
