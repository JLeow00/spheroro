from django.shortcuts import render
from django.http import HttpResponse

from django.http import HttpResponseRedirect

from .models import Direction

# Create your views here.
def index(request):
	directions = Direction.objects.all()
	for direction in directions:
		return HttpResponse(direction.direction)

def change(request):
    return render(request, 'spheroproject/change.html')

def changedirection(request, dir):
	Direction.objects.all().update(direction=dir)
	return HttpResponseRedirect("/ball/change/")
