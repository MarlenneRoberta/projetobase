from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from bop.api import grant, revoke
from rolepermissions.roles import assign_role, get_user_roles

from rolepermissions.decorators import has_role_decorator, has_permission_decorator
# Create your views here.

@has_role_decorator('gerente')
def caixarapido(request):
    print(get_user_roles(request.user))
    grant(request.user, 'cadastros_ativos', 'cadastros_encerrados', 'reativar_cadastro', 'gerenciar_usuario', 'gerenciar_conta', 'gerenciar_transacoes')
    return HttpResponse(request.user, 'ver cadastros ativos e encerrados')


@has_permission_decorator('cliente')
def editar_cadastro(request):

    revoke(request.user, 'ver_cadastros_ativos', 'ver_cadastros_encerrados', 'reativar_cadastro')
    grant(request.user, 'gerenciar_usuario', 'gerenciar_conta', 'gerenciar_transacoes')
    return HttpResponse(request.user, 'Altere aqui seus dados')

@has_permission_decorator('gerente', 'cliente')
def criar_usuario(request):
    user = User.obects.create_user(username="caio", password="1234")
    user.save()
    assign_role(user, 'cliente')
    return HttpResponse(request.user, 'Usuário salvo com sucesso')