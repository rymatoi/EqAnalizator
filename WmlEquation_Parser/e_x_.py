# e_x_.py - число со степенью

from WmlEquation_Parser.utils.we import we, doc
from lxml import etree

e = we.run_('e')  # основание
x = we.run_('x')  # степень
e_x = we.e_x_(e, x)
equation = we.equation_(e_x)

xml_equation = etree.fromstring(equation)

p = doc.add_paragraph()
p._element.append(xml_equation)

doc.save('words/e_x_.docx')
