from django.urls import path

from apps.portfolio import views

app_name = "portfolio"

urlpatterns = [
    path("", views.project_list, name="list"),
    path("<str:slug>/", views.project_detail, name="detail"),
]
