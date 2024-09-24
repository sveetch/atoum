from django.urls import path

from .views import (
    BlogIndexView, BlogDetailView,
    ArticleDetailView,
    RecursiveTreeView,
)


app_name = "atoum"


urlpatterns = [
    path("", RecursiveTreeView.as_view(), name="recursive-tree"),
]
