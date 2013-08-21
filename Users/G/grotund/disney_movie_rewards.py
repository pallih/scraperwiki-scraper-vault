import scraperwiki
import lxml.html
from string import lowercase

def get_titles(page):
    for div in page.cssselect("div[class='text']"):
        h2s        = div.cssselect("h2")[0]
        points_str = div.cssselect("span[class='points']")[0].text_content();
        earn_pos   = points_str.find('Earn');
        number_pos = points_str.find('points');
        points     = points_str[earn_pos+5:number_pos-1];
        data = {
          'title'  : h2s.text_content(),
          'points' : points
        }
        scraperwiki.sqlite.save(unique_keys=['title'], data=data);

browse_by  = lowercase + '0';
base_url   = 'http://www.disneymovierewards.go.com/mobile/eligible-titles/blu-ray-dvd?'

for lower in browse_by:
    page_count = 1;
    html = scraperwiki.scrape(base_url + "q=" + lower + "&page=" + str(page_count))
    root = lxml.html.fromstring(html)

    for explanation in root.cssselect("span[class='explanation']"):
        expl_str    = explanation.text_content();
        of_pos      = expl_str.find('of');
        results_pos = expl_str.find('Results');
        divider     = int(expl_str[of_pos+3:results_pos-1])/10;
        remainder   = int(expl_str[of_pos+3:results_pos-1]) % 10;

        if (remainder == 0):
            page_count = divider;
        else:
            page_count = divider + 1;

    print lower +": " + str(page_count);
    
    get_titles(root);

    if page_count > 1:
        for cur_page in range(2,page_count+1):
                html = scraperwiki.scrape(base_url + "q=" + lower + "&page=" + str(cur_page))
                root = lxml.html.fromstring(html)
                get_titles(root);

