# e___x_.py - число со степенью и индексом

from WmlEquation_Parser.utils.we import we, doc
from lxml import etree

e = we.run_('e')  # основание
x = we.run_('x')  # степень
i = we.run_('i')  # индекс
e___x = we.e___x_(e, i, x)
equation = we.equation_(e___x)

xml_equation = etree.fromstring(equation)

p = doc.add_paragraph()
p._element.append(xml_equation)

doc.save('words/e___x_.docx')
