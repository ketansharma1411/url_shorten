import http
from random import choice, randint, random
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from url.models import operation, signin
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request,'home.html')

def add_signin_info(request):               #signin
    user=request.POST.get('username')
    email1=request.POST.get("email")
    passw=request.POST.get("password")
    #--------------------------------------------------------------
    #imposing restrictions on duplicate entry
    data=signin.objects.filter(username=user) 
    if len(data)!=0:
        return JsonResponse("USER ALREADY EXSISTS",safe=False)
    #--------------------------------------------------------------
    ot=otp(4)
    
    object=signin(username=user,email=email1,password=passw,otp=ot,is_verified=0)
    object.save()
    

    send_mail('verification','This mail is regarding the email verification your otp for verification is'+ot,'sendermail33@gmail.com',[email1])
    
    return JsonResponse("records have been added successfully",safe=False)

def verify_email(request):                  #integrated with sigin page
    user=request.POST.get('username')
    otp_u=int(request.POST.get('otp'))
    data=signin.objects.filter(username=user)
    otp_d=int(data[0].otp)
    if otp_u==otp_d:
        signin.objects.filter(username=user).update(is_verified=1)
        return HttpResponse("EMAIL VERIFIED SUCCESSFULLY")
    else:
        return JsonResponse("EMAIL VERIFICATION FAILED",safe=False)
    

def pass_generator(size):                    #utility Function
    passw=''
    char='abcdefghijklmnopqurstuvwxyzABCDEFGHIJKLMNOPQURSTUVWXYZ!@#&1234567890'
    for i in range(size):
        passw+=choice(char)
    return passw




def login(request):                     #login
    user=request.POST.get('username')
    passw=request.POST.get("password")
    data=signin.objects.filter(username=user,password=passw)
    if len(data)==0:
        return JsonResponse("BAD CREDENTIALS",safe=False)
    param={'username':user}
    return render(request,"login_items.html",param)
    
    # em=int(data[0].is_verified)
    # if em==1:
    #     return JsonResponse('LOGIN SUCCESSFULL',safe=False)
    # else:
    #     return JsonResponse("Please Verify emailID",safe=False)

def otp(digit):                         #utility Function
    result=''
    for i in range(digit):
        ott=randint(0,9)
        result=result+str(ott)
    return result

def forget_password(request):               #forget_password
    user=request.POST.get("username")
    
    data=signin.objects.filter(username=user)
    if len(data)==0:
        return JsonResponse("USER NOT FOUND",safe=False)
    em=data[0].email
    verify_status=data[0].is_verified
    if verify_status==1:
        new_password=pass_generator(8)
        send_mail('recovery email','This Email contains your recovery password.Kindly do not disclose this with any one :: '+str(new_password),'sendermail33@gmail.com',[em])
        signin.objects.filter(username=user).update(password=new_password)
        return HttpResponse("PASSWORD HAS BEEN UPDATED SUCCESSFULLY")
    else:
        return HttpResponse('User Name Found, but sorry Your Email is not verified!!! Kindly contact the helpline number 1800 1800 500 to recover your account.')

def change_password(request):
    user=request.POST.get("username")
    passw=request.POST.get("password")
    new_passw=request.POST.get("new_passw")
    data=signin.objects.filter(username=user,password=passw)
    if len(data)==0:
        return JsonResponse("BAD CREDIENTIALS",safe=False)
    
    signin.objects.filter(username=user).update(password=new_passw)
    return HttpResponse("YOUR PASSWORD HAS BEEN UPDATED SUCCESSFULLY")


def add_info(request):                      #urleditor(home)
    long_url=request.POST.get("long")
    short_url=request.POST.get("short")
    user=request.POST.get("username")
    data1=signin.objects.filter(username=user)
    if len(data1)==0:
        user_id=0
    else:
        user_id=data1[0].id
    data=operation.objects.filter(short_url='ket/'+short_url)
    if len(data)==0:
        object=operation(long_url=long_url,short_url='ket/'+short_url,user_id=user_id)
        object.save()
        return JsonResponse("data added successfully",safe=False)
    else:
        return JsonResponse('please select another short url',safe=False)
    
def short_long(request):                    #fetching_url
    short=request.POST.get("short")
    data=operation.objects.filter(short_url='ket/'+short)
    #print(len(data))
    if len(data)==0:
        return JsonResponse("invalid",safe=False)
    long=data[0].long_url
    d={"long_url":long}
    return render(request,'fetching_url.html',d)
   
def user_history(request):
    user=request.POST.get("username")
    data=operation.objects.filter(username=user)
    
    if len(data)==0:
        return JsonResponse("USER HAS NO HISTORY",safe=False)
    result={}
    for i in data:
        result={i.short_url:i.long_url}
        print(result)
    return render(request,'history.html',result)
    # return JsonResponse(result)
    


