<?php
$sourcescraper = '';
scraperwiki::attach("pcusa_church_data");
$ch_id = 10825;
$chData = scraperwiki::select("* from churches where church_id=" . $ch_id);

foreach($chData as $church)
    {
    print "<h2>PCUSA: " . $church["name"] . "</h2>\n\r";
    print "<ul>";
    print "<li>id=" . $church["church_id"] . "</li>\n\r";
    print "<li>" . $church["adr1"] . "</li>\n\r";
    print "<li>" . $church["adr2"] . "</li>\n\r";
    print "<li>" . $church["city"] . "," . $church["state"]     . " " . $church["zip_blob"] . "</li>\n\r";

    print "<li>Phone:" . $church["phone"] . "<li> Fax:" . $church["fax"] . "</li>\n\r";
    print "<li>URL:\"" . $church["url"]     . "\"</li>\n\r";
    print "<li>Email:\"" . $church["email"]     . "\"</li>\n\r";
    print "<li>Lon:" . $church["lon"] . " Lat:" . $church["lat"] . "</li>\n\r";
    print "</ul>\n\r<table border=1>";

    print "<tr><td>item</td><td>2000</td><td>2001</td><td>2002</td><td>2003</td><td>2004</td><td>2005</td><td>2006</td><td>2007</td><td>2008</td><td>2009</td><td>2010</td></tr>\n\r";
    print "<tr><td>Members</td><td>". number_format($church["m2000"])."</td><td>". number_format($church["m2001"])."</td><td>". number_format($church["m2002"])."</td><td>". number_format($church["m2003"])."</td><td>". number_format($church["m2004"])."</td><td>". number_format($church["m2005"])."</td><td>". number_format($church["m2006"])."</td><td>". number_format($church["m2007"])."</td><td>". number_format($church["m2008"])."</td><td>". number_format($church["m2009"])."</td><td>". number_format($church["m2010"])."</td></tr>\n\r";
    print "<tr><td>Worship</td><td>". number_format($church["w2000"])."</td><td>". number_format($church["w2001"])."</td><td>". number_format($church["w2002"])."</td><td>". number_format($church["w2003"])."</td><td>". number_format($church["w2004"])."</td><td>". number_format($church["w2005"])."</td><td>". number_format($church["w2006"])."</td><td>". number_format($church["w2007"])."</td><td>". number_format($church["w2008"])."</td><td>". number_format($church["w2009"])."</td><td>". number_format($church["w2010"])."</td></tr>\n\r";
    print "<tr><td>Contributions</td><td>". number_format($church["c2000"])."</td><td>". number_format($church["c2001"])."</td><td>". number_format($church["c2002"])."</td><td>". number_format($church["c2003"])."</td><td>". number_format($church["c2004"])."</td><td>". number_format($church["c2005"])."</td><td>". number_format($church["c2006"])."</td><td>". number_format($church["c2007"])."</td><td>". number_format($church["c2008"])."</td><td>". number_format($church["c2009"])."</td><td>". number_format($church["c2010"])."</td></tr>\n\r";
    }
?>

<?php
$sourcescraper = '';
scraperwiki::attach("pcusa_church_data");
$ch_id = 10825;
$chData = scraperwiki::select("* from churches where church_id=" . $ch_id);

foreach($chData as $church)
    {
    print "<h2>PCUSA: " . $church["name"] . "</h2>\n\r";
    print "<ul>";
    print "<li>id=" . $church["church_id"] . "</li>\n\r";
    print "<li>" . $church["adr1"] . "</li>\n\r";
    print "<li>" . $church["adr2"] . "</li>\n\r";
    print "<li>" . $church["city"] . "," . $church["state"]     . " " . $church["zip_blob"] . "</li>\n\r";

    print "<li>Phone:" . $church["phone"] . "<li> Fax:" . $church["fax"] . "</li>\n\r";
    print "<li>URL:\"" . $church["url"]     . "\"</li>\n\r";
    print "<li>Email:\"" . $church["email"]     . "\"</li>\n\r";
    print "<li>Lon:" . $church["lon"] . " Lat:" . $church["lat"] . "</li>\n\r";
    print "</ul>\n\r<table border=1>";

    print "<tr><td>item</td><td>2000</td><td>2001</td><td>2002</td><td>2003</td><td>2004</td><td>2005</td><td>2006</td><td>2007</td><td>2008</td><td>2009</td><td>2010</td></tr>\n\r";
    print "<tr><td>Members</td><td>". number_format($church["m2000"])."</td><td>". number_format($church["m2001"])."</td><td>". number_format($church["m2002"])."</td><td>". number_format($church["m2003"])."</td><td>". number_format($church["m2004"])."</td><td>". number_format($church["m2005"])."</td><td>". number_format($church["m2006"])."</td><td>". number_format($church["m2007"])."</td><td>". number_format($church["m2008"])."</td><td>". number_format($church["m2009"])."</td><td>". number_format($church["m2010"])."</td></tr>\n\r";
    print "<tr><td>Worship</td><td>". number_format($church["w2000"])."</td><td>". number_format($church["w2001"])."</td><td>". number_format($church["w2002"])."</td><td>". number_format($church["w2003"])."</td><td>". number_format($church["w2004"])."</td><td>". number_format($church["w2005"])."</td><td>". number_format($church["w2006"])."</td><td>". number_format($church["w2007"])."</td><td>". number_format($church["w2008"])."</td><td>". number_format($church["w2009"])."</td><td>". number_format($church["w2010"])."</td></tr>\n\r";
    print "<tr><td>Contributions</td><td>". number_format($church["c2000"])."</td><td>". number_format($church["c2001"])."</td><td>". number_format($church["c2002"])."</td><td>". number_format($church["c2003"])."</td><td>". number_format($church["c2004"])."</td><td>". number_format($church["c2005"])."</td><td>". number_format($church["c2006"])."</td><td>". number_format($church["c2007"])."</td><td>". number_format($church["c2008"])."</td><td>". number_format($church["c2009"])."</td><td>". number_format($church["c2010"])."</td></tr>\n\r";
    }
?>

