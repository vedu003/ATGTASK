from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate
from django.views.decorators.cache import cache_control

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):

    if request.session.get('vendor') != None:
        return redirect('home')

    department = ['patient', 'doctor']

    if request.method == 'POST':
        dname = request.POST['dname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        propic = request.FILES['propic']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if CustomUser.objects.filter(email=email):
            msg = 'You have already regiter email!!!'
            return render(request,'app/register.html',{'department':department,'msg':msg})
            
        if CustomUser.objects.filter(username=username):
            msg = 'Username already exist please try another username.'
            return render(request,'app/register.html',{'department':department,'msg':msg})
        
        if (password == confirm_password):
            usr = CustomUser.objects.create_user(user_type=dname,first_name=fname,last_name=lname,propic= propic,
                                username=username,email=email,password=password,address=address,
                                city=city,state=state,pincode=pincode)
            usr.is_active = True
            usr.is_staff = True
            usr.save()
            return redirect('login')
            
        else:
            msg = "Password are not matched!!!"
            return render(request,'app/register.html',{'department':department,'msg':msg})

    return render(request,'app/register.html',{'department':department})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):

    department = ['patient', 'doctor']

    if request.session.get('vendor') != None:
        return redirect('home')

    if request.method == 'POST':
        dname = request.POST['dname']
        email = request.POST['email']
        pwd = request.POST['password']

        usr = authenticate(email=email,password=pwd)
        
        if usr:
            usr = CustomUser.objects.get(email=email)
            if usr.user_type == dname :
                if (usr.is_staff == True):
                    vendor = {'vendor_name':usr.username,'vendor_email':usr.email}
                    request.session['vendor'] = vendor
                    request.session['vendor_email'] = usr.email
                    return redirect('home')
                else:                
                    return render(request,'app/login.html',{'department':department})
            else:
                msg = "Incorrect Details!!!"
                return render(request,'app/login.html',{'msg':msg,'department':department})
        else:
            msg = "Incorrect Email or Password!!!"
            return render(request,'app/login.html',{'msg':msg,'department':department})
    
    return render(request,'app/login.html',{'department':department})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if (request.session.get('vendor') != None):
        request.session.delete()
        return redirect('login')
    else:
        return redirect('login')

def home(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    cuser = request.session.get('vendor_email')
    usr = CustomUser.objects.get(email=cuser)
    return render(request, 'app/index.html',{'usr':usr})
