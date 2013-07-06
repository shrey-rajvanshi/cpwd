# Create your views here.
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from home.models import *
#from django.utils import timezone
from datetime import datetime
from work.models import *



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
    progr = Work.objects.filter(date_start__lte=datetime.now()).filter(progress= 0).count()
    comple = 0
    comple += Work.objects.filter(date_start__lte=datetime.now()).filter(stipulated_date__lte=datetime.now()).count()
    remk = 0
    remk += Work.objects.filter(progress=100).filter(remarks= '').count()
    hdacc = 0
    hdacc += Work.objects.filter(final_amt__gte=1).filter(head_acc = '').count()
    nitdt = 0
    nitdt += Work.objects.filter(tender_amt__gte=1).filter(agmnt_no= '').count()
    result= {'Progress not updated': progr, 'Completion time passed': comple, 'Remarks not updated':remk, 'Head of Account not added':hdacc, 'Agreement number and Agency not added':nitdt}

    return render(request,'home.html',{'content':content,'alerts':alerts,'result':result})

def searchHome(request, num):
    return [Work.objects.filter(final_amt__gte=1).filter(head_acc = ''),Work.objects.filter(date_start__lte=datetime.now()).filter(stipulated_date__lte=datetime.now()),Work.objects.filter(date_start__lte=datetime.now()).filter(progress= 0),Work.objects.filter(progress=100).filter(remarks= ''),Work.objects.filter(tender_amt__gte=1).filter(agent_no= '')][num-1]
    """
    listprogr = Work.objects.filter(date_start__lte=datetime.now()).filter(progress= 0)
    listcomple = Work.objects.filter(date_start__lte=datetime.now()).filter(stipulated_date__lte=datetime.now())
    listremk = Work.objects.filter(progress=100).filter(remarks= '')
    listhdacc = Work.objects.filter(final_amt__gte=1).filter(head_acc = '')
    listnitdt = Work.objects.filter(tender_amt__gte=1).filter(agent_no= '')

	check it once

    """

def searchr(request, num):
    num=int(num)
    arr=searchHome(request, num)
    alerts=Alert.objects.all()
    return render(request,"results.html",{'list':arr,'alerts':alerts})

