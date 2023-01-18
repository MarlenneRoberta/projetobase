
from django.urls import path
from . import views

urlpatterns = [
    path('usuario/', views.criar_usuario),
    path('', views.caixarapido)
]
