<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php'; 

#$nextPageLink = "http://dl.acm.org/results.cfm?CFID=192482131&CFTOKEN=17329111&adv=1&COLL=DL&DL=ACM&termzone=all&allofem=%22serious+games%22&anyofem=&noneofem=&peoplezone=Name&people=&peoplehow=and&keyword=&keywordhow=AND&affil=&affilhow=AND&pubin=&pubinhow=and&pubby=&pubbyhow=OR&since_year=2004&before_year=&pubashow=OR&sponsor=&sponsorhow=AND&confdate=&confdatehow=OR&confloc=&conflochow=OR&isbnhow=OR&isbn=&doi=&ccs=&subj=&Go.x=26&Go.y=12";

#$nextPageLink = "http://dl.acm.org/results.cfm?CFID=196152628&CFTOKEN=70127669&adv=1&COLL=DL&DL=ACM&Go.x=29&Go.y=6&termzone=Abstract&allofem=evaluation&anyofem=web2+wiki+blog+podcast+vodcast&noneofem=&peoplezone=Name&people=&peoplehow=and&keyword=&keywordhow=AND&affil=&affilhow=AND&pubin=&pubinhow=and&pubby=&pubbyhow=OR&since_year=2000&before_year=&pubashow=OR&sponsor=&sponsorhow=AND&confdate=&confdatehow=OR&confloc=&conflochow=OR&isbnhow=OR&isbn=&doi=&ccs=&subj=";

$nextPageLink = "http://dl.acm.org/results.cfm?CFID=196152628&CFTOKEN=70127669&adv=1&COLL=DL&DL=ACM&termzone=Abstract&allofem=evaluation&anyofem=%22e-portfolio%22&noneofem=&peoplezone=Name&people=&peoplehow=and&keyword=&keywordhow=AND&affil=&affilhow=AND&pubin=&pubinhow=and&pubby=&pubbyhow=OR&since_year=2000&before_year=&pubashow=OR&sponsor=&sponsorhow=AND&confdate=&confdatehow=OR&confloc=&conflochow=OR&isbnhow=OR&isbn=&doi=&ccs=&subj=&Go.x=30&Go.y=8";

#$html_content = scraperWiki::scrape($nextPageLink); 
#$html1 = str_get_html($html_content);
#$nextLink = $html1->find("td[@colspan='2']", 0);
#$nextPageLink = getNextLink($nextLink);
#parsePage($html1);

#print "Next page link: " . $nextPageLink . "\n";
print "title, author, year, addinfo, publisher, abstract" . "\n";

#scraperwiki::sqliteexecute("create table acmdata1 (a int, `title` string, 'author' string, 'year' string, 'addinfo' string, 'publisher' string, 'abstract' string)"); 

$maxPages = 0;
$numrecords = 1;
while (strlen($nextPageLink) > 0 and $maxPages < 6)
    {
        $maxPages++;        

#print "Moving on to next page" . "\n";

        $html_content = scraperWiki::scrape($nextPageLink);
        $html1 = str_get_html($html_content);

#print $html1 . "\n";

        $nextLink = $html1->find("td[@colspan='2']", 0);
# print "Next link: " . $nextLink->innertext . "\n";
        $nextPageLink = getNextLink($nextLink);

        $numrecords = parsePage($html1, $maxPages);
        sleep(120);
    }

print "No further pages" . "\n";        
$data = scraperwiki::select("* from acmdata1");

print "<html><table>";
print "<tr><th>Title</th><th>Author</th><th>Year</th><th>AddInfo</th><th>Publisher</th><th>Abstract</th>";
foreach($data as $d)
{
print "<tr>"; 
    print "<td>" . "ACM" . "</td>"; 
    print "<td>" . $d["title"] . "</td>"; 
    print "<td>" . $d["author"] . "</td>"; 
    print "<td>" . $d["year"] . "</td>"; 
    print "<td>" . $d["addinfo"] . "</td>"; 
    print "<td>" . $d["publisher"] . "</td>"; 
    print "<td>" . $d["abstract"] . "</td>"; 
print "</tr>";
}
print "</table></html>";
flush();

function parsePage($html1, $pageNo)
{
    $numrecords = 1 + 20*$pageNo;
    foreach ($html1->find("table[@style='padding: 5px; 5px; 5px; 5px;']") as $row) 
        {
        $tr1 = $row->find("tr", 0);
        # print $tr1 . "\n"; 
        $title = $tr1->find("a[@target='_self']", 0);
        $papertitle = "http://dl.acm.org/" . $title->href."&preflayout=flat";

        foreach ($tr1->find("div.authors") as $author) 
            { 
                $tr2 = $row->find("tr", 1);
                $year = $tr2->find("td", 0);
                $addinfo = $tr2->find("td", 2);
                $tr3 = $row->find("tr", 2);
                $publisher = $tr3->find("td", 0);
                $abstract = getAbstract($papertitle);
print "abstract " . $abstract . "\n";

                sleep(30);

print $title->innertext . ", "; 
print $author->plaintext . ", " ; 
print $year->innertext . ", ";
print $addinfo->plaintext . ", ";
print $publisher->plaintext . ", ";
print $abstract ."/n";
flush();

scraperwiki::save_sqlite(array("a"), array("a"=>$numrecords, "title"=>$title->innertext, "author"=>$author->plaintext, "year"=>$year->innertext, "addinfo"=>$addinfo->plaintext, "publisher"=>$publisher->plaintext, "abstract"=>$abstract), $table_name="acmdata1", $verbose=2); 
scraperwiki::sqlitecommit(); 
$numrecords++;

flush();
            }
             
    }
return $numrecords;
}

function getAbstract($paperURL)
{
    #print "URL: " . $paperURL ."\n";

    $html_content = scraperWiki::scrape($paperURL);
    $html = str_get_html($html_content);

    $abstract = $html->find("div[@style='display:inline']", 0);
print "abstract " . $abstract->plaintext . "\n";
    $abstractText = $abstract->plaintext;
    $html->__destruct();
return $abstractText;
}

function getNextLink($nextLink)
{
    $link = "";
    foreach ($nextLink->find("a") as $ref)
    {
        if (strpos($ref->plaintext, "next") > 0)
        {
            $link = "http://dl.acm.org/" . $ref->href;
            $link = str_replace(" ", "%20", $link);
            
            #print "Ref found " . "\n";
        }
    }
    #print "Next link: " . strlen($link) . " " . $link . "\n";

return $link;
}

?>
<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php'; 

#$nextPageLink = "http://dl.acm.org/results.cfm?CFID=192482131&CFTOKEN=17329111&adv=1&COLL=DL&DL=ACM&termzone=all&allofem=%22serious+games%22&anyofem=&noneofem=&peoplezone=Name&people=&peoplehow=and&keyword=&keywordhow=AND&affil=&affilhow=AND&pubin=&pubinhow=and&pubby=&pubbyhow=OR&since_year=2004&before_year=&pubashow=OR&sponsor=&sponsorhow=AND&confdate=&confdatehow=OR&confloc=&conflochow=OR&isbnhow=OR&isbn=&doi=&ccs=&subj=&Go.x=26&Go.y=12";

#$nextPageLink = "http://dl.acm.org/results.cfm?CFID=196152628&CFTOKEN=70127669&adv=1&COLL=DL&DL=ACM&Go.x=29&Go.y=6&termzone=Abstract&allofem=evaluation&anyofem=web2+wiki+blog+podcast+vodcast&noneofem=&peoplezone=Name&people=&peoplehow=and&keyword=&keywordhow=AND&affil=&affilhow=AND&pubin=&pubinhow=and&pubby=&pubbyhow=OR&since_year=2000&before_year=&pubashow=OR&sponsor=&sponsorhow=AND&confdate=&confdatehow=OR&confloc=&conflochow=OR&isbnhow=OR&isbn=&doi=&ccs=&subj=";

$nextPageLink = "http://dl.acm.org/results.cfm?CFID=196152628&CFTOKEN=70127669&adv=1&COLL=DL&DL=ACM&termzone=Abstract&allofem=evaluation&anyofem=%22e-portfolio%22&noneofem=&peoplezone=Name&people=&peoplehow=and&keyword=&keywordhow=AND&affil=&affilhow=AND&pubin=&pubinhow=and&pubby=&pubbyhow=OR&since_year=2000&before_year=&pubashow=OR&sponsor=&sponsorhow=AND&confdate=&confdatehow=OR&confloc=&conflochow=OR&isbnhow=OR&isbn=&doi=&ccs=&subj=&Go.x=30&Go.y=8";

#$html_content = scraperWiki::scrape($nextPageLink); 
#$html1 = str_get_html($html_content);
#$nextLink = $html1->find("td[@colspan='2']", 0);
#$nextPageLink = getNextLink($nextLink);
#parsePage($html1);

#print "Next page link: " . $nextPageLink . "\n";
print "title, author, year, addinfo, publisher, abstract" . "\n";

#scraperwiki::sqliteexecute("create table acmdata1 (a int, `title` string, 'author' string, 'year' string, 'addinfo' string, 'publisher' string, 'abstract' string)"); 

$maxPages = 0;
$numrecords = 1;
while (strlen($nextPageLink) > 0 and $maxPages < 6)
    {
        $maxPages++;        

#print "Moving on to next page" . "\n";

        $html_content = scraperWiki::scrape($nextPageLink);
        $html1 = str_get_html($html_content);

#print $html1 . "\n";

        $nextLink = $html1->find("td[@colspan='2']", 0);
# print "Next link: " . $nextLink->innertext . "\n";
        $nextPageLink = getNextLink($nextLink);

        $numrecords = parsePage($html1, $maxPages);
        sleep(120);
    }

print "No further pages" . "\n";        
$data = scraperwiki::select("* from acmdata1");

print "<html><table>";
print "<tr><th>Title</th><th>Author</th><th>Year</th><th>AddInfo</th><th>Publisher</th><th>Abstract</th>";
foreach($data as $d)
{
print "<tr>"; 
    print "<td>" . "ACM" . "</td>"; 
    print "<td>" . $d["title"] . "</td>"; 
    print "<td>" . $d["author"] . "</td>"; 
    print "<td>" . $d["year"] . "</td>"; 
    print "<td>" . $d["addinfo"] . "</td>"; 
    print "<td>" . $d["publisher"] . "</td>"; 
    print "<td>" . $d["abstract"] . "</td>"; 
print "</tr>";
}
print "</table></html>";
flush();

function parsePage($html1, $pageNo)
{
    $numrecords = 1 + 20*$pageNo;
    foreach ($html1->find("table[@style='padding: 5px; 5px; 5px; 5px;']") as $row) 
        {
        $tr1 = $row->find("tr", 0);
        # print $tr1 . "\n"; 
        $title = $tr1->find("a[@target='_self']", 0);
        $papertitle = "http://dl.acm.org/" . $title->href."&preflayout=flat";

        foreach ($tr1->find("div.authors") as $author) 
            { 
                $tr2 = $row->find("tr", 1);
                $year = $tr2->find("td", 0);
                $addinfo = $tr2->find("td", 2);
                $tr3 = $row->find("tr", 2);
                $publisher = $tr3->find("td", 0);
                $abstract = getAbstract($papertitle);
print "abstract " . $abstract . "\n";

                sleep(30);

print $title->innertext . ", "; 
print $author->plaintext . ", " ; 
print $year->innertext . ", ";
print $addinfo->plaintext . ", ";
print $publisher->plaintext . ", ";
print $abstract ."/n";
flush();

scraperwiki::save_sqlite(array("a"), array("a"=>$numrecords, "title"=>$title->innertext, "author"=>$author->plaintext, "year"=>$year->innertext, "addinfo"=>$addinfo->plaintext, "publisher"=>$publisher->plaintext, "abstract"=>$abstract), $table_name="acmdata1", $verbose=2); 
scraperwiki::sqlitecommit(); 
$numrecords++;

flush();
            }
             
    }
return $numrecords;
}

function getAbstract($paperURL)
{
    #print "URL: " . $paperURL ."\n";

    $html_content = scraperWiki::scrape($paperURL);
    $html = str_get_html($html_content);

    $abstract = $html->find("div[@style='display:inline']", 0);
print "abstract " . $abstract->plaintext . "\n";
    $abstractText = $abstract->plaintext;
    $html->__destruct();
return $abstractText;
}

function getNextLink($nextLink)
{
    $link = "";
    foreach ($nextLink->find("a") as $ref)
    {
        if (strpos($ref->plaintext, "next") > 0)
        {
            $link = "http://dl.acm.org/" . $ref->href;
            $link = str_replace(" ", "%20", $link);
            
            #print "Ref found " . "\n";
        }
    }
    #print "Next link: " . strlen($link) . " " . $link . "\n";

return $link;
}

?>
