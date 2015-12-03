from django.shortcuts import render, redirect
from main.forms import UserForm, UserCreationForm
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