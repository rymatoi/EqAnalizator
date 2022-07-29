# d_.py - текст в скобках (скобки скалируются от размера выражения внутри)

from WmlEquation_Parser.utils.we import we, doc
from lxml import etree

text = we.run_('text')
d1 = we.d_(text, delimiters=['(', ')'])
equation1 = we.equation_(d1)

num = we.run_('num')  # числитель
den = we.run_('den')  # знаменатель
frac = we.frac_(num, den)
d2 = we.d_(frac, delimiters=['(', ')'])
equation2 = we.equation_(d2)

xml_equation1 = etree.fromstring(equation1)
xml_equation2 = etree.fromstring(equation2)

p = doc.add_paragraph()
p._element.append(xml_equation1)
p._element.append(xml_equation2)

doc.save('words/d_.docx')
