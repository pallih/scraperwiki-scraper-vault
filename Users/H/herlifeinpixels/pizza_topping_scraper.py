import scraperwiki
import lxml.html

print "RANDOM PIZZA PIZZA TOPPING GENERATOR"

meat = scraperwiki.scrape("http://www.pizzapizza.ca/fresh-toppings-bk/meattab/")
vege = scraperwiki.scrape("http://www.pizzapizza.ca/fresh-toppings-bk/veggietab/")
sauce = scraperwiki.scrape("http://www.pizzapizza.ca/fresh-toppings-bk/saucesanddoughtab/")
cheese = scraperwiki.scrape("http://www.pizzapizza.ca/fresh-toppings-bk/cheesetab/")

toppingTypes = [meat, vege, sauce, cheese]

for toppingType in toppingTypes:
    root = lxml.html.fromstring(toppingType)

    # Get at topping in DOM
    toppings = root.cssselect("div.tabset-holder")[0]
    for idx, elm in enumerate(toppings) :
        #skip first element
        if idx == 0:
            toppingType = elm.cssselect("h3")[0].text.strip(' \n\r').split()[-1] #one word title
        else:
            topping = elm.cssselect("h3")[0].text.strip(' \n\r')
            data = (toppingType, topping)
            #save each topping type under a seperate table
            #scraperwiki.sqlite.save(unique_keys=["topping"], data={"topping":topping}, table_name=toppingType, verbose=2)
            #save all in one table
            scraperwiki.sqlite.save(unique_keys=["topping"], data={"toppingType":toppingType, "topping":topping}, table_name="pizzas", verbose=2)