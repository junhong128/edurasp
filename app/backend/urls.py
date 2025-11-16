from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('practice/', views.test, name='practice'),
    path('api/check-answer/', views.check_answer, name='check_answer'),
    path('api/next-question/', views.next_question, name='next_question'),
]