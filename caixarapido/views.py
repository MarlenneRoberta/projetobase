from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from rolepermissions.roles import revoke_permission, grant_permission
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
# Create your views here.

@has_role_decorator('gerente')
def caixarapido(request):
    
    return HttpResponse('ver cadastros ativos e encerrados')


@has_permission_decorator('cliente')
def editar_cadastro(request):

    revoke_permission(request.user, 'ver_cadastros_ativos', 'ver_cadastros_encerrados', 'reativar_cadastro')
    grant_permission(request.user, 'gerenciar_usuario', 'gerenciar_conta', 'gerenciar_transacoes')
    return HttpResponse('Altere aqui seus dados')

def criar_usuario(request):
    user = User.obects.create_user(username="caio", password="1234")
    user.save()
    assign_role(user, 'cliente')
    return HttpResponse(request.user, 'Usuário salvo com sucesso')