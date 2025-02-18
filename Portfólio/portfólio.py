import time, os, csv

# These variable are to store the names of the files that will be used in this system
events = "eventos.csv"
registrations = "registrations.csv"

# Function to create file of the Events
def create_events_file(a = "", b = "", c = "", d = ""):
    """ This function creates the file if it does not exist. If the file exists,
    it appends new data to it. """
    try:
        # Try creating a new file with the header
        with open(events, 'x', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            field = (["ID", "NOME DO EVENTO", "DATA DE INICIO", "QTD VAGAS"])
            writer.writerow(field)
    except FileExistsError:
        # If file exists, it appends the data
        with open(events, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if a and b and c and d:
                writer.writerow([a, b, c, d])
    except OSError as e:
        print(f"Erro ao acessar o arquivo: {e}")


# Função para exibir a tela de boas-vindas
def welcome_screen():
    print("\n" * 5)  # Espacos para centralizar a mensagem
    print("***************************************")
    print("*   Bem-vindo ao Sistema de Eventos   *")
    print("*             UniFECAF                *")
    print("****************************************")
    time.sleep(3)  # Espera 3 segundos

# Função para exibir a tela de opções de login
def tela_login():
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela para sistemas Windows ou Linux/Mac
    print("\n" * 5)  # Espacos para centralizar
    print("****************************************")
    print("*   Escolha uma opção de utilização   *")
    print("****************************************")
    print("1. Utilizar como Organizador")
    print("2. Utilizar como Aluno")
    print("****************************************")

# Função para lidar com a escolha do usuário
def escolher_login():
    while True:
        escolha = input("\nDigite o número da opção desejada: ")
        if escolha == "1":
            print("\nVocê escolheu login como Organizador.")
            time.sleep(10)
            tela_login_organizador()
            break
        elif escolha == "2":
            print("\nVocê escolheu login como Aluno.")
            time.sleep(10)
            break
        else:
            print("\nOpção inválida. Por favor, digite 1 ou 2.")

# Função principal que executa o fluxo
def main():
    welcome_screen()  # Exibe a tela de boas-vindas
    tela_login()  # Exibe a tela de login
    escolher_login()  # Solicita a escolha do usuário
    tela_login_organizador()  # Exibe a tela de login como Organizador

# Rodando a aplicação
if __name__ == "__main__":
    main()