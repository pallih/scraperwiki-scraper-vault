# Demoulidor Python Globo Ciberdemocracia
import scraperwiki #permite que a gente salve os nossos resultados
from lxml.html import parse
import re

url_busca = "http://busca.globo.com/Busca/oglobo/?query=Ciberdemocracia"

ps_busca = parse(url_busca).getroot()
print 'Alô Mundo!' # ps_busca

