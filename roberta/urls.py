from django.contrib import admin
from django.urls import path, include
from roberta import views
urlpatterns = [
    path('roberta_file_analyze/', views.roberta_file_analyze),
    path('roberta_content_analyze/', views.roberta_content_analyze),
    path('roberta_link_analyze/', views.roberta_link_analyze),
]