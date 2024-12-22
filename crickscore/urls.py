from crickscore import views
from django.urls import path

urlpatterns = [
    path("",views.boards,name="boards"),
    path("new",views.create_match,name="create_match"),
]