<?php
# Hi. Welcome to the PHP editor window on ScraperWiki.

# To see if everything is working okay, click the RUN button on the bottom left
# to make the following four lines of code do its stuff

require 'scraperwiki/simple_html_dom.php';

for($i = 0; $i < 10; $i++)
{
    print "Hello, " . $i . "\n";
}

# Did it work? 10 lines should have been printed in the console window below
# If not, try using Google Chrome or the latest version of FireFox.

# The first job of any scraper is to download the text of a web-page.  
# Uncomment the next two lines of code (remove the # from the beginning of the line)
# and click RUN again to see how it works.

$html = scraperwiki::scrape('http://scraperwiki.com/hello_world.html');
echo $html;

$dom = new simple_html_dom();
$dom->load($html);

foreach ($dom->find("tbody tr") as $data) {
    $tds = $data->find("td");    
    if ($tds != null) {
        $record = array(
            'row' => $tds[0]->plaintext,
        );
        scraperwiki::save(array('row'), $record);
    }
}

# The text will appear in the console, and the URL that it downloaded from
# should appear under "Sources".
?>
<?php
# Hi. Welcome to the PHP editor window on ScraperWiki.

# To see if everything is working okay, click the RUN button on the bottom left
# to make the following four lines of code do its stuff

require 'scraperwiki/simple_html_dom.php';

for($i = 0; $i < 10; $i++)
{
    print "Hello, " . $i . "\n";
}

# Did it work? 10 lines should have been printed in the console window below
# If not, try using Google Chrome or the latest version of FireFox.

# The first job of any scraper is to download the text of a web-page.  
# Uncomment the next two lines of code (remove the # from the beginning of the line)
# and click RUN again to see how it works.

$html = scraperwiki::scrape('http://scraperwiki.com/hello_world.html');
echo $html;

$dom = new simple_html_dom();
$dom->load($html);

foreach ($dom->find("tbody tr") as $data) {
    $tds = $data->find("td");    
    if ($tds != null) {
        $record = array(
            'row' => $tds[0]->plaintext,
        );
        scraperwiki::save(array('row'), $record);
    }
}

# The text will appear in the console, and the URL that it downloaded from
# should appear under "Sources".
?>
