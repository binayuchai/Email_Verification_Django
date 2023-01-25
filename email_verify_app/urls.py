from django.urls import path
from email_verify_app.views import home, login_page

app_name= "email_verify_app"
urlpatterns = [
    path("",home,name="home"),
    path("login/",login_page,name="login_page")
]
