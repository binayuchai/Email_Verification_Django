from django.urls import path
from email_verify_app.views import home,register_view, token_send_view, verify,error_view, login_view

app_name= "user"
urlpatterns = [
    path("",home,name="home"),
    path("login/",login_view,name="login"),
    path("register/",register_view,name="register"),
    path("token-send/",token_send_view,name="token_send"),
    path("verify/<auth_token>/",verify,name="verify"),
    path("error",error_view,name="error"),
]
