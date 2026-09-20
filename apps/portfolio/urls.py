from django.urls import path

from apps.portfolio import views

app_name = "portfolio"

urlpatterns = [
    path("", views.home, name="home"),
    path("work/<slug:slug>/", views.case_study, name="case_study"),
    path("contact/", views.contact, name="contact"),
]
