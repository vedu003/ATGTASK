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
    user = CustomUser.objects.get(email=cuser)
    user_type = user.user_type

    return render(request, 'app/index.html',{'usr':user, 'user_type':user_type})

def createblog(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    user_type = user.user_type

    if request.method == 'POST':
        title = request.POST['title']
        summary = request.POST['summary']
        content = request.POST['content']
        blogpic = request.FILES['blogpic']
        category = request.POST['category']

        cuser = request.session.get('vendor_email')
        user = CustomUser.objects.get(email=cuser)

        if request.POST.get('draft',''):
                draft = True
        else:
            draft = False

        Blog(user=user,title=title, summary=summary,  content=content, category = category,
                 blogpic=blogpic,draft=draft).save()

        if draft == False:
            msg = 'Your Blog is Successfully Created.'
            blogs = Blog.objects.all()
            return render(request, 'app/displayblog.html',{'msg':msg,'blogs':blogs,'user_type':user_type})
        else:
            msg = 'Your Blog is Drafted.'
            blogs = Blog.objects.filter(draft = True)
            return render(request, 'app/draft.html',{'msg':msg,'blogs':blogs,'user_type':user_type})


    return render(request, 'app/createblog.html',{'user_type':user_type})

def displayblogs(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    blogs = Blog.objects.filter(draft = False)
    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    user_type = user.user_type

    return render(request, 'app/displayblog.html',{'blogs':blogs,'user_type':user_type})

def mycurrblog(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    blogs = Blog.objects.filter(user=user)
    user_type = user.user_type

    return render(request, 'app/mycurrblog.html',{'blogs':blogs,'user_type':user_type})

def draft(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    blogs = Blog.objects.filter(draft = True)
    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    user_type = user.user_type

    return render(request, 'app/draft.html',{'blogs':blogs,'user_type':user_type})

def editdraft(request,id):
    if request.session.get('vendor') == None:
        return redirect('login')

    blogcat = ['Mental Health','Heart Disease','Covid19','Immunization']

    blog = Blog.objects.get(id=id)
    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    user_type = user.user_type


    if request.method == 'POST':
        blog.title = request.POST['title']
        blog.summary = request.POST['summary']
        blog.content = request.POST['content']
        blog.category = request.POST['category']

        if request.POST.get('draft',''):
                draft = True
        else:
            draft = False

        blog.draft = draft
        blog.save()

        if draft == False:
            msg = 'Your Blog is Successfully Created.'
            blogs = Blog.objects.all()
            return render(request, 'app/displayblog.html',{'msg':msg,'blogs':blogs,'user_type':user_type})
        else:
            msg = 'Your Blog is Drafted.'
            blogs = Blog.objects.filter(draft = True)
            return render(request, 'app/draft.html',{'msg':msg,'blogs':blogs,'user_type':user_type})

    return render(request, 'app/editdraft.html',{'blog':blog,'user_type':user_type, 'blogcat':blogcat})


def delblog(request,id):
    if request.session.get('vendor') == None:
        return redirect('login')

    blog = Blog.objects.get(id=id)
    blog.delete()

    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    blogs = Blog.objects.filter(user=user)
    user_type = user.user_type

    return render(request, 'app/mycurrblog.html',{'blogs':blogs,'user_type':user_type})
