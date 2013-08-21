<?php

# Specify the URL of the PDF
$src_pdf = "http://samplepdf.com/sample.pdf";

# Some temporary files
$pdf_f = tempnam('/tmp', 'inp') . '.pdf';
$xml_f = tempnam('/tmp', 'out') . '.xml';

# Download the PDF into a temporary file
file_put_contents($pdf_f, file_get_contents($src_pdf));

# Convert the PDF to XML
$cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "' . $pdf_f . '" "'. $xml_f .'" >/dev/null 2>&1';
system($cmd);

# Load the XML and parse it.... we are really just iterating over the page elements 
# but https://views.scraperwiki.com/run/pdf-to-html-preview-1/ should give
# a better idea of the XML output you can expect.
$xml = new SimpleXMLElement( file_get_contents($xml_f) );
$p = 1;
foreach( $xml->page as $page) {
    print (">> Processing text on page " . $p . "\n");
    $t = 1;
    foreach( $page->text as $txt) {
        if ( strlen( trim($txt) ) > 0 ) {
            print "> Text block " . $t . "\n";
            print " " . $txt . "\n";
            $t += 1;
        }
    }
}

?>

<?php

# Specify the URL of the PDF
$src_pdf = "http://samplepdf.com/sample.pdf";

# Some temporary files
$pdf_f = tempnam('/tmp', 'inp') . '.pdf';
$xml_f = tempnam('/tmp', 'out') . '.xml';

# Download the PDF into a temporary file
file_put_contents($pdf_f, file_get_contents($src_pdf));

# Convert the PDF to XML
$cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "' . $pdf_f . '" "'. $xml_f .'" >/dev/null 2>&1';
system($cmd);

# Load the XML and parse it.... we are really just iterating over the page elements 
# but https://views.scraperwiki.com/run/pdf-to-html-preview-1/ should give
# a better idea of the XML output you can expect.
$xml = new SimpleXMLElement( file_get_contents($xml_f) );
$p = 1;
foreach( $xml->page as $page) {
    print (">> Processing text on page " . $p . "\n");
    $t = 1;
    foreach( $page->text as $txt) {
        if ( strlen( trim($txt) ) > 0 ) {
            print "> Text block " . $t . "\n";
            print " " . $txt . "\n";
            $t += 1;
        }
    }
}

?>

