# e__x_.py - число со индексом

from WmlEquation_Parser.utils.we import we, doc
from lxml import etree

e = we.run_('e')  # основание
i = we.run_('i')  # индекс
e__x = we.e__x_(e, i)
equation = we.equation_(e__x)

xml_equation = etree.fromstring(equation)

p = doc.add_paragraph()
p._element.append(xml_equation)

doc.save('words/e__x_.docx')
