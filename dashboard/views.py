from django.shortcuts import render



def dashboard(request):
    return render(request, "dashboard/dashboard.html")


def needy_list(request):
    return render(request, "dashboard/needy_list.html")


