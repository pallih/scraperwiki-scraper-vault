import scraperwiki
import mechanize
import re, csv, urllib, urllib2, warnings
import urlparse
from scraperwiki import datastore
import datetime

reDM = re.compile ("([0-9]{1,2})\s([A-Za-z]{4,6})")
months = [[ 'July', '7' ], [ 'August', '8' ]]

def SelfScrapeSW(scraper):
    url = "http://scraperwiki.com/scrapers/export/%s/" % scraper
    s = urllib.urlopen(url)
    c = csv.reader(s.readlines())
    headers = c.next()
    #print headers
    return [ dict(zip(headers, row)) for row in c ]

class Data(object):
    def __init__(self, data):
        if type(self) == Data:
            raise AbstractClassException('This is an abstract class')
        self.data = data

    @classmethod
    def float_scale_value(cls, value, range):
        lower, upper = range
        assert upper > lower
        scaled = (value - lower) * (float(cls.max_value) / (upper - lower))
        return scaled

    @classmethod
    def clip_value(cls, value):
        return max(0, min(value, cls.max_value))

    @classmethod
    def int_scale_value(cls, value, range):
        return int(round(cls.float_scale_value(value, range)))

    @classmethod
    def scale_value(cls, value, range):
        scaled = cls.int_scale_value(value, range)
        clipped = cls.clip_value(scaled)
        Data.check_clip(scaled, clipped)
        return clipped

    @staticmethod
    def check_clip(scaled, clipped):
        if clipped != scaled:
            warnings.warn('One or more of of your data points has been '
                'clipped because it is out of range.')


class ExtendedData(Data):
    max_value = 4095
    enc_map = \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.'

    def __repr__(self):
        encoded_data = []
        enc_size = len(ExtendedData.enc_map)
        for data in self.data:
            sub_data = []
            for value in data:
                if value is None:
                    sub_data.append('__')
                elif 0 <= value <= self.max_value:
                    first, second = divmod(int(value), enc_size)
                    sub_data.append('%s%s' % (
                        ExtendedData.enc_map[first],
                        ExtendedData.enc_map[second]))
                else:
                    raise DataOutOfRangeException( \
                        'Item #%i "%s" is out of range' % (data.index(value), \
                        value))
            encoded_data.append(''.join(sub_data))
        return 'chd=e:' + ','.join(encoded_data)

class Axis(object):
    BOTTOM = 'x'
    TOP = 't'
    LEFT = 'y'
    RIGHT = 'r'
    TYPES = (BOTTOM, TOP, LEFT, RIGHT)

    def __init__(self, axis_index, axis_type, **kw):
        assert axis_type in Axis.TYPES
        self.has_style = False
        self.axis_index = axis_index
        self.axis_type = axis_type
        self.positions = None

    def set_index(self, axis_index):
        self.axis_index = axis_index

    def set_positions(self, positions):
        self.positions = positions

    def set_style(self, colour, font_size=None, alignment=None):
        _check_colour(colour)
        self.colour = colour
        self.font_size = font_size
        self.alignment = alignment
        self.has_style = True

    def style_to_url(self):
        bits = []
        bits.append(str(self.axis_index))
        bits.append(self.colour)
        if self.font_size is not None:
            bits.append(str(self.font_size))
            if self.alignment is not None:
                bits.append(str(self.alignment))
        return ','.join(bits)

    def positions_to_url(self):
        bits = [str(self.axis_index)] + [str(a) for a in self.positions]
        return ','.join(bits)
        
class LabelAxis(Axis):
    def __init__(self, axis_index, axis_type, values, **kwargs):
        Axis.__init__(self, axis_index, axis_type, **kwargs)
        self.values = [str(a) for a in values]

    def __repr__(self):
        return '%i:|%s' % (self.axis_index, '|'.join(self.values))
        
class RangeAxis(Axis):
    def __init__(self, axis_index, axis_type, low, high, **kwargs):
        Axis.__init__(self, axis_index, axis_type, **kwargs)
        self.low = low
        self.high = high

    def __repr__(self):
        return '%i,%s,%s' % (self.axis_index, self.low, self.high)

class Chart(object):
    base_url = "http://chart.apis.google.com/chart?"

    def __init__(self, width, height, legend=None, auto_scale=True, x_range=None, y_range=None):
        assert(isinstance(width, int))
        assert(isinstance(height, int))
        self.data = []
        self.width = width
        self.height = height
        self.set_legend(legend)
        self.axis = []
        self.auto_scale = auto_scale
        self.x_range = x_range
        self.y_range = y_range

    def get_url(self, data_class=None):
        url_bits = self.get_url_bits(data_class=data_class)
        return self.base_url + '&'.join(url_bits)

    def get_url_bits(self, data_class=None):
        url_bits = []
        # Chart type
        url_bits.append(self.type_to_url())
        # Chart size
        url_bits.append('chs=%ix%i' % (self.width, self.height))
        # Chart data
        url_bits.append(self.data_to_url(data_class=data_class))
        # Chart legend
        if self.legend:
            url_bits.append('chdl=%s' % '|'.join(self.legend))
        # Chart axis
        ret = self.axis_to_url()
        if ret:
            url_bits.append(ret) 
        return url_bits
     
    def set_legend(self, legend):
        assert isinstance(legend, (list, tuple)) or legend is None
        if legend:
            self.legend = [urllib.quote(a) for a in legend]
        else:
            self.legend = None
        
    def scaled_data(self, data_class, x_range=None, y_range=None):
        self.scaled_data_class = data_class

        if x_range is None:
            x_range = self.data_x_range()
            if x_range and x_range[0] > 0:
                x_range = (x_range[0], x_range[1])
        self.scaled_x_range = x_range

        if y_range is None:
            y_range = self.data_y_range()
            if y_range and y_range[0] > 0:
                y_range = (y_range[0], y_range[1])
        self.scaled_y_range = y_range

        scaled_data = []
        for type, dataset in self.annotated_data():
            if type == 'y':
                scale_range = y_range
            elif type == 'marker-size':
                scale_range = (0, max(dataset))
            scaled_dataset = []
            for v in dataset:
                if v is None:
                    scaled_dataset.append(None)
                else:
                    scaled_dataset.append(
                        data_class.scale_value(v, scale_range))
            scaled_data.append(scaled_dataset)
        return scaled_data
        
    def _filter_none(self, data):
        return [r for r in data if r is not None]
        
    def data_x_range(self):
        try:
            lower = min(min(self._filter_none(s))
                        for type, s in self.annotated_data()
                        if type == 'x')
            upper = max(max(self._filter_none(s))
                        for type, s in self.annotated_data()
                        if type == 'x')
            return (lower, upper)
        except ValueError:
            return None

    def data_y_range(self):
        try:
            lower = min(min(self._filter_none(s))
                        for type, s in self.annotated_data()
                        if type == 'y')
            upper = max(max(self._filter_none(s)) + 1
                        for type, s in self.annotated_data()
                        if type == 'y')
            return (lower, upper)
        except ValueError:
            return None
        
    def add_data(self, data):
        self.data.append(data)
        return len(self.data) - 1
    
    def data_class_detection(self, data):
        assert isinstance(data, (list, tuple))
        if not isinstance(self, BarChart) or self.height < 100:
            return SimpleData
        else:
            return ExtendedData
        
    def data_to_url(self, data_class=None):
        if not data_class:
            data_class = self.data_class_detection(self.data)
        if not issubclass(data_class, Data):
            raise UnknownDataTypeException()
        if self.auto_scale:
            data = self.scaled_data(data_class, self.x_range, self.y_range)
        else:
            data = self.data
        return repr(data_class(data))
    
    def set_axis_labels(self, axis_type, values):
        assert axis_type in Axis.TYPES
        values = [urllib.quote(str(a)) for a in values]
        axis_index = len(self.axis)
        axis = LabelAxis(axis_index, axis_type, values)
        self.axis.append(axis)
        return axis_index
    
    def axis_to_url(self):
        available_axis = []
        label_axis = []
        range_axis = []
        positions = []
        styles = []
        for axis in self.axis:
            available_axis.append(axis.axis_type)
            if isinstance(axis, RangeAxis):
                range_axis.append(repr(axis))
            if isinstance(axis, LabelAxis):
                label_axis.append(repr(axis))
            if axis.positions:
                positions.append(axis.positions_to_url())
            if axis.has_style:
                styles.append(axis.style_to_url())
        if not available_axis:
            return
        url_bits = []
        url_bits.append('chxt=%s' % ','.join(available_axis))
        if label_axis:
            url_bits.append('chxl=%s' % '|'.join(label_axis))
        if range_axis:
            url_bits.append('chxr=%s' % '|'.join(range_axis))
        if positions:
            url_bits.append('chxp=%s' % '|'.join(positions))
        if styles:
            url_bits.append('chxs=%s' % '|'.join(styles))
        return '&'.join(url_bits)

class BarChart(Chart):
    def __init__(self, *args, **kwargs):
        if type(self) == BarChart:
            raise AbstractClassException('This is an abstract class')
        Chart.__init__(self, *args, **kwargs)
        self.bar_width = None
        self.zero_lines = {}

    def set_bar_width(self, bar_width):
        self.bar_width = bar_width

    def set_zero_line(self, index, zero_line):
        self.zero_lines[index] = zero_line

    def get_url_bits(self, data_class=None, skip_chbh=False):
        url_bits = Chart.get_url_bits(self, data_class=data_class)
        if not skip_chbh and self.bar_width is not None:
            url_bits.append('chbh=%i' % self.bar_width)
        zero_line = []
        if self.zero_lines:
            for index in xrange(max(self.zero_lines) + 1):
                if index in self.zero_lines:
                    zero_line.append(str(self.zero_lines[index]))
                else:
                    zero_line.append('0')
            url_bits.append('chp=%s' % ','.join(zero_line))
        return url_bits

class StackedVerticalBarChart(BarChart):
    def type_to_url(self):
        return 'cht=bvs'

    def annotated_data(self):
        for dataset in self.data:
            yield ('y', dataset)

def Main():
    oe = SelfScrapeSW("olympic-2012-events")
    data = []
    date = []
    for day in xrange(24, 45):
        day = str(datetime.date(2010, 07, 01) + datetime.timedelta(day))
        #x = [int(sport.get("gold") or "0")  for sport in oe  if sport.get("startdate") <= day <= sport.get("finishdate")]
        x = [int(sport.get("athletes") or "0")  for sport in oe  if sport.get("startdate") <= day <= sport.get("finishdate")]
        data.append(sum(x))
        date.append(day)
    chart = StackedVerticalBarChart(700, 425, y_range=(0, 7000))
    chart.set_legend(['ATHLETES'])
    axis_index = chart.set_axis_labels(Axis.LEFT, ['0', '1000', '2000', '3000', '4000', '5000', '6000', '7000'])
    axis_index = chart.set_axis_labels(Axis.BOTTOM, date)
    axis_index = chart.set_axis_labels(Axis.TOP, data)
    chart.add_data(data)
    chart_url = chart.get_url()
    print chart_url

Main()






def convertMonth(name):
    for month in months:
        if name.upper() == month[0].upper():
            return int(month[1])

def convertDate(value):
    m = reDM.match(value)
    if m:
        return '2010-%02d-%02d' % (convertMonth(m.group(2)), int(m.group(1)))
    else:
        return value

#def Main():
    url = "http://www.london2012.com/games/olympic-sports/"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    base = br.open(url)
    page = base.read()
    area = re.findall('(?si)<span class="selected">Olympic sports</span><ul>(.*?)</ul>', page)
    events = re.findall('(?si)<li>(.*?)</li>', area[0])
    for event in events:
        data = {}
        sport = re.findall('(?si)<a href=".*?">(.*?)\s\-\s.*?</a>', event)
        if sport:
            data["sport"] = sport[0]
        else:
            sport = re.findall('(?si)<a href=".*?">(.*?)</a>', event)
            if sport:
                sport = sport[0].replace("Canoe Slalom", "Canoe").replace("Canoe Sprint", "Canoe")
                data["sport"] = sport
        category = re.findall('(?si)<a href=".*?">\w*?\s\-\s(.*?)</a>', event)
        if category:
            data["category"] = category[0]
        else:
            category = re.findall('(?si)<a href=".*?">Canoe (.*?)</a>', event)
            if category:
                data["category"] = category[0]
        link = re.findall('(?si)<a href="(.*?)">.*?</a>', event)
        details = br.follow_link(url_regex=link[0])
        getDetails(details.read(), data)
        br.back()
        link = urlparse.urljoin("http://www.london2012.com/", link[0])
        data["link"] = link
        datastore.save(unique_keys=['sport', 'link'], data=data)
        print data
        print "--------------------------------------------------------------------"

def getDetails(details, data):
    all = re.findall('(?si)(.*)', details)
    venue = re.findall('(?si)<strong>Venue\w*?:\s*</strong>(.*?)<.*?>', details)
    if venue:
        venuelist = re.findall('(?si)(.+?),\s(.+?),\s(.+?),\s(.+?)\sand\s(.+)', venue[0])
        if venuelist:
            data["venue"] = repr(venuelist)
        else:
            venue = venue[0].replace("\xc2\xa0", "")
            data["venue"] = SimplifyHTML(venue)
    else:
        venue = re.findall('(?si)<.*?>Venue</.*?>:(.*?)<br />', details)
        if venue:
            data["venue"] = SimplifyHTML(venue[0])
    date = re.findall('(?si)<.*?>D.*?ates<.*?>:(.*?)<.*?>', details)
    if date:
        date = SimplifyHTML(date[0])
    else:
        date = re.findall('(?si)<.*?>Date\w*?:\s*<.*?>\s*(.*?)<.*?>', details)
        if date:
            date = SimplifyHTML(date[0])
    dates = re.findall('(?si)(\d{1,2}.*?\w{4,6})', date)
    if dates:
        startdate = dates[0].replace("6 \xe2\x80\x93 Tuesda", "6 August")
        startdate = startdate.replace("\xc2\xa0", " ")
        startdate = convertDate(startdate)
        data["startdate"] = startdate
        data["finishdate"] = convertDate(dates[1])
    gold = re.findall('(?si)<.*?>Gold medals<.*?>:\s*(\d{1,2}).*?<.*?>', details)
    if gold:
        data["gold"] = int(gold[0])
    else:
        gold = re.findall('(?si)<.*?>Gold medals:\s*<.*?>(\d{1,2}).*?<.*?>', details)
        if gold:
            data["gold"] = int(gold[0])
    athletes = re.findall('(?si)<.*?>Athletes<.*?>:\s*(\d{2,5})\s*.*?<.*?>', details)
    if athletes:
        athletes = athletes[0].replace("\xc2\xa0", "").replace("\xe2\x80\x93", "")
        data["athletes"] = int(athletes)
    else:
        athletes = re.findall('(?si)<.*?>Athletes:\s*<.*?>\s*(\d{2,5})\s*.*?<.*?>', details)
        if athletes:
            data["athletes"] = int(athletes[0])
    history = re.findall('(?si)<div>.*?<h2>.*?Key facts.*?</h2>.*?<h2>.*?</h2>(.*?)<h2>.*?</div>', details)
    if history:
        data["history"] = SimplifyHTML(history[0])
    else:
        history = re.findall('(?si)<div><p>.*?</p><h2>Canoeing at the Olympic Games\s*</h2>(.*?)<h2>.*?</div>', details)
        if history:
            data["history"] = SimplifyHTML(history[0])

def SimplifyHTML(t):
    t = re.sub("<p>", "NEWLINE", t)
    t = re.sub("<h2>(.*)</h2>", r"==\1==", t)
    t = re.sub("&amp;", "&", t)
    t = re.sub("&[\w#]*;?", " ", t)
    t = re.sub("(?s)<style>.*?</style>|<!--.*?-->", " ", t)
    t = re.sub("(?:<[^>]*>|\s)+", " ", t)
    t = re.sub("(?:NEWLINE)+", "\n\n", t)
    return t.strip()

#Main()
