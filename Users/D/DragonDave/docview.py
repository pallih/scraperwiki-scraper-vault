# Blank Python
import pygments

import cgi
import os

from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.lexers import RubyLexer,PythonLexer,PhpLexer
from pygments.formatters import HtmlFormatter

get = os.getenv("QUERY_STRING")
(fname,_,lineno)=get.partition(':')
#lineno=int(lineno)
lexer=get_lexer_for_filename(fname)


#f=open(fname).read().replace(' ','&nbsp;').split('\n')

code = f=open(fname).read()
#lexer=guess_lexer(code)
print lexer
print "<style>"
print HtmlFormatter().get_style_defs('.highlight')
print "</style>"
nos=True
print highlight(code, lexer, HtmlFormatter(linenos=nos))

# Blank Python
import pygments

import cgi
import os

from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.lexers import RubyLexer,PythonLexer,PhpLexer
from pygments.formatters import HtmlFormatter

get = os.getenv("QUERY_STRING")
(fname,_,lineno)=get.partition(':')
#lineno=int(lineno)
lexer=get_lexer_for_filename(fname)


#f=open(fname).read().replace(' ','&nbsp;').split('\n')

code = f=open(fname).read()
#lexer=guess_lexer(code)
print lexer
print "<style>"
print HtmlFormatter().get_style_defs('.highlight')
print "</style>"
nos=True
print highlight(code, lexer, HtmlFormatter(linenos=nos))

