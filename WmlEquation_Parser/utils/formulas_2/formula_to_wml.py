from docx import Document
from lxml import etree


def word_formula_to_wml(filename):
    doc = Document(filename)
    for p_ in doc.paragraphs:
        for el in p_._element:
            string = etree.tounicode(el, pretty_print=True)
            if 'oMathPara' in string:
                with open(filename.replace('.docx', '.wml'), 'w', encoding='utf-8') as f:
                    f.write(string)
                return 'success'
    return 'no formula found. invalid file format'




if __name__ == '__main__':
    filename = 'int.docx'
    word_formula_to_wml(filename)
