from django.shortcuts import render
from .forms import TestForm
from data_analysis import visitor_info_analysis


def post_list(request):
    if request.method == 'POST': # 폼 제출
        form = TestForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            wait(request)
            visitor_info_analysis(start_date, end_date)
            return statistics(request)
    else:
        form = TestForm() # An unbound form

    return render(request, 'blog/input.html', {'form': form, })


def wait(request):
    return render(request, 'blog/wait.html', {})


def statistics(request):
    return render(request, 'blog/statistics.html', {})


def bar(request):
    return render(request, 'blog/bar.html', {})


def line(request):
    return render(request, 'blog/line.html', {})


def pie(request):
    return render(request, 'blog/pie.html', {})

