from django.shortcuts import render
from django.http import HttpResponse
from .forms import RequestForm


def index(request):
    return render(request, 'tahapp/index.html')


def needful(request):
    return render(request, 'tahapp/needful.html')#HttpResponse("Hello, world. You're at the polls index.")

def submitRequest(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['type']
    return HttpResponse("Hello, world. You're at the polls index. %s" % answer)

# Create your views here.
