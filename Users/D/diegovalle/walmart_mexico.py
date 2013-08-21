import scraperwiki
import lxml.etree
import lxml.html

store_codes = [1003,1007,1015,1016,1022,1027,1031,1032,1044,1045,1054,1067,1084,1107,1108,1119,1130,1138,1139,1140,1169,1170,1171,1195,1202,1204,1205,1206,1403,1404,1423,1425,1462,1489,1549,1550,1584,1585,1622,1623,1624,1683,1684,1685,1686,1724,1727,1833,1834,1902,2023,2033,2034,2041,2042,2044,2049,2050,2074,2075,2076,2079,2080,2089,2090,2091,2179,2218,2219,2302,2303,2304,2342,2343,2344,2345,2346,2347,2349,2356,2375,2377,2378,2379,2380,2381,2382,2383,2384,2430,2431,2432,2433,2463,2464,2465,2466,2468,2670,2676,2689,2731,2732,2733,2734,2735,2765,2839,2840,3005,3014,3015,3016,3030,3031,3033,3051,3061,3069,3071,3091,3113,3127,3198,3293,3355,3356,3357,3358,3506,3555,3622,3630,3631,3632,3664,3718,3719,3720,3721,3745,3746,3747,3790,3794,3800,3845,3846,3847,3848,3850,3851,3852,3853,3854,3856,3857,3858,3861,3862,3863,3864,3872,3876,3877,3878,3879,3886,3893,3894,3895,3900,3909,4011,4012,4018,4025,4026,4036,4048,4062,4071,4072,4073,4090,4109,4120,4122,4137,4138,4139,4154,4155,4156,4157,4187,4191,4540,4546,4547,4548,4549,4999,5700,5702,5727,5728,5749,5764,5765,5791,5825,5855,5999]

def getData(url, stores, store_type):
    for i in stores:
        html = scraperwiki.scrape(url + str(i))
        root = lxml.html.fromstring(html)
        linimble = root.cssselect("div .club-box")[0]

        idx = lxml.etree.tostring(root).find("GLatLng")
        data = {
          'lat' : lxml.etree.tostring(root)[idx+8:idx+26].split(',')[0].replace(')', '').replace(';',''),
          'long' : lxml.etree.tostring(root)[idx+8:idx+26].split(',')[1].replace(')', '').replace(';','').replace('googleMark',''),
          'address' : lxml.etree.tostring(linimble),
          'index' : i,
          'type' :  store_type
        }

        if data['address'] != '<div class="club-box">&#13; &#13; <h3>WALMART&#160;</h3>&#13; &#13; <ul><li>&#13; <h3>&#13; Horario:&#13; </h3>&#13; </li>&#13; <li class="bottom-space">&#13; &#13; a&#13; &#13; hrs.&#13; </li>&#13; <li>&#13; <h3>&#13; N&#195;&#186;mero Telef&#195;&#179;nico:&#13; </h3>&#13; </li>&#13; <li>&#13; &#160;&#13; </li>&#13; </ul><ul><li>&#13; <h3>&#13; Direcci&#195;&#179;n:&#13; </h3>&#13; </li>&#13; <li>&#13; &#160;,&#13; &#13; </li>&#13; <li>&#13; ,&#160;&#13; </li>&#13; <li>&#13; 0&#13; </li>&#13; </ul><ul class="large"><li>&#13; <h3>&#13; Servicios:&#13; </h3>&#13; </li>&#13; <li>&#13; Fotorevelado , Carnicer&#195;&#173;a , Rosticer&#195;&#173;a , Panader&#195;&#173;a , Frutas y Verduras , Deli , SAM&#194;&#180;S CAF&#195;&#137; , Farmacia , Joyer&#195;&#173;a , &#195;&#147;ptica , Centro Llantero&#13; </li>&#13; </ul></div>&#13; &#13;':
            scraperwiki.sqlite.save(unique_keys=['lat', 'long', 'address', 'type'], data = data)
    return(data)

#getData("http://www.walmart.com.mx/pages/SelectClubLocalization.aspx?clubId=", store_codes, 'walmart')
 
getData("http://www.sams.com.mx/pages/SelectClubLocalization.aspx?clubId=", range(7000, 8000), 'sams') 