import os
from copy import copy

from docx import Document
from lxml import etree


class WmlEquation:
    arrow = r'&#8594;'
    double_arrow_right = r'&#8658;'
    infty = r'&#8734;'

    def __init__(self, dir='formulas_2'):
        self.init_wml(dir)

    def init_wml(self, dir):
        # for file in [file for file in os.listdir(dir) if file.endswith('.wml')]:
        for file in os.listdir(dir):
            if file.endswith('.wml'):
                with open(os.path.join(dir, file), 'r') as f:
                    name = file.replace('.wml', '')
                    formula_string = f.read()
                    setattr(self, name, formula_string)  # self.name = formula_string

    def run_(self, a):
        run = copy(getattr(self, 'run'))  # run = copy(self.run)
        run = run.replace('<m:t/>', f'<m:t>{a}</m:t>')
        return run

    def run_f_(self, a):
        run = copy(getattr(self, 'run_f'))
        run = run.replace('<m:t/>', f'<m:t>{a}</m:t>')
        return run

    def frac_(self, a, b):
        frac = copy(getattr(self, 'frac'))
        frac = frac.replace('<m:num/>', f'<m:num>{"".join(a)}</m:num>')
        frac = frac.replace('<m:den/>', f'<m:den>{"".join(b)}</m:den>')
        return frac

    def e_x_(self, e, x):
        e_x = copy(getattr(self, 'e_x'))
        e_x = e_x.replace('<m:e/>', f'<m:e>{"".join(e)}</m:e>')
        e_x = e_x.replace('<m:sup/>', f'<m:sup>{"".join(x)}</m:sup>')
        return e_x

    def e__x_(self, e, x):
        e__x = copy(getattr(self, 'e__x'))
        e__x = e__x.replace('<m:e/>', f'<m:e>{"".join(e)}</m:e>')
        e__x = e__x.replace('<m:sub/>', f'<m:sub>{"".join(x)}</m:sub>')
        return e__x

    def e___x_(self, e, x, y):
        e___x = copy(getattr(self, 'e___x'))
        e___x = e___x.replace('<m:e/>', f'<m:e>{"".join(e)}</m:e>')
        e___x = e___x.replace('<m:sub/>', f'<m:sub>{"".join(x)}</m:sub>')
        e___x = e___x.replace('<m:sup/>', f'<m:sup>{"".join(y)}</m:sup>')
        return e___x

    def d_(self, e, beginChr='', endChr=''):
        d = copy(getattr(self, 'd'))
        d = d.replace('<m:e/>', f'<m:e>{"".join(e)}</m:e>')
        d = d.replace('<m:begChr/>', f'<m:begChr m:val="{beginChr}"/>')
        d = d.replace('<m:endChr/>', f'<m:endChr m:val="{endChr}"/>')
        return d

    def lim_(self, lim_, e):
        lim = copy(getattr(self, 'lim'))
        lim = lim.replace('<m:lim/>', f'<m:lim>{"".join(lim_)}</m:lim>')
        lim = lim.replace('<m:e/>', f'<m:e>{"".join(e)}</m:e>')
        return lim

    def func_(self, fname, e):
        func = copy(getattr(self, 'func'))
        func = func.replace('<m:fName/>', f'<m:fName>{"".join(fname)}</m:fName>')
        func = func.replace('<m:e/>', f'<m:e>{"".join(e)}</m:e>')
        return func

    def matrix_(self, mass, beginchr='', endchr='', alignment='left'):
        matrix = copy(getattr(self, 'matrix'))
        result = ''
        for row in mass:
            e_row = ''
            for val in row:
                e_row += '<m:e>' + "".join(val) + '</m:e>'
            result += '<m:mr>' + e_row + '</m:mr>'
        # <m:count m:val="5"/>
        # <m:mcJc m:val="left"/>
        matrix = matrix.replace(r'<m:mcJc/>', rf'<m:mcJc m:val="{alignment}"/>')
        matrix = matrix.replace(r'<m:count/>', rf'<m:count m:val="{len(mass[0])}"/>')
        matrix = matrix.replace('<m:begChr/>', rf'<m:begChr m:val="{beginchr}"/>')
        matrix = matrix.replace('<m:endChr/>', rf'<m:endChr m:val="{endchr}"/>')
        return matrix.replace('<m:mr/>', result)

    def integral_3_(self, sub, sup, e):
        integral_3 = copy(getattr(self, 'integral_3'))
        integral_3 = integral_3.replace('<m:sub/>', f'<m:sub>{"".join(sub)}</m:sub>')
        integral_3 = integral_3.replace('<m:sup/>', f'<m:sup>{"".join(sup)}</m:sup>')
        integral_3 = integral_3.replace('<m:e/>', f'<m:e>{"".join(e)}</m:e>')
        return integral_3

    def equation_(self, formula, alignment='center'):
        return getattr(self, 'base').replace('<m:jc m:val="center"/>', f'<m:jc m:val="{alignment}"/>').replace(
            '<m:oMath/>', f'<m:oMath>{formula}</m:oMath>')


if __name__ == '__main__':

    we = WmlEquation('formulas_2')

    doc = Document()
    a11 = we.e__x_(we.run_('a'), we.run_('11'))
    a12 = we.e__x_(we.run_('a'), we.run_('12'))
    a21 = we.e__x_(we.run_('a'), we.run_('21'))
    a22 = we.e__x_(we.run_('a'), we.run_('22'))

    matrix = we.matrix_([[a11, we.run_('+'), a12, we.run_('='), we.run_('0')],
                         [a21, we.run_('+'), a22, we.run_('='), we.run_('1')]
                         ], beginchr='{')

    equation = we.equation_(matrix)
    xml_equation = etree.fromstring(equation)
    p = doc.add_paragraph()
    p._element.append(xml_equation)

    doc.save(f'test.docx')
