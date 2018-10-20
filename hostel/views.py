from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Diff, Student, Room, Change, Swap
from django.shortcuts import render

@login_required
def index(request):
    diff = Diff.objects.get( user = request.user)
    return render(request, 'hostel/index.html', {'diff' : diff, })
