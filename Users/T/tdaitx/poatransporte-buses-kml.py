import scraperwiki

document_start = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Rotas dos ônibus de Porto Alegre</name>
    <description>Rotas de todos os ônibus de Porto Alegre. Fonte: https://scraperwiki.com/scrapers/poatransporte-buses/</description>
    <Style id='Style-line'>
      <LabelStyle>
        <scale>0.0</scale>
      </LabelStyle>
      <LineStyle>
        <color>800000ff</color>
        <width>2</width>
      </LineStyle>
      <BalloonStyle>
        <text>$[description]</text>
      </BalloonStyle>
    </Style>
    <Style id='Style-line-hover'>
      <LineStyle>
        <color>800000ff</color>
        <width>2</width>
      </LineStyle>
      <BalloonStyle>
        <text>$[description]</text>
      </BalloonStyle>
    </Style>
    <StyleMap id='Style-line-map'>
      <Pair>
        <key>normal</key>
        <styleUrl>#Style-line</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#Style-line-hover</styleUrl>
      </Pair>
    </StyleMap>"""

document_end = """    </Document>
</kml>
"""

placemark_template = """    <Placemark>
      <name>%(codigo)s</name>
      <description>%(id)d - %(codigo)s-%(sentido)d - %(nome)s - %(distancia).2f Km</description>
      <styleUrl>#Style-line-map</styleUrl>
      <ExtendedData>
        <Data name='linha_id'>
          <value>%(id)d</value>
        </Data>
        <Data name='nome'>
          <value>%(nome)s</value>
        </Data>
        <Data name='sentido'>
          <value>%(sentido)d</value>
        </Data>
        <Data name='distancia'>
          <value>%(distancia)d Km</value>
        </Data>
      </ExtendedData>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>%(rota)s</coordinates>
      </LineString>
    </Placemark>"""

#scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
scraperwiki.utils.httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")
scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment; filename=poatransporte-rotas.kml")
scraperwiki.sqlite.attach('poatransporte-buses', 'buses')
buses = scraperwiki.sqlite.select('* from buses')

print document_start
for bus in buses:
    print (placemark_template % bus)
print document_end
import scraperwiki

document_start = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Rotas dos ônibus de Porto Alegre</name>
    <description>Rotas de todos os ônibus de Porto Alegre. Fonte: https://scraperwiki.com/scrapers/poatransporte-buses/</description>
    <Style id='Style-line'>
      <LabelStyle>
        <scale>0.0</scale>
      </LabelStyle>
      <LineStyle>
        <color>800000ff</color>
        <width>2</width>
      </LineStyle>
      <BalloonStyle>
        <text>$[description]</text>
      </BalloonStyle>
    </Style>
    <Style id='Style-line-hover'>
      <LineStyle>
        <color>800000ff</color>
        <width>2</width>
      </LineStyle>
      <BalloonStyle>
        <text>$[description]</text>
      </BalloonStyle>
    </Style>
    <StyleMap id='Style-line-map'>
      <Pair>
        <key>normal</key>
        <styleUrl>#Style-line</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#Style-line-hover</styleUrl>
      </Pair>
    </StyleMap>"""

document_end = """    </Document>
</kml>
"""

placemark_template = """    <Placemark>
      <name>%(codigo)s</name>
      <description>%(id)d - %(codigo)s-%(sentido)d - %(nome)s - %(distancia).2f Km</description>
      <styleUrl>#Style-line-map</styleUrl>
      <ExtendedData>
        <Data name='linha_id'>
          <value>%(id)d</value>
        </Data>
        <Data name='nome'>
          <value>%(nome)s</value>
        </Data>
        <Data name='sentido'>
          <value>%(sentido)d</value>
        </Data>
        <Data name='distancia'>
          <value>%(distancia)d Km</value>
        </Data>
      </ExtendedData>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>%(rota)s</coordinates>
      </LineString>
    </Placemark>"""

#scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
scraperwiki.utils.httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")
scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment; filename=poatransporte-rotas.kml")
scraperwiki.sqlite.attach('poatransporte-buses', 'buses')
buses = scraperwiki.sqlite.select('* from buses')

print document_start
for bus in buses:
    print (placemark_template % bus)
print document_end
import scraperwiki

document_start = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Rotas dos ônibus de Porto Alegre</name>
    <description>Rotas de todos os ônibus de Porto Alegre. Fonte: https://scraperwiki.com/scrapers/poatransporte-buses/</description>
    <Style id='Style-line'>
      <LabelStyle>
        <scale>0.0</scale>
      </LabelStyle>
      <LineStyle>
        <color>800000ff</color>
        <width>2</width>
      </LineStyle>
      <BalloonStyle>
        <text>$[description]</text>
      </BalloonStyle>
    </Style>
    <Style id='Style-line-hover'>
      <LineStyle>
        <color>800000ff</color>
        <width>2</width>
      </LineStyle>
      <BalloonStyle>
        <text>$[description]</text>
      </BalloonStyle>
    </Style>
    <StyleMap id='Style-line-map'>
      <Pair>
        <key>normal</key>
        <styleUrl>#Style-line</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#Style-line-hover</styleUrl>
      </Pair>
    </StyleMap>"""

document_end = """    </Document>
</kml>
"""

placemark_template = """    <Placemark>
      <name>%(codigo)s</name>
      <description>%(id)d - %(codigo)s-%(sentido)d - %(nome)s - %(distancia).2f Km</description>
      <styleUrl>#Style-line-map</styleUrl>
      <ExtendedData>
        <Data name='linha_id'>
          <value>%(id)d</value>
        </Data>
        <Data name='nome'>
          <value>%(nome)s</value>
        </Data>
        <Data name='sentido'>
          <value>%(sentido)d</value>
        </Data>
        <Data name='distancia'>
          <value>%(distancia)d Km</value>
        </Data>
      </ExtendedData>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>%(rota)s</coordinates>
      </LineString>
    </Placemark>"""

#scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
scraperwiki.utils.httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")
scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment; filename=poatransporte-rotas.kml")
scraperwiki.sqlite.attach('poatransporte-buses', 'buses')
buses = scraperwiki.sqlite.select('* from buses')

print document_start
for bus in buses:
    print (placemark_template % bus)
print document_end
import scraperwiki

document_start = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Rotas dos ônibus de Porto Alegre</name>
    <description>Rotas de todos os ônibus de Porto Alegre. Fonte: https://scraperwiki.com/scrapers/poatransporte-buses/</description>
    <Style id='Style-line'>
      <LabelStyle>
        <scale>0.0</scale>
      </LabelStyle>
      <LineStyle>
        <color>800000ff</color>
        <width>2</width>
      </LineStyle>
      <BalloonStyle>
        <text>$[description]</text>
      </BalloonStyle>
    </Style>
    <Style id='Style-line-hover'>
      <LineStyle>
        <color>800000ff</color>
        <width>2</width>
      </LineStyle>
      <BalloonStyle>
        <text>$[description]</text>
      </BalloonStyle>
    </Style>
    <StyleMap id='Style-line-map'>
      <Pair>
        <key>normal</key>
        <styleUrl>#Style-line</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#Style-line-hover</styleUrl>
      </Pair>
    </StyleMap>"""

document_end = """    </Document>
</kml>
"""

placemark_template = """    <Placemark>
      <name>%(codigo)s</name>
      <description>%(id)d - %(codigo)s-%(sentido)d - %(nome)s - %(distancia).2f Km</description>
      <styleUrl>#Style-line-map</styleUrl>
      <ExtendedData>
        <Data name='linha_id'>
          <value>%(id)d</value>
        </Data>
        <Data name='nome'>
          <value>%(nome)s</value>
        </Data>
        <Data name='sentido'>
          <value>%(sentido)d</value>
        </Data>
        <Data name='distancia'>
          <value>%(distancia)d Km</value>
        </Data>
      </ExtendedData>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>%(rota)s</coordinates>
      </LineString>
    </Placemark>"""

#scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
scraperwiki.utils.httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")
scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment; filename=poatransporte-rotas.kml")
scraperwiki.sqlite.attach('poatransporte-buses', 'buses')
buses = scraperwiki.sqlite.select('* from buses')

print document_start
for bus in buses:
    print (placemark_template % bus)
print document_end
