from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import AuthenticationForm


app_name = "accounts"


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            form_class=AuthenticationForm,
            template_name="accounts/login.html",
        ),
        name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
