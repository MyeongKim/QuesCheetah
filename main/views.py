from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from main.forms import UserForm, UserCreationForm
from main.models import User, ApiKey

# Create your views here.


def index(request):
    context = {

    }
    return render(request, 'main/pages/index.html', context)


def user_signup(request):
    context = {

    }

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:index')
    else:
        form = UserCreationForm()

    context.update({'form': form})
    return render(request, 'main/pages/signup.html', context)


def user_login(request):

    context = {

    }
    next = ""
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                if request.POST.get('next') == "":
                    return redirect('main:index')
                else:
                    return HttpResponseRedirect(request.POST.get('next'))
            else:
                # Return a 'disabled account' error message
                return HttpResponse('active user 가 아닙니다.')
        else:
            # Return an 'invalid login' error message.
            return HttpResponse('로그인 실패')
    else :
        next = request.GET['next']
        context.update({'next':next})
        return render(request, 'main/pages/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('main:index')

# TODO Unicode-objects must be encoded before hashing 에러 처리


@login_required
def apikey_new(request):
    context = {

    }
    if request.method == 'POST':
        #ApiKey.objects.generate(request.user)
        return HttpResponse('발급완료')
    else:
        return render(request, 'main/pages/apikey_new.html', context)


