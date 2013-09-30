<?php

date_default_timezone_set('GMT');

$TodaysDateDay = "31";
$TodaysDateMonth = "10";
$TodaysDateYear = "2011";

$MonthsDateDay = date("d",strtotime("+1 month"));
$MonthsDateMonth = date("m",strtotime("+1 month"));
$MonthsDateYear = date("Y",strtotime("+1 month"));


$HTML = file_get_contents("http://www.statistics.gov.uk/hub/release-calendar/index.html?newquery=*&newoffset=10&theme=&source-agency=&uday={$MonthsDateDay}&umonth={$MonthsDateMonth}&uyear={$MonthsDateYear}&lday={$TodaysDateDay}&lmonth={$TodaysDateMonth}&lyear={$TodaysDateYear}&coverage=%22%22&designation=&geographic-breakdown=%22%22&title=%22%22&pagetype=calendar-entry");

//GET NUMBER OF ITEMS
$ResultCount = explode('<span class="count">',$HTML);
$ResultCountPos = strpos($ResultCount[1],"|")+2;
$ResultCount = substr($ResultCount[1],$ResultCountPos);
$ResultCountPos = strpos($ResultCount," result");
$ResultCount = substr($ResultCount,0,$ResultCountPos);

//WORK OUT NUMBER OF PAGES
$NumOfPages = round($ResultCount/10);

$iCalString = "";

for($ii=0;$ii<=$NumOfPages;$ii++) {
    
    $OFFSET = $ii*10;
    
    $HTML = file_get_contents("http://www.statistics.gov.uk/hub/release-calendar/index.html?newquery=*&newoffset={$OFFSET}&theme=&source-agency=&uday={$MonthsDateDay}&umonth={$MonthsDateMonth}&uyear={$MonthsDateYear}&lday={$TodaysDateDay}&lmonth={$TodaysDateMonth}&lyear={$TodaysDateYear}&coverage=%22%22&designation=&geographic-breakdown=%22%22&title=%22%22&pagetype=calendar-entry");

//GET ARTICLES
//START AT 1 AS 0 IS THE CRAP BEFORE HAND

$Articles = explode('<div class="calendar-result">',$HTML);
$count=count($Articles); 
for($i=1;$i<$count;$i++) {
    
    //LINK
    $LinkHREF = substr($Articles[$i],strpos($Articles[$i],"<a href=")+9);
    $LinkHREF = substr($LinkHREF,0,strpos($LinkHREF,'">'));

    //TITLE
    //$Title = substr($Articles[$i],strpos($Articles[$i],"<a href="),strpos($Articles[$i],"</a>")-strpos($Articles[$i],"<a href="));
    //$Title = substr($Title,strpos($Title,'">')+2);
    
    $Title = substr($Articles[$i],strpos($Articles[$i],'<h2 class="result-title">'),strpos($Articles[$i],'</h2>')-strpos($Articles[$i],'<h2 class="result-title">'));
    $Title = strip_tags($Title);
    $Title = trim($Title);
    $Title = substr($Title,6);
    $Title = trim($Title);
    
    //DATE
    $Date = substr($Articles[$i],strpos($Articles[$i],'elease date: ')+13);
    $Date = substr($Date,0,strpos($Date,'<'));
    
    //CHECK IF THERES TIME
    if(strpos($Date," at")===false) {
        //NO TIME
        //IF WHOLE MONTH
        if(strpos($Date,"-")===false) {
            $CustomDATE = ";VALUE=DATE:".date('Ymd',strtotime($Date))."\nDTEND;VALUE=DATE:".date('Ymd',strtotime("+1 day",strtotime($Date)));
        } else {
            $tmpSplit = explode("-",$Date);
            $CustomDATE = ";VALUE=DATE:".date('Ymd',strtotime("1 ".$tmpSplit[0]))."\nDTEND;VALUE=DATE:".date('Ymd',strtotime($tmpSplit[1]));
        }
        $CustomDATETIMESTAMP = ":".date("Ymd")."T".date("His")."Z";
        //DTSTART;VALUE=DATE:20111101
    } else {
        $Date = str_replace(" at","",$Date);
        $CustomDATE = ":".date("Ymd",strtotime($Date))."T".date("His",strtotime($Date))."Z";
        $CustomDATETIMESTAMP = ":".date("Ymd")."T".date("His")."Z";
    }

    //THEME
    $Theme = substr($Articles[$i],strpos($Articles[$i],'<span class="result-info-label">Theme: </span>')+46);
    $Theme = substr($Theme,0,strpos($Theme," |"));
    
    //SUMMARY
    $Summary = substr($Articles[$i],strpos($Articles[$i],'<div class="summary">')+24);
    $Summary = trim(substr($Summary,0,strpos($Summary,"</div>")));
    
    $Summary = str_replace("\n","\\n",$Summary);
    $Title = str_replace("\n","\\n",$Title);
    $Theme = str_replace("\n","\\n",$Theme);
    
    scraperwiki::save_sqlite(array("title"), array("Title"=>$Title, "DTSTAMP"=>$CustomDATETIMESTAMP, "DTSTART"=>$CustomDATE, "Theme"=>$Theme, "Summary"=>$Summary), "vevents");
}

}


?>
<?php

date_default_timezone_set('GMT');

$TodaysDateDay = "31";
$TodaysDateMonth = "10";
$TodaysDateYear = "2011";

$MonthsDateDay = date("d",strtotime("+1 month"));
$MonthsDateMonth = date("m",strtotime("+1 month"));
$MonthsDateYear = date("Y",strtotime("+1 month"));


$HTML = file_get_contents("http://www.statistics.gov.uk/hub/release-calendar/index.html?newquery=*&newoffset=10&theme=&source-agency=&uday={$MonthsDateDay}&umonth={$MonthsDateMonth}&uyear={$MonthsDateYear}&lday={$TodaysDateDay}&lmonth={$TodaysDateMonth}&lyear={$TodaysDateYear}&coverage=%22%22&designation=&geographic-breakdown=%22%22&title=%22%22&pagetype=calendar-entry");

//GET NUMBER OF ITEMS
$ResultCount = explode('<span class="count">',$HTML);
$ResultCountPos = strpos($ResultCount[1],"|")+2;
$ResultCount = substr($ResultCount[1],$ResultCountPos);
$ResultCountPos = strpos($ResultCount," result");
$ResultCount = substr($ResultCount,0,$ResultCountPos);

//WORK OUT NUMBER OF PAGES
$NumOfPages = round($ResultCount/10);

$iCalString = "";

for($ii=0;$ii<=$NumOfPages;$ii++) {
    
    $OFFSET = $ii*10;
    
    $HTML = file_get_contents("http://www.statistics.gov.uk/hub/release-calendar/index.html?newquery=*&newoffset={$OFFSET}&theme=&source-agency=&uday={$MonthsDateDay}&umonth={$MonthsDateMonth}&uyear={$MonthsDateYear}&lday={$TodaysDateDay}&lmonth={$TodaysDateMonth}&lyear={$TodaysDateYear}&coverage=%22%22&designation=&geographic-breakdown=%22%22&title=%22%22&pagetype=calendar-entry");

//GET ARTICLES
//START AT 1 AS 0 IS THE CRAP BEFORE HAND

$Articles = explode('<div class="calendar-result">',$HTML);
$count=count($Articles); 
for($i=1;$i<$count;$i++) {
    
    //LINK
    $LinkHREF = substr($Articles[$i],strpos($Articles[$i],"<a href=")+9);
    $LinkHREF = substr($LinkHREF,0,strpos($LinkHREF,'">'));

    //TITLE
    //$Title = substr($Articles[$i],strpos($Articles[$i],"<a href="),strpos($Articles[$i],"</a>")-strpos($Articles[$i],"<a href="));
    //$Title = substr($Title,strpos($Title,'">')+2);
    
    $Title = substr($Articles[$i],strpos($Articles[$i],'<h2 class="result-title">'),strpos($Articles[$i],'</h2>')-strpos($Articles[$i],'<h2 class="result-title">'));
    $Title = strip_tags($Title);
    $Title = trim($Title);
    $Title = substr($Title,6);
    $Title = trim($Title);
    
    //DATE
    $Date = substr($Articles[$i],strpos($Articles[$i],'elease date: ')+13);
    $Date = substr($Date,0,strpos($Date,'<'));
    
    //CHECK IF THERES TIME
    if(strpos($Date," at")===false) {
        //NO TIME
        //IF WHOLE MONTH
        if(strpos($Date,"-")===false) {
            $CustomDATE = ";VALUE=DATE:".date('Ymd',strtotime($Date))."\nDTEND;VALUE=DATE:".date('Ymd',strtotime("+1 day",strtotime($Date)));
        } else {
            $tmpSplit = explode("-",$Date);
            $CustomDATE = ";VALUE=DATE:".date('Ymd',strtotime("1 ".$tmpSplit[0]))."\nDTEND;VALUE=DATE:".date('Ymd',strtotime($tmpSplit[1]));
        }
        $CustomDATETIMESTAMP = ":".date("Ymd")."T".date("His")."Z";
        //DTSTART;VALUE=DATE:20111101
    } else {
        $Date = str_replace(" at","",$Date);
        $CustomDATE = ":".date("Ymd",strtotime($Date))."T".date("His",strtotime($Date))."Z";
        $CustomDATETIMESTAMP = ":".date("Ymd")."T".date("His")."Z";
    }

    //THEME
    $Theme = substr($Articles[$i],strpos($Articles[$i],'<span class="result-info-label">Theme: </span>')+46);
    $Theme = substr($Theme,0,strpos($Theme," |"));
    
    //SUMMARY
    $Summary = substr($Articles[$i],strpos($Articles[$i],'<div class="summary">')+24);
    $Summary = trim(substr($Summary,0,strpos($Summary,"</div>")));
    
    $Summary = str_replace("\n","\\n",$Summary);
    $Title = str_replace("\n","\\n",$Title);
    $Theme = str_replace("\n","\\n",$Theme);
    
    scraperwiki::save_sqlite(array("title"), array("Title"=>$Title, "DTSTAMP"=>$CustomDATETIMESTAMP, "DTSTART"=>$CustomDATE, "Theme"=>$Theme, "Summary"=>$Summary), "vevents");
}

}


?>
