from django.urls import path

from .views import StyleguideIndexView


app_name = "styleguide"


urlpatterns = [path("", StyleguideIndexView.as_view(), name="index")]
