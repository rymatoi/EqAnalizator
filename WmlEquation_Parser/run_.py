# run_.py - обычный текст

from WmlEquation_Parser.utils.we import we, doc
from lxml import etree

run = we.run_('run')
equation = we.equation_(run)

xml_equation = etree.fromstring(equation)

p = doc.add_paragraph()
p._element.append(xml_equation)

doc.save('words/run.docx')

