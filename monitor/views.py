from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ScreenStream

# Create your views here.
def home(request):
    return render(request,'monitor/home.html')

@login_required(login_url='login')
def storedvideo(request):
    videos = ScreenStream.objects.all()  # Fetch all videos from the database
    context = {'videos': videos}
    return render(request,'monitor/video.html',context)

@login_required(login_url='login')
def multiplestream(request):
    return render(request,'monitor/multiple-stream.html')

@login_required(login_url='login')
def livestream(request):
    return render(request,'monitor/live-stream.html')


def admin_das(request):
    return render(request,'monitor/admin.html')


def loginPage(request):
    context={}
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'You have successfully logged in!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    
        messages.error(request, 'The username or password is incorrect.')
    return render(request,'login.html') 


    
def signupPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'signup.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'signup.html')

        # Create new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # Show success message
        messages.success(request, "User created successfully. Please login.")
        return redirect('login')  # Redirect to login page

    return render(request, 'signup.html')

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    messages.success(request,"successfully logged out")
    return redirect('login')