import scraperwiki
from scrapemark import scrape

URL = "http://www.upperhuttcity.com/wow"
PATTERN = """
{*
    <table>
        <tbody>
            <tr>
                <td><strong>{{ [events].title }}</strong></td>
                <td></td>
            </tr>
            <tr>
                <td>Date:</td>
                <td>{{ [events].date }}</td>
            </tr>
            <tr>
                <td>Time:</td>
                <td>{{ [events].time}}</td>
            </tr>
            <tr>
                <td>Location:</td>
                <td>{{ [events].location }}</td>
            </tr>
            <tr>
                <td>Cost:</td>
                <td>{{ [events].cost }}</td>
            </tr>
            <tr>
                <td>Description:</td>
            </tr>
            <tr>
                <td>{{ [events].description }}</td>
            </tr>
        </tbody>
    </table>

*}"""

for event in scrape(PATTERN, url=URL)['events']:
    scraperwiki.sqlite.save(['title', 'date'], event)import scraperwiki
from scrapemark import scrape

URL = "http://www.upperhuttcity.com/wow"
PATTERN = """
{*
    <table>
        <tbody>
            <tr>
                <td><strong>{{ [events].title }}</strong></td>
                <td></td>
            </tr>
            <tr>
                <td>Date:</td>
                <td>{{ [events].date }}</td>
            </tr>
            <tr>
                <td>Time:</td>
                <td>{{ [events].time}}</td>
            </tr>
            <tr>
                <td>Location:</td>
                <td>{{ [events].location }}</td>
            </tr>
            <tr>
                <td>Cost:</td>
                <td>{{ [events].cost }}</td>
            </tr>
            <tr>
                <td>Description:</td>
            </tr>
            <tr>
                <td>{{ [events].description }}</td>
            </tr>
        </tbody>
    </table>

*}"""

for event in scrape(PATTERN, url=URL)['events']:
    scraperwiki.sqlite.save(['title', 'date'], event)