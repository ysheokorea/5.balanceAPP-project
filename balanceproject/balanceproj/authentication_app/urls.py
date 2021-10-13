from django.urls import path
from . import views

app_name="authentication"

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.RegistrationView.as_view(), name="register"),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name="activate"),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('reset-password', views.RequestPasswordResetEmail.as_view(), name="reset_password"),
    path('set-new-password/<uidb64>/<token>', views.CompleteResetPassword.as_view(), name="set_new_password"),

]