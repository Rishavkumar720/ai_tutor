from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.tutor_view, name="tutor"),

    path("dashboard/", views.dashboard, name="dashboard"),

    # ✅ Auth URLs
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page="login"),   
        name="logout"
    ),
     path("register/", views.register, name="register"),
]
