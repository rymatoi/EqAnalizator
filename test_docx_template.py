from docxtpl import DocxTemplate

from analisator import Parser

parser = Parser()


doc = DocxTemplate("my_word_template.docx")
context = { 'company_name' : parser.render_equation("1_{3}") }
doc.render(context)
doc.save("generated_doc.docx")