from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.urls import include, path
from django.utils import datetime
from django.shortcuts import render, redirect


# Create your models here.
class Gerenciar_conta(models.Model):
    #CRAIÇÃO DE USUÁRIOS
    def cadastrar_usuario(request):
        if request.method == "POST":
            form_usuario = UserCreationForm(request.POST)
            if form_usuario.is_valid():
                form_usuario.save()
            return redirect('index')#alterar retorno
        else:
            form_usuario = UserCreationForm()
        return render(request, 'cadastro.html', {'form_usuario': form_usuario})#alterar retorno
    
    #UÁRIO LOGAR
    def logar_usuario(request):
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            usuario = authenticate(request, username=username, password=password)
            if usuario is None:
                form_login = AuthenticationForm()
            else:
                login(request, usuario)
                return redirect('index')
            return render(request, 'login.html', {'form_login': form_login})

    #REDIRECIONAR PÁGINAS
    @login_required(login_url='/logar_usuario')
    def index(request):
        return render(request, 'index.html')#alterar retorno

    @login_required(login_url='/logar_usuario')
    def deslogar_usuario(request):
        logout(request)
        return redirect('index')#alterar retorno

    #USUÁRIO ALTERAR SENHA
    @login_required(login_url='/logar_usuario')
    def alterar_senha(request):
        if request.method == "POST":
            form_senha = PasswordChangeForm(request.user, request.POST)
            if form_senha.is_valid():
                user = form_senha.save()
                update_session_auth_hash(request, user)
                return redirect('index')#alterar retorno
        else:
            form_senha = PasswordChangeForm(request.user)
        return render(request, 'alterar_senha.html', {'form_senha': form_senha})#alterar retorno
    
    #USUÁRIO ENCERRAR CONTA
    def encerrar_conta(request):
        if request.method == "POST":
            form_usuario = UserCreationForm(request.POST)
            if form_usuario.is_valid():
                form_usuario.save()
                return redirect('index')#alterar retorno
        else:
            form_usuario = UserCreationForm()
        return render(request, 'cadastro.html', {'form_usuario': form_usuario})

    #SOLICITAR SALDO
    def __init__(self, valor_total_conta, ultima_atualizacao, realizar_saque):
        self.valor_total_conta >= 0.00
        valor_total_conta == self.saldo_atual - realizar_saque + valor_deposito - realizar_transferencia
        return (self.valor_total_conta)

    #SOLICITAR EXTRATO
    def solicitacao_extrato(self, ):

        self.horario_transferencia_realizada = datetime.now()
        self.horario_transferencia_recebida = datetime.now()
        self.horario_deposito = datetime.now()
        self.horario_saque = datetime.now()

        self.valor_transferencia_realizada = 
        self.valor_transferencia_recebida = 
        self.valor_depósito =
        self.valor_saque = 


        return ()

class Gerenciar_transacoes(models.Model):