import time
import os

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
    print("*      Escolha uma opção de login      *")
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

def tela_login_organizador():
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela para sistemas Windows ou Linux/Mac
    print("\n" * 5)  # Espacos para centralizar
    print("Vc foi redirecionado...")

# Função principal que executa o fluxo
def main():
    welcome_screen()  # Exibe a tela de boas-vindas
    tela_login()  # Exibe a tela de login
    escolher_login()  # Solicita a escolha do usuário
    tela_login_organizador()  # Exibe a tela de login como Organizador

# Rodando a aplicação
if __name__ == "__main__":
    main()
