<?php
// Attach the data
scraperwiki::attach("lichfield_cathedral_events");

// Get the data
$data = scraperwiki::select(           
    "* from lichfield_cathedral_events.swdata limit 10"
);
//print_r($data);

echo '<?xml version="1.0" encoding="utf-8"?>';
?>
<rdf:RDF 
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
    xmlns:ev="http://purl.org/rss/1.0/modules/event/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:georss="http://www.georss.org/georss"
    xmlns:creativeCommons="http://backend.userland.com/creativeCommonsRssModule"
    xmlns="http://purl.org/rss/1.0/">
    
    <rdf:Description rdf:about="http://lichfieldlive.co.uk/">
        <dc:title>Lichfield What's On Importer</dc:title>
        <dc:source rdf:resource="http://www.lichfield-cathedral.org/"/>
        <dc:creator>Lichfield Community Media</dc:creator>
        <dc:language>en</dc:language>
    </rdf:Description>
    
    <channel rdf:about="http://lichfieldlive.co.uk/events">
        <title>Lichfield Live What's On Importer</title>
        <link>http://lichfieldlive.co.uk/category/whatson</link>
        <description>Combines multiple feeds into one, optimised for import by Lichfield Live</description>
        <creativeCommons:license>http://creativecommons.org/licenses/by-nc-sa/2.0/uk/</creativeCommons:license>
    </channel>
    
    <items>
        <rdf:Seq>
        <?php
            foreach ($data as $item){
                echo '<rdf:li rdf:resource="'.$item['link'].'" />'."\n        ";
            }
        ?>
        </rdf:Seq>
    </items>
    
    <?php
        unset($item);
        foreach ($data as $item){
            $startdate = date('c', strtotime($item['pubDate'])); // RFC2822 the start date
            $enddate = date('c', strtotime($item['pubDate'])+3600);
            ?>
    <item rdf:about="<?php echo $item['link']; ?>">
        <title><?php echo ucwords(strtolower($item['title'])); ?></title>
        <link><?php echo $item['link']; ?></link>
        <description><?php echo ucfirst(strtolower($item['description'])); ?></description>
        <ev:startdate><?php echo $startdate; ?></ev:startdate>
        <ev:enddate><?php echo $enddate; ?></ev:enddate>
        <ev:location>Lichfield Cathedral</ev:location>
        <georss:point>52.685556 -1.830556</georss:point>
    </item>
    
            <?php
        }
    ?>
</rdf:RDF><?php
// Attach the data
scraperwiki::attach("lichfield_cathedral_events");

// Get the data
$data = scraperwiki::select(           
    "* from lichfield_cathedral_events.swdata limit 10"
);
//print_r($data);

echo '<?xml version="1.0" encoding="utf-8"?>';
?>
<rdf:RDF 
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
    xmlns:ev="http://purl.org/rss/1.0/modules/event/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:georss="http://www.georss.org/georss"
    xmlns:creativeCommons="http://backend.userland.com/creativeCommonsRssModule"
    xmlns="http://purl.org/rss/1.0/">
    
    <rdf:Description rdf:about="http://lichfieldlive.co.uk/">
        <dc:title>Lichfield What's On Importer</dc:title>
        <dc:source rdf:resource="http://www.lichfield-cathedral.org/"/>
        <dc:creator>Lichfield Community Media</dc:creator>
        <dc:language>en</dc:language>
    </rdf:Description>
    
    <channel rdf:about="http://lichfieldlive.co.uk/events">
        <title>Lichfield Live What's On Importer</title>
        <link>http://lichfieldlive.co.uk/category/whatson</link>
        <description>Combines multiple feeds into one, optimised for import by Lichfield Live</description>
        <creativeCommons:license>http://creativecommons.org/licenses/by-nc-sa/2.0/uk/</creativeCommons:license>
    </channel>
    
    <items>
        <rdf:Seq>
        <?php
            foreach ($data as $item){
                echo '<rdf:li rdf:resource="'.$item['link'].'" />'."\n        ";
            }
        ?>
        </rdf:Seq>
    </items>
    
    <?php
        unset($item);
        foreach ($data as $item){
            $startdate = date('c', strtotime($item['pubDate'])); // RFC2822 the start date
            $enddate = date('c', strtotime($item['pubDate'])+3600);
            ?>
    <item rdf:about="<?php echo $item['link']; ?>">
        <title><?php echo ucwords(strtolower($item['title'])); ?></title>
        <link><?php echo $item['link']; ?></link>
        <description><?php echo ucfirst(strtolower($item['description'])); ?></description>
        <ev:startdate><?php echo $startdate; ?></ev:startdate>
        <ev:enddate><?php echo $enddate; ?></ev:enddate>
        <ev:location>Lichfield Cathedral</ev:location>
        <georss:point>52.685556 -1.830556</georss:point>
    </item>
    
            <?php
        }
    ?>
</rdf:RDF>