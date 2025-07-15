import tkinter as tk
from tkinter import messagebox
import random

# Janela
janela = tk.Tk()
janela.title("Jogo da Velha - Touch-Friendly")
janela.configure(bg="#fafafa")


janela.geometry("400x520") 


botoes = []
placar_jogador = 0
placar_bot = 0
empates = 0


label_placar = tk.Label(janela, text="", font=("Arial", 16, "bold"), bg="#fafafa")
label_placar.pack(pady=10)

def atualizar_placar():
    label_placar.config(text=f"👤 Jogador: {placar_jogador}     🤖 Bot: {placar_bot}     🤝 Empates: {empates}")

def verificar_vitoria():
    combinacoes = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a, b, c in combinacoes:
        if botoes[a]["text"] == botoes[b]["text"] == botoes[c]["text"] != "":
            botoes[a].configure(bg="lightgreen")
            botoes[b].configure(bg="lightgreen")
            botoes[c].configure(bg="lightgreen")
            return botoes[a]["text"]
    
    if all(botao["text"] != "" for botao in botoes):
        return "Empate"
    return None

def bot_jogar():
    def pode_vencer(simbolo):
        for a, b, c in [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]:
            valores = [botoes[a]["text"], botoes[b]["text"], botoes[c]["text"]]
            if valores.count(simbolo) == 2 and valores.count("") == 1:
                if botoes[a]["text"] == "":
                    return a
                elif botoes[b]["text"] == "":
                    return b
                elif botoes[c]["text"] == "":
                    return c
        return None

    pos = pode_vencer("O")
    if pos is not None:
        botoes[pos]["text"] = "O"
        botoes[pos].configure(fg="red")
        verificar_fim()
        return

    pos = pode_vencer("X")
    if pos is not None:
        botoes[pos]["text"] = "O"
        botoes[pos].configure(fg="red")
        verificar_fim()
        return

    livres = [i for i, botao in enumerate(botoes) if botao["text"] == ""]
    if livres:
        escolha = random.choice(livres)
        botoes[escolha]["text"] = "O"
        botoes[escolha].configure(fg="red")
        verificar_fim()

def clique(pos):
    if botoes[pos]["text"] == "":
        botoes[pos]["text"] = "X"
        botoes[pos].configure(fg="blue")
        resultado = verificar_vitoria()
        if resultado:
            fim_jogo(resultado)
        else:
            janela.after(400, bot_jogar)

def verificar_fim():
    resultado = verificar_vitoria()
    if resultado:
        fim_jogo(resultado)

def fim_jogo(resultado):
    global placar_jogador, placar_bot, empates

    if resultado == "X":
        messagebox.showinfo("Vitória!", "Você venceu!")
        placar_jogador += 1
    elif resultado == "O":
        messagebox.showinfo("Derrota!", "O bot venceu!")
        placar_bot += 1
    else:
        messagebox.showinfo("Empate", "Ninguém venceu.")
        empates += 1

    atualizar_placar()
    janela.after(200, reiniciar_jogo)

def reiniciar_jogo():
    for botao in botoes:
        botao["text"] = ""
        botao.configure(bg="white")

# central para os botões (tabuleiro)
frame_tabuleiro = tk.Frame(janela, bg="#fafafa")
frame_tabuleiro.pack(pady=10)

# Criar botões do tabuleiro
for i in range(9):
    botao = tk.Button(frame_tabuleiro, text="", font=("Helvetica", 36, "bold"), width=5, height=2,
                      bg="white", command=lambda i=i: clique(i))
    botao.grid(row=i//3, column=i%3, padx=8, pady=8)
    botoes.append(botao)


atualizar_placar()

janela.mainloop()
