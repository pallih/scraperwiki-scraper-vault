<?php
    //We're loading the data here
    $sourcescraper = 'csv-scraper';
    $data = scraperwiki::getData($sourcescraper);

    //Little function to convert the object retrieved into an array
    function object_2_array($result) 
    { 
        $array = array(); 
        foreach ($result as $key=>$value) 
        { 
            if (is_object($value)) 
            { 
                $array[$key]=object_2_array($value); 
            } 
            elseif (is_array($value)) 
            { 
                $array[$key]=object_2_array($value); 
            } 
            else 
            { 
                $array[$key]=$value; 
            } 
        } 
        return $array; 
    }

    $arraydata = object_2_array($data);

    //This is all for debug purposes
    //echo count($data);

    //foreach($arraydata as $dataline){
    //echo $dataline['Postcode'];
    //echo $dataline['Data'];
    //}

    //Right! Let's try and make a map out of this stuff...
?>





<!DOCTYPE html "-//W3C//DTD XHTML 1.0 Strict//EN" 
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <title>Google Map Data View from Scraped CSV Data</title>

    <style>
        body{
            padding: 0px;
            margin: 0px;
            font-family: verdana;
        }      

        div#map_canvas{
            display: block;
            position: absolute;
            left: 0px;
            top: 0px;
        }

        div.bubble{
            height: 350px;
            overflow: auto;
            text-align: left;
        }

        div.bubble table{
            font-size: .6em;
            width: 98%;
            border-collapse: collapse;
        }
        
        div.bubble table td{
            padding: 3px;
            border-top: solid 1px #ccc;
            border-bottom: solid 1px #ccc;
        }

        div.bubble table td.cell_right{
            border-right: solid 1px #ccc;
            text-align: center;
        }

        div.bubble table td.cell_left{
            border-left: solid 1px #ccc;
        }

        div.bubble table tr.decent td{
            background-color: #ffff00;
        }

        div.bubble table tr.unsurveyed td{
            background-color: #ccffcc;
        }

        div.bubble table td.bathroom{
            background-color: #ff6600;
        }

        div.bubble table td.chimneys{
            background-color: #99cc00;
        }

        div.bubble table td.electrics{
            background-color: #ccffff;
        }

        div.bubble table td.heating{
            background-color: #c0c0c0;
        }

        div.bubble table td.kitchen{
            background-color: #cc99ff;
        }

        div.bubble table td.thermal{
            background-color: #ff99cc;
        }

        div.bubble table td.doors{
            background-color: #3366ff;
        }

        div.bubble table td.center{
            text-align: center;
        }

        div.bubble table tbody tr:hover td{
            border-bottom: solid 1px red;
        }

        div.bubble table thead td{
            font-weight: bold;
            background-color: #ccc;
            text-align: center;
            /* font-size: .8em;*/
        }
    </style>

    <!--[if lt IE 9]>
    <style>
        div#map_canvas{
            height: auto;
        }
    </style>
    <![endif]-->

    <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=ABQIAAAAJg6auI5fsh-7tMXxfBq79RRTVXw9r635OREAczmDfEdUK8Z4IhT-WC9P0CtKu9YyYqW3fnIbQNQPng" type="text/javascript"></script>    
    <script src="http://www.google.com/uds/api?file=uds.js&v=1.0&source=uds-msw&key=ABQIAAAAJg6auI5fsh-7tMXxfBq79RRTVXw9r635OREAczmDfEdUK8Z4IhT-WC9P0CtKu9YyYqW3fnIbQNQPng" type="text/javascript"></script>

    <script type="text/javascript">
        var map;
        
        function createMarker(point,html,tooltip) {
            //This bit sets a different icon - I'm not using this but you could pass a variable in to change it from the data
            var blueIcon = new GIcon(G_DEFAULT_ICON);
            blueIcon.image = "http://www.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png";

            markerOptions = { icon:blueIcon };

          // FF 1.5 fix
          html = '<div style="white-space:nowrap;">' + html + '</div>';
            var marker = new GMarker(point, {title:tooltip});
          GEvent.addListener(marker, "click", function() {
            marker.openInfoWindowHtml(html);
          });
          return marker;
        }
         
        function usePointFromPostcode(postcode, infoText, callbackFunction) {
        var localSearch = new GlocalSearch();
         
         localSearch.setSearchCompleteCallback(null, 
          function() {
           
           if (localSearch.results[0])
           {  
            var resultLat = localSearch.results[0].lat;
            var resultLng = localSearch.results[0].lng;
            var point = new GLatLng(resultLat,resultLng);
            callbackFunction(point,infoText,postcode);
           }else{
            alert("Postcode not found!");
           }
          }); 
         localSearch.execute(postcode + ", UK");
        }
        function placeMarkerAtPoint(point, infoText, tooltip)
        {
              var marker = createMarker(point,infoText,tooltip)
              map.addOverlay(marker);
        }
        function setCenterToPoint(point)
        {
         map.setCenter(point, 15, G_NORMAL_MAP);
        }
         
         function mapLoad() {
         if (GBrowserIsCompatible()) {
          map = new GMap2(document.getElementById("map_canvas"));
          
          map.addControl(new GLargeMapControl());
          map.addControl(new GMapTypeControl());

             //centerpoint = '<?php $arraydata[0]['Postcode'] ?>';
             //alert(centerpoint);
          usePointFromPostcode('LN1 1DD', '', setCenterToPoint); // This sets the map to the centre
          
          <?php foreach($arraydata as $dataline){ ?>
              info = '';
                                                  usePointFromPostcode('<?php echo $dataline['Postcode'] ?>', '<h2><?php echo $dataline['Postcode'] ?></h2><div class="bubble"><table><thead><tr><td></td><td>Type</td><td>Status</td><td>Bathroom</td><td>Chimneys</td><td>Electrics</td><td>Heating</td><td>Kitchen</td><td>Roof</td><td>Structure</td><td>Thermal Comfort</td><td>Doors</td></tr></thead><tbody><?php echo $dataline['Data'] ?></tbody></table></div>', placeMarkerAtPoint); // This adds the markers from the data we've gathered
          <?php } ?>
         }
        }
            
            
            function initialize() {
              if (GBrowserIsCompatible()) {
                var map = new GMap2(document.getElementById("map_canvas"));
                map.setCenter(new GLatLng(37.4419, -122.1419), 13);
                map.setUIToDefault();
              }
            }

    </script>
  </head>
  <body onload="mapLoad()" onunload="GUnload()"><div id="map_canvas" style="width: 100%; height: 100%;">If you cannot see the map then you must have Javascript disabled</div></body>
</html>