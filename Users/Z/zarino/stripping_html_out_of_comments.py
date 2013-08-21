import requests
import lxml.html
import re

html = """<div id="info">
  <table >
    <tr >
      <td  class="Tabla_01"><p>Nombre y Apellido</p></td>
      <td  class="Tabla_03"><strong>David HIRTZ</strong></td>
    </tr>
    <tr >
      <td class="textoTabla_01"><p>Cargo</p></td>
      <td class="textoTabla_04"><strong>Intendente</strong></td>
    </tr>
    <!-- <tr >
      <td class="Tabla_01"><p>Part&iacute;do pol&iacute;tico</p></td>
      <td class="Tabla_04"><strong>Unión para el Desarrollo Social</strong></td>
    </tr>
    <tr >
      <td class="Tabla_01"><p>Cobertura territorial de la agrupaci&oacute;n</p></td>
      <td class="Tabla_04"><strong>Nacional</strong></td>
    </tr> -->
    <tr >
      <td class="Tabla_01"><p>Reelecto</p></td>
      <td <strong>No</strong></td>
    </tr>
  </table>
</div>"""

cleaned_html = re.sub(r'(<!--)|(-->)', '', html)

dom = lxml.html.fromstring(cleaned_html)

print len(dom.cssselect('tr')), 'rows'

for tr in dom.cssselect('tr'):
    print '-', tr.text_content()


