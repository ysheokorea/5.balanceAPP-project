from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http.request import validate_host
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User

# Login
from django.contrib import auth

# Reset_Password
from validate_email import validate_email

# Message
from django.contrib import messages
from django.core.mail import EmailMessage, message
from django.core import mail
from django.core.mail import send_mail

# Email
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token
from django.contrib import auth
import threading

# User Verification
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned




# Create your views here.
def index(request):
    return render(request, '/')


# class that can be used for email login
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try: #to allow authentication through phone number or any other field, modify the below statement
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")
    
    
    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]

        if email and password:
            user = auth.authenticate(username=email, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome ' + user.username + " you are logged in")
                    return redirect('/')
                messages.error(request, "Account is not activated")
                return redirect('authentication:login')
            messages.error(request, "Invalid Credentials")
            return redirect('authentication:login')
        messages.error(request, "Please Fill Forms")
        return redirect('authentication:login')

class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, "You have logged out")
        return redirect('authentication:login')


    def post(self, request):
        auth.logout(request)

        messages.success(request, "You have logged out")
        return redirect('authentication:login')


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        context = {
            'fieldsValue' : request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                
                if password!=password2: 
                    messages.error(request, "Please Check your password")
                    return render(request, "authentication/register.html", context)

                if len(password) < 6:
                    messages.error(request, "Password is too short!")
                    return render(request, "authentication/register.html", context)
                
                # New account created using "create_user() method"
                user=User.objects.create_user(username=username, email=email)
                user.set_password(password2)
                user.is_active = False
                user.save()                
            

                # Verif ication Email sending
                # EmailMessage Usage
                # 1. getting domain we are on
                # 2. generate relative URL to verify
                # 3. encode uid
                # 4. generate new token

                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                domain=get_current_site(request).domain
                link = reverse('authentication:activate', kwargs={
                    'uidb64':uidb64, 'token': account_activation_token.make_token(user)
                })
                activate_url = 'http://'+domain+link

                # Email Configuration
                email_subject = 'Activate your account'
                email_body = \
                    'Hi there' + user.username + \
                    'Please use link below to verify your account\n' + \
                    activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'nonreply@semycolon.com',
                    [email]
                )
                EmailThread(email).start()
                messages.success(request, "Account created successfully")
                return render(request, 'authentication/register.html')
            messages.success(request, "Email already exists")                
            return render(request, 'authentication/register.html')  
        messages.success(request, "Username already exists ")
        return render(request, 'authentication/register.html')
        
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('authentication:login' + '?message=' + 'User Already Activated')
            if user.is_active:
                return redirect('authentication:login')

            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('authentication:login')
        except Exception as e:
            pass
        return redirect('authentication:login')
        
class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')        

    def post(self, request):
        email = request.POST['email']
        context = {
            'fieldsValue' : request.POST
        }
        if not validate_email(email):
            messages.error(request, 'Please Check your email address')
            return render(request, 'authentication:reset_password')

        user = User.objects.filter(email=email)
        current_site = get_current_site(request)

        email_content = {
            'user' : user[0],
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token' : PasswordResetTokenGenerator().make_token(user[0]),
        }

        if user.exists():
            link = reverse('authentication:set_new_password', 
                kwargs={'uidb64':email_content['uid'], 'token' : email_content['token']})
            
            email_subject = "Password Reset Instructions"
            reset_url = 'http://'+current_site.domain+link
            email_body = \
                'Hi there, ' + user[0].username + \
                'Please use link below to reset your password\n' + \
                reset_url
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@testservice.com',
                [email]
            )
            EmailThread(email).start()
        messages.success(request, "We have sent you an email to reset password")
        return render(request, 'authentication/reset-password.html')



class CompleteResetPassword(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64' : uidb64,
            'token' : token,
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator.check_token(user, token):
                messages.error(request, "Password Link is Invalid, Please request a new one")
                return render(request, 'authentication/reset-password.html', context)
        except Exception as e:
            pass

        return render(request, 'authentication/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64' : uidb64,
            'token' : token,
        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Please check your password")
            return render(request, 'authentication/set-new-password.html', context)

        if len(password) < 6:
            messages.error(request, "Password is too short")
            return render(request, 'authentication/set-new-password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password2)
            user.save()

            messages.success(request, "Password reset successfully")
            return redirect('authentication:login')
        
        except Exception as e:
            messages.error(request, "Something went wrong, try again")
            return render(request, 'authentication/set-new-password.html', context)

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)      

        