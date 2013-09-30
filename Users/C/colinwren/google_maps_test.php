<?php
# Blank PHP
$sourcescraper = 'nhschoicesorgscraper';
scraperwiki::attach($sourcescraper);
$data = scraperwiki::select(           
    "* from ".$sourcescraper.".swdata 
    order by title desc limit 100"
);
?>
<div id="map_canvas" style="width: 500px; height: 400px; position: relative; margin: 0px;">Map Div</div>
<p><a href="javascript:initialize();" title="Runthe script">Run the map thing</a></p>
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript">
            function initialize(){
                var startplace = new google.maps.LatLng(<?php
                    $postcode_start = scraperwiki::gb_postcode_to_latlng("SW170EX");
                  ?>);
                 var directionsService = new google.maps.DirectionsService();
                 var myOptions = {
                     zoom: 13,
                     center: startplace,
                     mapTypeId: google.maps.MapTypeId.ROADMAP
                 };
                map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);

                <?php
                $counter = 0;
                foreach($data as $gp){
                    $postcode = $gp["postcode"];
                    $long_lat = scraperwiki::gb_postcode_to_latlng($postcode);
                    ?>
                    
                    var myLatLng<?php echo($counter); ?> = new google.maps.LatLng(<?php echo($long_lat[0].",".$long_lat[1]); ?>);
                    var marker<?php echo($counter); ?> = new google.maps.Marker({
                        position: myLatLng<?php echo($counter); ?>,
                        map: map,
                        animation: google.maps.Animation.DROP,
                        title: "<?php echo($gp["title"]); ?>"
                    });


                    <?php
                       $counter++;
                    }

                ?>
                
            }
</script>
<?php
# Blank PHP
$sourcescraper = 'nhschoicesorgscraper';
scraperwiki::attach($sourcescraper);
$data = scraperwiki::select(           
    "* from ".$sourcescraper.".swdata 
    order by title desc limit 100"
);
?>
<div id="map_canvas" style="width: 500px; height: 400px; position: relative; margin: 0px;">Map Div</div>
<p><a href="javascript:initialize();" title="Runthe script">Run the map thing</a></p>
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript">
            function initialize(){
                var startplace = new google.maps.LatLng(<?php
                    $postcode_start = scraperwiki::gb_postcode_to_latlng("SW170EX");
                  ?>);
                 var directionsService = new google.maps.DirectionsService();
                 var myOptions = {
                     zoom: 13,
                     center: startplace,
                     mapTypeId: google.maps.MapTypeId.ROADMAP
                 };
                map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);

                <?php
                $counter = 0;
                foreach($data as $gp){
                    $postcode = $gp["postcode"];
                    $long_lat = scraperwiki::gb_postcode_to_latlng($postcode);
                    ?>
                    
                    var myLatLng<?php echo($counter); ?> = new google.maps.LatLng(<?php echo($long_lat[0].",".$long_lat[1]); ?>);
                    var marker<?php echo($counter); ?> = new google.maps.Marker({
                        position: myLatLng<?php echo($counter); ?>,
                        map: map,
                        animation: google.maps.Animation.DROP,
                        title: "<?php echo($gp["title"]); ?>"
                    });


                    <?php
                       $counter++;
                    }

                ?>
                
            }
</script>
