from http.client import HTTPResponse
from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def caixarapido(request):
    pass

def criar_usuario(request):
    user = User.obects.create_user(username="caio", password="1234")
    user.save()
    return HTTPResponse('Usuário salvo com sucesso')