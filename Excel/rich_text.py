import xlwt

# пример работы с rich текстом в word.
# https://stackoverflow.com/questions/41770461/how-to-put-rich-text-in-a-merged-cell-using-xlwt
#


wb = xlwt.Workbook()
ws = wb.add_sheet('Sheet1')

font0 = xlwt.easyfont('')
font1 = xlwt.easyfont('bold true')
font2 = xlwt.easyfont('color_index red')
style = xlwt.easyxf('font: color_index blue')
fontMA = xlwt.easyfont('color_index red')
fontMA_LK = xlwt.easyfont('color_index red, bold true, name Times New Roman')
fontLA = xlwt.easyfont('color_index green')
fontLA_LK = xlwt.easyfont('color_index green, bold true')

# seg1 = ('bold', font1)
# seg2 = ('red', font2)
# seg3 = ('plain', font0)
# seg4 = ('boldagain', font1)
seg1 = ('(1)', font1)
seg2 = ('2', fontMA)
seg3 = ('(3)', fontMA_LK)
seg4 = ('4', fontMA_LK)
seg5 = ('5', fontLA_LK)
seg6 = ('(6)', fontLA)
seg7 = ('(7)', fontLA_LK)

ws.write_rich_text(2, 5, (seg1, seg2, seg3, seg4, seg5, seg6, seg7))
ws.write_rich_text(4, 1, ('xyz', seg1, '', seg2, seg3, '123', seg5), style)

wb.save('rich_text.xls')

# МА красный
# ЛАиАГ зеленый
# остальные - черным
