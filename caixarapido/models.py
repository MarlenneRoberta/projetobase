from operator import contains
from typing import Container
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db import models

from django.urls import include, path
from rolepermissions.decorators import has_permission_decorator
from datetime import datetime
from django.shortcuts import render, redirect


# Create your models here.
class Gerenciar_conta(models.Model):
    #SOLICITAR SALDO***
    def __init__(self, valor_total_conta):
        self.valor_total_conta >= 0.00
        valor_total_conta == (self.saldo_atual - self.realizar_saque + self.valor_deposito - self.realizar_transferencia + self.receber_transferencia)
        return (valor_total_conta)

    #CRIAÇÃO DE USUÁRIOS
    def cadastrar_usuario(request):
        if request.method == "POST":
            form_usuario = UserCreationForm(request.POST)
            if form_usuario.is_valid():
                form_usuario.save()
            return redirect('index')#alterar retorno
        else:
            form_usuario = UserCreationForm()
        return render(request, 'cadastro.html', {'form_usuario': form_usuario})#alterar retorno
    
    #USUÁRIO LOGAR
    def logar_usuario(request):
        if request.method == "POST":
            cpf = request.POST["username"]
            senha = request.POST["password"]
            usuario = authenticate(request, username=cpf, password=senha)
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
            form_senha = PasswordChangeForm(request.usuario, request.POST)
            if form_senha.is_valid():
                usuario = form_senha.save()
                update_session_auth_hash(request, usuario)
                return redirect('index')#alterar retorno
        else:
            form_senha = PasswordChangeForm(request.usuario)
        return render(request, 'alterar_senha.html', {'form_senha': form_senha})#alterar retorno
    
    #USUÁRIO ENCERRAR CONTA
    @has_permission_decorator('gerente', 'cliente')
    @login_required(login_url='/logar_usuario')
    def encerrar_conta(request):
        if request.method == "POST":
            form_usuario = UserCreationForm(request.POST)
            if form_usuario.is_valid():
                form_usuario.save()
                return redirect('cadastro_usuario.html')#alterar retorno
        else:
            form_usuario = UserCreationForm()
        return render(request, 'login.html', {'form_usuario': form_usuario})
    
    @has_permission_decorator('gerente')
    def status_conta(self):
        if self.encerrar_conta == True:
            self.cadastro_encerrado.save()
            return redirect ('index')
        else:
            self.cadastro_ativo.save()
            return redirect ('index')

    #SOLICITAR EXTRATO
class Historico(UserCreationForm):
    class Meta:
        ordering = ('descricao',)

        descricao = models.CharField(max_length=50)

        def __unicode__(self):
            return (self.descricao)

    class Pessoa(models.Model):
        class Meta:
            ordering = ('cpf',)

        cpf = models.CharField(max_length=11)
        senha = models.CharField(max_length=6, blank=True)

        def __unicode__(self):
            return self.cpf

CONTA_OPERACAO_DEBITO = 'd'
CONTA_OPERACAO_CREDITO = 'c'
CONTA_OPERACAO_CHOICES = (
    (CONTA_OPERACAO_DEBITO, ('Debito')),
    (CONTA_OPERACAO_CREDITO, ('Credito')),
)

CONTA_STATUS_APAGAR = 'a'
CONTA_STATUS_PAGO = 'p'
CONTA_STATUS_CHOICES = (
    (CONTA_STATUS_APAGAR, ('A Pagar')),
    (CONTA_STATUS_PAGO, ('Pago')),
)


class Conta(models.Model):
    class Meta:
        
        ordering = ('-data_vencimento', 'valor')

        pessoa = models.ForeignKey('Pessoa', on_delete=models.SET (Historico))
        historico = models.ForeignKey('Historico', on_delete=models.SET (Historico))
        data_vencimento = models.DateField()
        data_pagamento = models.DateField(null=True, blank=True)
        valor = models.DecimalField(max_digits=15, decimal_places=2)
        operacao = models.CharField(

            max_length=1,
            default= CONTA_OPERACAO_DEBITO,
            choices= CONTA_OPERACAO_CHOICES,
            blank=True,
            )

        status = models.CharField(
            max_length=1,
            default= CONTA_STATUS_APAGAR,
            choices= CONTA_STATUS_CHOICES,
            blank=True,
            )

        descricao = models.TextField(blank=True)

        class ContaPagar(Container):
            def save(self, *args, **kwargs):
                self.operacao = CONTA_OPERACAO_DEBITO
                super(self.ContaPagar, self).save(*args, **kwargs)

        class ContaReceber(Container):
            def save(self, *args, **kwargs):
                self.operacao = CONTA_OPERACAO_CREDITO
                super(self.ContaReceber, self).save(*args, **kwargs)

        class Pagamento(models.Model):
            class Meta:
                abstract = True

            data_pagamento = models.DateField()
            valor = models.DecimalField(max_digits=15, decimal_places=2)

        class PagamentoPago(Pagamento):
            conta = models.ForeignKey('ContaPagar', on_delete=models.SET (Historico))

            transferencia_realizada = models.ForeignKey('ContaPagar', on_delete=models.SET (Historico))
            saque = models.ForeignKey('ContaPagar', on_delete=models.SET (Historico))


        class PagamentoRecebido(Pagamento):
            conta = models.ForeignKey('ContaReceber', on_delete=models.SET (Historico))

            deposito = models.ForeignKey('ContaReceber', on_delete=models.SET (Historico))
            transferencia_recebida = models.ForeignKey('ContaReceber', on_delete=models.SET (Historico))

        @has_permission_decorator('gerente', 'cliente')    
        def solicitacao_extrato(self, request, usuario):
            input_data_inicial = input('DATA INICIAL:')
            input_data_final = input('DATA FINAL: ')
            data_inicial = datetime.strptime(input_data_inicial, '%d/%m/%y')
            data_final = datetime.strptime(input_data_final, '%d/%m/%y')

            diferenca = data_final.date() - data_inicial.date()
            print(diferenca.days) # diferença em dias
            
            while True:
                try:
                    input_data_inicial = input('DATA INICIAL: ')
                    data_inicial = datetime.strptime(input_data_inicial, '%d/%m/%y')
                    input_data_final = input('DATA FINAL: ')
                    data_final = datetime.strptime(input_data_final, '%d/%m/%y')
                    break
                except ValueError:
                    print('Data em formato inválido, tente novamente')
                    
            self.horario_transferencia_realizada = datetime.now()
            self.horario_transferencia_recebida = datetime.now()
            self.horario_deposito = datetime.now()
            self.horario_saque = datetime.now()

            self.valor_transferencia_realizada
            self.valor_transferencia_recebida
            self.valor_depósito
            self.valor_saque


            return ()

class Gerenciar_transacoes(models.Model):

    @has_permission_decorator('gerente', 'cliente')
    def __init__(self):
        self.valor_total_conta = self.saldo_atual
        self.ultima_atualizacao = (self.saldo_atual - self.valor_possivel)
        self.numero_da_conta = self.conta_destino

    @has_permission_decorator('gerente', 'cliente')
    def realizar_transferencia (self, horario_transferencia_realizada):
        self.horario_transferencia_realizada = datetime.now()
        if horario_transferencia_realizada.hour >= datetime.time(9,00,0) & self.horario_transferencia_realizada.hour < datetime.time(18,00,0) & self.valor_transferencia_realizada <= 1000.00:
            self.valor_taxa = 5.00
            return (self.valor_transferencia + self.valor_taxa)
        elif self.horario_transferencia_realizada.hour < datetime.time(9,00,0) | self.horario_transferencia_realizada.hour >= datetime.time(18,00,0) & self.valor_transferencia_realizada <= 1000.00:
            self.valor_taxa = 7.00
            return (self.valor_transferencia_realizada + self.valor_taxa)
        elif self.valor_transferencia_realizada > 1000.00:
            self.taxa_extra = 10.00
            return (self.valor_transferencia_realizada + self.taxa_extra)

    def tensferencia_possivel(self, valor_total_conta):
        self.valor_total_conta = valor_total_conta
        
        if (valor_total_conta < (self.valor_transferencia + self.valor_taxa)) :
            return ('Saldo insuficiente', self.valor_total_conta)
        else:
            return (self.realizar_transferencia)

    class Saque(models.Model):
        horario_saque = datetime.now()

        @has_permission_decorator('gerente', 'cliente')
        def __init__(self, valor_total_conta):
            self.valor_total_conta = self.saldo_atual
            self.ultima_atualizacao = (self.saldo_atual - self.valor_transferencia) + self.valor_deposito - self.valor_saque
            if valor_total_conta == 0.00 & valor_total_conta < self.valor_saque:
                return ('Saldo insuficiente', self.valor_total_conta)
            else:
                def realizar_saque (self):
                    self.horario_saque = datetime.now()
                    return ('Valor sacado com sucesso!', self.valor_saque == True)


