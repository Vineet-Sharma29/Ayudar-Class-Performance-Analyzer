from openpyxl import load_workbook

wb = load_workbook(filename = 'sample.xlsx')
ws = wb['Sheet1']


for row in ws.rows:
    for cell in row:
        print(cell.value,end="\t")
    print()