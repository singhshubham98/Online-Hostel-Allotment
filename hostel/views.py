from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import UserForm, DiffForm, StudentForm, RoomForm
from .models import Diff, Student, Room, Change, Swap
from django.contrib.auth.models import User
from django.template import RequestContext
import csv, os
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Diff class for authentication if login user is not hostel admin or Student then
# login page will display error 
@login_required
def index(request):
    diff = Diff.objects.get( user = request.user)
    return render(request, 'hostel/index.html', {'diff' : diff, })

# --------- RegisterPage view --------

def register(request):
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    if request.method == 'POST':
        user_from    = UserForm(data = request.POST)
        diff_from    = DiffForm(data = request.POST)
        student_from = StudentForm(data = request.POST)

        if user_from.is_valid() and diff_from.is_valid() and student_from.is_valid():
            user = user_from.save()
            # user.username(label_tag='roll_no')
            # using set_password method, hash the password
            user.set_password(user.password)
            user.save()

            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            diff = diff_from.save(commit = False)
            diff.user = user
            diff.save()

            student  = student_from.save()
            student.roll_no = user
            student.save()

            registered = True

        else:
            print user_from.errors, student_from.errors, diff_from.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_from = UserForm()
        student_from = StudentForm()
        diff_from = DiffForm()

    return render(request, 'hostel/register.html', {
        'user_form' : user_from,
        'student_form' : student_from,
        'diff_form' : diff_from,
    })

# --------- Loginpage view --------

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate( username=username, password=password)

        if user:
            if user.is_active:
                # We'll send the user back to the homepage.
                login(request, user)

                return HttpResponseRedirect('/hostel/')
            else:
                return HttpResponse('Your Account is disabled')
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            messages.add_message(request, messages.ERROR, 'Invalid Password or Username. Try again!')
            return HttpResponseRedirect("/hostel/login")
    else:
        return render(request,'hostel/login.html', {})

# ----- Logout-----
@login_required
def logout1(request):
    logout(request)
    return redirect('/hostel/login/')

# -------Allocate Room ------
# @login_required
# def allocate(request):








