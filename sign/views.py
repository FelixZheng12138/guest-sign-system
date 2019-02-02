from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def index(request):
    # return HttpResponse('hello world')
    return render(request,"index.html")
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username = username,password = password)
        if user is not None:
            auth.login(request,user)
        # if username == 'admin' and password == 'admin123':
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user',username,3600)
            request.session['user'] = username
            return response
            # return HttpResponse('login successful')
            # return HttpResponseRedirect('/event_manage/')
    # return HttpResponse('error: username or password invalide')
    return render(request,"index.html",{'error':'username or password invalid'})
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user','')
    # username = request.session.get('user','')
    # return render(request,"event_manage.html",{'user':username})
    event_list = Event.objects.all()
    username = request.session.get('user','')
    return render(request,"event_manage.html",{"user":username,'events':event_list})
@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get("name","")
    event_list = Event.objects.filter(name__contains=search_name)
    # return HttpResponse(event_list)
    return render(request,'event_manage.html',{'user':username,"events":event_list})
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('user','')
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator,page(paginator.num_pages)
    # return HttpResponse(guest_list)
    return render(request,"guest_manage.html",{"user":username,'guests':contacts})
@login_required
def search_realname(request):
    username = request.session.get('user','')
    search_realname = request.GET.get("realname","")
    guest_list = Guest.objects.filter(realname__contains=search_realname)
    # return HttpResponse(event_list)
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator,page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,"guests":contacts,'realname':search_realname})
@login_required
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)
    return render(request,'sign_index.html',{"event":event})
    # return HttpResponse('签到成功')
@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event,id=eid)
    phone = request.POST.get('phone','')
    print(phone)
    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,"hint":"phone error"})
    result = Guest.objects.filter(phone = phone,event_id=eid)
    if not result:
        return render(request,'sign_index.html',{'event':event,"hint":"phone or eid error"})
    result = Guest.objects.get(phone = phone,event_id=eid)
    if result.sign:
        return render(request,"sign_index.html",{'event':event,"hint":"user has sign in"})
    else:
        Guest.objects.filter(phone = phone,event_id = eid).update(sign = '1')
        guest_sign = Guest.objects.filter(sign = 1,event_id=eid)
        guest_not_sign = Guest.objects.filter(sign = 0,event_id=eid)
        percent = '%s/%s'%(len(guest_sign),len(guest_sign)+len(guest_not_sign))
        # return HttpResponse(percent)
        return render(request,"sign_index.html",{'event':event,"hint":"sign in success",'guest':result,'percent':percent})
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response
