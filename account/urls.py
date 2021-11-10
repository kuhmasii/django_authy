from django.urls import path
from . import views


app_name = "account"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.register_view, name="register_view"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view")
]

