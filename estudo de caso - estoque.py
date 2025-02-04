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

def choose_item_to_delete():
  clear_screen()
  print("Para deletar um produto, vc deve saber o numero de identificação (ID) do produto!")
  print("Voce sabe o numero da ID? ")
  print("1 - Sim")
  print("2 - Não")
  resposta = input("Digite sua opção: ")
  if resposta == '1':
    id = input("Digite a ID do produto a ser excluído: ")
    delete_item(filename, id)
  elif resposta == '2':
    ver_estoque()
  else:
    print("Opção inválida. Tente novamente.")
    choose_item_to_delete()
  
def delete_item(arquivo, id_procurado):
    # Lê o conteúdo do arquivo CSV
    with open(arquivo, mode='r', newline='', encoding='utf-8') as file:
        leitor_csv = csv.reader(file)
        linhas = list(leitor_csv)
        
    # Verifica se o arquivo está vazio
    if len(linhas) == 0:
        print("O arquivo está vazio.")
        return
    
    # Encontrar o índice da coluna "ID"
    cabecalho = linhas[0]
    if "ID" not in cabecalho:
        print("A coluna 'ID' não foi encontrada.")
        return
    indice_id = cabecalho.index("ID")
    
    # Filtra as linhas, excluindo a que tem o ID procurado
    linhas_filtradas = [linha for linha in linhas if linha[indice_id] != str(id_procurado)]
    
    # Verifica se alguma linha foi excluída
    if len(linhas_filtradas) == len(linhas):
        print(f"Nenhuma linha com o ID {id_procurado} foi encontrada.")
        return
    
    # Escreve as linhas de volta no arquivo CSV, sobrescrevendo o original
    with open(arquivo, mode='w', newline='', encoding='utf-8') as file:
        escritor_csv = csv.writer(file)
        escritor_csv.writerows(linhas_filtradas)
    print(f"O Produto com a ID {id_procurado} foi removido com sucesso.")

def update_item():
    clear_screen()
    product_id = input("Digite o ID do produto a ser atualizado: ")
    reader = csv.reader(open('estoque.csv', 'r', encoding="utf-8"))
    data = list(reader)
    header = data.pop(0)
    
    # Procurando o produto pelo ID
    item_found = False
    for row in data:
        if row[0] == product_id:
            item_found = True
            print(f"Produto encontrado: {row}")
            new_name = input(f"Novo nome (deixe vazio para não alterar): ")
            new_price = input(f"Novo preço (deixe vazio para não alterar): ")
            new_qty = input(f"Nova quantidade (deixe vazio para não alterar): ")
            
            if new_name != "":
                row[1] = remove_acentos(new_name)
            if new_price != "":
                row[2] = re.sub(",", ".", new_price)
            if new_qty != "":
                row[3] = new_qty

            # Atualizar os dados no arquivo CSV
            with open('estoque.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(data)
            print("Produto atualizado com sucesso.")
            break

    if not item_found:
        print(f"Produto com ID {product_id} não encontrado.")


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
      update_item()  # Chamando a função para atualizar produto

    elif opcao == '3':
      create_file()
      choose_item_to_delete()
    elif opcao == '4':
      create_file()
      ver_estoque()
    elif opcao == '5':
      timer_sair()
      clear_screen()
      #print("Saindo do programa...")
      break
    elif opcao == '6':
      clear_screen()
    else:
      print("Opção inválida. Tente novamente.")

menu()