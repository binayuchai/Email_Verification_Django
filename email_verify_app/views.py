from django.shortcuts import render,redirect
from email_verify_app.forms import CustomerRegisterForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from email_verify_app.models import Profile
from django.forms import forms
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required



User = get_user_model()
@login_required
def home(request):
    return render(request,"home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user_pass = request.POST.get("password")
        
        user_obj = User.objects.filter(username = username).first()
        print(user_obj)
        if user_obj is None:
            messages.error(request,"Invalid user")
            return redirect("user:login")
        
        
        profile_obj = Profile.objects.filter(user=user_obj).first()
        
        if not profile_obj.is_verified:
            messages.error(request,"Your account is not verified so check your mail.")
            return redirect("user:login")
        
        valid_user = authenticate(username = username, password = user_pass)
        if valid_user is None:
            messages.error(request,"Invalid email or password")
            return redirect("user:login")
        login(request,valid_user)
        return redirect("user:home")
    return render(request,"login.html")
    






    

# def CustomRegisterView(CreateView):
#     model = User
#     form_class = UserRegisterForm
#     template_name = "register.html"
#     success_url = reverse_lazy("email_user_app:login")
    
    
def register_view(request):

    if request.method == "POST":
        print("POST")
        user_name = request.POST.get("username")
        user_email = request.POST.get("email")
        print(user_name)

        try:       
            form  = CustomerRegisterForm(request.POST)

            if form.is_valid():
                
                user_obj = form.save()
            
            # user_obj = User.objects.get(user_name)   
            print(user_obj) 
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            send_main_after_registration(user_email,auth_token)
            messages.success(request,"User is registered")
            return redirect("user:token_send")
            
                
        except Exception as e:
            print(e)    
            
    else:
        form = CustomerRegisterForm()
        
    return render(request,"register.html",{"form":form})
         
         
def token_send_view(request):
    return render(request,"token_send.html")         

def send_main_after_registration(email, token):
    subject = "Your account need to be verified"
    message =f"Hi, visit the link to verify your account, http://127.0.0.1:8000/verify/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    

def verify(request,auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,"Email has been already verified")
                return redirect("user:login")
                
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,"Email has been verified")
            return redirect("user:login")
        else:
            return redirect("user:error")   
    except Exception as e:
        print(e)
        return redirect("user:error")
        
        

def error_view(request):
    return render(request,"error.html")
