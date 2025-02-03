import time, sys, os, csv, unicodedata
filename = "estoque.csv"

#remove caracteres especiais para evitar erros no arquivo
def remove_acentos(texto):
     return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

def create_file():
  """ Esta função cria o arquivo com nome definido em filename, 
  caso ele não exista na mesma pasta do código. Caso o arquivo já exista,
  ele apenas adiciona linhas ao final do mesmo.  
  """
  try:
    with open(filename, 'x', newline='') as file:
        writer = csv.writer(file)
        field = ["ID", "NOME", "PRECO UNITARIO [R$]", "QTD ESTOQUE"]
        writer.writerow(field)
  except:
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["idx", "este e, um exemplo de nome", "9.99","502"])

def limpa_tela():
  os.system("cls" if os.name == "nt" else "clear")

def timer_sair():
  cont = 1
  for i in range(4, -1, -1):
    sys.stdout.write("\r Saindo do sistema{}".format("."*cont))
    sys.stdout.flush()
    time.sleep(1)
    cont = cont + 1
  #print ("\nFim")

def add_Item():
  product_name = input("Digite o nome do produto: ")
  product_price = float(input("Digite o preço unitário do produto (use ponto para separar os centavos): "))
  product_qty = int(input("Digite a quantidade em estoque do produto: "))
  
# Base do sistema : Menu de opçoes para o usuário
def menu():
  limpa_tela()
  while True:
    print("-"*30)
    print("MENU")
    print("-"*30)
    print("1 - Cadastrar Produto")
    print("2 - Atualizar Produto")
    print("3 - Excluir produto")
    print("4 - Visualizar estoque")
    print("5 - Sair do sistema")
    print("-"*30)
    opcao = input("Digite sua opção: ")
    if opcao == '1':
      # funcao de cadastrar produtos
      add_Item()
      limpa_tela()
    elif opcao == '2':
      #função de atualizar
      create_file()
    elif opcao == '3':
      #função de visualiza estoque
      create_file()
    elif opcao == '4':
      #função de visualizar estoque
      create_file()
    elif opcao == '5':
      timer_sair()
      limpa_tela()
      #print("Saindo do programa...")
      break
    else:
      print("Opção inválida. Tente novamente.")

menu()