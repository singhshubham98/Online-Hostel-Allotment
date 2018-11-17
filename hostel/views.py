
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
from django.core.files.storage import FileSystemStorage
# Diff class for authentication if login user is not hostel admin or Student then
# login page will display error 
@login_required
def index(request):
    diff = Diff.objects.get( user = request.user)
    return render(request, 'hostel/index.html', {'diff' : diff, })

# --------- RegisterPage view --------
@login_required
def register(request):
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    if request.method == 'POST':
        user_form    = UserForm(request.POST)
        diff_form    = DiffForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        
            
        if user_form.is_valid() and diff_form.is_valid() and student_form.is_valid():
            try:
                user = user_form.save()
                # user.username(label_tag='roll_no')
                # using set_password method, hash the password
                user.is_active = False
                user.set_password(user.password)
                user.save()
                
                # Since we need to set the user attribute ourselves, we set commit=False.
                # This delays saving the model until we're ready to avoid integrity problems.
                diff = diff_form.save(commit = False)
                diff.user = user
                diff.save()
                student  = student_form.save(commit = False)
                student.roll_no = user
                student.save()
                registered = True
                
                return HttpResponseRedirect('/')
            except:
                pass

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        student_form = StudentForm()
        diff_form = DiffForm()

    return render(request,'hostel/register.html', {
        'user_form' : user_form,
        'student_form' : student_form,
        'diff_form' : diff_form,
        'registered': registered,
    })

# --------- Login --------
@lo
def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate( username=username, password=password)

        if user:
            if user.is_active:
                # We'll send the user back to the homepage.
                login(request, user)

                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Your Account is disabled')
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            messages.add_message(request, messages.ERROR, 'Invalid Password or Username. Try again!')
            return HttpResponseRedirect("/login")
    else:
        return render(request,'hostel/login.html', {})

# <!----- Logout----->
@login_required
def logout1(request):
    logout(request)
    return redirect('/login/')

# <!-------Allocate Room ------>
@login_required
def allocate(request):

    if request.method == 'POST':

        roll_no = request.POST['roll_no']
        room_no = request.POST['room_no']

        try:
            student_roll_no = User.objects.get(username = roll_no)
            student = Student.objects.get(roll_no = student_roll_no)
            room_new = Room.objects.get(room_no = room_no)
            
            
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Check the details again!')
            return render(request, 'hostel/staff_allocate_room.html', {})
        
        if room_new is not None and student.room is None:
            if room_new.vacancy > 0:
                student.room = room_new
                room_new.vacancy -= 1
                student.save()
                room_new.save()
                return HttpResponseRedirect('/')
            else:
                html = '<html><body style="background-color:rgb(123,225,236); text-align:center; margin-top:100px;"><h2>Sorry, The Room is full</h2> </body></html>'
                return HttpResponse(html)
        else:
            return HttpResponseRedirect('/')
    
    else:
        return render(request, 'hostel/staff_allocate_room.html', {})


@login_required
def student_details(request):
    student = Student.objects.get(roll_no = request.user)
    room = Room.objects.get(room_no = student.room.room_no)
    students  = Student.objects.filter(room = student.room.room_no)
    return render(request, 'hostel/student_details.html', {'student': student,'room1': room,'students':students })


@login_required
def change_request(request):

    if request.method == 'POST':
        student = Student.objects.get(roll_no = request.user)
        reason  = request.POST['reason']
        flag    = request.POST['flag']

        if flag:
            request = Change.objects.create(student = student, reason = reason)
        else:
            return HttpResponseRedirect('/')
        
        return HttpResponseRedirect('/success')
    else:
        return render(request, 'hostel/change_req.html', {})
        

@login_required
def change(request):
    if request.method == 'POST':
        roll_no  = request.POST['roll_no']
        room_no  = request.POST['room_no']

        try:
            user = User.objects.get(username = roll_no)
            student = Student.objects.get(roll_no = user)
            room_new = Room.objects.get(room_no = room_no)
       
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Check the details again!')
            return render(request, 'hostel/staff_change_room.html', {})
        
        if room_new is not None and student.room is not None:
            if room_new.vacancy > 0:
                old_room = Room.objects.get(room_no = student.room.room_no)
                old_room.vacancy += 1
                student.room = room_new
                room_new.vacancy -= 1
                old_room.save()
                student.save()
                room_new.save()
                return HttpResponseRedirect('/')
            else:
                html = '<html><body style="background-color:rgb(123,225,236); text-align:center; margin-top:100px;"><h2>Sorry, The Room is full</h2> </body></html>'
                return HttpResponse(html)
        else:
            return HttpResponseRedirect('/')
    else:
        return render(request, 'hostel/staff_change_room.html', {})

@login_required
def swap_request(request):
    if request.method == 'POST':

        stud2 = request.POST['stud2']
        reason   = request.POST['reason']
        flag     = request.POST['flag']

        try:
            user = User.objects.get(username = stud2)
            student2  = Student.objects.get( roll_no = user)
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Check the roll number again!')
            return render(request, 'hostel/swap_request.html', {})

        student1 = Student.objects.get(roll_no = request.user)
        if student2.room is not None:
            if flag:
                Swap.objects.create(student1 = student1, student2 = student2, reason = reason)
            else:
                return HttpResponseRedirect('/')
            return HttpResponseRedirect('/success')
        else:
            return HttpResponseRedirect('/')
    else:
        return render(request, 'hostel/swap_request.html', {})

@login_required
def swap(request):

    if request.method == 'POST':

        roll_no1 = request.POST['roll_no1']
        roll_no2 = request.POST['roll_no2']

        try:
            user1 = User.objects.get(username = roll_no1)
            student1 = Student.objects.get(roll_no = user1)
            user2 = User.objects.get(username = roll_no2)
            student2 = Student.objects.get(roll_no = user2)

        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'check the details again!')
            return HttpResponseRedirect('hostel/staff_swap_room.html', {})
        
        if student1.room is not None and student2.room is not None:

            room1 = student1.room
            room2 = student2.room
            student1.room = room2
            student2.room = room1
            student1.save()
            student2.save()
            html = '<html><body style="background-color:rgb(123,225,236); text-align:center; margin-top:100px;"><h2>Room Swapped Successfully</h2> </body></html>'
            return HttpResponse(html)
        
        else:
            return HttpResponseRedirect('/')
    
    else:
        return render(request, 'hostel/staff_swap_room.html', {})

@login_required
def swap_ack(request):

    user = request.user
    try:
        req = Swap.objects.get(student2 = request.user.username)
    except Swap.DoesNotExist:
        req = None
    if request.method == 'POST':

        if '_accept' in request.POST:
            req.accept = True
            req.save()
        if '_decline' in request.POST:
            req.delete()
        return HttpResponseRedirect('/success')
    else:
        return render(request, 'hostel/swap_ack.html', {'request': req, 'user': user})


@login_required
def deallocate(request):
    if request.method == 'POST':
        join_year = request.POST['join_year']

        students = Student.objects.filter(join_year = join_year)
        length = len(students)
        if length == 0:
            messages.add_message(request, messages.ERROR, 'No Such Batch')
            return render(request, 'hostel/deallocate.html', {})
        
        else:
            for i in range(length):
                if students[i].room is not None:
                    old_room = Room.objects.get(room_no = students[i].room.room_no)
                    old_room.vacancy = old_room.capacity
                    print students[i], old_room
                    old_room.save()
                    students[i].room = None
                    students[i].save()
                    print students[i],old_room
                else:
                    students[i].save()
            return HttpResponseRedirect('/')
    else:
        return render(request, 'hostel/deallocate.html', {})

@login_required
def show_request(request):
    try:
        swap_req = Swap.objects.all()
    except Swap.DoesNotExist:
        swap_req = None

    try:
        changer = []
        change_req = Change.objects.all()
        for i in change_req:
            user = User.objects.get(username=i.student.roll_no)
            changer.append([user, i])
            #print (user, i)

    except Change.DoesNotExist:
        change_req = None
    return render(request, 'hostel/show_request.html', {'swap_req': swap_req, 'change_req': changer})

@login_required
def vacant_room(request):
    rooms = Room.objects.exclude(vacancy = 0)
    return render(request, 'hostel/vacant_room.html', {'rooms': rooms,})

@login_required
def show_students(request):
    changer = []
    students = Student.objects.all()
    for i in students:
        user = User.objects.get(username = i.roll_no)
        changer.append([user, i])
    
    return render(request, 'hostel/show_students.html', {'students': changer,})


@login_required
def success(request):
    return render(request, 'hostel/success.html', {})
