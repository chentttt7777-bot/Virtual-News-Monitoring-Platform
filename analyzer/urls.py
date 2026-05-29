from django.contrib import admin
from django.urls import path, include
from analyzer.views import index
from analyzer import views

urlpatterns = [
    path('bert_file_analyze/', views.bert_file_analyze),
    path('bert_content_analyze/', views.bert_content_analyze),
    path('bert_link_analyze/', views.bert_link_analyze),
    path('roberta_file_analyze/', views.roberta_file_analyze),
    path('roberta_content_analyze/', views.roberta_content_analyze),
    path('roberta_link_analyze/', views.roberta_link_analyze),
    path('upload/', views.upload_file),
    path('generate_pdf/', views.generate_pdf),
]

