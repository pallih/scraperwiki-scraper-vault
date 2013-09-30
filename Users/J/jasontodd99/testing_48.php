<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.legis.state.tx.us/BillLookup/History.aspx?LegSess=831&Bill=HB1");
$html = str_get_html($html_content);

foreach ($html->find("td#cellLastAction") as $lastaction) {
print $lastaction->plaintext . "\n";
}

foreach ($html->find("td#cellCaptionText") as $caption) {
print $caption->plaintext . "\n";
}

foreach ($html->find("td#cellCaptionVersion") as $captionversion) {
print $captionversion->plaintext . "\n";
}

foreach ($html->find("td#cellAuthors") as $authors) {
print $authors->plaintext . "\n";
}

foreach ($html->find("td#cellCosponsors") as $cosponsors) {
print $cosponsors->plaintext . "\n";

foreach ($html->find("td#cellSubjects") as $subjects) {
print $subjects->plaintext . "\n";
}

foreach ($html->find("td#cellComm1Title") as $committee1title) {
print $committee1title->plaintext . "\n";
}

foreach ($html->find("td#cellComm1Committee") as $committee1name) {
print $committee1name->plaintext . "\n";
}

foreach ($html->find("td#cellComm1Subcommittee") as $subcommittee1name) {
print $subcommittee1name->plaintext . "\n";
}

foreach ($html->find("td#cellComm1CommitteeStatus") as $committee1status) {
print $committee1status->plaintext . "\n";
}

foreach ($html->find("td#cellComm1CommitteeVote") as $cellComm1CommitteeVote) {
print $cellComm1CommitteeVote->plaintext . "\n";
}




$es = $html->find("table");
print $es . "\n";
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.legis.state.tx.us/BillLookup/History.aspx?LegSess=831&Bill=HB1");
$html = str_get_html($html_content);

foreach ($html->find("td#cellLastAction") as $lastaction) {
print $lastaction->plaintext . "\n";
}

foreach ($html->find("td#cellCaptionText") as $caption) {
print $caption->plaintext . "\n";
}

foreach ($html->find("td#cellCaptionVersion") as $captionversion) {
print $captionversion->plaintext . "\n";
}

foreach ($html->find("td#cellAuthors") as $authors) {
print $authors->plaintext . "\n";
}

foreach ($html->find("td#cellCosponsors") as $cosponsors) {
print $cosponsors->plaintext . "\n";

foreach ($html->find("td#cellSubjects") as $subjects) {
print $subjects->plaintext . "\n";
}

foreach ($html->find("td#cellComm1Title") as $committee1title) {
print $committee1title->plaintext . "\n";
}

foreach ($html->find("td#cellComm1Committee") as $committee1name) {
print $committee1name->plaintext . "\n";
}

foreach ($html->find("td#cellComm1Subcommittee") as $subcommittee1name) {
print $subcommittee1name->plaintext . "\n";
}

foreach ($html->find("td#cellComm1CommitteeStatus") as $committee1status) {
print $committee1status->plaintext . "\n";
}

foreach ($html->find("td#cellComm1CommitteeVote") as $cellComm1CommitteeVote) {
print $cellComm1CommitteeVote->plaintext . "\n";
}




$es = $html->find("table");
print $es . "\n";
}
?>
