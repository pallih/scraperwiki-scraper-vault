import scraperwiki
from lxml.html import parse
import mechanize

# Blank Python
#url = "http://www.acessoainformacao.gov.br/sistema/Login/Loginframes.aspx" /sistema/Login/Loginframes.aspx?txtUsuario=queremossaber&txtSenha=

br = mechanize.Browser()
req = mechanize.Request("http://www.acessoainformacao.gov.br/sistema/Login/Loginframes.aspx", "txtUsuario=queremossaber&txtSenha=")
req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.7) Gecko/20100713 Firefox/3.6.7")
req.add_header("Referer", "https://www.site.com/path")
#cj.add_cookie_header(req)
#res = mechanize.urlopen(req)
br.set_handle_robots(False)
br.open(req)
br.select_form(nr=0)
print br.form




#loginForm = br.forms().next()


