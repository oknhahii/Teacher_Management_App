from django.shortcuts import render, redirect
from django.db.models import Q
from .models import User,Class, Subject
from django.http import HttpResponse
from .forms import UserForm, ClassForm
from django.contrib import messages
import uuid

# Create your views here.

def home(request):
    global users
    users = User.objects.filter(is_superuser=False)

    print(users)
    print(request.method)
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        users = User.objects.filter((Q(full_name__icontains=keyword)|Q(teacher_id__icontains=keyword)|Q(phone__icontains=keyword)|Q(location__icontains=keyword))&Q(is_superuser=False))
    context = {'users':users}

    return render(request, 'modules/home.html',context)

def teacherInfo(request, pk):
    user = User.objects.get(id=pk)
    _class = Class.objects.filter(teacher=user)
    global salary, total_of_lesson
    salary,total_of_lesson = 0,0
    for cl in _class:
        total_of_lesson += cl.number_of_lessons
        print(salary)
        salary += cl.number_of_lessons*(user.degree + cl.subject.subject_factor+ cl.class_factor) * user.salary_per_hour
    salary = int(salary)
    context = {'user':user, 'owner_class':_class, 'salary': salary, 'total_of_lesson': total_of_lesson}
    return render(request,'modules/teacher_info.html',context)

def createTeacher(request):
    form = UserForm()
    global mess
    mess = ''
    if request.method == 'POST':
        teacher_id = User.objects.filter(teacher_id=request.POST.get('teacher_id'))
        phone = User.objects.filter(phone=request.POST.get('phone'))
        try:
            if len(teacher_id) != 0:
                raise ("x")
                # return redirect('home')
            elif len(phone) != 0:
                raise ("Teacher id exists")
            else:
                User.objects.create(
                    full_name=request.POST.get('full_name'),
                    teacher_id=request.POST.get('teacher_id'),
                    year_of_birth=int(request.POST.get('year_of_birth')),
                    phone=request.POST.get('phone'),
                    degree=float(request.POST.get('degree')),
                    salary_per_hour=int(request.POST.get('salary_per_hour')),
                    location=request.POST.get('location'),
                    username=request.POST.get('phone'),
                )
                return redirect('home')
        except:
            mess='Phone number or teacher id exists'

    context = {'form': form, 'mess': mess}
    return render(request, 'modules/create_teacher.html', context)

def updateTeacher(request,pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)

    global mess
    mess = ''
    if request.method == 'POST':
        teacher_id = User.objects.filter(teacher_id=request.POST.get('teacher_id'))
        phone = User.objects.filter(phone=request.POST.get('phone'))
        print(teacher_id[0])
        try:
            if len(teacher_id) != 0 and teacher_id[0].teacher_id != user.teacher_id:
                raise ("x")
                # return redirect('home')
            elif len(phone) != 0 and phone[0].phone != user.phone:
                raise ("Teacher id exists")
            else:
                print('update')
                user.full_name = request.POST.get('full_name')
                user.teacher_id = request.POST.get('teacher_id')
                user.year_of_birth = int(request.POST.get('year_of_birth'))
                user.phone = request.POST.get('phone')
                user.degree = float(request.POST.get('degree'))
                user.salary_per_hour = int(request.POST.get('salary_per_hour'))
                user.location = request.POST.get('location')
                user.username = request.POST.get('phone')
                user.save()
                return redirect('home')
        except Exception:
            print(Exception)
            mess = 'Phone number or teacher id exists'

    context = {'form': form, 'mess': mess}
    return render(request, 'modules/create_teacher.html', context)


def deleteTeacher(request,pk):
    user = User.objects.get(id=pk)
    if(request.method == 'POST'):
        user.delete()
        return redirect('home')

    _class = Class.objects.filter(teacher=user)
    global salary, total_of_lesson
    salary, total_of_lesson = 0, 0
    for cl in _class:
        total_of_lesson += cl.number_of_lessons
        salary += cl.number_of_lessons * (user.degree + cl.subject.subject_factor + cl.class_factor) * user.salary_per_hour
    salary = int(salary)
    context = {'user': user, 'owner_class': _class, 'salary': salary, 'total_of_lesson': total_of_lesson}

    return render(request, 'modules/delete_teacher.html', context)

def addClass(request,pk):
    form = ClassForm()
    global mess
    mess = ''

    if request.method == 'POST':
        class_id = Class.objects.filter(class_id= request.POST.get('class_id'))
        try:
            teacher = User.objects.get(id=pk)
            if len(class_id) != 0:
                raise ("Class id id exists or teacher_id is invalid")
            else:
                sj = Subject.objects.all()[int(request.POST.get('subject')) - 1]
                Class.objects.create(
                    class_id=request.POST.get('class_id'),
                    class_name=request.POST.get('class_name'),
                    class_factor=float(request.POST.get('class_factor')),
                    number_of_lessons=int(request.POST.get('number_of_lessons')),
                    teacher=teacher,
                    subject=sj
                )
                return redirect('teacher-info', pk=pk)
        except Exception as exception:
            mess = 'Phone number or teacher id exists'


    context = {'form':form, 'mess': mess}
    return render(request, 'modules/add_class.html', context)