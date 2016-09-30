from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Users
from .forms import UserForm


# Create your views here.
def index(request):
    return render(request, 'users/index.html', {})


def listUsers(request):
    users = Users.objects.order_by('-date_entered').all()
    context = {'users': users}
    return render(request, 'users/list.html', context)


def add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = Users(name=request.POST['name'], email=request.POST['email'])
            user.save()
            return HttpResponseRedirect('/list/')
    else:
        form = UserForm()
    return render(request, 'users/add.html', {'form': form})

