from django.contrib import admin
from django.urls import path, include
from bert import views
urlpatterns = [
    path('bert_file_analyze/', views.bert_file_analyze),
    path('bert_content_analyze/', views.bert_content_analyze),
    path('bert_link_analyze/',views.bert_link_analyze),
]