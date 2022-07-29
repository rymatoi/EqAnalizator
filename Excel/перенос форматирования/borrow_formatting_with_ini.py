import configparser

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, Border, Protection, Fill

# сначала нужно посмотреть borrow_formatting_new.py, так как текущий модуль делает то же самое, только с ini-файлом.
# в ini-файле прописываются вручную нужные свойства у строк и столбцов, порядок их указания определяет приоритет настроек:
# например, если сначала у строки 1 выставилось выравнивание вправо, а у столбца 1 выравнивание влево, то у ячейки [1,1]
# будет выравнивание столбца, так как он 'лег' на ячейку последним
# настройки берутся из свойств объектов openpyxl (так как мы говорим про столбцы и строки, то надо смотреть объекты
# row_dimensions и column_dimensions -> https://docs-python.ru/packages/modul-openpyxl/razmer-stroki-stolbtsa/)

# ini-файл можно создать программно, для этого см. модуль make_config.py

def get_dict_from_str(dict_str):
    namespace = {}
    exec(f"result = dict({dict_str})", locals(), namespace)
    return namespace["result"]


def _init_openpyxl_style_with_json(prop_name, props_string):
    styles = {
        'alignment': Alignment,
        'font': Font,
        'border': Border,
        'protection': Protection,
        'fill': Fill
    }
    if prop_name not in styles:
        return props_string
    props = get_dict_from_str(props_string)
    return styles[prop_name](**props)


def _copy_props(_obj, _prop_dict):
    [setattr(_obj, prop, _init_openpyxl_style_with_json(prop, _prop_dict[prop])) for prop in _prop_dict.keys() if
     hasattr(_obj, prop)]


config_path = 'example.ini'
file_out = 'result.xlsx'

config = configparser.ConfigParser()
config.read(config_path)

wb = load_workbook(file_out)
ws = wb.active

unusual_rows = []
unusual_columns = []
for section in config.sections():
    prop_dict = config[section]
    if prop_dict['type'] == 'column':
        _copy_props(ws.column_dimensions[section], prop_dict)
        unusual_columns.append(section)
    elif prop_dict['type'] == 'row':
        _copy_props(ws.row_dimensions[int(section)], prop_dict)
        unusual_rows.append(int(section))

for row in ws.rows:
    for cell in row:
        if cell.row in unusual_rows:
            if cell.column_letter in unusual_columns:
                for section in reversed(config.sections()):
                    if section == str(cell.row) or section == cell.column_letter:
                        _copy_props(cell, config[section])
                        break
            else:
                _copy_props(cell, config[str(cell.row)])
        elif cell.column_letter in unusual_columns:
            _copy_props(cell, config[cell.column_letter])

wb.save(file_out)
