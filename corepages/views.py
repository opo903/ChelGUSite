from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def index(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user_groups = user.groups.all()
                if user_groups.filter(name='admin').exists():
                    return redirect('administrator/')
                elif user_groups.filter(name='headman').exists():
                    return redirect('headman/')
                elif user_groups.filter(name='teacher').exists():
                    return redirect('teacher/')
    else:
        form = LoginForm()
    return render(request, 'corepages/startpage.html', {'form': form})