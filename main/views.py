# 직접 개발한 코드
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import password_reset
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from main.forms import UserForm, UserCreationForm
from main.models import User, ApiKey, Domain

import re
from urllib.parse import urlparse
import json

# Create your views here.


def index(request):
    context = {

    }
    return render(request, 'main/pages/index.html', context)


def user_signup(request):
    context = {

    }
    if request.is_ajax():
        response_data = {}

        postEmail = request.POST.get('email')
        postUsername = request.POST.get('username')
        postPassword = request.POST.get('password')

        user = User(email=postEmail, username=postUsername)
        user.set_password(postPassword)
        try:
            user.save()

        except IntegrityError as e:
            response_data['status'] = False
            response_data['msg'] = '이미 가입되어있는 이메일입니다.'
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json"
                                )
        response_data['status'] = True
        response_data['msg'] = '가입이 완료되었습니다.'

        return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )


    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()

        else:
            form = UserCreationForm()

        context.update({'form': form})
        return render(request, 'main/pages/signup.html', context)


def user_login(request):

    context = {}

    if request.is_ajax():
        response_data = {}

        postEmail = request.POST.get('email')
        postPassword = request.POST.get('password')

        try:
            user = authenticate(email=postEmail, password=postPassword)
        except:
            return JsonResponse({'error': 'no user'})

        if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'status': 'success'})

        return JsonResponse({})

    # else:
    #     next = ""
    #     if request.method == 'POST':
    #         email = request.POST['email']
    #         password = request.POST['password']
    #         user = authenticate(email=email, password=password)
    #         if user is not None:
    #             if user.is_active:
    #                 login(request, user)
    #                 # Redirect to a success page.
    #                 if request.POST.get('next') == "":
    #                     return redirect('main:index')
    #                 else:
    #                     return HttpResponseRedirect(request.POST.get('next'))
    #             else:
    #                 # Return a 'disabled account' error message
    #                 return HttpResponse('active user 가 아닙니다.')
    #         else:
    #             # Return an 'invalid login' error message.
    #             return HttpResponse('로그인 실패')
    #     else:
    #         next = request.GET.get('next')
    #         context.update({'next':next})
    #         return render(request, 'main/pages/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('main:index')


@login_required
def user_mypage(request, id):
    context = {
        'userId': id
    }

    u = User.objects.get(id=id)
    try:
        a = ApiKey.objects.get(user=u)
        d = Domain.objects.filter(api_key=a)
    except ObjectDoesNotExist:
        pass

    context.update({
        'api_key': a,
        'domains': d
    })

    return render(request, 'main/pages/mypage.html', context)


@login_required
def apikey_new(request):
    context = {}
    if request.method == 'POST':
        ApiKey.objects.generate(request.user)
        return redirect('main:user_mypage', request.user.id)
    else:
        return render(request, 'main/pages/apikey_new.html', context)


@login_required
def domain_new(request):
    context = {}
    if request.method == 'POST':
        domain = request.POST.get('domain')
        parsed_domain = urlparse(domain)

        print(parsed_domain)

        if parsed_domain.path[:9] == '127.0.0.1' or parsed_domain.path[:9] == 'localhost':
            post_domain = parsed_domain.path

        elif parsed_domain.netloc:
            post_domain = parsed_domain.netloc
            if post_domain[:4] == 'www.':
                post_domain = post_domain[4:]
        else:
            post_domain = parsed_domain.path

        try:
            a = ApiKey.objects.get(key=request.POST.get('api_key'))
        except ObjectDoesNotExist:
            print("api key doesn't exist.")
            return redirect('main:user_mypage', request.user.id)

        d = Domain(domain=post_domain, api_key=a)
        d.save()
        return redirect('main:user_mypage', request.user.id)
    else:
        return redirect('main:user_mypage', request.user.id)

