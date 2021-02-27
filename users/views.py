from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, Group
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

from courses.models import Course
from users.forms import LoginForm, RegistrationForm


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(email=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse_lazy('home'))
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect(reverse_lazy('home'))
    return render(request, 'users/logout.html')


def registration(request):
    form = RegistrationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            if form.cleaned_data["is_instructor"] is True:
                permission = Permission.objects.get(name="Can add course")
                instructor_group = Group.objects.get(name="instructor")
                user.groups.add(instructor_group)
                user.user_permissions.add(permission)
            else:
                permission = Permission.objects.get(name="Can view course")
                student_group = Group.objects.get(name="student")
                user.groups.add(student_group)
                user.user_permissions.add(permission)

            return redirect(reverse_lazy('users:login'))

    return render(request, 'users/registration.html', {'form': form})


def user_profile(request):
    if request.method == "GET":
        context = {}
        if request.user.is_authenticated:
            if request.user.is_instructor:
                courses = Course.objects.filter(owner=request.user.id)
                context['courses'] = courses

        return render(request, 'users/profile.html', context)
