from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'auth/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/index.html')

