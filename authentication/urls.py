from authentication import views
from django.urls import path

urlpatterns = [
    path("login",views.user_login,name="user_login"),
    path("logout",views.user_logout,name="user_logout"),
    path("signup",views.user_register,name="user_register"),
    path("menu",views.menu,name="menu"),
]