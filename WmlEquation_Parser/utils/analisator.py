from construct_eq import WmlEquation
from docx import Document
from lxml import etree
from bs4 import BeautifulSoup


# Parser - класс, преобразующий запись latex в Word Equation.

class Parser:
    def __init__(self):
        self.we = WmlEquation('formulas_2')
        # self.func_names -> те названия функций, которые должны записываться шрифтом для функций.
        # делается это потому, что для таких функций используется один и тот же шаблон.
        self.func_names = ['sin', 'cos', 'tg', 'ctg']
        # self.funcs отвечает за соответствие функции latex и функции WmlEquation.
        self.funcs = {
            'frac': self.we.frac_,
            'e_x': self.we.e_x_,
            'e__x': self.we.e__x_,
            'e___x': self.we.e___x_,
            'sin': self.we.func_,
            'cos': self.we.func_,
            'tg': self.we.func_,
            'ctg': self.we.func_,
            'iiint': self.we.integral_3_,
            'd': self.we.d_
        }

    # get_args - функция, парсящая запись latex типа \func{arg1}{arg2}{...}{argN}, возвращает массив аргументов args
    def get_args(self, latex):
        brackets = 0
        args = []
        buffer = ''
        for s in latex:
            if s == '}':
                brackets -= 1
            if s == '{':
                brackets += 1
            if brackets == 0:
                if buffer:
                    args.append(buffer[1:])
                    buffer = ''
            else:
                buffer += s
        return args

    # parse_ - рекурсивно парсящая latex запись функция.
    # главная задача функции parse_ - привести минимальные лексемы к виду \func{arg1}{..}{argN} или к обычному тексту
    # каждая итерация сначала делит запись на минимальные внешние лексемы
    # примеры минимальных внешних лексем:
    # a+b -> [a, +, b]
    # a+(b+c) -> [a, +, (b+c)]
    # \frac{a}{a+b}+c -> [\frac{a}{a+b}, +, c]
    # \sin{x} -> [\sin{x}]
    # затем обрабатывает каждую из получившихся лексем и рекурсивно делит ее до тех пор, пока не останется функция
    # или обычный текст
    # далее, в зависимости от получившегося результата, работает по трем сценариям:
    # 1. если запись содержит инфиксные операторы '_' или '^', то делит на внешние лексемы по этим разделителям,
    # а затем преобразует запись к формату \func{arg1}{..}{argN}
    # 2. если запись начинается с символа '\', то значит это функция, и идет работа как с функцией
    # 3. если запись это просто текст, то работает как с текстом и оборачивается в обычный run
    # рано или поздно каждая лексема дойдет до парсинга своих частей через парсинг простого текста
    def parse_(self, latex):
        result = ''
        latex = latex.replace(' ', '')
        if len(lexems := self.get_lexems(latex)) > 1:
            for lexem in lexems:
                result += self.parse_(lexem)
        else:
            lexems = self.get_lexems(latex, symbols=['^', '_'])
            if not (lexems.count('^') > 1 or lexems.count('_') > 1):
                if '^' in lexems and '_' in lexems:
                    sup_idx = lexems.index('^')
                    sub_idx = lexems.index('_')
                    if sup_idx > sub_idx:
                        latex = '\\e___x{' + lexems[0] + '}' + '{' + lexems[2] + '}' + '{' + lexems[4] + '}'
                    else:
                        latex = '\\e___x{' + lexems[0] + '}' + '{' + lexems[4] + '}' + '{' + lexems[2] + '}'
                elif '^' in lexems:
                    latex = '\\e_x{' + lexems[0] + '}' + '{' + lexems[2] + '}'
                elif '_' in lexems:
                    latex = '\\e__x{' + lexems[0] + '}' + '{' + lexems[2] + '}'
            if latex[0] != '\\':
                return self.we.run_(latex)
            func_name = latex.split('{')[0].replace('\\', '')
            args = self.get_args(latex)
            for i, arg in enumerate(args):
                lexems = self.get_lexems(arg)
                result_arg = ''
                for lexem in lexems:
                    result_arg += self.parse_(lexem)
                args[i] = result_arg
            if func_name in self.func_names:
                args = [self.we.run_f_(func_name)] + args
            result += self.funcs[func_name](*args)
        return result

    # {a} -> a
    # {a}+{b} -> {a}+{b}
    # {{a}+{b}} -> {a}+{b}
    def cut_extra_brackets(self, latex: str):
        if latex.startswith('{') and latex.endswith('}'):
            if self.is_balanced(latex[1:-1]):
                return latex[1:-1]
            return latex
        return latex

    # анализирует правильность расставления скобок
    def is_balanced(self, final_str):
        brackets = ['{', '}', '(', ')', '[', ']']
        final_str = ''.join([i for i in final_str if i in brackets])
        type_brackets = ['{}', '()', '[]']
        while any(x in final_str for x in type_brackets):
            for br in type_brackets:
                final_str = final_str.replace(br, '')
        return not final_str

    # делит запись на минимальные внешние разделители по заданным символам
    # если символы не заданы, то делит по стандартному набору ['+', '-', '=', '*']
    def get_lexems(self, latex, symbols=None):
        if symbols is None:
            symbols = ['+', '-', '=', '*']
        brackets = 0
        brackets_ = 0
        buffer = ''
        elements = []
        for s in latex:
            if s == '{':
                brackets += 1
            if s == '}':
                brackets -= 1
            if s == '(':
                brackets_ += 1
            if s == ')':
                brackets_ -= 1
            if s not in symbols:
                buffer += s
            else:
                if brackets == 0 and brackets_ == 0:
                    elements.append(buffer)
                    elements.append(s)
                    buffer = ''
                else:
                    buffer += s
        elements.append(buffer)
        result_list = [self.cut_extra_brackets(el) for el in elements if el]
        if len(result_list) == 1:
            if result_list[0].startswith('(') and result_list[0].endswith(')'):
                if self.is_balanced(result_list[0][1:-1]):
                    return ['(', result_list[0][1:-1], ')']
                return result_list
            return result_list
        return result_list

    # функция, которую нужно вызывать для парсинга, она:
    # 1. парсит запись
    # 2. оборачивает ее в теги oMathPara
    def render_equation_(self, latex):
        parsed = self.parse_(latex)
        result = self.we.equation_(parsed)
        return result


parser = Parser()
equation = parser.render_equation_(r'\frac{x}{a}+\frac{y}{b}+\frac{z}{c} = 1')
doc = Document()
p = doc.add_paragraph()
formula_xml = etree.fromstring(equation)
p._element.append(formula_xml)
doc.save(f'test.docx')
