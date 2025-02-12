#Dupla = Marcelo Boalento do Nascimento (RA: 24123087-9) e Orlando Nagrockis Bertholdo (RA: 24223003-5)

import os
import datetime
from datetime import timedelta, timezone
Clientes = {}
#Função para mostrar o menu
def menu():
  print("1. Novo Cliente", "\n2. Apaga Cliente", "\n3. Listar clientes", "\n4. Débito", "\n5. Depósito","\n6. Extrato", "\n7. Transferência entre clientes", "\n8. Débito autômatico", "\n9. Sair")
  #Operações que irão aparecer no menu
  return menu

#Função que irá colocar tudo que está em Clientes.txt em um dicionário Clientes
def GuardarClientes(Clientes):
  Clientes = {}
  #abrir o arquivo em modo read e colocar todas as linhas no dicionário Clientes
  arquivo = open("Clientes.txt", "r", encoding= "utf-8")
  for linha in arquivo.readlines():
    # define as varíaveis com base na linha do arquivo, cada varíavel separada pro vírgula
    razão, CNPJ, Tipo, Valor, Senha = linha.strip().split(",")
    CNPJ = int(CNPJ)
    Valor = float(Valor)
    Dados = {'razão' : razão, 
             'CNPJ' : CNPJ,
             'Tipo' : Tipo,
             'Saldo' : Valor,
             'Senha' : Senha}
    Clientes[CNPJ] = Dados
  arquivo.close()
  return Clientes

#Função que irá colocar os dados do cliente no arquiv Clientes.txt
def SalvarClientes(Clientes):
  #abrir o arquivo em modo write
  arquivo = open("Clientes.txt", "w")
  for Dados in Clientes.values():
    #o que será escrito no arquivo
    arquivo.write(f"{Dados['razão']},{Dados['CNPJ']},{Dados['Tipo']},{Dados['Saldo']},{Dados['Senha']}\n")
  arquivo.close()


#Função para a operação 1 de cadastrar um novo cliente
def novoClient(Clientes):
  #Informações para criar novo cliente
  razão = input("Nome da empresa: ")
  CNPJ = int(input("CNPJ da empresa: " ))
  # verifica se já há uma conta vínculada ao cnpj digitado
  if CNPJ in Clientes:
    print("CNPJ já vinculado a um cliente.")
    print()
  else:
    Tipo = input("Tipo de conta (Comum ou Premium): ")
    #verifica se o tipo escolhido é válido
    if Tipo != "Comum" and Tipo != "COMUM" and Tipo != "comum" and Tipo != "c" and Tipo != "C" and Tipo != "Premium" and Tipo != "PREMIUM" and Tipo != "premium" and Tipo != "p" and Tipo != "P":
      print("Tipo de conta inválido.")
      print()
    else:
      Valor = int(input("Valor inicial que deseja colocar na conta: "))
      Senha = input("Digite uma senha: ")
      #armazena esses dados em um dicionário
      Dados = {'razão' : razão, 
               'CNPJ' : CNPJ,
               'Tipo' : Tipo,
               'Saldo' : Valor,
               'Senha' : Senha}
      #coloca esse dicionario Dados dentro do dicionário Clientes vínculado ao CNPJ recebido
      Clientes[CNPJ] = Dados
      print()
      print("Cliente criado com sucesso!")
      print()
      #atualiza o arquivo Clientes.txt para colocar o novo cliente
      SalvarClientes(Clientes)
      
#Função para apagar cliente
def apagaCliente(Clientes):
  
  apagar = int(input("Digite o CNPJ: "))
  #verifica se o CNPJ colocado está no dicionario Clientes e possui uma conta vínculada a ele
  if apagar in Clientes:
    #se sim, irá apagar esse cliente no dicionário
    del Clientes[apagar]
    print()
    print("Cliente apagado com sucesso!")
    print()
  else:
    print("CNPJ não encontrado.")
  #então irá atualizar o arquivo Clientes.txt com o dicionário Clientes atualizado
  SalvarClientes(Clientes)


#Função para listar as informações dos clientes
def listaClientes(Clientes):
  #verifica os clientes cadastrados no dicionário Clientes
  for cnpj, info in Clientes.items():
    razao = info['razão']
    tipoConta = info['Tipo']
    saldo = info['Saldo']
    print()
    #printa tudo que está no dicionário clientes
    print(
        f"CNPJ: {cnpj}\nRazão Social: {razao}\nTipo de conta: {tipoConta}\nSaldo: {saldo}"
    )
  print()

#Função para debitar o dinheiro da conta
def Débito(Clientes):
  #armazena a data que a operação ocorreu para colocar no arquivo extrato.txt
  data = datetime.datetime.now()
  formata = data.strftime("%d/%m/%Y %H:%M:%S")
  #abre o arquivo extrato.txt em modo append
  extrato = open("extrato.txt","a")
  validarcnpj = int(input("Coloque o CNPJ da conta: "))
  validarsenha = input("Coloque a senha da conta: ")
  #verifica se há uma conta vínculada a esse CNPJ no dicionário dos Clientes
  if validarcnpj in Clientes:
    #verifica se a senha da conta vinculada com o CNPJ bate com a senha digitada pelo usuário
    if Clientes[validarcnpj]['Senha'] == validarsenha:
      #pede o valor que deseja debitar
      debito = int(input("Digite o valor que deseja retirar: "))
      #verifica qual o tipo da conta vinculada ao CNPJ
      if Clientes[validarcnpj]['Tipo'].lower() in ['comum', 'c']:
        taxaComum = debito * 0.05
        dinheirofinalc = debito + taxaComum
        #atualiza o saldo do cliente
        Clientes[validarcnpj]['Saldo'] = Clientes[validarcnpj]['Saldo'] - dinheirofinalc
        saldo = Clientes[validarcnpj]['Saldo']
        #verifica se o limite do saldo da conta comum não vai ser excedido
        if saldo >= -1000:
          print()
          print(f"A taxa de operação foi de R${taxaComum}")
          print(f"O valor de R${dinheirofinalc} foi debitado da conta")
          print("Débito realizado com sucesso!")
          print()
          #coloca as informações da operação no arquivo extrato.txt
          extrato.write(
          f"CNPJ: {validarcnpj} {formata} -{debito} Tarifa: {taxaComum} Saldo: {saldo}\n"
          )
          #então irá atualizar o arquivo Clientes.txt com o dicionário Clientes atualizado
          SalvarClientes(Clientes)
        else:
          print("Limite negativo no saldo excedido!")
      else:
        taxaPlus = debito * 0.03
        dinheirofinalp = debito + taxaPlus
        #atualiza o saldo do cliente
        Clientes[validarcnpj]['Saldo'] -= dinheirofinalp
        saldo = Clientes[validarcnpj]['Saldo']
        #verifica se o limite do saldo da conta premium não vai ser excedido
        if saldo >= -5000:
          print()
          print(f"A taxa de operação foi de R${taxaPlus}")
          print(f"O valor de R${dinheirofinalp} foi debitado da conta")
          print("Débito realizado com sucesso!")
          print()
          #coloca as informações da operação no arquivo extrato.txt
          extrato.write(
          f"CNPJ: {validarcnpj} {formata} -{debito} Tarifa: {taxaPlus} Saldo: {saldo}\n"
          )
          #então irá atualizar o arquivo Clientes.txt com o dicionário Clientes atualizado
          SalvarClientes(Clientes)
        else:
          print("Limite negativo no saldo excedido!")
    else:
      print("Senha incorreta!")
  else:
    print("CNPJ não encontrado!")
  extrato.close()

#Função para depositar dinheiro em um cliente
def deposito(Clientes):
  #abre o arquivo extrato.txt em modo append
  extrato = open("extrato.txt","a")
  validarcnpj = int(input("Coloque o CNPJ da conta: "))
  #armazena a data que a operação ocorreu para colocar no arquivo extrato.txt
  data = datetime.datetime.now()
  formata = data.strftime("%d/%m/%Y %H:%M:%S")
  #verifica se há uma conta vínculada a esse CNPJ no dicionário dos Clientes
  if validarcnpj in Clientes:
    #pede o valor a ser depositado
    deposito = int(input("Digite o valor a ser depositado: "))
    #atualiza o saldo do cliente
    Saldo = Clientes[validarcnpj]['Saldo']
    Saldo += deposito
    Clientes[validarcnpj]['Saldo'] = Saldo
    #coloca as informações da operação no arquivo extrato.txt
    extrato.write(
    f"CNPJ: {validarcnpj} {formata} +{deposito} Tarifa: 0.00 Saldo: {Saldo}\n"
    )
    print()
    print("Deposito realizado com sucesso!")
    print(f"O valor de {deposito} R$ foi depositado na conta.")
    print("Seu saldo após deposito é de %d " % Saldo)
    print()
  else:
    print("CNPJ não encontrado!")
  extrato.close()
  #então irá atualizar o arquivo Clientes.txt com o dicionário Clientes atualizado
  SalvarClientes(Clientes)

#Função para mostrar os extratos de um cliente
def Extrato(Clientes):
  validarcnpj = int(input("Coloque o CNPJ da conta: "))
  validarsenha = input("Digite a senha da conta: ")
  #verifica se há uma conta vínculada a esse CNPJ no dicionário dos Clientes
  if validarcnpj in Clientes:
    #verifica se a senha da conta vinculada com o CNPJ bate com a senha digitada pelo usuário
    if Clientes[validarcnpj]['Senha'] == validarsenha:
      #abre o arquivo extrato.txt em modo r
      extrato = open("extrato.txt","r")
      razao = Clientes[validarcnpj]['razão']
      tipo = Clientes[validarcnpj]['Tipo']
      print(f"CNPJ: {validarcnpj}\nRazão social: {razao}\nTipo: {tipo}")
      #lê as linhas do arquivo extrato.txt
      for linha in extrato:
        #verifica se a linha possui o CNPJ
        if str(validarcnpj) in linha:
          #mostra as linhas com aquele CNPJ
          print(linha)
    else:
      print("Senha incorreta!")
  else:
    print("CNPJ não encontrado!")
  


#Função de tranferencia de dinheiro
def transferencia(Clientes):
  #armazena a data que a operação ocorreu para colocar no arquivo extrato.txt
  data = datetime.datetime.now()
  formata = data.strftime("%d/%m/%Y %H:%M:%S")
  #abre o arquivo extrato.txt em modo append
  extrato = open("extrato.txt","a")
  validarcnpj1 = int(input("Digite o CNPJ da conta de origem: "))
  validarsenha = input("Digite a senha do CNPJ de origem: ")
  validarcnpj2 = int(input("Digite o CNPJ da conta de destino: "))
  #verifica se o CNPJ do cliente de origem e de destino estão no dicionário Clientes
  if validarcnpj1 in Clientes and validarcnpj2 in Clientes:
    #verifica se a senha da conta de origem vinculada com o CNPJ bate com a senha digitada pelo usuário
    if Clientes[validarcnpj1]['Senha'] == validarsenha:
      #valor a ser transferido
      tranferir = int(input("Digite o valor a ser tranferido: "))
      #atualiza o saldo da conta de origem e de destino
      Clientes[validarcnpj1]['Saldo'] -= tranferir
      Clientes[validarcnpj2]['Saldo'] += tranferir
      Saldo1 = Clientes[validarcnpj1]['Saldo']
      Saldo2 = Clientes[validarcnpj2]['Saldo']
      #verifica o tipo da conta de origem
      if Clientes[validarcnpj1]['Tipo'].lower() in ['comum', 'c']:
        #verifica se o limite da conta comum não foi excedido
        if Saldo1 >= -1000:
          #coloca as informações da operação no arquivo extrato.txt em relaçao a conta de origem e conta de destino
          extrato.write(
          f"CNPJ: {validarcnpj1} {formata} -{tranferir} Tarifa: 0.00 Saldo: {Saldo1}\n"
          )
          extrato.write(
          f"CNPJ: {validarcnpj2} {formata} +{tranferir} Tarifa: 0.00 Saldo: {Saldo2}\n"
          )
          print("Tranfêrencia concluida com sucesso!")
          print(f"O valor de {tranferir} R$ foi tranferido da conta de origem para a conta de destino.")
          SalvarClientes(Clientes)
        else:
          print("Limite negativo no saldo excedido!")
      else:
        #verifica se o limite da conta premium não foi excedido
        if Saldo1 >= -5000:
          #coloca as informações da operação no arquivo extrato.txt em relaçao a conta de origem e conta de destino
          extrato.write(
          f"CNPJ: {validarcnpj1} {formata} -{tranferir} Tarifa: 0.00 Saldo: {Saldo1}\n"
          )
          extrato.write(
          f"CNPJ: {validarcnpj2} {formata} +{tranferir} Tarifa: 0.00 Saldo: {Saldo2}\n"
          )
          print("Tranfêrencia concluida com sucesso!")
          print(f"O valor de {tranferir} R$ foi tranferido da conta de origem para a conta de destino.")
          SalvarClientes(Clientes)
        else:
          print("Limite negativo no saldo excedido!")
    else:
      print("Senha incorreta!")
  else:
    print("CNPJ não encontrado!")
  extrato.close()


#Função de debitar automaticamente
def debitoAutomatico(Clientes):
  validarcnpj = int(input("Coloque o CNPJ da conta que deseja manter o débito automático: "))
  #verifica se há uma conta vínculada a esse CNPJ no dicionário dos Clientes
  if validarcnpj in Clientes:
    Senha = input("Digite sua senha: ")
    #verifica se a senha da conta vinculada com o CNPJ bate com a senha digitada pelo usuário
    if Senha == Clientes[validarcnpj]['Senha']:
      # coloca as informações do débito automatico, como para qual isntituição vai, a quantidade, e que dia do mês
      inst = input("Digite a instituição de Destino: ")
      quant = float(input("Digite a quantidade que irá debitar por mês: "))
      Saldo = Clientes[validarcnpj]['Saldo']
      #verifica o tipo da conta 
      if Clientes[validarcnpj]['Tipo'].lower() in ['comum', 'c']:
        #verifica se o limite da conta comum não foi excedido
        if Saldo - quant >= -1000:
          dia = int(input("Digite o dia do mês para debitar automaticamente: "))
          print()
          print("Debito automatico definido!")
          #mostra a definição do débito automatico cadastrado
          print(f"O débito será realizado no dia {dia} de cada mês para a instituição {inst} no valor de {quant}")
          print()
        else:
          print("Saldo insuficiente!")
      else:
        #verifica se o limite da conta premium não foi excedido
        if Saldo - quant >= -5000:
          dia = int(input("Digite o dia do mês para debitar automaticamente: "))
          print()
          print("Debito automatico definido!")
          #mostra a definição do débito automatico cadastrado
          print(f"O débito será realizado no dia {dia} de cada mês para a instituição {inst} no valor de {quant}")
          print()
        else:
          print("Saldo insuficiente!")
    else:
        print("Senha incorreta!")
  else:
      print("CNPJ não encontrado!")




if os.path.isfile("Clientes.txt"): #checa se o caminho definido é visível no arquivo ou não
  Clientes = GuardarClientes(Clientes)

while True:
  #Sempre ao iniciar o sistema o dicionario Clientes é carregado com os dados do arquivo Clientes.txt a partir da função GuardarClientes
  ##Clientes = GuardarClientes()
  #chama o menu
  menu()
  print()
  #pede qual o número da operação a se realizar
  entrada = int(input("Qual operação realizar: ")) #Dependendo do número selecionado uma função diferente será utilizada, e caso o número seja 9 o looping quebra
  os.system('clear')
  print()
  if entrada == 1:
    novoClient(Clientes)
  elif entrada == 2:
    apagaCliente(Clientes)
  elif entrada == 3:
    listaClientes(Clientes)
  elif entrada == 4:
    Débito(Clientes)
  elif entrada == 5:
    deposito(Clientes)
  elif entrada == 6:
    Extrato(Clientes)
  elif entrada == 7:
    transferencia(Clientes)
  elif entrada == 8:
    debitoAutomatico(Clientes)
  elif entrada == 9:
    print("Obrigado por utilizar os serviços do QuemPoupaTem")
    SalvarClientes(Clientes)
    break
  else:
    print("Opção inválida! Tente novamente.")
    print()