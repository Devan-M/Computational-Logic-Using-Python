import csv
import os
import re
from datetime import datetime

class Evento:
    def __init__(self, nome, data, descricao, vagas_max):
        self.nome = nome
        self.data = data
        self.descricao = descricao
        self.vagas_max = vagas_max
        self.vagas_restantes = vagas_max
        self.inscritos = []

    def atualizar_evento(self, nova_data=None, novas_vagas=None):
        if nova_data:
            self.data = nova_data
        if novas_vagas:
            self.vagas_max = novas_vagas
            self.vagas_restantes = novas_vagas - len(self.inscritos)

    def inscrever_participante(self, participante):
        if self.vagas_restantes > 0:
            self.inscritos.append(participante)
            self.vagas_restantes -= 1
            print(f'{participante} foi inscrito(a) no evento {self.nome}!')
        else:
            print(f'Não há vagas disponíveis no evento {self.nome}.')

    def mostrar_evento(self):
        print(f'Evento: {self.nome}')
        print(f'Data: {self.data}')
        print(f'Descrição: {self.descricao}')
        print(f'Vagas restantes: {self.vagas_restantes}')
        print('---')

    def visualizar_inscricoes(self):
        if self.inscritos:
            print(f'Inscritos para o evento "{self.nome}":')
            for inscrito in self.inscritos:
                print(f'- {inscrito}')
        else:
            print(f'Nenhum participante inscrito para o evento "{self.nome}".')

    def excluir_evento(self):
        print(f'O evento "{self.nome}" foi excluído com sucesso!')


class SistemaEventos:
    def __init__(self):
        self.eventos = []
        self.carregar_dados()

    def carregar_dados(self):
        """Carrega os eventos e inscrições a partir de arquivos CSV."""
        if os.path.exists('eventos.csv'):
            with open('eventos.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Pular o cabeçalho
                for row in reader:
                    nome, data, descricao, vagas_max, inscritos = row
                    evento = Evento(nome, data, descricao, int(vagas_max))
                    if inscritos:
                        evento.inscritos = inscritos.split(';')
                        evento.vagas_restantes = int(vagas_max) - len(evento.inscritos)
                    self.eventos.append(evento)

    def salvar_dados(self):
        """Salva os eventos e inscrições em arquivos CSV."""
        with open('eventos.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Nome', 'Data', 'Descrição', 'Vagas_max', 'Inscritos'])  # Cabeçalho
            for evento in self.eventos:
                inscritos = ';'.join(evento.inscritos)
                writer.writerow([evento.nome, evento.data, evento.descricao, evento.vagas_max, inscritos])

    def criar_evento(self, nome, data, descricao, vagas_max):
        novo_evento = Evento(nome, data, descricao, vagas_max)
        self.eventos.append(novo_evento)
        print(f'O evento "{nome}" foi criado com sucesso!')
        self.salvar_dados()

    def listar_eventos(self):
        if not self.eventos:
            print('Não há eventos cadastrados.')
        else:
            for evento in self.eventos:
                evento.mostrar_evento()

    def atualizar_evento(self, nome, nova_data=None, novas_vagas=None):
        for evento in self.eventos:
            if evento.nome == nome:
                evento.atualizar_evento(nova_data, novas_vagas)
                print(f'O evento "{nome}" foi atualizado com sucesso!')
                self.salvar_dados()
                return
        print(f'Evento "{nome}" não encontrado.')

    def inscrever_em_evento(self, nome, participante):
        for evento in self.eventos:
            if evento.nome == nome:
                evento.inscrever_participante(participante)
                self.salvar_dados()
                return
        print(f'Evento "{nome}" não encontrado.')

    def visualizar_inscricoes(self, nome):
        for evento in self.eventos:
            if evento.nome == nome:
                evento.visualizar_inscricoes()
                return
        print(f'Evento "{nome}" não encontrado.')

    def excluir_evento(self, nome):
        for evento in self.eventos:
            if evento.nome == nome:
                self.eventos.remove(evento)
                evento.excluir_evento()
                self.salvar_dados()
                return
        print(f'Evento "{nome}" não encontrado.')


# Funções auxiliares
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def validar_data(data_str):
    """Valida se a data está no formato dd/mm/aaaa"""
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# Funções do sistema
def menu_organizador():
    sistema = SistemaEventos()

    while True:
        limpar_tela()
        print("\n--- Sistema de Cadastro de Eventos (Organizador) ---")
        print("1. Criar evento")
        print("2. Atualizar evento")
        print("3. Listar eventos")
        print("4. Inscrever-se em evento")
        print("5. Visualizar inscrições")
        print("6. Excluir evento")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input('Nome do evento: ')
            data = input('Data do evento (dd/mm/aaaa): ')
            while not validar_data(data):
                print("Data inválida! Use o formato dd/mm/aaaa.")
                data = input('Data do evento (dd/mm/aaaa): ')
            descricao = input('Descrição do evento: ')
            vagas_max = int(input('Número máximo de vagas: '))
            sistema.criar_evento(nome, data, descricao, vagas_max)

        elif opcao == '2':
            nome = input('Nome do evento a ser atualizado: ')
            nova_data = input('Nova data do evento (dd/mm/aaaa) ou deixe em branco para não alterar: ')
            if nova_data and not validar_data(nova_data):
                print("Data inválida! Use o formato dd/mm/aaaa.")
                continue
            novas_vagas = input('Novo número de vagas (deixe em branco para não alterar): ')
            novas_vagas = int(novas_vagas) if novas_vagas else None
            sistema.atualizar_evento(nome, nova_data if nova_data else None, novas_vagas)

        elif opcao == '3':
            sistema.listar_eventos()

        elif opcao == '4':
            nome_evento = input('Nome do evento para inscrição: ')
            participante = input('Nome do participante: ')
            sistema.inscrever_em_evento(nome_evento, participante)

        elif opcao == '5':
            nome_evento = input('Nome do evento para visualizar as inscrições: ')
            sistema.visualizar_inscricoes(nome_evento)

        elif opcao == '6':
            nome_evento = input('Nome do evento a ser excluído: ')
            sistema.excluir_evento(nome_evento)

        elif opcao == '7':
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida. Tente novamente.")


def menu_aluno():
    sistema = SistemaEventos()

    while True:
        limpar_tela()
        print("\n--- Sistema de Cadastro de Eventos (Aluno) ---")
        print("1. Listar eventos")
        print("2. Inscrever-se em evento")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            sistema.listar_eventos()

        elif opcao == '2':
            nome_evento = input('Nome do evento para inscrição: ')
            participante = input('Nome do participante: ')
            sistema.inscrever_em_evento(nome_evento, participante)

        elif opcao == '3':
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida. Tente novamente.")


def menu():
    while True:
        limpar_tela()
        print("\n--- Sistema de Cadastro de Eventos ---")
        print("1. Entrar como Organizador")
        print("2. Entrar como Aluno")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_organizador()

        elif opcao == '2':
            menu_aluno()

        elif opcao == '3':
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida. Tente novamente.")


# Iniciar o sistema
menu()