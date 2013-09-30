<?php
#############################################################################
# START HERE: Tutorial for scraping pages behind form, using the            #
# SimpleTest Scriptable Web Browser.                                        #
# Documentation is here: http://www.lastcraft.com/browser_documentation.php #
#############################################################################
require 'scraperwiki/simple_html_dom.php';
require_once('simpletest/browser.php');

# We're scraping the National Lottery grants form. You can
# replace this with the URL you're interested in.
$url = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx";

# Browse to the page with the form on it
$browser = &new SimpleBrowser();
$browser->get($url);

# Set the fields in the form. Here we're looking for grants by Arts Council England in London
$browser->setFieldById("ctl00_phMainContent_lbDistributingBody", "AE");
$browser->setFieldById("ctl00_phMainContent_lbGeographicalArea", "London");

# Submit the form
$html = $browser->clickSubmitById("ctl00_phMainContent_buttonSubmit");

# Process the results
$dom = new simple_html_dom();
$dom->load($html);
$results = $dom->find("span[id=ctl00_phMainContent_grantSearchResults_labelResultsCount]");
echo "Number of results = " . trim($results[0]->plaintext) . "\n";
?>
<?php
#############################################################################
# START HERE: Tutorial for scraping pages behind form, using the            #
# SimpleTest Scriptable Web Browser.                                        #
# Documentation is here: http://www.lastcraft.com/browser_documentation.php #
#############################################################################
require 'scraperwiki/simple_html_dom.php';
require_once('simpletest/browser.php');

# We're scraping the National Lottery grants form. You can
# replace this with the URL you're interested in.
$url = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx";

# Browse to the page with the form on it
$browser = &new SimpleBrowser();
$browser->get($url);

# Set the fields in the form. Here we're looking for grants by Arts Council England in London
$browser->setFieldById("ctl00_phMainContent_lbDistributingBody", "AE");
$browser->setFieldById("ctl00_phMainContent_lbGeographicalArea", "London");

# Submit the form
$html = $browser->clickSubmitById("ctl00_phMainContent_buttonSubmit");

# Process the results
$dom = new simple_html_dom();
$dom->load($html);
$results = $dom->find("span[id=ctl00_phMainContent_grantSearchResults_labelResultsCount]");
echo "Number of results = " . trim($results[0]->plaintext) . "\n";
?>
