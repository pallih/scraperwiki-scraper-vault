import scraperwiki
import lxml.html


def parsed_html(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)


def first_match_text(tree, selector):
    return tree.cssselect(selector)[0].text_content().strip()


def format_price(price_str):
    return price_str[1:]


def scrape_kooples_product_page(url):
    tree = parsed_html(url)
    data = {
        "url": tree.cssselect("link[rel=canonical]")[0].attrib["href"],
        "product_name": first_match_text(tree, "h1"),
        "product_price": format_price(first_match_text(tree, ".old-price .price")),
        "product_price_special": format_price(first_match_text(tree, ".special-price .price"))
    }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)
    return data


print scrape_kooples_product_page("http://www.thekooples.co.uk/traditional-duffle-coat.html")import scraperwiki
import lxml.html


def parsed_html(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)


def first_match_text(tree, selector):
    return tree.cssselect(selector)[0].text_content().strip()


def format_price(price_str):
    return price_str[1:]


def scrape_kooples_product_page(url):
    tree = parsed_html(url)
    data = {
        "url": tree.cssselect("link[rel=canonical]")[0].attrib["href"],
        "product_name": first_match_text(tree, "h1"),
        "product_price": format_price(first_match_text(tree, ".old-price .price")),
        "product_price_special": format_price(first_match_text(tree, ".special-price .price"))
    }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)
    return data


print scrape_kooples_product_page("http://www.thekooples.co.uk/traditional-duffle-coat.html")