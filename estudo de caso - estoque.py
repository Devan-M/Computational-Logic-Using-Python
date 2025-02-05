import time, sys, os, csv, unicodedata, re
import pandas as pd
from tabulate import tabulate

#Este será o nome do arquivo CSV gerado.
filename = "estoque.csv"

#remove caracteres especiais para evitar erros no arquivo
def remove_acentos(texto):
     return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

def create_file(a = "", b = "", c = "", d = ""):
    """ This function creates the file if it does not exist. If the file exists,
    it appends new data to it. """
    try:
        # Try creating a new file with the header
        with open(filename, 'x', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            field = (["ID", "NOME", "PRECO UNITARIO [R$]", "QTD ESTOQUE"])
            writer.writerow(field)
    except FileExistsError:
        # If file exists, it appends the data
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if a and b and c and d:
                writer.writerow([a, b, c, d])
    except OSError as e:
        print(f"Erro ao acessar o arquivo: {e}")


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

def check_duplicate_product(product_name, product_id=None):
    reader = csv.reader(open(filename, 'r', encoding="utf-8"))
    data = list(reader)
    for row in data[1:]:  # Skip header row
        if row[1].lower() == product_name.lower():  # Compare product names case-insensitively
            return True  # Duplicate found
        if product_id and row[0] == product_id:
            return True  # Duplicate ID found
    return False

def add_Item():
    clear_screen()
    product_name = input("Digite o nome do produto: ")
    product_name = remove_acentos(product_name)

    # Check if the product already exists
    if check_duplicate_product(product_name):
        print("Produto já existe no estoque.")
        return

    # Validate the price
    while True:
        product_price = input("Digite o preço unitário do produto: ")
        validated_price = validate_price(product_price)
        if validated_price:
            break

    # Validate the quantity
    while True:
        product_qty = input("Digite a quantidade em estoque do produto: ")
        validated_qty = validate_quantity(product_qty)
        if validated_qty is not None:
            break

    product_id = generate_id()
    create_file(product_id, product_name, validated_price, validated_qty)


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

def show_stock():
  reader = csv.reader(open('estoque.csv', 'r', encoding="utf-8"))
  data = []
  for row in reader:
    data.append(row)
  header = data.pop(0)
  draw_table(data, header)

def fixed_length(text, length):
    return text[:length].ljust(length)

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
    show_stock()
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
            
            # Validate new_name (if not empty, validate that it's a valid string)
            if new_name != "":
                new_name = remove_acentos(new_name)  # Clean name
                row[1] = new_name  # Update the name

            # Validate new_price (if not empty, validate that it's a valid price)
            if new_price != "":
                new_price = validate_price(new_price)
                if new_price is None:
                    print("Preço inválido. Não foi possível atualizar o produto.")
                    return  # Exit without updating product
                row[2] = new_price  # Update the price

            # Validate new_qty (if not empty, validate that it's a valid quantity)
            if new_qty != "":
                new_qty = validate_quantity(new_qty)
                if new_qty is None:
                    print("Quantidade inválida. Não foi possível atualizar o produto.")
                    return  # Exit without updating product
                row[3] = new_qty  # Update the quantity

            # Atualizar os dados no arquivo CSV
            with open('estoque.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(data)
            print("Produto atualizado com sucesso.")
            break

    if not item_found:
        print(f"Produto com ID {product_id} não encontrado.")
        

def validate_price(price):
    try:
        price = float(price.replace(",", "."))
        if price <= 0:
            raise ValueError
        return price
    except ValueError:
        print("Preço inválido. Insira um número válido.")
        return None

def validate_quantity(quantity):
    try:
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError
        return quantity
    except ValueError:
        print("Quantidade inválida. Insira um número inteiro positivo.")
        return None

def check_file_exists(filename):
    if not os.path.exists(filename):
        print(f"O arquivo {filename} não existe!")
        return False
    return True

def exibir_tabela_com_paginacao(caminho_arquivo, linhas_por_pagina=10):
    # Carregar o arquivo CSV para um DataFrame
    df = pd.read_csv(caminho_arquivo)

    total_linhas = len(df)
    total_paginas = (total_linhas // linhas_por_pagina) + (1 if total_linhas % linhas_por_pagina != 0 else 0)

    pagina_atual = 1

    while True:
        # Calcular o início e o fim da página
        inicio = (pagina_atual - 1) * linhas_por_pagina
        fim = inicio + linhas_por_pagina

        # Obter as linhas da página atual
        pagina = df.iloc[inicio:fim]

        # Exibir a tabela da página atual
        print(f"\nPágina {pagina_atual} de {total_paginas}")
        print(tabulate(pagina, headers='keys', tablefmt='pretty', showindex=False))

        # Opções de navegação
        print("\nOpções:")
        print("P - Próxima página")
        print("A - Página anterior")
        print("M - Menu principal")

        # Receber a opção do usuário
        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == 'p' and pagina_atual < total_paginas:
            pagina_atual += 1
        elif opcao == 'a' and pagina_atual > 1:
            pagina_atual -= 1
        elif opcao == 'm':
            menu()
            break
        else:
            print("Opção inválida. Tente novamente.")


  # Base do sistema : Menu de opçoes para o usuário
def menu():
    clear_screen()
    
    # Verificar se o arquivo existe antes de iniciar o menu
    if not check_file_exists(filename):
        print(f"O arquivo {filename} não existe. Criando um novo arquivo.")
        create_file()  # Cria o arquivo vazio com cabeçalho
    
    while True:
        print("-"*30)
        print("MENU - Sistema de Estoque")
        print("-"*30)
        print("1 - Cadastrar Produto")
        print("2 - Atualizar Produto")
        print("3 - Excluir produto")
        print("4 - Visualizar estoque")
        print("5 - Sair do sistema")
        print("-"*30)
        opcao = input("Digite sua opção (1-5): ")
        
        if opcao == '1':
            add_Item()
        elif opcao == '2':
            update_item()  # Atualizar Produto
        elif opcao == '3':
            choose_item_to_delete()
        elif opcao == '4':
          #na linha abaixo, ajustar "linhas_por_pagina" para um numero que melhor se adeque (para tabelas muito grandes)
          exibir_tabela_com_paginacao(filename, linhas_por_pagina=30)
        elif opcao == '5':
            timer_sair()
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()