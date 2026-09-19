from django.urls import path

from apps.common import views

app_name = "common"

urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.health, name="health"),
]
