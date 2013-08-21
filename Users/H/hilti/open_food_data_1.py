import scraperwiki
from BeautifulSoup import BeautifulSoup
from time import sleep
scraperwiki.metadata.save('data_columns', ['food_id','food_description', 'serving_size','total_calories',
                                           'calories_from_fat','total_fat','sat_fat',
                                           'cholesterol','sodium',
                                           'total_carbs','dietary_fiber','sugars', 
                                         'protein','calcium'])

start = 0  # so you can start from somewhere other than the beginning if something goes wrong
i = start
while i<7600: # December 2010: openfooddata.com had nothing past this.
    number_leading_zeros_needed = 4-len(str(i))   # formatting for url
    page = number_leading_zeros_needed*'0'+str(i)
    try:
        html = scraperwiki.scrape('http://www.openfooddata.com/food/'+page)
    #except: # This should really only handle a 'throttled' kind of exception but I dunno how
        print "Throttled, I think. Resting......."
        sleep(60)
        html = scraperwiki.scrape('http://www.openfooddata.com/food/'+page)
    except: # blank except to avoid raising exception
        pass

    # soup = BeautifulSoup(html)

    try:
        nutrition = soup.findAll(id="nutrition-box")[0].table
    except:
        print "Looks like there's no page "+page
        print "Continuing..."
        i += 1
        continue
    food_tag = soup.findAll('h2')
    nutrients = nutrition.table.findAll('tr')
    data = {}
    data['food_id'] = page
    data['food_description'] = food_tag[0].text
    data['total_calories'] = nutrition.tr.td.text[len('Calories '):]
    data['calories_from_fat'] = nutrition.tr.td.nextSibling.text[len('from fat '):]
    data['total_fat'] = nutrients[0].td.nextSibling.text
    data['sat_fat'] = nutrients[1].td.nextSibling.text
    data['cholesterol'] = nutrients[3].td.nextSibling.text
    data['sodium'] = nutrients[5].td.nextSibling.text
    data['total_carbs'] = nutrients[6].td.nextSibling.text
    data['dietary_fiber'] = nutrients[7].td.nextSibling.text
    data['sugars'] = nutrients[8].td.nextSibling.text
    data['protein'] = nutrients[10].td.nextSibling.text
    data['calcium'] = nutrients[12].td.nextSibling.text
    data['serving_size'] = soup.root.select.option.text
                                                    
# 2. Save the data in the ScraperWiki datastore.
    scraperwiki.datastore.save(['food_id'], data) # save the records one by one
    print "%s: %s" % (i, data['food_description'])
    i +=1