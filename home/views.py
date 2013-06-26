# Create your views here.
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from home.models import *

def start(request):
    alerts = Alert.objects.all()
    if request.user.is_authenticated():
        return HttpResponseRedirect("home/")
    if request.POST:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username','')
            password =request.POST.get('password','')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:         #see if the user is in the correct category
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page according to his category.
                return HttpResponseRedirect("../../home/")
            else:
                return HttpResponse("account is invalid")
        else:
            message = "invalid account username or password"
            return render(request,'start.html',{'form':form,'message':message,'alerts':alerts})

    else:
        form = AuthenticationForm()
    return render(request,'start.html',{'form':form})
@login_required
def home(request):
    alerts = Alert.objects.all()
    content = "User Profile"
    tabs = Tab.objects.all()
    return render(request,'home.html',{'content':content,'tabs':tabs,'alerts':alerts})
