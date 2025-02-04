import tkinter as tk

def calcular_quadrado():
    try:
        numero = float(entry_numero.get())  # Obtém o valor inserido
        quadrado = numero ** 2  # Calcula o quadrado do número
        label_resultado.config(text=f"O quadrado de {numero} é {quadrado}")  # Exibe o resultado
    except ValueError:
        label_resultado.config(text="Por favor, insira um número válido.")

# Criação da janela principal
root = tk.Tk()
root.title("Calculadora de Quadrado")

# Configurações da janela
root.geometry("300x200")

# Rótulo de instrução
label_instrucao = tk.Label(root, text="Insira um número:")
label_instrucao.pack(pady=10)

# Campo de entrada para o número
entry_numero = tk.Entry(root)
entry_numero.pack(pady=5)

# Botão para calcular o quadrado
botao_calcular = tk.Button(root, text="Calcular Quadrado", command=calcular_quadrado)
botao_calcular.pack(pady=10)

# Rótulo para exibir o resultado
label_resultado = tk.Label(root, text="")
label_resultado.pack(pady=10)

# Inicia a interface gráfica
root.mainloop()