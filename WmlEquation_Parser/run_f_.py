# run_f_.py - текст для названий функций

from WmlEquation_Parser.utils.we import we, doc
from lxml import etree

run_f = we.run_f('run_f')
equation = we.equation_(run_f)

xml_equation = etree.fromstring(equation)

p = doc.add_paragraph()
p._element.append(xml_equation)

doc.save('words/run_f_.docx')

