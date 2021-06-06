from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Profile
import random
import http.client
# Create your views here.
from django.conf import settings
from django.contrib.auth import authenticate, login

def send_otp(mobile, otp):
    print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY 
    headers = { 'content-type': "application/json" }
    urls = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your otp is "+otp +"&mobile="+mobile+"&authkey="+authkey+"&country=977"
    url = urls.replace(" ", "")
    conn.request("GET", url , headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(res)
    print(data)
    print(url)
    return None



def login_attempt(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')

        user = Profile.objects.filter(mobile = mobile).first()
        
        if user is None:
            context = {
                'message':'USER NOT FOUND','class':"danger"
            }
            return render(request,'login.html',context)
        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()

        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')


    return render(request,'login.html')


def login_otp(request):
    mobile = request.session['mobile']
    context = {
        'mobile':mobile
    }
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            user = User.objects.get(id = profile.user.id)
            login(request, user)
            return redirect('cart')
        else:
            context = {
                'message':'ENTER CORRECT OTP, OTP NOT ACCPETED',
                'class':"danger",
                'mobile': mobile,
            }
            return render(request,'login_otp.html',context)
   
    return render(request,'login_otp.html', context)



def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')

        check_user = User.objects.filter(email = email).first()
        check_profile = Profile.objects.filter(mobile = mobile).first()

        if check_user or check_profile:
            context = {
                'message':'USER ALREADY REGISTER','class':"danger"
            }
            return render(request,'register.html',context)

        user = User(email = email, first_name = name)
        user.save()

        otp = str(random.randint(1000, 9999))

        profile = Profile(user = user, mobile=mobile, otp = otp)
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')

    return render(request,'register.html')

def otp(request):
    mobile = request.session['mobile']
    context = {
        'mobile':mobile
    }
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            return redirect('cart')
        else:
            context = {
                'message':'ENTER CORRECT OTP, OTP NOT ACCPETED',
                'class':"danger",
                'mobile': mobile,
            }
            return render(request,'otp.html',context)
   
    return render(request,'otp.html', context)