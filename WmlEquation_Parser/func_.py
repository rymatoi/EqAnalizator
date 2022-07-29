# func_.py - функция с аргументом

from WmlEquation_Parser.utils.we import we, doc
from lxml import etree

num = we.run_('num')  # числитель
den = we.run_('den')  # знаменатель
frac = we.frac_(num, den)

sin = we.run_f_('sin')

func = we.func_(sin, [frac, we.run_('+'), frac])
equation = we.equation_(func)

xml_equation = etree.fromstring(equation)

p = doc.add_paragraph()
p._element.append(xml_equation)

doc.save('words/func_.docx')
