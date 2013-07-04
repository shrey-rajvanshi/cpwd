# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import Group

from home.models import *
from work.models import *
from work.forms import *
from work.xls import *

drawing_fields = ['name', 'project_code', 'requisition', 'pe_det', 'pe_date', 'pe_amt', 'pe_sent_to', 'client', 'aa_es_detail', 'head_acc', 'final_amt', 'auth', 'no_sub', 'ts_detail', 'ts_date', 'ts_amt', 'time_allowd', 'nit', 'nit_date']
accounts_fields = ['nit_amt', 'agency', 'agency_add', 'agent_no', 'tender_amt', 'date_start', 'stipulated_date', 'actual_date', 'status', 'expense', 'progress']

@login_required
def search(request):
    alerts = Alert.objects.all()
    if request.POST:
        form = Searchform(request.POST)
        if form.is_valid():
            pr_name = request.POST.get('project_name','')
            #pr_code = request.POST.get('pr_code',0)
            pr_agency = request.POST.get('project_agency','')
            work_list=searchinwork(pr_name,pr_agency)
            return render(request,"results.html",{'list':work_list,'name':pr_name,'agency':pr_agency,'alerts':alerts})
    else:
        form = Searchform
    return render(request,'search.html',{'form':form,'alerts':alerts})

def searchinwork(par_name,par_agency):
    list = Work.objects.filter(name__icontains = par_name,agency__icontains = par_agency)
    return list

@login_required
def draw(request,id):
    alerts = Alert.objects.all()
    w = Work.objects.get(id=id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print request.FILES['file']
        if request.FILES:
            newdoc = Document(docfile = request.FILES['file'],relwork = w)
            newdoc.save()
            status(w)
            w.save()
            return HttpResponse('drawing added')
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = w.document_set.all()

    # Render list page with the documents and the form
    return render_to_response(
        'drawings.html',
            {'documents': documents,'alerts':alerts,'form': form,'work':w},
        context_instance=RequestContext(request)
    )


@login_required
def add(request):
    alerts = Alert.objects.all()
    if request.POST:
        form = Addworkform(request.POST)
        if form.is_valid():
            work = form.save()
            status(work)
            work.save()
            return render(request,'addwork.html',{'message':'work added successfully','form':form,'alerts':alerts})
        else:
            return render(request,'addwork.html',{'message':'There was an error in you request','form':form,'alerts':alerts})
    else:
        form = Addworkform()
        return render(request,'addwork.html',{'form':form,'alerts':alerts})
@login_required
def all(request):
    alerts = Alert.objects.all()
    list = Work.objects.all().order_by('status')
    return render(request,"results.html",{'list':list,'alerts':alerts})

def edit_admin(request,id):
    work = Work.objects.get(pk=id)
    alerts = Alert.objects.all()

    if request.POST:
        form = Addworkform(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            work = Work.objects.get(id=id)
            work.delete()
            work=form.save()
            status(work)
            work.save()
            return render(request,'addwork.html',{'work':work,'message':'work edited successfully','form':form,'alerts':alerts})
        else:
            return render(request,'addwork.html',{'work':work,'message':'There was an error in you request','form':form,'alerts':alerts})
    else:
        form = Addworkform(instance =work)
        return render(request,'addwork.html',{'work':work,'form':form,'alerts':alerts})




@login_required
def edit(request,id):
    work = Work.objects.get(pk=id)
    alerts = Alert.objects.all()
    user_groups = request.user.groups.all()
    drawing_group = accounts_group = False
    for group in user_groups:
        if group.name == 'drawing':
            drawing_group = True
        if group.name == 'accounts':
            accounts_group = True
        if group.name == 'EE':
            edit_admin(request,id)

    global drawing_fields
    global accounts_fields

    if request.POST:
        form = Addworkform(request.POST)
        fieldset = []
        if drawing_group:
            fieldset.extend(drawing_fields)
        if accounts_group:
            fieldset.extend(accounts_fields)

        """ Remove duplicates, not using sets so that order is preserved"""
        output = []
        for x in fieldset:
            if x not in output:
                output.append(x)

        remove_fields = []

        for field in form.fields:
            if str(field) not in output:
                remove_fields.append(str(field))

        work_fields = work.get_fields()

        for field in remove_fields:
            form.fields.pop(field)

        if form.is_valid():
            data=form.cleaned_data
            work = Work.objects.get(id=id)
            for item in output:
                setattr(work, item, data[item])
            status(work)
            work.save()
            return render(request,'editwork.html',{'work':work, 'message': 'Work edited successfully!','form':form, 'work_fields':work_fields, 'fields_list':output, 'alerts':alerts})
        else:
            return render(request,'editwork.html',{'work':work,'message':'There was an error in you request','form':form, 'work_fields':work_fields, 'fields_list':output,'alerts':alerts})
    else:
        form = Addworkform(instance =work)
        fieldset = []
        if drawing_group:
            fieldset.extend(drawing_fields)
        if accounts_group:
            fieldset.extend(accounts_fields)

        """ Remove duplicates, not using sets so that order is preserved"""
        output = []
        for x in fieldset:
            if x not in output:
                output.append(x)

        remove_fields = []

        for field in form.fields:
            if str(field) not in output:
                remove_fields.append(str(field))

        work_fields = work.get_fields()

        for field in remove_fields:
            form.fields.pop(field)

        return render(request,'editwork.html',{'work':work,'form':form, 'work_fields':work_fields, 'fields_list':output, 'alerts':alerts})

@login_required
def xls(request):
    mapping = generate_mapping()
    format_book = open_workbook('media/format.xls')
    format_sheet = format_book.sheet_by_index(0)
    book = Workbook()
    sheet1 = book.add_sheet('Sheet 1')
    for col_index in range(format_sheet.ncols):
        sheet1.write(0,col_index,format_sheet.cell(0,col_index).value)
    for col_name,col_index in mapping.iteritems():
        row_index = 1
        for item in Work.objects.values(col_name):
            sheet1.write(row_index,col_index, item[col_name])
            row_index+=1
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=CPWDdetails.xls'
    book.save(response)
    return response

def status(work):
    if work.progress is 100:
        work.status = 6
    elif work.nit:
        work.status = 5
    elif work.ts_detail:
        work.status = 4
    elif work.pe_det:
        work.status = 3
    elif work.document_set.all().count()>0:
        work.status = 2
    else:
        work.status = 1

def showwork(request,id):
    work = Work.objects.get(id=id)
    alerts = Alert.objects.all()
    drawings = work.document_set.all()
    stats = status_choices[int(work.status)-1][1]
    return render(request,'project_view.html',{'work':work,'stats':stats,'alerts':alerts,'drawings':drawings})

def deldrawing(request,id):
    drawing = Document.objects.get(id=id)
    drawing.delete()
    return HttpResponse("Drawing deleted")

#def dropdrawing(request):