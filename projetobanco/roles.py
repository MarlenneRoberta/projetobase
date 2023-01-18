
from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {'ver_cadastros_ativos':True, 'ver_cadastros_encerrados': True, 'gerenciar_usuario':True, 'reativar_cadastro': True, 'gerenciar_conta':True, 'gerenciar_transacoes':True}

class Cliente(AbstractUserRole):
    available_permissions = {'gerenciar_usuario':True, 'gerenciar_conta':True, 'gerenciar_transacoes':True}
    