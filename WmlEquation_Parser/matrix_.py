# matrix_.py - матрица

from WmlEquation_Parser.utils.we import we, doc
from lxml import etree

a11 = we.run_('a11')
a12 = we.run_('a12')
a21 = we.run_('a21')
a22 = we.run_('a22')

matrix = we.matrix_([[a11, a12], [a21, a22]], beginchr='{')

equation = we.equation_(matrix)

xml_equation = etree.fromstring(equation)

p = doc.add_paragraph()
p._element.append(xml_equation)

doc.save('words/matrix_.docx')
