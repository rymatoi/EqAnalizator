# frac_.py - дробь

from WmlEquation_Parser.utils.we import we, doc
from lxml import etree

num = we.run_('num')  # числитель
den = we.run_('den')  # знаменатель
frac = we.frac_(num, den)
equation = we.equation_(frac)

xml_equation = etree.fromstring(equation)

p = doc.add_paragraph()
p._element.append(xml_equation)

doc.save('words/frac_.docx')
