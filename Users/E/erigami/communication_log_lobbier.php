<?php 
scraperwiki::attach("communication_log");
$who = $_SERVER['URLQUERY'];

$w = urldecode($who);

# Note that we don't bother to SQL escape our arg - we have a read-only connection already, so meh. 
$data = scraperwiki::select("contact.contact_id AS id, person, title, organization, uri, date_contact_h FROM contact INNER JOIN victim ON victim.contact_id=contact.contact_id WHERE behalf='$w' ORDER BY date_contact_c DESC");

$orgs = array();

print "<h2>Contacts on behalf of $w</h2><ul>";
foreach ($data as $row) {
    extract($row);

    $sub = scraperwiki::select("subject FROM contact_subject WHERE contact_id='$id' ORDER BY subject");
    $s = array();
    foreach ($sub as $sRow) {
        $s[] = $sRow['subject'];
    }
    $s = join(', ', $s);
?>
    <li><?= $date_contact_h ?> <a href="<?= $uri ?>"><?= $id ?></a> <?= $person ?>, <?= $title ?>, <?= $organization ?> (<?= $s ?>)</li>
<?php

    $orgs[$organization] += 1;
}
print "</ul>";

print "<h2>Organizations contacted</h2><ul>";
foreach ($orgs as $o => $k) {
?><li><?= $o ?> (<?= $k ?>)</li><?php
}
print '</ul>';

$data = scraperwiki::select("count(*) AS c, subject AS s FROM contact INNER JOIN contact_subject ON contact_subject.contact_id=contact.contact_id WHERE behalf='$w' GROUP BY subject ORDER BY subject DESC");

print "<h2>Subjects covered</h2><ul>";
foreach ($data as $row) {
    extract($row);
?><li><?= $s ?> (<?= $c ?>)</li><?php
}
print "</ul>";
?><?php 
scraperwiki::attach("communication_log");
$who = $_SERVER['URLQUERY'];

$w = urldecode($who);

# Note that we don't bother to SQL escape our arg - we have a read-only connection already, so meh. 
$data = scraperwiki::select("contact.contact_id AS id, person, title, organization, uri, date_contact_h FROM contact INNER JOIN victim ON victim.contact_id=contact.contact_id WHERE behalf='$w' ORDER BY date_contact_c DESC");

$orgs = array();

print "<h2>Contacts on behalf of $w</h2><ul>";
foreach ($data as $row) {
    extract($row);

    $sub = scraperwiki::select("subject FROM contact_subject WHERE contact_id='$id' ORDER BY subject");
    $s = array();
    foreach ($sub as $sRow) {
        $s[] = $sRow['subject'];
    }
    $s = join(', ', $s);
?>
    <li><?= $date_contact_h ?> <a href="<?= $uri ?>"><?= $id ?></a> <?= $person ?>, <?= $title ?>, <?= $organization ?> (<?= $s ?>)</li>
<?php

    $orgs[$organization] += 1;
}
print "</ul>";

print "<h2>Organizations contacted</h2><ul>";
foreach ($orgs as $o => $k) {
?><li><?= $o ?> (<?= $k ?>)</li><?php
}
print '</ul>';

$data = scraperwiki::select("count(*) AS c, subject AS s FROM contact INNER JOIN contact_subject ON contact_subject.contact_id=contact.contact_id WHERE behalf='$w' GROUP BY subject ORDER BY subject DESC");

print "<h2>Subjects covered</h2><ul>";
foreach ($data as $row) {
    extract($row);
?><li><?= $s ?> (<?= $c ?>)</li><?php
}
print "</ul>";
?>