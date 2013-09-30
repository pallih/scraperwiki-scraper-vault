"""
Scraper for ilmeteo.it
"""

import datetime
import optparse
import re
import sys
import time
import traceback
import urllib2

import lxml.html


## Utility functions ===========================================================

re_first_int = re.compile(r"[^0-9\-]*(-?[0-9]+)")
re_first_float = re.compile(r"[^0-9\.\-]*(-?[0-9\.]+)")


def clean_text(text):
    return text.replace(u"\xa0", u" ").strip()


def get_first_float(text):
    try:
        return float(re_first_float.match(text).group(1))
    except:
        return None


def get_first_int(text):
    try:
        return int(re_first_int.match(text).group(1))
    except:
        return None


## The Scraper =================================================================

class IlMeteoSpider(object):
    """Spider for www.ilmeteo.it"""

    re_row_id = re.compile(r"^h(?P<hour>[0-9]+)-(?P<day>[0-9]+)-1$")

    def __init__(self, callback=None, on_scraperwiki=False):
        self.on_scraperwiki = on_scraperwiki
        self._callback = callback

    def _log(self, message):
        sys.stderr.write(">>> {}\n".format(message))

    def _request_page(self, url, retry=3):
        self._log("Request: {}".format(url))
        try:
            if self.on_scraperwiki:
                import scraperwiki
                page = scraperwiki.scrape(url)

            else:
                import requests
                page = requests.get(url).content

            return lxml.html.fromstring(page)
        except KeyboardInterrupt:
            raise
        except:  # Anything might happen up there.. doesn't matter.
            self._log("Request failed.")
            traceback.print_exc()
            if retry > 0:
                time.sleep(2)
                return self._request_page(url, retry - 1)
            else:
                raise

    def location_from_url(self, url):
        location = filter(None, url.split('/'))[-1]
        location = urllib2.unquote(location)
        location = location.replace('+', ' ')
        return location

    def url_start(self):
        return "http://www.ilmeteo.it/Italia"

    def url_region(self, name):
        name = urllib2.quote(name)
        return "http://www.ilmeteo.it/{}".format(name)

    def url_city(self, name):
        name = urllib2.quote(name)
        return "http://www.ilmeteo.it/meteo/{}".format(name)

    def _get_datatable_from_url(self, url):
        root = self._request_page(url)
        datatable = root.cssselect('.datatable')

        if len(datatable) < 1:

            the_frame = root.cssselect('#frmprevi')
            if len(the_frame):
                the_frame = the_frame[0]
                real_url = the_frame.attrib['src']
                root = self._request_page(real_url)
                datatable = root.cssselect('.datatable')

            else:
                raise Exception(
                    "Unable to find .datatable or #frmprevi in the page!")

        return datatable[0]

    def _get_datatable(self, url, retry=3):
        try:
            return self._get_datatable_from_url(url)
        except KeyboardInterrupt:
            raise
        except:
            self._log("Request failed.")
            traceback.print_exc()
            if retry > 0:
                time.sleep(2)
                return self._get_datatable(url, retry - 1)
            else:
                raise

    def spider_location(self, location=None, url=None, day_delta=0):

        if location is None:
            if url is None:
                raise ValueError("You must specify either a location or an URL")
            location = filter(None, url.split('/'))[-1]
            url = "{}/?g={}".format(url, day_delta)

        else:
            url = "{}/?g={}".format(self.url_city(location), day_delta)

        datatable = self._get_datatable(url)

        return self._extract_weather_data(location, datatable, day_delta)

    def _extract_weather_data(self, location, datatable, day_delta):

        now = datetime.datetime.now() + datetime.timedelta(days=day_delta)
        current_month = now.month
        current_year = now.year
        last_day = None

        ## First of all, determine the field positions...
        header_fields = {}

        def resolve_header_name(text):
            text = clean_text(text).strip().lower()
            if text == u"ora":
                return "hour"
            if text == u"tempo":
                return "condition"
            if text == u"t (\xb0c)":
                return "temperature"
            if text == u'vento (km/h)':
                return "wind"
            if text == u"precipitazioni":
                return "precipitations"
            if text == u"w.chill":
                return "wind_chill"
            if text == u"percepita":
                return "perceived"
            if text == u"umidit\xe0":
                return "humidity"
            if text == u"pressione":
                return "pressure"
            if text == u"visibilit\xe0":
                return "visibility"
            if text == u"uv":
                return "uv"
            if text == u"quota 0\xb0c":
                return "zero_deg_level"
            if text == u"grandine":
                return "hail"
            return None

        for td_id, td in enumerate(datatable.cssselect('tr')[0]):
            ## We can have two kind of columns:
            ## <td>val1</td>
            ## <td><span>val1</span><span>val2</span></td>
            children = td.getchildren()
            if len(children) == 0:
                header_name = resolve_header_name(td.text_content())
                if header_name is not None:
                    header_fields[header_name] = (td_id,)
            else:
                for child_id, child in enumerate(children):
                    header_name = resolve_header_name(child.text_content())
                    header_fields[header_name] = (td_id, child_id)
            # print lxml.html.tostring(td)

        def get_field_container(row, field_name):
            field_path = header_fields.get(field_name)
            if field_path is None:
                return None
            _row = row
            for el_id in field_path:
                _row = _row[el_id]
            return _row

        for tr in datatable.cssselect('tr'):
            tr_id = tr.attrib.get('id')
            if tr_id is None:
                continue
            id_match = self.re_row_id.match(tr_id)
            if not id_match:
                continue

            data = {}

            ## Extract the datetime from the row id --------------------------------
            hour = int(id_match.group('hour')) % 24
            day = int(id_match.group('day'))
            if last_day is not None:
                if day < last_day:
                    current_month += 1
                    if current_month > 12:
                        current_year += 1
                        current_month = 1
            last_day = day
            full_date = datetime.datetime(current_year, current_month, day, hour)
            timestamp = int(time.mktime(full_date.timetuple()))

            data.update({
                "location": location,
                "timestamp": timestamp,
            })

            ## Extract hour --------------------------------------------------------
            ## ..and check data is coherent
            cell_hour = get_field_container(tr, 'hour')
            hour2 = int(re.match(
                r"[^0-9]*(?P<hour>[0-9]+)[^0-9]*",
                cell_hour.text_content()
            ).group('hour')) % 24
            assert hour == hour2

            ## Extract condition ---------------------------------------------------
            cell_condition = get_field_container(tr, 'condition')
            data['condition'] = clean_text(cell_condition.text_content())

            ## Extract temperature -------------------------------------------------
            cell_temperature = get_field_container(tr, 'temperature')
            data['temperature'] = get_first_float(cell_temperature.text_content())

            ## Extract wind --------------------------------------------------------
            ## This is quite complex, actually, as it might contain a lot of
            ## information...

            ## <td><span class="descri">calma</span></td>

            ## <td>
            ##      <acronym style="cursor:help" title="9.7 nodi">
            ##          E&#160;18
            ##      </acronym>
            ##      &#160;
            ##      <span class="descri">
            ##          /&#160;
            ##          <acronym style="cursor:help" title="Possibili raffiche fino a 17.3 nodi">
            ##              max&#160;32
            ##          </acronym>
            ##      </span>
            ##      <br>
            ##      <span class="descri">
            ##          moderato
            ##      </span>
            ## </td>

            ## <td>
            ##      <acronym style="cursor:help" title="9.7 nodi">
            ##          E&#160;18
            ##      </acronym>
            ##      <br>
            ##      <span class="descri">
            ##          moderato
            ##      </span>
            ## </td>

            cell_wind = get_field_container(tr, 'wind')

            if cell_wind[0].tag == 'acronym':
                ## We are in case #2 or #3

                ## Extract wind direction/speed ------------------------------------
                _match = re.match(
                    r'(?P<direction>[NEWS]+)\s+(?P<speed>[0-9]+)',
                    clean_text(cell_wind[0].text_content()))
                if _match:
                    data['wind_direction'] = _match.group('direction')
                    data['wind_speed_kmh'] = int(_match.group('speed'))

                ## Extract wind speed in nodes -------------------------------------
                _title = cell_wind[0].attrib.get('title', '')
                _match = re.match(r'(?P<speed>[0-9\.]+) nodei', _title)
                if _match:
                    data['wind_speed_nodes'] = float(_match.group('speed'))

                ## Extract wind max speed (if specified) ---------------------------
                cell_wind_description_id = 3

                cell_wind_max_speed = cell_wind[1]
                if cell_wind_max_speed.tag == 'br':
                    pass  # We don't have cell_wind_max_speed
                    cell_wind_description_id = 2

                else:
                    ## Extract max speed, in km/h ----------------------------------
                    _match = re.match(
                        r'max\s+(?P<speed>[0-9]+)',
                        clean_text(cell_wind_max_speed.text_content()))
                    if _match:
                        data['wind_max_speed_kmh'] = int(_match.group('speed'))

                    ## Extract max speed, in nodes ---------------------------------
                    _title = cell_wind[0].attrib.get('title', '')
                    _match = re.match(
                        r'Possibili raffiche fino a (?P<speed>[0-9\.]+) nodi',
                        _title)
                    if _match:
                        data['wind_max_speed_nodes'] = float(_match.group('speed'))

                ## Extract wind description ----------------------------------------
                cell_wind_description = cell_wind[cell_wind_description_id]
                data['wind_description'] = \
                    clean_text(cell_wind_description.text_content())

            else:
                ## We are in the case #1
                data.update({
                    'wind_direction': None,
                    'wind_speed_kmh': 0,
                    'wind_speed_nodes': 0,
                    'wind_max_speed_kmh': 0,
                    'wind_max_speed_nodes': 0,
                    'wind_description': clean_text(cell_wind[0].text_content()),
                })

            ## Extract precipitations ----------------------------------------------

            # <td class="pl5">
            #     0.1&#160;mm<br>
            #     <span class="descri">deboli</span>
            # </td>

            # <td class="pl5">
            #     <div class="precontainer">
            #         <div class="prectop" style="height:12px;"></div>
            #         <div class="precbottom" style="height:10px;background-color:#69DAEF;"></div>
            #     </div>
            #     0&#160;~&#160;0.5&#160;cm<br>
            #     <span class="descri">deboli</span>
            # </td>
            #
            # <td class="pl5">
            #     <span class="descri">isolate</span>
            # </td>

            # <td class="pl5">
            #     <acronym style="cursor:help" title="Attenzione! Pioggia che congela al suolo">
            #         <img src="http://www.ilmeteo.it/portale/misc/warning2.png" border="0" align="left" alt="allerta" title="Attenzione! Pioggia che congela al suolo">
            #     </acronym>
            #     <div class="precontainer">
            #         <div class="prectop" style="height:19px;"></div>
            #         <div class="precbottom" style="height:3px;background-color:#FFF064;"></div>
            #     </div>
            #     <span class="descri">isolate</span>
            # </td>

            # <td class="pl5">
            #     <acronym style="cursor:help" title="Attenzione! Pioggia che congela al suolo">
            #         <img src="http://www.ilmeteo.it/portale/misc/warning2.png" border="0" align="left" alt="allerta" title="Attenzione! Pioggia che congela al suolo">
            #     </acronym>
            #     <span class="descri">isolate</span>
            # </td>

            # <td class="pl5">
            #     <acronym style="cursor:help" title="Neve">
            #       <img src="http://www.ilmeteo.it/portale/meteo/img/w11.gif" border="0" align="middle" alt="neve" title="Neve">
            #     </acronym>
            #     <div class="precontainer">
            #         <div class="prectop" style="height:12px;"></div>
            #         <div class="precbottom" style="height:10px;background-color:#69DAEF;"></div>
            #     </div>
            #     0.4&#160;cm<br>
            #     <span class="descri">deboli</span>
            # </td>

            cell_precipitations = get_field_container(tr, 'precipitations')
            prec_text = clean_text(
                ' '.join(cell_precipitations.xpath('text()')).strip())
            prec_descri = clean_text(
                cell_precipitations.cssselect('.descri')[0].text
            ).strip('- ')
            prec_snow = False
            prec_alerts = []

            for el in cell_precipitations:
                el_title = el.attrib.get('title', None)
                if el_title is None:
                    continue
                el_title = clean_text(el_title)
                if el_title.startswith('Attenzione!'):
                    prec_alerts.append(el_title)
                elif el_title == 'Neve':
                    prec_snow = True

            data.update({
                'precipitations': prec_text,
                'precipitations_desc': prec_descri,
                'precipitations_snow': prec_snow,
                'precipitations_alerts': prec_alerts,
            })

            ## Extract wind_chill --------------------------------------------------
            cell_wind_chill = get_field_container(tr, 'wind_chill')
            data['wind_chill'] = get_first_float(cell_wind_chill.text_content())

            ## Extract perceived ---------------------------------------------------
            cell_perceived = get_field_container(tr, 'perceived')
            data['perceived'] = get_first_float(cell_perceived.text_content())

            ## Extract humidity ----------------------------------------------------
            cell_humidity = get_field_container(tr, 'humidity')
            data['humidity'] = get_first_int(cell_humidity.text_content())

            ## Extract pressure ----------------------------------------------------
            cell_pressure = get_field_container(tr, 'pressure')
            data['pressure'] = get_first_int(cell_pressure.text_content())

            ## Extract visibility --------------------------------------------------
            cell_visibility = get_field_container(tr, 'visibility')
            data['visibility'] = cell_visibility.text_content()

            ## Extract uv ----------------------------------------------------------
            cell_uv = get_field_container(tr, 'uv')
            data['uv'] = get_first_int(cell_uv.text_content())

            ## Extract zero_deg_level ----------------------------------------------

            # <span id="c4a-99873">950m</span>

            # <span id="c4a-99882">1760m<br>
            #   <span class="descri">neve&#160;a&#160;1320m</span>
            # </span>

            cell_zero_deg_level = get_field_container(tr, 'zero_deg_level')

            data['zero_deg_level'] = get_first_int(cell_zero_deg_level)

            # 710m neve a 60m
            cell_snow = cell_zero_deg_level.cssselect('.descri')
            if len(cell_snow) > 0:
                data['snow_limit'] = get_first_int(cell_snow[0])

            ## Extract hail --------------------------------------------------------
            cell_hail = get_field_container(tr, 'hail')
            data['hail'] = get_first_int(cell_hail.text_content())


            # try:
            #     wind1 = clean_text(tr[5][0].text_content())
            #     wind2 = clean_text(tr[5][1].text_content())
            #
            # except:
            #     wind_dir = None
            #     wind_speed = None
            #     wind_max_speed = None
            #
            # else:
            #     wind_dir, wind_speed = re_winddir_speed.match(wind1).groups()
            #     wind_speed = int(wind_speed)
            #     wind_max_speed = get_first_int(wind2)
            #
            # try:
            #     wind_type = clean_text(tr[5][3].text_content())
            # except:
            #     wind_type = None
            #
            # if clean_text(tr[6].text_content()).strip(' - ') == 'assenti':
            #     prec_mm = 0
            #     prec_type = None
            # else:
            #     prec_mm = get_first_float(clean_text(' '.join(tr[6].xpath('text()'))))
            #     prec_type = clean_text(tr[6].cssselect('.descri')[0].text)
            #
            #
            # pressure = get_first_int(tr[8].text_content())
            # visibility = tr[9][0].text
            # vis_desc = tr[9].cssselect('.descri')[0].text
            # vis_hdata = tr[9].cssselect('.hdata')[0].text
            # termic_zero_altitude = get_first_int(tr[10][0].text)
            # snow_limit = tr[10][0].cssselect('.descri')

            # if len(snow_limit) > 0:
            #     snow_limit = clean_text(snow_limit[0].text)
            ## ...etc...

            # data = {
            #     "location": location,
            #     "timestamp": timestamp,
            #     "condition": condition,
            #     "temperature": temperature,
            #     "wind_direction": wind_dir,
            #     "wind_speed": wind_speed,
            #     "wind_max_speed": wind_max_speed,
            #     "wind_force": wind_type,
            #     "prec_mm": prec_mm,
            #     "prec_type": prec_type,
            #     "pressure": pressure,
            #     "visibility": visibility,
            #     "visibility_desc": vis_desc,
            #     "visibility_hdata": vis_hdata,
            #     "termic_zero_altitude": termic_zero_altitude,
            # }

            sys.stderr.write("Done. {}, {}\n".format(location, full_date))
            yield data

    def list_regions(self):
        url = "http://www.ilmeteo.it/Italia"
        root = self._request_page(url)
        for td in root.cssselect('#mainc table td'):
            if td.text_content().strip().startswith('Meteo regioni italiane'):
                for a in td.cssselect('a'):
                    if a.attrib.get('title', '').startswith('Previsioni meteo'):
                        href = a.attrib['href']
                        yield self.location_from_url(href), href

    def list_cities(self, region=None, url=None):
        if url is None:
            if region is None:
                raise ValueError("You must specify either a region or an URL")
            url = self.url_region(region)

        datatable = self._get_datatable(url)
        for a in datatable.cssselect('tr td.f > a'):
            href = a.attrib['href']
            yield self.location_from_url(href), href

    def list_all_cities(self):
        for region, url in self.list_regions():
            for city, url in self.list_cities(region):
                yield city, url

    def run_spider(self, cities, days):
        ## Build a list of URLs to be spidered
        pages_to_spider = set()
        spidered_pages = set()
        for city in cities:
            for day in days:
                pages_to_spider.add((city, day))

        ## Keep trying until we spidered successfully all the URLs
        retry = 3
        while (retry > 0) and (pages_to_spider != spidered_pages):
            _pages_to_spider = pages_to_spider - spidered_pages
            for success, page in self._run_spider(_pages_to_spider):
                if success:
                    spidered_pages.add(page)
                self._log("Progress: {}/{}".format(
                    len(spidered_pages), len(pages_to_spider)))
            retry -= 1

        _pages_to_spider = pages_to_spider - spidered_pages
        if len(_pages_to_spider):
            self._log("Spidering failed for pages: {!r}"
                      "".format(_pages_to_spider))

    def _run_spider(self, urls):
        for location, day in urls:
            try:
                for item in self.spider_location(location, day_delta=day):
                    self._register_item(item)
            except KeyboardInterrupt:
                raise
            except:
                yield False, (location, day)
            else:
                yield True, (location, day)

    def _register_item(self, data):
        if self._callback:
            self._callback(data)


def run_spider(cities, days, on_scraperwiki=False, outfile=None):
    if on_scraperwiki:
        print >>sys.stderr, "Running in ScraperWiki mode"
        import scraperwiki
        def callback(item):
            scraperwiki.sqlite.save(
                unique_keys=['location','timestamp'], data=item)

    else:
        print >>sys.stderr, "Running in normal mode"
        import msgpack
        def callback(item):
            outfile.write(msgpack.packb(item))

    the_spider = IlMeteoSpider(
        callback=callback,
        on_scraperwiki=on_scraperwiki)

    if cities is True:
        cities = [c[0] for c in the_spider.list_all_cities()]

    print >>sys.stderr, "Will run spider for cities: {}".format(', '.join(cities))
    print >>sys.stderr, "Will run spider for days: {}".format(', '.join(map(str, days)))

    the_spider.run_spider(cities, days)


def main():
    parser = optparse.OptionParser()

    group = optparse.OptionGroup(parser, 'Actions')
    group.add_option('--list-regions', action='store_const',
                     const='list-regions', dest='action')
    group.add_option('--list-cities', action='store_const',
                     const='list-cities', dest='action')
    group.add_option('--run-spider', action='store_const',
                     const='run-spider', dest='action')
    parser.add_option_group(group)

    group = optparse.OptionGroup(parser, 'Output control')
    group.add_option('-o', '--output', action='store', dest='output_file')
    parser.add_option_group(group)

    parser.add_option('--region', action='append', dest='regions')
    parser.add_option('--city', action='append', dest='cities')
    parser.add_option('--day', action='append', dest='days')

    opts, args = parser.parse_args()

    if opts.action is None:
        raise ValueError("You must specify one action. See --help.")

    if opts.action == 'list-regions':
        for region, url in IlMeteoSpider().list_regions():
            print region

    elif opts.action == 'list-cities':
        if not opts.regions:
            raise ValueError("You must specify at least a region name")
        for region in opts.regions:
            print region
            for city, url in IlMeteoSpider().list_cities(region):
                print "    {}".format(city)
            print ""

    elif opts.action == 'run-spider':
        ## Run the spider for all the selected region(s) and city (cities)

        if opts.output_file is None:
            raise ValueError("You must specify an output file!")

        the_spider = IlMeteoSpider()

        if not opts.regions and not opts.cities:
            selected_cities = True

        else:
            selected_cities = set()

            if opts.regions:
                for region in opts.regions:
                    for city, url in the_spider.list_cities(region):
                        selected_cities.add(city)

            if opts.cities:
                for city in opts.cities:
                    selected_cities.add(city)

            selected_cities = sorted(list(selected_cities))

        if opts.days:
            days = [int(x.strip()) for x in opts.days.split(',')]
        else:
            days = range(7)

        with open(opts.output_file, 'w') as outfile:
            run_spider(selected_cities, days, outfile=outfile)


if __name__ == '__main__':
    main()

elif __name__ == 'scraper':
    run_spider(True, range(7), on_scraperwiki=True)
"""
Scraper for ilmeteo.it
"""

import datetime
import optparse
import re
import sys
import time
import traceback
import urllib2

import lxml.html


## Utility functions ===========================================================

re_first_int = re.compile(r"[^0-9\-]*(-?[0-9]+)")
re_first_float = re.compile(r"[^0-9\.\-]*(-?[0-9\.]+)")


def clean_text(text):
    return text.replace(u"\xa0", u" ").strip()


def get_first_float(text):
    try:
        return float(re_first_float.match(text).group(1))
    except:
        return None


def get_first_int(text):
    try:
        return int(re_first_int.match(text).group(1))
    except:
        return None


## The Scraper =================================================================

class IlMeteoSpider(object):
    """Spider for www.ilmeteo.it"""

    re_row_id = re.compile(r"^h(?P<hour>[0-9]+)-(?P<day>[0-9]+)-1$")

    def __init__(self, callback=None, on_scraperwiki=False):
        self.on_scraperwiki = on_scraperwiki
        self._callback = callback

    def _log(self, message):
        sys.stderr.write(">>> {}\n".format(message))

    def _request_page(self, url, retry=3):
        self._log("Request: {}".format(url))
        try:
            if self.on_scraperwiki:
                import scraperwiki
                page = scraperwiki.scrape(url)

            else:
                import requests
                page = requests.get(url).content

            return lxml.html.fromstring(page)
        except KeyboardInterrupt:
            raise
        except:  # Anything might happen up there.. doesn't matter.
            self._log("Request failed.")
            traceback.print_exc()
            if retry > 0:
                time.sleep(2)
                return self._request_page(url, retry - 1)
            else:
                raise

    def location_from_url(self, url):
        location = filter(None, url.split('/'))[-1]
        location = urllib2.unquote(location)
        location = location.replace('+', ' ')
        return location

    def url_start(self):
        return "http://www.ilmeteo.it/Italia"

    def url_region(self, name):
        name = urllib2.quote(name)
        return "http://www.ilmeteo.it/{}".format(name)

    def url_city(self, name):
        name = urllib2.quote(name)
        return "http://www.ilmeteo.it/meteo/{}".format(name)

    def _get_datatable_from_url(self, url):
        root = self._request_page(url)
        datatable = root.cssselect('.datatable')

        if len(datatable) < 1:

            the_frame = root.cssselect('#frmprevi')
            if len(the_frame):
                the_frame = the_frame[0]
                real_url = the_frame.attrib['src']
                root = self._request_page(real_url)
                datatable = root.cssselect('.datatable')

            else:
                raise Exception(
                    "Unable to find .datatable or #frmprevi in the page!")

        return datatable[0]

    def _get_datatable(self, url, retry=3):
        try:
            return self._get_datatable_from_url(url)
        except KeyboardInterrupt:
            raise
        except:
            self._log("Request failed.")
            traceback.print_exc()
            if retry > 0:
                time.sleep(2)
                return self._get_datatable(url, retry - 1)
            else:
                raise

    def spider_location(self, location=None, url=None, day_delta=0):

        if location is None:
            if url is None:
                raise ValueError("You must specify either a location or an URL")
            location = filter(None, url.split('/'))[-1]
            url = "{}/?g={}".format(url, day_delta)

        else:
            url = "{}/?g={}".format(self.url_city(location), day_delta)

        datatable = self._get_datatable(url)

        return self._extract_weather_data(location, datatable, day_delta)

    def _extract_weather_data(self, location, datatable, day_delta):

        now = datetime.datetime.now() + datetime.timedelta(days=day_delta)
        current_month = now.month
        current_year = now.year
        last_day = None

        ## First of all, determine the field positions...
        header_fields = {}

        def resolve_header_name(text):
            text = clean_text(text).strip().lower()
            if text == u"ora":
                return "hour"
            if text == u"tempo":
                return "condition"
            if text == u"t (\xb0c)":
                return "temperature"
            if text == u'vento (km/h)':
                return "wind"
            if text == u"precipitazioni":
                return "precipitations"
            if text == u"w.chill":
                return "wind_chill"
            if text == u"percepita":
                return "perceived"
            if text == u"umidit\xe0":
                return "humidity"
            if text == u"pressione":
                return "pressure"
            if text == u"visibilit\xe0":
                return "visibility"
            if text == u"uv":
                return "uv"
            if text == u"quota 0\xb0c":
                return "zero_deg_level"
            if text == u"grandine":
                return "hail"
            return None

        for td_id, td in enumerate(datatable.cssselect('tr')[0]):
            ## We can have two kind of columns:
            ## <td>val1</td>
            ## <td><span>val1</span><span>val2</span></td>
            children = td.getchildren()
            if len(children) == 0:
                header_name = resolve_header_name(td.text_content())
                if header_name is not None:
                    header_fields[header_name] = (td_id,)
            else:
                for child_id, child in enumerate(children):
                    header_name = resolve_header_name(child.text_content())
                    header_fields[header_name] = (td_id, child_id)
            # print lxml.html.tostring(td)

        def get_field_container(row, field_name):
            field_path = header_fields.get(field_name)
            if field_path is None:
                return None
            _row = row
            for el_id in field_path:
                _row = _row[el_id]
            return _row

        for tr in datatable.cssselect('tr'):
            tr_id = tr.attrib.get('id')
            if tr_id is None:
                continue
            id_match = self.re_row_id.match(tr_id)
            if not id_match:
                continue

            data = {}

            ## Extract the datetime from the row id --------------------------------
            hour = int(id_match.group('hour')) % 24
            day = int(id_match.group('day'))
            if last_day is not None:
                if day < last_day:
                    current_month += 1
                    if current_month > 12:
                        current_year += 1
                        current_month = 1
            last_day = day
            full_date = datetime.datetime(current_year, current_month, day, hour)
            timestamp = int(time.mktime(full_date.timetuple()))

            data.update({
                "location": location,
                "timestamp": timestamp,
            })

            ## Extract hour --------------------------------------------------------
            ## ..and check data is coherent
            cell_hour = get_field_container(tr, 'hour')
            hour2 = int(re.match(
                r"[^0-9]*(?P<hour>[0-9]+)[^0-9]*",
                cell_hour.text_content()
            ).group('hour')) % 24
            assert hour == hour2

            ## Extract condition ---------------------------------------------------
            cell_condition = get_field_container(tr, 'condition')
            data['condition'] = clean_text(cell_condition.text_content())

            ## Extract temperature -------------------------------------------------
            cell_temperature = get_field_container(tr, 'temperature')
            data['temperature'] = get_first_float(cell_temperature.text_content())

            ## Extract wind --------------------------------------------------------
            ## This is quite complex, actually, as it might contain a lot of
            ## information...

            ## <td><span class="descri">calma</span></td>

            ## <td>
            ##      <acronym style="cursor:help" title="9.7 nodi">
            ##          E&#160;18
            ##      </acronym>
            ##      &#160;
            ##      <span class="descri">
            ##          /&#160;
            ##          <acronym style="cursor:help" title="Possibili raffiche fino a 17.3 nodi">
            ##              max&#160;32
            ##          </acronym>
            ##      </span>
            ##      <br>
            ##      <span class="descri">
            ##          moderato
            ##      </span>
            ## </td>

            ## <td>
            ##      <acronym style="cursor:help" title="9.7 nodi">
            ##          E&#160;18
            ##      </acronym>
            ##      <br>
            ##      <span class="descri">
            ##          moderato
            ##      </span>
            ## </td>

            cell_wind = get_field_container(tr, 'wind')

            if cell_wind[0].tag == 'acronym':
                ## We are in case #2 or #3

                ## Extract wind direction/speed ------------------------------------
                _match = re.match(
                    r'(?P<direction>[NEWS]+)\s+(?P<speed>[0-9]+)',
                    clean_text(cell_wind[0].text_content()))
                if _match:
                    data['wind_direction'] = _match.group('direction')
                    data['wind_speed_kmh'] = int(_match.group('speed'))

                ## Extract wind speed in nodes -------------------------------------
                _title = cell_wind[0].attrib.get('title', '')
                _match = re.match(r'(?P<speed>[0-9\.]+) nodei', _title)
                if _match:
                    data['wind_speed_nodes'] = float(_match.group('speed'))

                ## Extract wind max speed (if specified) ---------------------------
                cell_wind_description_id = 3

                cell_wind_max_speed = cell_wind[1]
                if cell_wind_max_speed.tag == 'br':
                    pass  # We don't have cell_wind_max_speed
                    cell_wind_description_id = 2

                else:
                    ## Extract max speed, in km/h ----------------------------------
                    _match = re.match(
                        r'max\s+(?P<speed>[0-9]+)',
                        clean_text(cell_wind_max_speed.text_content()))
                    if _match:
                        data['wind_max_speed_kmh'] = int(_match.group('speed'))

                    ## Extract max speed, in nodes ---------------------------------
                    _title = cell_wind[0].attrib.get('title', '')
                    _match = re.match(
                        r'Possibili raffiche fino a (?P<speed>[0-9\.]+) nodi',
                        _title)
                    if _match:
                        data['wind_max_speed_nodes'] = float(_match.group('speed'))

                ## Extract wind description ----------------------------------------
                cell_wind_description = cell_wind[cell_wind_description_id]
                data['wind_description'] = \
                    clean_text(cell_wind_description.text_content())

            else:
                ## We are in the case #1
                data.update({
                    'wind_direction': None,
                    'wind_speed_kmh': 0,
                    'wind_speed_nodes': 0,
                    'wind_max_speed_kmh': 0,
                    'wind_max_speed_nodes': 0,
                    'wind_description': clean_text(cell_wind[0].text_content()),
                })

            ## Extract precipitations ----------------------------------------------

            # <td class="pl5">
            #     0.1&#160;mm<br>
            #     <span class="descri">deboli</span>
            # </td>

            # <td class="pl5">
            #     <div class="precontainer">
            #         <div class="prectop" style="height:12px;"></div>
            #         <div class="precbottom" style="height:10px;background-color:#69DAEF;"></div>
            #     </div>
            #     0&#160;~&#160;0.5&#160;cm<br>
            #     <span class="descri">deboli</span>
            # </td>
            #
            # <td class="pl5">
            #     <span class="descri">isolate</span>
            # </td>

            # <td class="pl5">
            #     <acronym style="cursor:help" title="Attenzione! Pioggia che congela al suolo">
            #         <img src="http://www.ilmeteo.it/portale/misc/warning2.png" border="0" align="left" alt="allerta" title="Attenzione! Pioggia che congela al suolo">
            #     </acronym>
            #     <div class="precontainer">
            #         <div class="prectop" style="height:19px;"></div>
            #         <div class="precbottom" style="height:3px;background-color:#FFF064;"></div>
            #     </div>
            #     <span class="descri">isolate</span>
            # </td>

            # <td class="pl5">
            #     <acronym style="cursor:help" title="Attenzione! Pioggia che congela al suolo">
            #         <img src="http://www.ilmeteo.it/portale/misc/warning2.png" border="0" align="left" alt="allerta" title="Attenzione! Pioggia che congela al suolo">
            #     </acronym>
            #     <span class="descri">isolate</span>
            # </td>

            # <td class="pl5">
            #     <acronym style="cursor:help" title="Neve">
            #       <img src="http://www.ilmeteo.it/portale/meteo/img/w11.gif" border="0" align="middle" alt="neve" title="Neve">
            #     </acronym>
            #     <div class="precontainer">
            #         <div class="prectop" style="height:12px;"></div>
            #         <div class="precbottom" style="height:10px;background-color:#69DAEF;"></div>
            #     </div>
            #     0.4&#160;cm<br>
            #     <span class="descri">deboli</span>
            # </td>

            cell_precipitations = get_field_container(tr, 'precipitations')
            prec_text = clean_text(
                ' '.join(cell_precipitations.xpath('text()')).strip())
            prec_descri = clean_text(
                cell_precipitations.cssselect('.descri')[0].text
            ).strip('- ')
            prec_snow = False
            prec_alerts = []

            for el in cell_precipitations:
                el_title = el.attrib.get('title', None)
                if el_title is None:
                    continue
                el_title = clean_text(el_title)
                if el_title.startswith('Attenzione!'):
                    prec_alerts.append(el_title)
                elif el_title == 'Neve':
                    prec_snow = True

            data.update({
                'precipitations': prec_text,
                'precipitations_desc': prec_descri,
                'precipitations_snow': prec_snow,
                'precipitations_alerts': prec_alerts,
            })

            ## Extract wind_chill --------------------------------------------------
            cell_wind_chill = get_field_container(tr, 'wind_chill')
            data['wind_chill'] = get_first_float(cell_wind_chill.text_content())

            ## Extract perceived ---------------------------------------------------
            cell_perceived = get_field_container(tr, 'perceived')
            data['perceived'] = get_first_float(cell_perceived.text_content())

            ## Extract humidity ----------------------------------------------------
            cell_humidity = get_field_container(tr, 'humidity')
            data['humidity'] = get_first_int(cell_humidity.text_content())

            ## Extract pressure ----------------------------------------------------
            cell_pressure = get_field_container(tr, 'pressure')
            data['pressure'] = get_first_int(cell_pressure.text_content())

            ## Extract visibility --------------------------------------------------
            cell_visibility = get_field_container(tr, 'visibility')
            data['visibility'] = cell_visibility.text_content()

            ## Extract uv ----------------------------------------------------------
            cell_uv = get_field_container(tr, 'uv')
            data['uv'] = get_first_int(cell_uv.text_content())

            ## Extract zero_deg_level ----------------------------------------------

            # <span id="c4a-99873">950m</span>

            # <span id="c4a-99882">1760m<br>
            #   <span class="descri">neve&#160;a&#160;1320m</span>
            # </span>

            cell_zero_deg_level = get_field_container(tr, 'zero_deg_level')

            data['zero_deg_level'] = get_first_int(cell_zero_deg_level)

            # 710m neve a 60m
            cell_snow = cell_zero_deg_level.cssselect('.descri')
            if len(cell_snow) > 0:
                data['snow_limit'] = get_first_int(cell_snow[0])

            ## Extract hail --------------------------------------------------------
            cell_hail = get_field_container(tr, 'hail')
            data['hail'] = get_first_int(cell_hail.text_content())


            # try:
            #     wind1 = clean_text(tr[5][0].text_content())
            #     wind2 = clean_text(tr[5][1].text_content())
            #
            # except:
            #     wind_dir = None
            #     wind_speed = None
            #     wind_max_speed = None
            #
            # else:
            #     wind_dir, wind_speed = re_winddir_speed.match(wind1).groups()
            #     wind_speed = int(wind_speed)
            #     wind_max_speed = get_first_int(wind2)
            #
            # try:
            #     wind_type = clean_text(tr[5][3].text_content())
            # except:
            #     wind_type = None
            #
            # if clean_text(tr[6].text_content()).strip(' - ') == 'assenti':
            #     prec_mm = 0
            #     prec_type = None
            # else:
            #     prec_mm = get_first_float(clean_text(' '.join(tr[6].xpath('text()'))))
            #     prec_type = clean_text(tr[6].cssselect('.descri')[0].text)
            #
            #
            # pressure = get_first_int(tr[8].text_content())
            # visibility = tr[9][0].text
            # vis_desc = tr[9].cssselect('.descri')[0].text
            # vis_hdata = tr[9].cssselect('.hdata')[0].text
            # termic_zero_altitude = get_first_int(tr[10][0].text)
            # snow_limit = tr[10][0].cssselect('.descri')

            # if len(snow_limit) > 0:
            #     snow_limit = clean_text(snow_limit[0].text)
            ## ...etc...

            # data = {
            #     "location": location,
            #     "timestamp": timestamp,
            #     "condition": condition,
            #     "temperature": temperature,
            #     "wind_direction": wind_dir,
            #     "wind_speed": wind_speed,
            #     "wind_max_speed": wind_max_speed,
            #     "wind_force": wind_type,
            #     "prec_mm": prec_mm,
            #     "prec_type": prec_type,
            #     "pressure": pressure,
            #     "visibility": visibility,
            #     "visibility_desc": vis_desc,
            #     "visibility_hdata": vis_hdata,
            #     "termic_zero_altitude": termic_zero_altitude,
            # }

            sys.stderr.write("Done. {}, {}\n".format(location, full_date))
            yield data

    def list_regions(self):
        url = "http://www.ilmeteo.it/Italia"
        root = self._request_page(url)
        for td in root.cssselect('#mainc table td'):
            if td.text_content().strip().startswith('Meteo regioni italiane'):
                for a in td.cssselect('a'):
                    if a.attrib.get('title', '').startswith('Previsioni meteo'):
                        href = a.attrib['href']
                        yield self.location_from_url(href), href

    def list_cities(self, region=None, url=None):
        if url is None:
            if region is None:
                raise ValueError("You must specify either a region or an URL")
            url = self.url_region(region)

        datatable = self._get_datatable(url)
        for a in datatable.cssselect('tr td.f > a'):
            href = a.attrib['href']
            yield self.location_from_url(href), href

    def list_all_cities(self):
        for region, url in self.list_regions():
            for city, url in self.list_cities(region):
                yield city, url

    def run_spider(self, cities, days):
        ## Build a list of URLs to be spidered
        pages_to_spider = set()
        spidered_pages = set()
        for city in cities:
            for day in days:
                pages_to_spider.add((city, day))

        ## Keep trying until we spidered successfully all the URLs
        retry = 3
        while (retry > 0) and (pages_to_spider != spidered_pages):
            _pages_to_spider = pages_to_spider - spidered_pages
            for success, page in self._run_spider(_pages_to_spider):
                if success:
                    spidered_pages.add(page)
                self._log("Progress: {}/{}".format(
                    len(spidered_pages), len(pages_to_spider)))
            retry -= 1

        _pages_to_spider = pages_to_spider - spidered_pages
        if len(_pages_to_spider):
            self._log("Spidering failed for pages: {!r}"
                      "".format(_pages_to_spider))

    def _run_spider(self, urls):
        for location, day in urls:
            try:
                for item in self.spider_location(location, day_delta=day):
                    self._register_item(item)
            except KeyboardInterrupt:
                raise
            except:
                yield False, (location, day)
            else:
                yield True, (location, day)

    def _register_item(self, data):
        if self._callback:
            self._callback(data)


def run_spider(cities, days, on_scraperwiki=False, outfile=None):
    if on_scraperwiki:
        print >>sys.stderr, "Running in ScraperWiki mode"
        import scraperwiki
        def callback(item):
            scraperwiki.sqlite.save(
                unique_keys=['location','timestamp'], data=item)

    else:
        print >>sys.stderr, "Running in normal mode"
        import msgpack
        def callback(item):
            outfile.write(msgpack.packb(item))

    the_spider = IlMeteoSpider(
        callback=callback,
        on_scraperwiki=on_scraperwiki)

    if cities is True:
        cities = [c[0] for c in the_spider.list_all_cities()]

    print >>sys.stderr, "Will run spider for cities: {}".format(', '.join(cities))
    print >>sys.stderr, "Will run spider for days: {}".format(', '.join(map(str, days)))

    the_spider.run_spider(cities, days)


def main():
    parser = optparse.OptionParser()

    group = optparse.OptionGroup(parser, 'Actions')
    group.add_option('--list-regions', action='store_const',
                     const='list-regions', dest='action')
    group.add_option('--list-cities', action='store_const',
                     const='list-cities', dest='action')
    group.add_option('--run-spider', action='store_const',
                     const='run-spider', dest='action')
    parser.add_option_group(group)

    group = optparse.OptionGroup(parser, 'Output control')
    group.add_option('-o', '--output', action='store', dest='output_file')
    parser.add_option_group(group)

    parser.add_option('--region', action='append', dest='regions')
    parser.add_option('--city', action='append', dest='cities')
    parser.add_option('--day', action='append', dest='days')

    opts, args = parser.parse_args()

    if opts.action is None:
        raise ValueError("You must specify one action. See --help.")

    if opts.action == 'list-regions':
        for region, url in IlMeteoSpider().list_regions():
            print region

    elif opts.action == 'list-cities':
        if not opts.regions:
            raise ValueError("You must specify at least a region name")
        for region in opts.regions:
            print region
            for city, url in IlMeteoSpider().list_cities(region):
                print "    {}".format(city)
            print ""

    elif opts.action == 'run-spider':
        ## Run the spider for all the selected region(s) and city (cities)

        if opts.output_file is None:
            raise ValueError("You must specify an output file!")

        the_spider = IlMeteoSpider()

        if not opts.regions and not opts.cities:
            selected_cities = True

        else:
            selected_cities = set()

            if opts.regions:
                for region in opts.regions:
                    for city, url in the_spider.list_cities(region):
                        selected_cities.add(city)

            if opts.cities:
                for city in opts.cities:
                    selected_cities.add(city)

            selected_cities = sorted(list(selected_cities))

        if opts.days:
            days = [int(x.strip()) for x in opts.days.split(',')]
        else:
            days = range(7)

        with open(opts.output_file, 'w') as outfile:
            run_spider(selected_cities, days, outfile=outfile)


if __name__ == '__main__':
    main()

elif __name__ == 'scraper':
    run_spider(True, range(7), on_scraperwiki=True)
