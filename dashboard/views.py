from django.shortcuts import render
import openpyxl


def dashboard(request):
    if "GET" == request.method:
        return render(request, "dashboard/dashboard.html")
    else:
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

        return render(request,'dashboard/dashboard.html',{"excel_data":excel_data})

