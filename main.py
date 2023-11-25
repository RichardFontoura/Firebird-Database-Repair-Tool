import tkinter as tk
import datetime
import subprocess
import threading
import os
import sys
import zipfile
import time
from tkinter import scrolledtext, filedialog


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def scroll_to_bottom():
    resultado_text.yview(tk.END)

def executar_gfix_e_gbak(diretorio_selecionado):
    caminho_banco = caminho_fb_entry.get()
    destino_gbak = os.path.join(caminho_gbk_entry.get(), "BackupBanco.gbk")
    destino_nv = os.path.join(caminho_nv_entry.get(), "NovoBanco.FB")

    now = datetime.datetime.now()
    data_hora = now.strftime("%d-%m-%Y-%H-%M-%S")
    log_arquivo = f"log_{data_hora}.txt"

    try:
        resultado_text.config(state=tk.NORMAL)
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, f"Executando Análise no Banco de Dados, Por Favor Aguarde...\n\n")
        resultado_text.config(state=tk.DISABLED)

        diretorio_firebird = diretorio_selecionado

        gfix_comando = [
            os.path.join(diretorio_firebird, "gfix"),
            "-user", "SYSDBA",
            "-password", "masterkey",
            "-mend",
            "-full",
            "-ignore",
            caminho_banco
        ]

        with subprocess.Popen(gfix_comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, creationflags=subprocess.CREATE_NO_WINDOW) as gfix_processo:
            for linha in gfix_processo.stdout:
                resultado_text.config(state=tk.NORMAL)
                resultado_text.insert(tk.END, linha)
                resultado_text.config(state=tk.DISABLED)
                scroll_to_bottom()

            for linha in gfix_processo.stderr:
                resultado_text.config(state=tk.NORMAL)
                resultado_text.insert(tk.END, linha)
                resultado_text.config(state=tk.DISABLED)
                scroll_to_bottom()

            resultado_text.config(state=tk.NORMAL)
            resultado_text.insert(tk.END, f"\nAnalise Efetuada com Sucesso.\n\nGravando Novos Dados...\n\n")
            resultado_text.config(state=tk.DISABLED)
            scroll_to_bottom()

            gbak_comando_1 = [
            os.path.join(diretorio_firebird, "gbak"),
            "-user",
            "SYSDBA",
            "-password",
            "masterkey",
            "-b",
            "-v",
            "-garbage",
            caminho_banco,
            destino_gbak
            ]

            with subprocess.Popen(gbak_comando_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, creationflags=subprocess.CREATE_NO_WINDOW) as gbak_processo_1:
                for linha in gbak_processo_1.stdout:
                    resultado_text.config(state=tk.NORMAL)
                    resultado_text.insert(tk.END, linha)
                    resultado_text.config(state=tk.DISABLED)
                    scroll_to_bottom()

                for linha in gbak_processo_1.stderr:
                    resultado_text.config(state=tk.NORMAL)
                    resultado_text.insert(tk.END, linha)
                    resultado_text.config(state=tk.DISABLED)
                    scroll_to_bottom()
                    

            resultado_text.config(state=tk.NORMAL)
            resultado_text.insert(tk.END, f"\nDados Gravados com Sucesso.\n\nCriando Novo Banco de Dados .FB...\n\n")
            resultado_text.config(state=tk.DISABLED)
            scroll_to_bottom()

            gbak_comando_2 = [
            os.path.join(diretorio_firebird, "gbak"),
            destino_gbak,
            destino_nv,
            "-c",
            "-v",
            "-o",
            "-user",
            "SYSDBA",
            "-password",
            "masterkey"
            ]  

            with subprocess.Popen(gbak_comando_2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, creationflags=subprocess.CREATE_NO_WINDOW) as gbak_processo_2:
                for linha in gbak_processo_2.stdout:
                    resultado_text.config(state=tk.NORMAL)
                    resultado_text.insert(tk.END, linha)
                    resultado_text.config(state=tk.DISABLED)
                    scroll_to_bottom()

                for linha in gbak_processo_2.stderr:
                    resultado_text.config(state=tk.NORMAL)
                    resultado_text.insert(tk.END, linha)
                    resultado_text.config(state=tk.DISABLED)
                    scroll_to_bottom()

                resultado_text.config(state=tk.NORMAL)
                resultado_text.insert(tk.END, f"\nManutenção Realizada com Sucesso.\n")
                resultado_text.config(state=tk.DISABLED)
                scroll_to_bottom()

            with open(log_arquivo, 'w') as file:
                file.write(resultado_text.get('1.0', tk.END))

    except subprocess.CalledProcessError as e:
        resultado_text.config(state=tk.NORMAL)
        resultado_text.insert(tk.END, f"Erro ao executar o comando: {e.stderr}\n")
        resultado_text.config(state=tk.DISABLED)
        scroll_to_bottom()

def compactar_banco():
    CompactarBanco()

def compactar_banco_opcao_1():
    arquivo_a_compactar = caminho_nv_entry.get()
    if arquivo_a_compactar:
        compactar_arquivo(arquivo_a_compactar)
    else:
        resultado_text.config(state=tk.NORMAL)
        resultado_text.insert(tk.END, "Nenhum arquivo selecionado.\n")
        resultado_text.config(state=tk.DISABLED)
        scroll_to_bottom()

def compactar_banco_opcao_2():
    arquivo_a_compactar = caminho_fb_entry.get()
    if arquivo_a_compactar:
        compactar_arquivo(arquivo_a_compactar)
    else:
        resultado_text.config(state=tk.NORMAL)
        resultado_text.insert(tk.END, "Nenhum arquivo selecionado.\n")
        resultado_text.config(state=tk.DISABLED)
        scroll_to_bottom()

def compactar_arquivo(arquivo_a_compactar):
    if arquivo_a_compactar:
        def executar_compactacao():
            try:
                nome_arquivo_zip = f"{arquivo_a_compactar}.zip"
                resultado_text.config(state=tk.NORMAL)
                resultado_text.insert(tk.END, f"Iniciando compactação: {arquivo_a_compactar} -> {nome_arquivo_zip}\n")
                resultado_text.config(state=tk.DISABLED)
                scroll_to_bottom()

                for i in range(10):
                    time.sleep(1)

                    resultado_text.config(state=tk.NORMAL)
                    resultado_text.insert(tk.END, f"Progresso da compactação: {i * 10}%\n")
                    resultado_text.config(state=tk.DISABLED)
                    scroll_to_bottom()

                with zipfile.ZipFile(nome_arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(arquivo_a_compactar, os.path.basename(arquivo_a_compactar))

                resultado_text.config(state=tk.NORMAL)
                resultado_text.insert(tk.END, f"Compactação concluída com sucesso: {nome_arquivo_zip}\n")
                resultado_text.config(state=tk.DISABLED)
                scroll_to_bottom()

            except Exception as e:
                resultado_text.config(state=tk.NORMAL)
                resultado_text.insert(tk.END, f"Erro durante a compactação: {str(e)}\n")
                resultado_text.config(state=tk.DISABLED)
                scroll_to_bottom()
        t = threading.Thread(target=executar_compactacao)
        t.start()
    else:
        resultado_text.config(state=tk.NORMAL)
        resultado_text.insert(tk.END, "Nenhum arquivo selecionado para compactação.\n")
        resultado_text.config(state=tk.DISABLED)
        scroll_to_bottom()

    t = threading.Thread(target=executar_compactacao)
    t.start()


def thread_executar_gfix_e_gbak():
    t = threading.Thread(target=executar_gfix_e_gbak, args=(diretorio_selecionado,))
    t.start()

def obter_diretorio_firebird():
    return filedialog.askdirectory()

def selecionar_diretorio_firebird():
    global Tj
    global diretorio_selecionado
    diretorio_selecionado = obter_diretorio_firebird()
    print(f'Diretório selecionado: {diretorio_selecionado}')
    Tj.destroy()

Tj = tk.Tk()
Tj.title("Restore DOS v_0.9")
Tj.resizable(False, False)

#icone_path = resource_path("teste.ico")
#Tj.iconbitmap(icone_path)

def criar_janela():
    largura_tela = Tj.winfo_screenwidth()
    altura_tela = Tj.winfo_screenheight()

    largura_janela = 300
    altura_janela = 70

    x_pos = (largura_tela - largura_janela) // 2
    y_pos = (altura_tela - altura_janela) // 2 - 80

    Tj.geometry(f"{largura_janela}x{altura_janela}+{x_pos}+{y_pos}")

    Tj.configure(bg='gray12')

    botao_selecionar_diretorio = tk.Button(Tj, text="Selecionar Diretório Firebird", command=selecionar_diretorio_firebird, bg='gray', fg='white')
    botao_selecionar_diretorio.pack(pady=20)

    Tj.mainloop()

criar_janela()

Tj2 = tk.Tk()
Tj2.title("Restore DOS v_0.9")

#icone_path = resource_path("teste.ico")
#Tj2.iconbitmap(icone_path)

largura_tela = Tj2.winfo_screenwidth()
altura_tela = Tj2.winfo_screenheight()

largura_Janela = 650
altura_Janela = 600

x_pos = (largura_tela - largura_Janela) // 2
y_pos = (altura_tela - altura_Janela) // 2 - 80

Tj2.geometry(f"{largura_Janela}x{altura_Janela}+{x_pos}+{y_pos}")
Tj2.resizable(False, False)

Tj2.configure(bg='gray12')

def CompactarBanco():
    Tj3 = tk.Tk()
    Tj3.title("Compactar Banco de Dados")
    Tj3.resizable(False, False)
    Tj3.configure(bg='gray12')

    largura_janela = 350
    altura_janela = 100

    largura_tela = Tj3.winfo_screenwidth()
    altura_tela = Tj3.winfo_screenheight()

    x_pos = (largura_tela - largura_janela) // 2
    y_pos = (altura_tela - altura_janela) // 2 - 80

    Tj3.geometry(f"{largura_janela}x{altura_janela}+{x_pos}+{y_pos}")

    def fechar_janela():
        Tj3.destroy()

    frame = tk.Frame(Tj3, bg='gray12')
    frame.pack(pady=20)

    botao_opcao_1 = tk.Button(frame, text="Compactar NovoBanco", command=lambda: [compactar_banco_opcao_1(), fechar_janela()], bg='gray', fg='white')
    botao_opcao_1.pack(padx=10, pady=10, side=tk.LEFT)

    botao_opcao_2 = tk.Button(frame, text="Compactar Banco Antigo", command=lambda: [compactar_banco_opcao_2(), fechar_janela()], bg='gray', fg='white')
    botao_opcao_2.pack(padx=10, pady=10, side=tk.LEFT)

    Tj3.mainloop()


def escolher_arquivo_Banco():
    caminho_selecionado = filedialog.askopenfilename()
    caminho_fb_entry.delete(0, tk.END)
    caminho_fb_entry.insert(0, caminho_selecionado)

def escolher_diretorio_gbk():
    caminho_selecionado = filedialog.askdirectory()
    caminho_gbk_entry.delete(0, tk.END)
    caminho_gbk_entry.insert(0, caminho_selecionado)

def escolher_diretorio_NV():
    caminho_selecionado = filedialog.askdirectory()
    caminho_nv_entry.delete(0, tk.END)
    caminho_nv_entry.insert(0, caminho_selecionado)


caminho_fb_label = tk.Label(Tj2, text="Caminho do Banco de Dados:", bg='gray12', fg='white')
caminho_fb_label.pack()
caminho_fb_frame = tk.Frame(Tj2, bg='gray12')
caminho_fb_frame.pack()
caminho_fb_entry = tk.Entry(caminho_fb_frame, width=35)
caminho_fb_entry.pack(side=tk.LEFT)
escolher_arquivo_fb_botao = tk.Button(caminho_fb_frame, text="📑", command=escolher_arquivo_Banco, bg='gray', fg='white')
escolher_arquivo_fb_botao.pack(side=tk.RIGHT, padx=5, pady=10)

caminho_gbk_label = tk.Label(Tj2, text="Destino para BackupBanco.GBK:", bg='gray12', fg='white')
caminho_gbk_label.pack()
caminho_gbk_frame = tk.Frame(Tj2, bg='gray12')
caminho_gbk_frame.pack()
caminho_gbk_entry = tk.Entry(caminho_gbk_frame, width=35)
caminho_gbk_entry.pack(side=tk.LEFT)
escolher_diretorio_gbk_botao = tk.Button(caminho_gbk_frame, text="📁", command=escolher_diretorio_gbk, bg='gray', fg='white')
escolher_diretorio_gbk_botao.pack(side=tk.RIGHT, padx=5, pady=10)

caminho_nv_label = tk.Label(Tj2, text="Destino para o NovoBanco.FB:", bg='gray12', fg='white')
caminho_nv_label.pack()
caminho_nv_frame = tk.Frame(Tj2, bg='gray12')
caminho_nv_frame.pack()
caminho_nv_entry = tk.Entry(caminho_nv_frame, width=35)
caminho_nv_entry.pack(side=tk.LEFT)
escolher_diretorio_botao = tk.Button(caminho_nv_frame, text="📁", command=escolher_diretorio_NV, bg='gray', fg='white')
escolher_diretorio_botao.pack(side=tk.RIGHT, padx=5, pady=10)

executar_gfix_botao = tk.Button(Tj2, text="Executar Restore", command=lambda: thread_executar_gfix_e_gbak(), bg='gray', fg='white')
executar_gfix_botao.pack(padx=20, pady=10)

compactar_botao = tk.Button(Tj2, text="Compactar Banco de Dados", command=compactar_banco, bg='gray', fg='white')
compactar_botao.pack(padx=20, pady=10)

resultado_text = scrolledtext.ScrolledText(Tj2, state=tk.DISABLED, wrap=tk.WORD, width=60, height=15)
resultado_text.pack()


Tj2.mainloop()

