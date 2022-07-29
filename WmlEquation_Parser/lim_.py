# lim_.py - предел

from WmlEquation_Parser.utils.we import we, doc
from lxml import etree

num = we.run_('x')
den = we.run_('y')
frac = we.frac_(num, den)
lim_low = we.run_('0')
lim_high = we.run_('1')
integral_3 = we.integral_3_(lim_low, lim_high, [frac, we.run_('dx')])
equation = we.equation_(integral_3)
xml_equation = etree.fromstring(equation)
p = doc.add_paragraph()
p._element.append(xml_equation)
doc.save('words/integral_3_.docx')
