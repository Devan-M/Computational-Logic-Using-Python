import time, sys, os, csv, unicodedata, re

#Este será o nome do arquivo CSV gerado.
filename = "estoque.csv"

#remove caracteres especiais para evitar erros no arquivo
def remove_acentos(texto):
     return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

def create_file(a = "", b = "", c = "", d = ""):
  """ Esta função cria o arquivo com nome definido em filename,
  caso ele não exista na mesma pasta do código, cria cabeçalho e
  adiciona linha com os dados digitados. Caso o arquivo já exista (except),
  ele apenas adiciona linhas ao final do mesmo.
  """
  try:
    with open(filename, 'x', newline='') as file:
        writer = csv.writer(file)
        field = (["ID", "NOME", "PRECO UNITARIO [R$]", "QTD ESTOQUE"])
        writer.writerow(field)
  except:
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if (a == "" or b == "" or c == "" or d == ""):
          pass
        else:
          writer.writerow([a, b, c, d])

def clear_screen():
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
  clear_screen()
  product_name = input("Digite o nome do produto: ")
  product_name = remove_acentos(product_name)
  product_price = re.sub(",",".",input("Digite o preço unitário do produto: "))
  product_qty = int(input("Digite a quantidade em estoque do produto: "))
  product_id = generate_id()
  create_file(product_id, product_name, product_price, product_qty)

def generate_id():
  reader = csv.reader(open('estoque.csv', 'r', encoding="utf-8"))
  data = []
  for row in reader:
    data.append(row)
  header = data.pop(0)
  if not data:
    generated_id = 1
  else:
    last_row = data[-1]
    last_id = int(last_row[0])
    generated_id = last_id + 1
  return generated_id

def ver_estoque():
  reader = csv.reader(open('estoque.csv', 'r', encoding="utf-8"))
  data = []
  for row in reader:
    data.append(row)
  header = data.pop(0)
  draw_table(data, header)

def fixed_length(text, length):
  if len (text) > length:
    text = text[:length]
  elif len (text) < length:
    text = (text + " " * length)[:length]
  return text

def draw_table(data, header):
  clear_screen()
  print("-"*106) 
  print("#", end=" ")
  counter = 0
  for column in header:
    if counter == 0:
      print(fixed_length(column, 7), end =" #   ")
    elif counter == 1:
      print(fixed_length(column, 40), end =" #   ")
    else:
      print(fixed_length(column, 20), end =" #   ")
    counter = counter + 1 
  print("")
  print("-"*106)
  
  for row in data:
    print("# ", end="")
    counter = 0
    for column in row:
      if counter == 0:
        print(fixed_length(column, 7), end =" #   ")
      elif counter == 1:
        print(fixed_length(column, 40), end =" #   ")
      else:
        print(fixed_length(column, 20), end =" #   ")
      counter = counter + 1
    print()
  print("-"*106)

  # Base do sistema : Menu de opçoes para o usuário
def menu():
  clear_screen()
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
      clear_screen()
    elif opcao == '2':
      #função de atualizar
      create_file()
    elif opcao == '3':
      #função de visualiza estoque
      create_file()
    elif opcao == '4':
      create_file()
      ver_estoque()
    elif opcao == '5':
      timer_sair()
      clear_screen()
      #print("Saindo do programa...")
      break
    else:
      print("Opção inválida. Tente novamente.")

menu()